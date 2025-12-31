"""
Custom exceptions for CryptoSentinel framework.

This module defines all custom exceptions used throughout the CryptoSentinel
framework for graceful error handling and meaningful error messages.

Developer: saisrujanmurthy@gmail.com
"""

from typing import Any, Optional


class CryptoSentinelError(Exception):
    """
    Base exception class for all CryptoSentinel-related errors.
    
    This is the root exception that all other custom exceptions inherit from,
    allowing for catch-all exception handling when needed.
    
    Attributes:
        message: Human-readable error description
        details: Optional dictionary containing additional error context
    """
    
    def __init__(
        self, 
        message: str, 
        details: Optional[dict[str, Any]] = None
    ) -> None:
        """
        Initialize the CryptoSentinel base exception.
        
        Args:
            message: A descriptive error message
            details: Optional dictionary with additional error context
        """
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """
        Return string representation of the exception.
        
        Returns:
            Formatted error message with details if available
        """
        if self.details:
            details_str = ", ".join(
                f"{key}={value}" for key, value in self.details.items()
            )
            return f"{self.message} ({details_str})"
        return self.message
    
    def __repr__(self) -> str:
        """
        Return detailed representation for debugging.
        
        Returns:
            Developer-friendly exception representation
        """
        return f"{self.__class__.__name__}(message={self.message!r}, details={self.details!r})"


class EncryptionError(CryptoSentinelError):
    """Raised when encryption operation fails."""
    pass


class DecryptionError(CryptoSentinelError):
    """Raised when decryption operation fails."""
    pass


class InvalidKeyError(CryptoSentinelError):
    """Raised when provided key is invalid or incompatible."""
    pass


class HashingError(CryptoSentinelError):
    """Raised when hashing operation fails."""
    pass


class FileOperationError(CryptoSentinelError):
    """Raised when file I/O operations fail."""
    pass


class ValidationError(CryptoSentinelError):
    """Raised when input validation fails."""
    pass


class CrackingError(CryptoSentinelError):
    """Raised when automated cracking attempt fails."""
    pass
