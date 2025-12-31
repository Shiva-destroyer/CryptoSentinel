"""
Morse Code handler implementation.

Morse code is a character encoding that represents text characters as
sequences of dots and dashes (or dits and dahs).

Developer: saisrujanmurthy@gmail.com
"""

from typing import Any, Union
from crypto_sentinel.core.base_cipher import CipherInterface
from crypto_sentinel.core.exceptions import (
    EncryptionError,
    DecryptionError,
    ValidationError,
)


class MorseHandler(CipherInterface):
    """
    Morse Code encoder/decoder.
    
    Converts text to/from International Morse Code using dots (.) and
    dashes (-). Spaces between letters are represented by spaces,
    and spaces between words are represented by forward slashes (/).
    
    Features:
        - Encoding text to Morse code
        - Decoding Morse code to text
        - Support for letters, numbers, and common punctuation
        - No key required (not a cipher in traditional sense)
    
    Time Complexity:
        - Encode/Decode: O(n) where n is input length
        - Crack: O(n) (just calls decrypt)
    
    Space Complexity: O(n) for output
    
    Examples:
        >>> morse = MorseHandler()
        >>> encoded = morse.encrypt("HELLO", key=None)
        >>> print(encoded)
        '.... . .-.. .-.. --- '
        >>> decoded = morse.decrypt(".... . .-.. .-.. --- ", key=None)
        >>> print(decoded)
        'HELLO'
    """
    
    # International Morse Code mapping
    MORSE_CODE_DICT = {
        'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',   'E': '.',
        'F': '..-.',  'G': '--.',   'H': '....',  'I': '..',    'J': '.---',
        'K': '-.-',   'L': '.-..',  'M': '--',    'N': '-.',    'O': '---',
        'P': '.--.',  'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
        'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',  'Y': '-.--',
        'Z': '--..',
        
        '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
        '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
        
        '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.',
        '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-',
        '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-',
        '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.',
        '$': '...-..-', '@': '.--.-.',
    }
    
    # Reverse mapping for decoding
    REVERSE_MORSE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}
    
    def encrypt(self, data: Union[str, bytes], key: Any = None) -> Union[str, bytes]:
        """
        Encode text to Morse code.
        
        Converts each character to its Morse code representation.
        Letters are separated by spaces, words by ' / '.
        
        Args:
            data: Plaintext string to encode
            key: Not used (for interface compatibility)
        
        Returns:
            Morse code string
        
        Raises:
            EncryptionError: If encoding fails
            ValidationError: If data is invalid
        
        Time Complexity: O(n) where n is length of data
        Space Complexity: O(n) for result string
        
        Examples:
            >>> morse = MorseHandler()
            >>> morse.encrypt("SOS")
            '... --- ... '
            >>> morse.encrypt("HELLO WORLD")
            '.... . .-.. .-.. ---  / .-- --- .-. .-.. -.. '
        """
        if isinstance(data, bytes):
            raise ValidationError(
                "Morse code requires string input, not bytes",
                details={"provided_type": "bytes"}
            )
        
        if not isinstance(data, str):
            raise ValidationError(
                f"Data must be a string, got {type(data).__name__}",
                details={"provided_type": type(data).__name__}
            )
        
        if not data:
            return ""
        
        try:
            result = []
            words = data.upper().split()
            
            for word in words:
                morse_word = []
                for char in word:
                    if char in self.MORSE_CODE_DICT:
                        morse_word.append(self.MORSE_CODE_DICT[char])
                    else:
                        # Unknown character, skip or use placeholder
                        continue
                
                # Join letters with spaces
                if morse_word:
                    result.append(' '.join(morse_word) + ' ')
            
            # Join words with ' / '
            return ' / '.join(result) if len(result) > 1 else (result[0] if result else '')
        
        except Exception as e:
            raise EncryptionError(
                f"Failed to encode to Morse code: {e}",
                details={"error": str(e), "data_length": len(data)}
            )
    
    def decrypt(self, data: Union[str, bytes], key: Any = None) -> Union[str, bytes]:
        """
        Decode Morse code to text.
        
        Converts Morse code sequences back to characters.
        Expects letters separated by spaces and words by ' / '.
        
        Args:
            data: Morse code string to decode
            key: Not used (for interface compatibility)
        
        Returns:
            Decoded plaintext string
        
        Raises:
            DecryptionError: If decoding fails
            ValidationError: If data is invalid
        
        Time Complexity: O(n) where n is length of data
        Space Complexity: O(n) for result string
        
        Examples:
            >>> morse = MorseHandler()
            >>> morse.decrypt("... --- ... ")
            'SOS'
            >>> morse.decrypt(".... . .-.. .-.. ---  / .-- --- .-. .-.. -.. ")
            'HELLO WORLD'
        """
        if isinstance(data, bytes):
            raise ValidationError(
                "Morse code requires string input, not bytes",
                details={"provided_type": "bytes"}
            )
        
        if not isinstance(data, str):
            raise ValidationError(
                f"Data must be a string, got {type(data).__name__}",
                details={"provided_type": type(data).__name__}
            )
        
        if not data or data.strip() == '':
            return ""
        
        try:
            result = []
            
            # Split by word separator ' / '
            words = data.split(' / ')
            
            for word in words:
                # Split by letter separator (space)
                morse_chars = word.strip().split()
                
                decoded_word = []
                for morse_char in morse_chars:
                    if morse_char in self.REVERSE_MORSE_DICT:
                        decoded_word.append(self.REVERSE_MORSE_DICT[morse_char])
                    else:
                        # Unknown Morse sequence, use '?' as placeholder
                        if morse_char.strip():  # Only if not empty
                            decoded_word.append('?')
                
                if decoded_word:
                    result.append(''.join(decoded_word))
            
            return ' '.join(result)
        
        except Exception as e:
            raise DecryptionError(
                f"Failed to decode Morse code: {e}",
                details={"error": str(e), "data_length": len(data)}
            )
    
    def crack(self, data: Union[str, bytes]) -> dict[str, Any]:
        """
        'Crack' Morse code (really just decode it).
        
        Morse code doesn't use a key, so cracking is equivalent to decoding.
        This method exists to satisfy the CipherInterface.
        
        Args:
            data: Morse code string
        
        Returns:
            Dictionary containing:
                - success: bool
                - key: None (Morse has no key)
                - plaintext: str, decoded text
                - confidence: 1.0 (always confident if decode succeeds)
                - method: str
                - attempts: 1
        
        Raises:
            ValidationError: If input data is invalid
        
        Time Complexity: O(n) where n is length of data
        Space Complexity: O(n) for plaintext
        
        Examples:
            >>> morse = MorseHandler()
            >>> result = morse.crack("... --- ... ")
            >>> print(result['plaintext'])
            'SOS'
        """
        if isinstance(data, bytes):
            raise ValidationError(
                "Morse code requires string input, not bytes",
                details={"provided_type": "bytes"}
            )
        
        if not isinstance(data, str):
            raise ValidationError(
                f"Data must be a string, got {type(data).__name__}",
                details={"provided_type": type(data).__name__}
            )
        
        try:
            plaintext = self.decrypt(data, key=None)
            
            # Check if decoding was successful (no unknown characters)
            success = '?' not in plaintext
            confidence = 1.0 if success else 0.5
            
            return {
                'success': True,
                'key': None,
                'plaintext': plaintext,
                'confidence': confidence,
                'method': 'standard_decoding',
                'attempts': 1,
                'note': 'Morse code does not use encryption keys'
            }
        
        except DecryptionError as e:
            return {
                'success': False,
                'key': None,
                'plaintext': None,
                'confidence': 0.0,
                'method': 'standard_decoding',
                'attempts': 1,
                'error': str(e)
            }
    
    def encode_to_audio_pattern(self, text: str) -> list[tuple[str, float]]:
        """
        Convert text to audio timing pattern for Morse code.
        
        Returns a list of (signal_type, duration) tuples where:
        - 'dit' represents a dot (short signal)
        - 'dah' represents a dash (long signal)
        - 'gap' represents silence between elements
        
        Args:
            text: Text to convert
        
        Returns:
            List of (signal_type, duration) tuples
        
        Time Complexity: O(n)
        
        Examples:
            >>> morse = MorseHandler()
            >>> morse.encode_to_audio_pattern("SOS")
            [('dit', 1), ('gap', 1), ('dit', 1), ('gap', 1), ('dit', 1), ...]
        """
        morse = self.encrypt(text, key=None)
        pattern = []
        
        for char in morse:
            if char == '.':
                pattern.append(('dit', 1.0))
                pattern.append(('gap', 1.0))
            elif char == '-':
                pattern.append(('dah', 3.0))
                pattern.append(('gap', 1.0))
            elif char == ' ':
                pattern.append(('gap', 3.0))
            elif char == '/':
                pattern.append(('gap', 7.0))
        
        return pattern
    
    def __repr__(self) -> str:
        """Return string representation."""
        return "MorseHandler()"
