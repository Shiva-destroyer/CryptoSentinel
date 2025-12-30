"""
Abstract base class for hashing implementations.

This module defines the HasherInterface ABC that all hashing algorithm
implementations must inherit from, ensuring consistent API for all hash functions.

Author: saisrujanmurthy@gmail.com
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union


class HasherInterface(ABC):
    """
    Abstract base class defining the interface for all hashing implementations.
    
    All concrete hasher classes (MD5, SHA256, etc.) must inherit from this
    class and implement its abstract methods to ensure a consistent API
    across the framework.
    
    The interface enforces two core operations:
    - hash_string: Generate hash of in-memory text
    - hash_file: Generate hash of file contents with streaming support
    """
    
    @abstractmethod
    def hash_string(self, text: str) -> str:
        """
        Generate cryptographic hash of the provided text string.
        
        This method must be implemented by all concrete hasher classes to
        compute the hash digest of in-memory text data.
        
        Args:
            text: The text string to hash
        
        Returns:
            Hexadecimal string representation of the hash digest
        
        Raises:
            HashingError: If hashing operation fails
            ValidationError: If input text is invalid
        
        Examples:
            >>> hasher = SHA256Hasher()
            >>> hasher.hash_string("Hello World")
            'a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e'
        """
        pass
    
    @abstractmethod
    def hash_file(self, filepath: Union[str, Path]) -> str:
        """
        Generate cryptographic hash of file contents using streaming.
        
        This method must be implemented to compute hash of large files
        efficiently without loading entire content into memory. The
        implementation should use chunked reading for memory efficiency.
        
        Args:
            filepath: Path to the file to hash (string or Path object)
        
        Returns:
            Hexadecimal string representation of the hash digest
        
        Raises:
            HashingError: If hashing operation fails
            FileOperationError: If file cannot be read
            FileNotFoundError: If file does not exist
            ValidationError: If filepath is invalid
        
        Examples:
            >>> hasher = SHA256Hasher()
            >>> hasher.hash_file("/path/to/large_file.bin")
            'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
            
        Notes:
            Implementations should read files in chunks (e.g., 8192 bytes)
            to support large files that may not fit in memory. This ensures
            consistent performance regardless of file size.
        """
        pass
    
    @property
    @abstractmethod
    def algorithm_name(self) -> str:
        """
        Return the name of the hashing algorithm.
        
        Returns:
            String identifier for the algorithm (e.g., "SHA256", "MD5")
        """
        pass
    
    @property
    @abstractmethod
    def digest_size(self) -> int:
        """
        Return the size of the hash digest in bytes.
        
        Returns:
            Integer representing digest size in bytes
        
        Examples:
            >>> hasher = SHA256Hasher()
            >>> hasher.digest_size
            32  # SHA-256 produces 256 bits = 32 bytes
        """
        pass
    
    def hash_bytes(self, data: bytes) -> str:
        """
        Generate cryptographic hash of raw bytes.
        
        This is a convenience method that can be optionally overridden
        for optimization. Default implementation converts bytes to string.
        
        Args:
            data: Raw bytes to hash
        
        Returns:
            Hexadecimal string representation of the hash digest
        
        Raises:
            HashingError: If hashing operation fails
        """
        # Default implementation - can be overridden for better performance
        return self.hash_string(data.decode('utf-8', errors='replace'))
    
    def verify_file(
        self, 
        filepath: Union[str, Path], 
        expected_hash: str
    ) -> bool:
        """
        Verify that file matches the expected hash.
        
        This convenience method computes the file hash and compares it
        with the expected value for integrity verification.
        
        Args:
            filepath: Path to the file to verify
            expected_hash: Expected hash value (hexadecimal string)
        
        Returns:
            True if hash matches, False otherwise
        
        Raises:
            FileOperationError: If file cannot be read
            ValidationError: If inputs are invalid
        
        Examples:
            >>> hasher = SHA256Hasher()
            >>> hasher.verify_file("file.txt", "a591a6d40bf420...")
            True
        """
        computed_hash = self.hash_file(filepath)
        return computed_hash.lower() == expected_hash.lower()
    
    def __repr__(self) -> str:
        """
        Return string representation of the hasher instance.
        
        Returns:
            Developer-friendly representation
        """
        return f"{self.__class__.__name__}(algorithm={self.algorithm_name})"
