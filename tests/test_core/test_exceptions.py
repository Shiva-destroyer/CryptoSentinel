"""
Unit tests for core exception classes.

Author: saisrujanmurthy@gmail.com
"""

import pytest
from crypto_sentinel.core.exceptions import (
    CryptoSentinelError,
    EncryptionError,
    DecryptionError,
    InvalidKeyError,
    HashingError,
    FileOperationError,
    ValidationError,
    CrackingError,
)


class TestCryptoSentinelError:
    """Test cases for base exception class."""
    
    def test_basic_exception(self) -> None:
        """Test creating exception with message only."""
        error = CryptoSentinelError("Test error")
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.details == {}
    
    def test_exception_with_details(self) -> None:
        """Test creating exception with details dict."""
        error = CryptoSentinelError(
            "Test error",
            details={"key": "value", "count": 42}
        )
        error_str = str(error)
        assert "Test error" in error_str
        assert "key=value" in error_str
        assert "count=42" in error_str
    
    def test_exception_repr(self) -> None:
        """Test exception representation."""
        error = CryptoSentinelError("Test", details={"x": 1})
        repr_str = repr(error)
        assert "CryptoSentinelError" in repr_str
        assert "message='Test'" in repr_str
    
    def test_exception_can_be_raised(self) -> None:
        """Test that exception can be raised and caught."""
        with pytest.raises(CryptoSentinelError) as exc_info:
            raise CryptoSentinelError("Test error")
        
        assert "Test error" in str(exc_info.value)


class TestSpecificExceptions:
    """Test cases for specific exception types."""
    
    def test_encryption_error(self) -> None:
        """Test EncryptionError inherits from base."""
        error = EncryptionError("Encryption failed")
        assert isinstance(error, CryptoSentinelError)
        assert isinstance(error, Exception)
    
    def test_decryption_error(self) -> None:
        """Test DecryptionError inherits from base."""
        error = DecryptionError("Decryption failed")
        assert isinstance(error, CryptoSentinelError)
    
    def test_invalid_key_error(self) -> None:
        """Test InvalidKeyError inherits from base."""
        error = InvalidKeyError("Invalid key")
        assert isinstance(error, CryptoSentinelError)
    
    def test_hashing_error(self) -> None:
        """Test HashingError inherits from base."""
        error = HashingError("Hashing failed")
        assert isinstance(error, CryptoSentinelError)
    
    def test_file_operation_error(self) -> None:
        """Test FileOperationError inherits from base."""
        error = FileOperationError("File not found")
        assert isinstance(error, CryptoSentinelError)
    
    def test_validation_error(self) -> None:
        """Test ValidationError inherits from base."""
        error = ValidationError("Invalid input")
        assert isinstance(error, CryptoSentinelError)
    
    def test_cracking_error(self) -> None:
        """Test CrackingError inherits from base."""
        error = CrackingError("Cracking failed")
        assert isinstance(error, CryptoSentinelError)
    
    def test_all_exceptions_catchable_as_base(self) -> None:
        """Test that all specific exceptions can be caught as base type."""
        exceptions = [
            EncryptionError("test"),
            DecryptionError("test"),
            InvalidKeyError("test"),
            HashingError("test"),
            FileOperationError("test"),
            ValidationError("test"),
            CrackingError("test"),
        ]
        
        for exc in exceptions:
            try:
                raise exc
            except CryptoSentinelError:
                pass  # Successfully caught as base type
