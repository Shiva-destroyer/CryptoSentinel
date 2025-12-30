"""
Caesar Cipher implementation with frequency analysis cracking.

The Caesar cipher is a substitution cipher where each letter is shifted by
a fixed number of positions in the alphabet. Named after Julius Caesar.

Author: saisrujanmurthy@gmail.com
"""

from typing import Any, Union
from crypto_sentinel.core.base_cipher import CipherInterface
from crypto_sentinel.core.exceptions import (
    EncryptionError,
    DecryptionError,
    InvalidKeyError,
    ValidationError,
)
from crypto_sentinel.utils.math_helpers import chi_squared


class CaesarCipher(CipherInterface):
    """
    Caesar Cipher implementation with chi-squared frequency analysis.
    
    The Caesar cipher shifts each letter by a fixed number of positions.
    For example, with a shift of 3, A becomes D, B becomes E, etc.
    
    Features:
        - Encryption/Decryption with integer keys (0-25)
        - Preserves case and non-alphabetic characters
        - Advanced cracking using chi-squared frequency analysis
    
    Time Complexity:
        - Encrypt/Decrypt: O(n) where n is text length
        - Crack: O(26n) for trying all possible shifts
    
    Space Complexity: O(n) for output string
    
    Examples:
        >>> cipher = CaesarCipher()
        >>> encrypted = cipher.encrypt("HELLO", key=3)
        >>> print(encrypted)
        'KHOOR'
        >>> decrypted = cipher.decrypt("KHOOR", key=3)
        >>> print(decrypted)
        'HELLO'
    """
    
    ALPHABET_SIZE = 26
    
    # English letter frequency (percentage, A-Z)
    ENGLISH_FREQ = [
        8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966,
        0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987,
        6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074
    ]
    
    def encrypt(self, data: Union[str, bytes], key: Any) -> Union[str, bytes]:
        """
        Encrypt plaintext using Caesar cipher.
        
        Shifts each alphabetic character by the key value. Non-alphabetic
        characters are preserved unchanged. Case is maintained.
        
        Args:
            data: Plaintext string to encrypt
            key: Integer shift value (0-25)
        
        Returns:
            Encrypted ciphertext string
        
        Raises:
            InvalidKeyError: If key is not an integer or out of range
            EncryptionError: If encryption fails
            ValidationError: If data is not a string
        
        Time Complexity: O(n) where n is length of data
        Space Complexity: O(n) for result string
        
        Examples:
            >>> cipher = CaesarCipher()
            >>> cipher.encrypt("HELLO WORLD", key=3)
            'KHOOR ZRUOG'
            >>> cipher.encrypt("Attack at dawn!", key=5)
            'Fyyfhp fy ifbs!'
        """
        # Validate input
        if isinstance(data, bytes):
            raise ValidationError(
                "Caesar cipher requires string input, not bytes",
                details={"provided_type": "bytes"}
            )
        
        if not isinstance(data, str):
            raise ValidationError(
                f"Data must be a string, got {type(data).__name__}",
                details={"provided_type": type(data).__name__}
            )
        
        # Validate key
        if not isinstance(key, int):
            raise InvalidKeyError(
                f"Key must be an integer, got {type(key).__name__}",
                details={"provided_type": type(key).__name__}
            )
        
        if not 0 <= key < self.ALPHABET_SIZE:
            raise InvalidKeyError(
                f"Key must be in range [0, {self.ALPHABET_SIZE-1}], got {key}",
                details={"key": key, "valid_range": f"0-{self.ALPHABET_SIZE-1}"}
            )
        
        try:
            result = []
            for char in data:
                if char.isalpha():
                    # Determine if uppercase or lowercase
                    base = ord('A') if char.isupper() else ord('a')
                    # Shift character
                    shifted = (ord(char) - base + key) % self.ALPHABET_SIZE
                    result.append(chr(base + shifted))
                else:
                    # Preserve non-alphabetic characters
                    result.append(char)
            
            return ''.join(result)
        
        except Exception as e:
            raise EncryptionError(
                f"Failed to encrypt data: {e}",
                details={"error": str(e), "key": key}
            )
    
    def decrypt(self, data: Union[str, bytes], key: Any) -> Union[str, bytes]:
        """
        Decrypt ciphertext using Caesar cipher.
        
        Reverses the encryption by shifting in the opposite direction.
        
        Args:
            data: Ciphertext string to decrypt
            key: Integer shift value (0-25)
        
        Returns:
            Decrypted plaintext string
        
        Raises:
            InvalidKeyError: If key is not an integer or out of range
            DecryptionError: If decryption fails
            ValidationError: If data is not a string
        
        Time Complexity: O(n) where n is length of data
        Space Complexity: O(n) for result string
        
        Examples:
            >>> cipher = CaesarCipher()
            >>> cipher.decrypt("KHOOR", key=3)
            'HELLO'
        """
        if not isinstance(key, int):
            raise InvalidKeyError(
                f"Key must be an integer, got {type(key).__name__}",
                details={"provided_type": type(key).__name__}
            )
        
        try:
            # Decryption is encryption with negative key
            return self.encrypt(data, (self.ALPHABET_SIZE - key) % self.ALPHABET_SIZE)
        except EncryptionError as e:
            raise DecryptionError(
                f"Failed to decrypt data: {e}",
                details={"error": str(e), "key": key}
            )
    
    def crack(self, data: Union[str, bytes]) -> dict[str, Any]:
        """
        Crack Caesar cipher using chi-squared frequency analysis.
        
        Tries all 26 possible shifts and scores each decryption by comparing
        letter frequencies to English language statistics using chi-squared test.
        The shift producing the lowest chi-squared value (best match to English)
        is selected as the most likely plaintext.
        
        Args:
            data: Ciphertext string to crack
        
        Returns:
            Dictionary containing:
                - success: bool indicating if crack was successful
                - key: int, the recovered shift value
                - plaintext: str, the decrypted text
                - confidence: float (0-1), based on chi-squared score
                - method: str, cracking method used
                - attempts: int, number of keys tried (always 26)
                - scores: dict, chi-squared scores for each key
        
        Raises:
            ValidationError: If input data is invalid
        
        Time Complexity: O(26n) = O(n) where n is length of ciphertext
        Space Complexity: O(n) for storing best plaintext
        
        Examples:
            >>> cipher = CaesarCipher()
            >>> result = cipher.crack("KHOOR ZRUOG")
            >>> print(result['key'])
            3
            >>> print(result['plaintext'])
            'HELLO WORLD'
        """
        if isinstance(data, bytes):
            raise ValidationError(
                "Caesar cipher requires string input, not bytes",
                details={"provided_type": "bytes"}
            )
        
        if not isinstance(data, str):
            raise ValidationError(
                f"Data must be a string, got {type(data).__name__}",
                details={"provided_type": type(data).__name__}
            )
        
        if not data or not any(c.isalpha() for c in data):
            return {
                'success': False,
                'key': None,
                'plaintext': None,
                'confidence': 0.0,
                'method': 'frequency_analysis',
                'attempts': 0,
                'scores': {},
                'error': 'No alphabetic characters to analyze'
            }
        
        best_key = 0
        best_plaintext = ""
        best_score = float('inf')
        scores = {}
        
        for key in range(self.ALPHABET_SIZE):
            # Try decrypting with this key
            try:
                plaintext = self.decrypt(data, key)
                score = self._score_text(plaintext)
                scores[key] = score
                
                if score < best_score:
                    best_score = score
                    best_key = key
                    best_plaintext = plaintext
            
            except Exception:
                continue
        
        # Calculate confidence (lower chi-squared = higher confidence)
        # Normalize to 0-1 range (chi-squared typically 0-500 for bad matches)
        confidence = max(0.0, min(1.0, 1.0 - (best_score / 500.0)))
        
        return {
            'success': True,
            'key': best_key,
            'plaintext': best_plaintext,
            'confidence': round(confidence, 4),
            'method': 'frequency_analysis',
            'attempts': self.ALPHABET_SIZE,
            'scores': scores,
            'best_chi_squared': round(best_score, 4)
        }
    
    def _score_text(self, text: str) -> float:
        """
        Score text using chi-squared test against English letter frequencies.
        
        Lower scores indicate better match to English language statistics.
        
        Args:
            text: Text to score
        
        Returns:
            Chi-squared statistic (lower is better)
        
        Time Complexity: O(n) where n is text length
        """
        # Count letter frequencies
        letter_counts = [0] * self.ALPHABET_SIZE
        total_letters = 0
        
        for char in text.upper():
            if char.isalpha():
                letter_counts[ord(char) - ord('A')] += 1
                total_letters += 1
        
        if total_letters == 0:
            return float('inf')
        
        # Calculate expected frequencies
        expected = [
            (freq / 100.0) * total_letters 
            for freq in self.ENGLISH_FREQ
        ]
        
        # Use chi-squared test from our math helpers
        try:
            return chi_squared(letter_counts, expected)
        except Exception:
            return float('inf')
    
    def __repr__(self) -> str:
        """Return string representation."""
        return "CaesarCipher()"
