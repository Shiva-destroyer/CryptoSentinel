"""
Advanced hashing implementations using hashlib with streaming file support.

This module provides MD5 and SHA256 hashers that can efficiently handle
files of any size (including 10GB+) by reading them in chunks.

Developer: saisrujanmurthy@gmail.com
"""

import hashlib
from pathlib import Path
from typing import Any

from crypto_sentinel.core.base_hasher import HasherInterface
from crypto_sentinel.core.exceptions import (
    FileOperationError,
    HashingError,
    ValidationError,
)


class MD5Hasher(HasherInterface):
    """
    MD5 hash generator for strings and files.
    
    MD5 produces a 128-bit (32 hexadecimal character) hash value.
    
    Warning:
        MD5 is cryptographically broken and should NOT be used for security
        purposes. Use it only for checksums and non-security applications.
    
    Features:
        - Streaming file reading (64KB chunks) for large files
        - Graceful error handling for missing files
        - Supports both string and file hashing
    
    Time Complexity:
        - String: O(n) where n is string length
        - File: O(n) where n is file size, constant memory
    
    Space Complexity: O(1) - constant memory usage regardless of file size
    
    Example:
        >>> hasher = MD5Hasher()
        >>> hash_value = hasher.hash_string("Hello World")
        >>> print(hash_value)
        'b10a8db164e0754105b7a99be72e3fe5'
        >>> file_hash = hasher.hash_file("large_file.bin")
    """
    
    CHUNK_SIZE: int = 65536  # 64KB chunks for streaming
    
    def __init__(self) -> None:
        """Initialize MD5 hasher."""
        self.algorithm = "md5"
    
    @property
    def algorithm_name(self) -> str:
        """Return the algorithm name."""
        return "MD5"
    
    @property
    def digest_size(self) -> int:
        """Return digest size in bytes (MD5 = 128 bits = 16 bytes)."""
        return 16
    
    def hash_string(self, data: str) -> str:
        """
        Generate MD5 hash of a string.
        
        Args:
            data: Input string to hash
            
        Returns:
            Hexadecimal hash string (32 characters)
            
        Raises:
            ValidationError: If data is not a string
            HashingError: If hashing operation fails
            
        Time Complexity: O(n) where n is length of data
        """
        if not isinstance(data, str):
            raise ValidationError(
                f"Expected string, got {type(data).__name__}"
            )
        
        try:
            hash_obj = hashlib.md5()
            hash_obj.update(data.encode('utf-8'))
            return hash_obj.hexdigest()
        except Exception as e:
            raise HashingError(
                f"MD5 hashing failed: {str(e)}"
            ) from e
    
    def hash_file(self, filepath: str) -> str:
        """
        Generate MD5 hash of a file using streaming reads.
        
        This method reads the file in 64KB chunks to prevent memory
        exhaustion on large files (10GB+). The entire file is never
        loaded into memory at once.
        
        Implementation:
            1. Open file in binary read mode
            2. Read 64KB chunks in a loop
            3. Update hash incrementally
            4. Return final hexadecimal digest
        
        Args:
            filepath: Path to file to hash
            
        Returns:
            Hexadecimal hash string (32 characters)
            
        Raises:
            FileOperationError: If file doesn't exist or can't be read
            HashingError: If hashing operation fails
            
        Time Complexity: O(n) where n is file size
        Space Complexity: O(1) - only 64KB buffer in memory
        
        Example:
            >>> hasher = MD5Hasher()
            >>> # Works efficiently even on 10GB files
            >>> hash_value = hasher.hash_file("/path/to/large_file.bin")
        """
        path = Path(filepath)
        
        if not path.exists():
            raise FileOperationError(
                f"File not found: {filepath}"
            )
        
        if not path.is_file():
            raise FileOperationError(
                f"Path is not a file: {filepath}"
            )
        
        try:
            hash_obj = hashlib.md5()
            
            with open(path, 'rb') as f:
                while True:
                    chunk = f.read(self.CHUNK_SIZE)
                    if not chunk:
                        break
                    hash_obj.update(chunk)
            
            return hash_obj.hexdigest()
            
        except PermissionError as e:
            raise FileOperationError(
                f"Permission denied reading file: {filepath}"
            ) from e
        except Exception as e:
            raise HashingError(
                f"MD5 file hashing failed: {str(e)}"
            ) from e
    
    def __repr__(self) -> str:
        """String representation of hasher."""
        return f"MD5Hasher(algorithm='{self.algorithm}')"


class SHA256Hasher(HasherInterface):
    """
    SHA-256 hash generator for strings and files.
    
    SHA-256 is part of the SHA-2 family and produces a 256-bit
    (64 hexadecimal character) hash value. It's cryptographically secure
    and suitable for security applications.
    
    Features:
        - Cryptographically secure hashing
        - Streaming file reading (64KB chunks) for large files
        - Graceful error handling for missing files
        - Collision resistance
    
    Security Properties:
        - Pre-image resistance: Hard to find input from hash
        - Second pre-image resistance: Hard to find different input with same hash
        - Collision resistance: Hard to find two inputs with same hash
    
    Time Complexity:
        - String: O(n) where n is string length
        - File: O(n) where n is file size, constant memory
    
    Space Complexity: O(1) - constant memory usage regardless of file size
    
    Example:
        >>> hasher = SHA256Hasher()
        >>> hash_value = hasher.hash_string("Hello World")
        >>> print(hash_value)
        'a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e'
    """
    
    CHUNK_SIZE: int = 65536  # 64KB chunks for streaming
    
    def __init__(self) -> None:
        """Initialize SHA-256 hasher."""
        self.algorithm = "sha256"
    
    @property
    def algorithm_name(self) -> str:
        """Return the algorithm name."""
        return "SHA-256"
    
    @property
    def digest_size(self) -> int:
        """Return digest size in bytes (SHA-256 = 256 bits = 32 bytes)."""
        return 32
    
    def hash_string(self, data: str) -> str:
        """
        Generate SHA-256 hash of a string.
        
        Args:
            data: Input string to hash
            
        Returns:
            Hexadecimal hash string (64 characters)
            
        Raises:
            ValidationError: If data is not a string
            HashingError: If hashing operation fails
            
        Time Complexity: O(n) where n is length of data
        """
        if not isinstance(data, str):
            raise ValidationError(
                f"Expected string, got {type(data).__name__}"
            )
        
        try:
            hash_obj = hashlib.sha256()
            hash_obj.update(data.encode('utf-8'))
            return hash_obj.hexdigest()
        except Exception as e:
            raise HashingError(
                f"SHA-256 hashing failed: {str(e)}"
            ) from e
    
    def hash_file(self, filepath: str) -> str:
        """
        Generate SHA-256 hash of a file using streaming reads.
        
        This method reads the file in 64KB chunks to prevent memory
        exhaustion on large files (10GB+). The entire file is never
        loaded into memory at once.
        
        Algorithm:
            1. Initialize SHA-256 hash object
            2. Open file in binary mode
            3. Read and process 64KB chunks iteratively
            4. Finalize and return hexadecimal digest
        
        Args:
            filepath: Path to file to hash
            
        Returns:
            Hexadecimal hash string (64 characters)
            
        Raises:
            FileOperationError: If file doesn't exist or can't be read
            HashingError: If hashing operation fails
            
        Time Complexity: O(n) where n is file size
        Space Complexity: O(1) - only 64KB buffer in memory
        
        Performance:
            - Can hash 10GB file with only ~64KB RAM usage
            - Typical speed: 200-500 MB/s depending on disk
        
        Example:
            >>> hasher = SHA256Hasher()
            >>> hash_value = hasher.hash_file("/path/to/sensitive_file.bin")
            >>> # Verify file integrity
            >>> expected = "abc123..."
            >>> assert hash_value == expected
        """
        path = Path(filepath)
        
        if not path.exists():
            raise FileOperationError(
                f"File not found: {filepath}"
            )
        
        if not path.is_file():
            raise FileOperationError(
                f"Path is not a file: {filepath}"
            )
        
        try:
            hash_obj = hashlib.sha256()
            
            with open(path, 'rb') as f:
                while True:
                    chunk = f.read(self.CHUNK_SIZE)
                    if not chunk:
                        break
                    hash_obj.update(chunk)
            
            return hash_obj.hexdigest()
            
        except PermissionError as e:
            raise FileOperationError(
                f"Permission denied reading file: {filepath}"
            ) from e
        except Exception as e:
            raise HashingError(
                f"SHA-256 file hashing failed: {str(e)}"
            ) from e
    
    def __repr__(self) -> str:
        """String representation of hasher."""
        return f"SHA256Hasher(algorithm='{self.algorithm}')"
