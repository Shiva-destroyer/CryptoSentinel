"""
XOR Cipher implementation with single-byte key brute force.

XOR cipher uses the bitwise XOR operation for encryption. It's symmetric,
meaning the same operation is used for both encryption and decryption.

Developer: saisrujanmurthy@gmail.com
"""

from typing import Any, Union
from crypto_sentinel.core.base_cipher import CipherInterface
from crypto_sentinel.core.exceptions import (
    EncryptionError,
    DecryptionError,
    InvalidKeyError,
    ValidationError,
)


class XORCipher(CipherInterface):
    """
    XOR Cipher with support for both string and byte operations.
    
    The XOR cipher applies bitwise XOR between plaintext and key bytes.
    It's a symmetric cipher where encryption and decryption use the same operation.
    
    Features:
        - String encryption (returns hex output)
        - Raw byte encryption (for file encryption)
        - Single-byte key brute force (0-255)
        - Key repetition for longer plaintexts
    
    Time Complexity:
        - Encrypt/Decrypt: O(n) where n is data length
        - Crack: O(256n) for single-byte key brute force
    
    Space Complexity: O(n) for output
    
    Examples:
        >>> cipher = XORCipher()
        >>> encrypted = cipher.encrypt("HELLO", key=42)
        >>> print(encrypted)
        '62575c5c5d'  # hex output
        >>> decrypted = cipher.decrypt(encrypted, key=42)
        >>> print(decrypted)
        'HELLO'
    """
    
    # Common English words for scoring plaintext
    COMMON_WORDS = {
        'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
        'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
        'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
        'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what'
    }
    
    def encrypt(self, data: Union[str, bytes], key: Any) -> Union[str, bytes]:
        """
        Encrypt data using XOR cipher.
        
        For string input, returns hexadecimal string representation.
        For bytes input, returns encrypted bytes.
        Key is repeated cyclically if shorter than data.
        
        Args:
            data: Plaintext (string or bytes) to encrypt
            key: Integer key (0-255) or bytes key
        
        Returns:
            For string input: Hex string of encrypted bytes
            For bytes input: Encrypted bytes
        
        Raises:
            InvalidKeyError: If key is invalid
            EncryptionError: If encryption fails
            ValidationError: If data is invalid
        
        Time Complexity: O(n) where n is length of data
        Space Complexity: O(n) for output
        
        Examples:
            >>> cipher = XORCipher()
            >>> cipher.encrypt("HELLO", key=42)
            '62575c5c5d'
            >>> cipher.encrypt(b"HELLO", key=42)
            b'bW\\\\\\]'
        """
        # Validate and normalize key
        if isinstance(key, int):
            if not 0 <= key <= 255:
                raise InvalidKeyError(
                    f"Integer key must be in range [0, 255], got {key}",
                    details={"key": key, "valid_range": "0-255"}
                )
            key_bytes = bytes([key])
        elif isinstance(key, bytes):
            if len(key) == 0:
                raise InvalidKeyError(
                    "Bytes key cannot be empty",
                    details={"key_length": 0}
                )
            key_bytes = key
        elif isinstance(key, str):
            # Convert string key to bytes
            key_bytes = key.encode('utf-8')
            if len(key_bytes) == 0:
                raise InvalidKeyError(
                    "String key cannot be empty",
                    details={"key": key}
                )
        else:
            raise InvalidKeyError(
                f"Key must be int, bytes, or str, got {type(key).__name__}",
                details={"provided_type": type(key).__name__}
            )
        
        try:
            # Convert input to bytes if string
            is_string_input = isinstance(data, str)
            if is_string_input:
                data_bytes = data.encode('utf-8')
            elif isinstance(data, bytes):
                data_bytes = data
            else:
                raise ValidationError(
                    f"Data must be string or bytes, got {type(data).__name__}",
                    details={"provided_type": type(data).__name__}
                )
            
            # XOR operation
            result_bytes = bytes([
                data_bytes[i] ^ key_bytes[i % len(key_bytes)]
                for i in range(len(data_bytes))
            ])
            
            # Return hex string for string input, bytes for bytes input
            if is_string_input:
                return result_bytes.hex()
            else:
                return result_bytes
        
        except Exception as e:
            raise EncryptionError(
                f"Failed to encrypt data: {e}",
                details={"error": str(e), "key_type": type(key).__name__}
            )
    
    def decrypt(self, data: Union[str, bytes], key: Any) -> Union[str, bytes]:
        """
        Decrypt data using XOR cipher.
        
        XOR is symmetric, so decryption uses the same operation as encryption.
        For hex string input, converts to bytes first.
        
        Args:
            data: Ciphertext (hex string or bytes) to decrypt
            key: Integer key (0-255) or bytes key
        
        Returns:
            For hex string input: Decrypted string
            For bytes input: Decrypted bytes
        
        Raises:
            InvalidKeyError: If key is invalid
            DecryptionError: If decryption fails
            ValidationError: If data is invalid
        
        Time Complexity: O(n) where n is length of data
        Space Complexity: O(n) for output
        
        Examples:
            >>> cipher = XORCipher()
            >>> cipher.decrypt("62575c5c5d", key=42)
            'HELLO'
        """
        try:
            # Check if data is hex string
            is_hex_string = False
            if isinstance(data, str):
                try:
                    data_bytes = bytes.fromhex(data)
                    is_hex_string = True
                except ValueError:
                    # Not hex, treat as regular string
                    data_bytes = data.encode('utf-8')
            elif isinstance(data, bytes):
                data_bytes = data
            else:
                raise ValidationError(
                    f"Data must be string or bytes, got {type(data).__name__}",
                    details={"provided_type": type(data).__name__}
                )
            
            # XOR operation (same as encryption)
            result = self.encrypt(data_bytes, key)
            
            # Convert bytes result to string if input was hex string
            if is_hex_string and isinstance(result, bytes):
                try:
                    return result.decode('utf-8')
                except UnicodeDecodeError:
                    # Return as bytes if not valid UTF-8
                    return result
            
            return result
        
        except EncryptionError as e:
            raise DecryptionError(
                f"Failed to decrypt data: {e}",
                details={"error": str(e), "key": key}
            )
        except Exception as e:
            raise DecryptionError(
                f"Failed to decrypt data: {e}",
                details={"error": str(e), "key": key}
            )
    
    def crack(self, data: Union[str, bytes]) -> dict[str, Any]:
        """
        Crack XOR cipher with single-byte key using brute force.
        
        Tries all 256 possible single-byte keys (0-255) and scores each
        result based on:
        1. Valid UTF-8 decoding
        2. Printable ASCII characters
        3. Presence of common English words
        
        Args:
            data: Ciphertext (hex string or bytes) to crack
        
        Returns:
            Dictionary containing:
                - success: bool
                - key: int, the recovered key (0-255)
                - plaintext: str or bytes, decrypted data
                - confidence: float (0-1)
                - method: str
                - attempts: int (always 256)
                - scores: dict of key -> score mappings
        
        Raises:
            ValidationError: If input data is invalid
        
        Time Complexity: O(256n) = O(n) where n is data length
        Space Complexity: O(n) for storing best plaintext
        
        Examples:
            >>> cipher = XORCipher()
            >>> result = cipher.crack("62575c5c5d")
            >>> print(result['key'])
            42
            >>> print(result['plaintext'])
            'HELLO'
        """
        if isinstance(data, str):
            try:
                data_bytes = bytes.fromhex(data)
            except ValueError:
                raise ValidationError(
                    "String data must be valid hex or use bytes input",
                    details={"data_type": "string"}
                )
        elif isinstance(data, bytes):
            data_bytes = data
        else:
            raise ValidationError(
                f"Data must be string or bytes, got {type(data).__name__}",
                details={"provided_type": type(data).__name__}
            )
        
        if len(data_bytes) == 0:
            return {
                'success': False,
                'key': None,
                'plaintext': None,
                'confidence': 0.0,
                'method': 'single_byte_brute_force',
                'attempts': 0,
                'error': 'Empty data'
            }
        
        best_key = 0
        best_plaintext = None
        best_score = -1
        scores = {}
        
        for key in range(256):
            try:
                # XOR with this key
                decrypted_bytes = bytes([
                    data_bytes[i] ^ key
                    for i in range(len(data_bytes))
                ])
                
                # Try to decode as UTF-8
                try:
                    decrypted_str = decrypted_bytes.decode('utf-8')
                    score = self._score_plaintext(decrypted_str)
                except UnicodeDecodeError:
                    # Not valid UTF-8, score very low
                    score = -1000
                    decrypted_str = None
                
                scores[key] = score
                
                if score > best_score:
                    best_score = score
                    best_key = key
                    best_plaintext = decrypted_str if decrypted_str else decrypted_bytes
            
            except Exception:
                scores[key] = -1000
                continue
        
        # Calculate confidence (normalize score)
        if best_score > 0:
            confidence = min(1.0, best_score / 100.0)
        else:
            confidence = 0.0
        
        return {
            'success': best_score > 0,
            'key': best_key,
            'plaintext': best_plaintext,
            'confidence': round(confidence, 4),
            'method': 'single_byte_brute_force',
            'attempts': 256,
            'scores': scores,
            'best_score': best_score
        }
    
    def _score_plaintext(self, text: str) -> float:
        """
        Score plaintext based on English language characteristics.
        
        Scoring criteria:
        - Printable ASCII characters: +1 per char
        - Common English words: +10 per word
        - Alphabetic characters: +2 per char
        - Spaces: +1 per space
        
        Args:
            text: Plaintext to score
        
        Returns:
            Score (higher is better)
        
        Time Complexity: O(n) where n is text length
        """
        if not text:
            return 0.0
        
        score = 0.0
        
        # Check printable characters
        for char in text:
            if char.isprintable() or char in '\n\r\t':
                score += 1
            else:
                score -= 5  # Penalize non-printable
        
        # Check for alphabetic characters
        alpha_count = sum(1 for c in text if c.isalpha())
        score += alpha_count * 2
        
        # Check for spaces (indicates word boundaries)
        space_count = text.count(' ')
        score += space_count
        
        # Check for common English words
        words = text.lower().split()
        common_word_count = sum(1 for word in words if word in self.COMMON_WORDS)
        score += common_word_count * 10
        
        # Normalize by length
        if len(text) > 0:
            score = score / len(text) * 100
        
        return score
    
    def __repr__(self) -> str:
        """Return string representation."""
        return "XORCipher()"
