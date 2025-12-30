"""
Checksum validation utility for file integrity verification.

This module provides tools to compare file hashes for integrity checking,
supporting both file-to-file and file-to-hash-string comparisons.

Author: saisrujanmurthy@gmail.com
"""

from pathlib import Path
from typing import Any

from crypto_sentinel.hashing.hash_engine import MD5Hasher, SHA256Hasher
from crypto_sentinel.core.exceptions import FileOperationError, ValidationError


class ChecksumValidator:
    """
    File integrity validator using cryptographic hashes.
    
    This class provides methods to verify file integrity by comparing
    hash values. Supports:
        - File-to-file comparison
        - File-to-hash-string comparison
        - Multiple hash algorithms (MD5, SHA-256)
    
    Use Cases:
        - Verify downloaded files match expected checksums
        - Detect file corruption or tampering
        - Compare file copies for bit-identical verification
        - Integrity checks in backup systems
    
    Supported Algorithms:
        - MD5: Fast but not cryptographically secure
        - SHA256: Secure and recommended for integrity verification
    
    Example:
        >>> validator = ChecksumValidator()
        >>> # Compare two files
        >>> result = validator.compare_files("file1.bin", "file2.bin")
        >>> print(result['match'])  # True if identical
        >>> 
        >>> # Verify against known hash
        >>> result = validator.validate_file(
        ...     "download.iso",
        ...     "abc123...",
        ...     algorithm="sha256"
        ... )
        >>> print(result['match'])  # True if hash matches
    """
    
    def __init__(self) -> None:
        """Initialize checksum validator with supported hashers."""
        self.hashers = {
            'md5': MD5Hasher(),
            'sha256': SHA256Hasher(),
        }
    
    def compare_files(
        self,
        filepath1: str,
        filepath2: str,
        algorithm: str = "sha256"
    ) -> dict[str, Any]:
        """
        Compare two files by computing and comparing their hashes.
        
        This method computes the hash of both files independently and
        compares them. Files are considered identical if their hashes match.
        
        Args:
            filepath1: Path to first file
            filepath2: Path to second file
            algorithm: Hash algorithm to use ('md5' or 'sha256')
            
        Returns:
            Dictionary containing:
                - match (bool): True if files are identical
                - algorithm (str): Algorithm used
                - hash1 (str): Hash of first file
                - hash2 (str): Hash of second file
                - file1 (str): First file path
                - file2 (str): Second file path
                
        Raises:
            ValidationError: If algorithm is not supported
            FileOperationError: If files don't exist or can't be read
            
        Time Complexity: O(n + m) where n, m are file sizes
        
        Example:
            >>> validator = ChecksumValidator()
            >>> result = validator.compare_files(
            ...     "original.bin",
            ...     "backup.bin",
            ...     algorithm="sha256"
            ... )
            >>> if result['match']:
            ...     print("Files are identical!")
            ... else:
            ...     print(f"Mismatch: {result['hash1']} != {result['hash2']}")
        """
        algorithm = algorithm.lower()
        
        if algorithm not in self.hashers:
            raise ValidationError(
                f"Unsupported algorithm: {algorithm}. "
                f"Supported: {list(self.hashers.keys())}"
            )
        
        hasher = self.hashers[algorithm]
        
        # Compute hashes
        hash1 = hasher.hash_file(filepath1)
        hash2 = hasher.hash_file(filepath2)
        
        # Compare
        match = hash1 == hash2
        
        return {
            'match': match,
            'algorithm': algorithm,
            'hash1': hash1,
            'hash2': hash2,
            'file1': filepath1,
            'file2': filepath2,
        }
    
    def validate_file(
        self,
        filepath: str,
        expected_hash: str,
        algorithm: str = "sha256"
    ) -> dict[str, Any]:
        """
        Validate a file against a known hash value.
        
        This is commonly used to verify downloaded files against
        checksums provided by the distributor.
        
        Args:
            filepath: Path to file to validate
            expected_hash: Expected hash value (hexadecimal string)
            algorithm: Hash algorithm to use ('md5' or 'sha256')
            
        Returns:
            Dictionary containing:
                - match (bool): True if hash matches expected value
                - algorithm (str): Algorithm used
                - computed_hash (str): Computed hash of file
                - expected_hash (str): Expected hash value
                - file (str): File path
                
        Raises:
            ValidationError: If algorithm is not supported or hash format invalid
            FileOperationError: If file doesn't exist or can't be read
            
        Time Complexity: O(n) where n is file size
        
        Example:
            >>> validator = ChecksumValidator()
            >>> # Verify downloaded ISO file
            >>> expected = "abc123def456..."  # From website
            >>> result = validator.validate_file(
            ...     "ubuntu-22.04.iso",
            ...     expected,
            ...     algorithm="sha256"
            ... )
            >>> if result['match']:
            ...     print("Download verified! File is authentic.")
            ... else:
            ...     print("WARNING: Hash mismatch! File may be corrupted.")
        """
        algorithm = algorithm.lower()
        
        if algorithm not in self.hashers:
            raise ValidationError(
                f"Unsupported algorithm: {algorithm}. "
                f"Supported: {list(self.hashers.keys())}"
            )
        
        # Validate hash format
        expected_hash = expected_hash.lower().strip()
        expected_length = 32 if algorithm == 'md5' else 64
        
        if len(expected_hash) != expected_length:
            raise ValidationError(
                f"Invalid {algorithm.upper()} hash length: "
                f"expected {expected_length}, got {len(expected_hash)}"
            )
        
        if not all(c in '0123456789abcdef' for c in expected_hash):
            raise ValidationError(
                f"Invalid hash format: must be hexadecimal string"
            )
        
        hasher = self.hashers[algorithm]
        
        # Compute actual hash
        computed_hash = hasher.hash_file(filepath)
        
        # Compare
        match = computed_hash == expected_hash
        
        return {
            'match': match,
            'algorithm': algorithm,
            'computed_hash': computed_hash,
            'expected_hash': expected_hash,
            'file': filepath,
        }
    
    def generate_report(
        self,
        filepath: str,
        algorithms: list[str] | None = None
    ) -> dict[str, Any]:
        """
        Generate comprehensive hash report for a file.
        
        Computes multiple hash values for a single file, useful for
        creating verification files or detailed integrity reports.
        
        Args:
            filepath: Path to file to analyze
            algorithms: List of algorithms to use (default: all supported)
            
        Returns:
            Dictionary containing:
                - file (str): File path
                - size (int): File size in bytes
                - hashes (dict): Hash values for each algorithm
                
        Raises:
            FileOperationError: If file doesn't exist or can't be read
            ValidationError: If algorithm is not supported
            
        Example:
            >>> validator = ChecksumValidator()
            >>> report = validator.generate_report("file.bin")
            >>> print(f"MD5:    {report['hashes']['md5']}")
            >>> print(f"SHA256: {report['hashes']['sha256']}")
            >>> print(f"Size:   {report['size']} bytes")
        """
        path = Path(filepath)
        
        if not path.exists():
            raise FileOperationError(f"File not found: {filepath}")
        
        if algorithms is None:
            algorithms = list(self.hashers.keys())
        
        # Validate algorithms
        for algo in algorithms:
            if algo.lower() not in self.hashers:
                raise ValidationError(
                    f"Unsupported algorithm: {algo}. "
                    f"Supported: {list(self.hashers.keys())}"
                )
        
        # Compute hashes
        hashes = {}
        for algo in algorithms:
            algo = algo.lower()
            hasher = self.hashers[algo]
            hashes[algo] = hasher.hash_file(filepath)
        
        # Get file size
        size = path.stat().st_size
        
        return {
            'file': filepath,
            'size': size,
            'hashes': hashes,
        }
    
    def __repr__(self) -> str:
        """String representation of validator."""
        return f"ChecksumValidator(algorithms={list(self.hashers.keys())})"
