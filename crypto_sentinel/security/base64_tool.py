"""
Base64 encoding and decoding utility with robust error handling.

This module provides Base64 encoding/decoding with automatic padding
correction for malformed input.

Author: saisrujanmurthy@gmail.com
"""

import base64
from typing import Any

from crypto_sentinel.core.base_cipher import CipherInterface
from crypto_sentinel.core.exceptions import (
    EncryptionError,
    DecryptionError,
    ValidationError,
)


class Base64Encoder(CipherInterface):
    """
    Base64 encoder/decoder with robust error handling.
    
    Base64 is a binary-to-text encoding scheme that represents binary
    data in ASCII string format. It's commonly used for:
        - Email attachments (MIME)
        - Storing binary data in JSON/XML
        - URL-safe data transmission
        - Embedding images in HTML/CSS
    
    Features:
        - Standard Base64 encoding
        - Automatic padding correction
        - Graceful error handling
        - Both string and bytes input support
    
    Padding:
        Base64 requires output length to be multiple of 4.
        Missing padding ('=') is automatically added during decode.
    
    Character Set:
        A-Z, a-z, 0-9, +, / (64 characters)
        '=' for padding
    
    Overhead:
        Base64 increases data size by ~33% (4 chars for every 3 bytes)
    
    Note:
        Base64 is NOT encryption! It's encoding for data representation.
        Anyone can decode Base64 - it provides no security.
    
    Example:
        >>> encoder = Base64Encoder()
        >>> encoded = encoder.encrypt("Hello World")
        >>> print(encoded)
        'SGVsbG8gV29ybGQ='
        >>> decoded = encoder.decrypt(encoded)
        >>> print(decoded)
        'Hello World'
    """
    
    def __init__(self) -> None:
        """Initialize Base64 encoder."""
        self.name = "Base64"
    
    def encrypt(self, data: str | bytes, key: Any = None) -> str:
        """
        Encode data to Base64.
        
        Args:
            data: String or bytes to encode
            key: Ignored (Base64 doesn't use keys)
            
        Returns:
            Base64-encoded string
            
        Raises:
            ValidationError: If data type is invalid
            EncryptionError: If encoding fails
            
        Time Complexity: O(n) where n is length of data
        Space Complexity: O(n) - output is ~33% larger than input
        
        Example:
            >>> encoder = Base64Encoder()
            >>> encoder.encrypt("Hello")
            'SGVsbG8='
            >>> encoder.encrypt(b"\\x00\\x01\\x02")
            'AAEC'
        """
        if not isinstance(data, (str, bytes)):
            raise ValidationError(
                f"Expected str or bytes, got {type(data).__name__}"
            )
        
        try:
            # Convert string to bytes if needed
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
            
            # Encode to Base64
            encoded_bytes = base64.b64encode(data_bytes)
            
            # Return as string
            return encoded_bytes.decode('ascii')
            
        except Exception as e:
            raise EncryptionError(
                f"Base64 encoding failed: {str(e)}"
            ) from e
    
    def decrypt(self, data: str | bytes, key: Any = None) -> str:
        """
        Decode Base64 data with automatic padding correction.
        
        This method handles malformed Base64 by automatically adding
        missing padding characters ('=') if needed.
        
        Padding Logic:
            Base64 length must be multiple of 4.
            If not, add '=' until it is:
            - Length % 4 == 1: Invalid (error)
            - Length % 4 == 2: Add '=='
            - Length % 4 == 3: Add '='
        
        Args:
            data: Base64-encoded string or bytes to decode
            key: Ignored (Base64 doesn't use keys)
            
        Returns:
            Decoded string
            
        Raises:
            ValidationError: If data type is invalid
            DecryptionError: If decoding fails
            
        Time Complexity: O(n) where n is length of data
        
        Example:
            >>> encoder = Base64Encoder()
            >>> # Correct padding
            >>> encoder.decrypt("SGVsbG8=")
            'Hello'
            >>> # Missing padding (auto-corrected)
            >>> encoder.decrypt("SGVsbG8")
            'Hello'
        """
        if not isinstance(data, (str, bytes)):
            raise ValidationError(
                f"Expected str or bytes, got {type(data).__name__}"
            )
        
        try:
            # Convert to string if bytes
            if isinstance(data, bytes):
                data_str = data.decode('ascii')
            else:
                data_str = data
            
            # Auto-correct padding
            data_str = self._fix_padding(data_str)
            
            # Decode from Base64
            decoded_bytes = base64.b64decode(data_str)
            
            # Return as string
            return decoded_bytes.decode('utf-8')
            
        except UnicodeDecodeError as e:
            raise DecryptionError(
                f"Base64 decode failed: output contains non-UTF-8 bytes. "
                f"Original data may not have been text."
            ) from e
        except Exception as e:
            raise DecryptionError(
                f"Base64 decoding failed: {str(e)}"
            ) from e
    
    def _fix_padding(self, data: str) -> str:
        """
        Automatically add missing Base64 padding.
        
        Base64 strings must have length divisible by 4.
        This method adds '=' padding characters as needed.
        
        Args:
            data: Base64 string (possibly missing padding)
            
        Returns:
            Base64 string with correct padding
            
        Logic:
            remainder = len(data) % 4
            if remainder == 2: add '=='
            if remainder == 3: add '='
            if remainder == 1: invalid
        
        Example:
            >>> encoder = Base64Encoder()
            >>> encoder._fix_padding("SGVsbG8")
            'SGVsbG8='
            >>> encoder._fix_padding("SGVs")
            'SGVs'
        """
        remainder = len(data) % 4
        
        if remainder == 0:
            # Already correct
            return data
        elif remainder == 2:
            # Add 2 padding chars
            return data + '=='
        elif remainder == 3:
            # Add 1 padding char
            return data + '='
        else:
            # remainder == 1: Invalid Base64 length
            # Try to continue anyway - might work
            return data
    
    def crack(self, data: str | bytes) -> dict[str, Any]:
        """
        Base64 doesn't have keys, so 'cracking' is just decoding.
        
        This method attempts to decode the Base64 data and returns
        the result. Since Base64 is not encryption, no actual cracking
        is needed.
        
        Args:
            data: Base64-encoded data
            
        Returns:
            Dictionary containing:
                - success (bool): True if decoded successfully
                - plaintext (str): Decoded data
                - key (None): No key for Base64
                - confidence (float): 1.0 if successful
                
        Example:
            >>> encoder = Base64Encoder()
            >>> result = encoder.crack("SGVsbG8gV29ybGQ=")
            >>> print(result['plaintext'])
            'Hello World'
        """
        try:
            plaintext = self.decrypt(data)
            return {
                'success': True,
                'plaintext': plaintext,
                'key': None,
                'confidence': 1.0,
            }
        except DecryptionError:
            return {
                'success': False,
                'plaintext': '',
                'key': None,
                'confidence': 0.0,
            }
    
    def encode_bytes(self, data: bytes) -> str:
        """
        Convenience method to encode bytes to Base64.
        
        Args:
            data: Bytes to encode
            
        Returns:
            Base64-encoded string
            
        Example:
            >>> encoder = Base64Encoder()
            >>> encoder.encode_bytes(b"\\x00\\xff\\x42")
            'AP9C'
        """
        return self.encrypt(data, key=None)
    
    def decode_bytes(self, data: str) -> bytes:
        """
        Decode Base64 to bytes (not string).
        
        Useful when original data was binary, not text.
        
        Args:
            data: Base64-encoded string
            
        Returns:
            Decoded bytes
            
        Raises:
            DecryptionError: If decoding fails
            
        Example:
            >>> encoder = Base64Encoder()
            >>> encoder.decode_bytes("AP9C")
            b'\\x00\\xff\\x42'
        """
        try:
            data_str = self._fix_padding(data)
            return base64.b64decode(data_str)
        except Exception as e:
            raise DecryptionError(
                f"Base64 decoding to bytes failed: {str(e)}"
            ) from e
    
    def is_valid_base64(self, data: str) -> bool:
        """
        Check if string is valid Base64.
        
        Args:
            data: String to validate
            
        Returns:
            True if valid Base64 format
            
        Example:
            >>> encoder = Base64Encoder()
            >>> encoder.is_valid_base64("SGVsbG8=")
            True
            >>> encoder.is_valid_base64("not base64!")
            False
        """
        try:
            # Fix padding and try to decode
            data_str = self._fix_padding(data)
            base64.b64decode(data_str, validate=True)
            return True
        except Exception:
            return False
    
    def __repr__(self) -> str:
        """String representation of encoder."""
        return "Base64Encoder(encoding='standard')"
