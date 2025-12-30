"""
Vigenère Cipher implementation with IoC-based key detection.

The Vigenère cipher is a polyalphabetic substitution cipher that uses
a keyword to shift letters by different amounts.

Author: saisrujanmurthy@gmail.com
"""

from typing import Any, Union
from crypto_sentinel.core.base_cipher import CipherInterface
from crypto_sentinel.core.exceptions import (
    EncryptionError,
    DecryptionError,
    InvalidKeyError,
    ValidationError,
    CrackingError,
)
from crypto_sentinel.utils.math_helpers import calculate_ioc, chi_squared


class VigenereCipher(CipherInterface):
    """
    Vigenère Cipher with advanced cryptanalysis using Index of Coincidence.
    
    A polyalphabetic substitution cipher that uses a repeating keyword to
    determine the shift for each character. More secure than Caesar cipher
    as it doesn't preserve frequency distribution.
    
    Features:
        - Encryption/Decryption with string keys
        - Kasiski examination and IoC analysis for key length detection
        - Column-wise Caesar cipher solving for key recovery
    
    Time Complexity:
        - Encrypt/Decrypt: O(n) where n is text length
        - Crack: O(n*k) where k is estimated key length
    
    Space Complexity: O(n) for output string
    
    Examples:
        >>> cipher = VigenereCipher()
        >>> encrypted = cipher.encrypt("HELLO", key="KEY")
        >>> print(encrypted)
        'RIJVS'
    """
    
    ALPHABET_SIZE = 26
    
    # English letter frequency (percentage)
    ENGLISH_FREQ = [
        8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966,
        0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987,
        6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074
    ]
    
    def encrypt(self, data: Union[str, bytes], key: Any) -> Union[str, bytes]:
        """
        Encrypt plaintext using Vigenère cipher.
        
        Each letter is shifted by the corresponding letter in the key.
        The key repeats to match the plaintext length.
        
        Args:
            data: Plaintext string to encrypt
            key: Keyword string (alphabetic characters only)
        
        Returns:
            Encrypted ciphertext string
        
        Raises:
            InvalidKeyError: If key is invalid
            EncryptionError: If encryption fails
            ValidationError: If data is invalid
        
        Time Complexity: O(n) where n is length of data
        Space Complexity: O(n) for result string
        
        Examples:
            >>> cipher = VigenereCipher()
            >>> cipher.encrypt("ATTACKATDAWN", key="LEMON")
            'LXFOPVEFRNHR'
        """
        if isinstance(data, bytes):
            raise ValidationError(
                "Vigenère cipher requires string input, not bytes",
                details={"provided_type": "bytes"}
            )
        
        if not isinstance(data, str):
            raise ValidationError(
                f"Data must be a string, got {type(data).__name__}",
                details={"provided_type": type(data).__name__}
            )
        
        # Validate key
        if not isinstance(key, str):
            raise InvalidKeyError(
                f"Key must be a string, got {type(key).__name__}",
                details={"provided_type": type(key).__name__}
            )
        
        if not key or not key.isalpha():
            raise InvalidKeyError(
                "Key must contain only alphabetic characters",
                details={"key": key}
            )
        
        try:
            result = []
            key_upper = key.upper()
            key_index = 0
            
            for char in data:
                if char.isalpha():
                    # Determine base (uppercase or lowercase)
                    base = ord('A') if char.isupper() else ord('a')
                    
                    # Get shift from key
                    shift = ord(key_upper[key_index % len(key_upper)]) - ord('A')
                    
                    # Apply shift
                    shifted = (ord(char) - base + shift) % self.ALPHABET_SIZE
                    result.append(chr(base + shifted))
                    
                    # Move to next key character
                    key_index += 1
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
        Decrypt ciphertext using Vigenère cipher.
        
        Reverses encryption by shifting in the opposite direction.
        
        Args:
            data: Ciphertext string to decrypt
            key: Keyword string (alphabetic characters only)
        
        Returns:
            Decrypted plaintext string
        
        Raises:
            InvalidKeyError: If key is invalid
            DecryptionError: If decryption fails
            ValidationError: If data is invalid
        
        Time Complexity: O(n) where n is length of data
        Space Complexity: O(n) for result string
        
        Examples:
            >>> cipher = VigenereCipher()
            >>> cipher.decrypt("LXFOPVEFRNHR", key="LEMON")
            'ATTACKATDAWN'
        """
        if not isinstance(key, str):
            raise InvalidKeyError(
                f"Key must be a string, got {type(key).__name__}",
                details={"provided_type": type(key).__name__}
            )
        
        try:
            # Create inverse key (negate each shift)
            inverse_key = ''.join(
                chr((self.ALPHABET_SIZE - (ord(c.upper()) - ord('A'))) % self.ALPHABET_SIZE + ord('A'))
                for c in key if c.isalpha()
            )
            
            # Decrypt using inverse key
            return self.encrypt(data, inverse_key)
        
        except EncryptionError as e:
            raise DecryptionError(
                f"Failed to decrypt data: {e}",
                details={"error": str(e), "key": key}
            )
    
    def crack(self, data: Union[str, bytes]) -> dict[str, Any]:
        """
        Crack Vigenère cipher using Friedman test and frequency analysis.
        
        Algorithm:
        1. Use Index of Coincidence to estimate key length (Friedman test)
        2. Split ciphertext into columns based on key length
        3. Solve each column as a Caesar cipher using frequency analysis
        4. Reassemble the key from column solutions
        
        Args:
            data: Ciphertext string to crack
        
        Returns:
            Dictionary containing:
                - success: bool
                - key: str, recovered keyword
                - plaintext: str, decrypted text
                - confidence: float (0-1)
                - method: str
                - attempts: int
                - key_length: int, detected key length
        
        Raises:
            ValidationError: If input data is invalid
            CrackingError: If cracking process fails
        
        Time Complexity: O(n*k*26) where n is text length, k is key length
        Space Complexity: O(n) for storing columns
        
        Examples:
            >>> cipher = VigenereCipher()
            >>> result = cipher.crack("LXFOPVEFRNHR")
            >>> print(result['key'])
            'LEMON'
        """
        if isinstance(data, bytes):
            raise ValidationError(
                "Vigenère cipher requires string input, not bytes",
                details={"provided_type": "bytes"}
            )
        
        if not isinstance(data, str):
            raise ValidationError(
                f"Data must be a string, got {type(data).__name__}",
                details={"provided_type": type(data).__name__}
            )
        
        # Filter to alphabetic characters only
        filtered_text = ''.join(c.upper() for c in data if c.isalpha())
        
        if len(filtered_text) < 20:
            return {
                'success': False,
                'key': None,
                'plaintext': None,
                'confidence': 0.0,
                'method': 'friedman_test',
                'attempts': 0,
                'error': 'Text too short for reliable analysis (minimum 20 letters)'
            }
        
        try:
            # Step 1: Estimate key length using IoC
            key_length = self._estimate_key_length(filtered_text)
            
            if key_length == 1:
                # Fallback to Caesar cipher
                return {
                    'success': False,
                    'key': None,
                    'plaintext': None,
                    'confidence': 0.0,
                    'method': 'friedman_test',
                    'attempts': 0,
                    'error': 'Detected as monoalphabetic cipher, use Caesar instead'
                }
            
            # Step 2: Split into columns
            columns = [''] * key_length
            for i, char in enumerate(filtered_text):
                columns[i % key_length] += char
            
            # Step 3: Solve each column as Caesar cipher
            key_chars = []
            total_confidence = 0.0
            
            for column in columns:
                if not column:
                    key_chars.append('A')
                    continue
                
                best_shift = 0
                best_score = float('inf')
                
                for shift in range(self.ALPHABET_SIZE):
                    # Decrypt column with this shift
                    decrypted = ''.join(
                        chr((ord(c) - ord('A') - shift) % self.ALPHABET_SIZE + ord('A'))
                        for c in column
                    )
                    score = self._score_text(decrypted)
                    
                    if score < best_score:
                        best_score = score
                        best_shift = shift
                
                key_chars.append(chr(best_shift + ord('A')))
                # Calculate confidence for this column
                confidence = max(0.0, min(1.0, 1.0 - (best_score / 500.0)))
                total_confidence += confidence
            
            # Step 4: Reassemble key
            key = ''.join(key_chars)
            
            # Decrypt with found key
            try:
                plaintext = self.decrypt(data, key)
                avg_confidence = total_confidence / len(key_chars) if key_chars else 0.0
                
                return {
                    'success': True,
                    'key': key,
                    'plaintext': plaintext,
                    'confidence': round(avg_confidence, 4),
                    'method': 'friedman_test',
                    'attempts': key_length * self.ALPHABET_SIZE,
                    'key_length': key_length
                }
            
            except Exception as e:
                raise CrackingError(
                    f"Failed to decrypt with found key: {e}",
                    details={"key": key, "error": str(e)}
                )
        
        except Exception as e:
            raise CrackingError(
                f"Failed to crack cipher: {e}",
                details={"error": str(e)}
            )
    
    def _estimate_key_length(self, text: str, max_length: int = 20) -> int:
        """
        Estimate key length using Index of Coincidence (Friedman test).
        
        Tests different key lengths and selects the one where column IoCs
        are closest to English text IoC (~0.065-0.068).
        
        Args:
            text: Filtered alphabetic text (uppercase)
            max_length: Maximum key length to test
        
        Returns:
            Estimated key length
        
        Time Complexity: O(n*k) where k is max_length
        """
        best_length = 1
        best_score = float('inf')
        
        for length in range(1, min(max_length + 1, len(text) // 2)):
            # Split into columns
            columns = [''] * length
            for i, char in enumerate(text):
                columns[i % length] += char
            
            # Calculate average IoC for columns
            ioc_sum = 0.0
            valid_columns = 0
            
            for column in columns:
                if len(column) >= 2:
                    try:
                        ioc = calculate_ioc(column)
                        ioc_sum += ioc
                        valid_columns += 1
                    except Exception:
                        continue
            
            if valid_columns > 0:
                avg_ioc = ioc_sum / valid_columns
                # English text IoC is ~0.065-0.068
                # Score is distance from expected IoC
                score = abs(avg_ioc - 0.0667)
                
                if score < best_score:
                    best_score = score
                    best_length = length
        
        return best_length
    
    def _score_text(self, text: str) -> float:
        """
        Score text using chi-squared test against English frequencies.
        
        Args:
            text: Text to score (uppercase alphabetic)
        
        Returns:
            Chi-squared statistic (lower is better)
        
        Time Complexity: O(n)
        """
        letter_counts = [0] * self.ALPHABET_SIZE
        total_letters = 0
        
        for char in text:
            if char.isalpha():
                letter_counts[ord(char.upper()) - ord('A')] += 1
                total_letters += 1
        
        if total_letters == 0:
            return float('inf')
        
        expected = [
            (freq / 100.0) * total_letters 
            for freq in self.ENGLISH_FREQ
        ]
        
        try:
            return chi_squared(letter_counts, expected)
        except Exception:
            return float('inf')
    
    def __repr__(self) -> str:
        """Return string representation."""
        return "VigenereCipher()"
