"""
Comprehensive unit tests for classical cipher implementations.

Tests encryption, decryption, and cracking for Caesar, Vigenère, XOR,
Substitution, and Morse code implementations.

Author: saisrujanmurthy@gmail.com
"""

import pytest
from crypto_sentinel.ciphers import (
    CaesarCipher,
    VigenereCipher,
    XORCipher,
    SubstitutionCipher,
    MorseHandler,
)
from crypto_sentinel.core.exceptions import (
    EncryptionError,
    DecryptionError,
    InvalidKeyError,
    ValidationError,
)


class TestCaesarCipher:
    """Test cases for Caesar cipher."""
    
    def test_encrypt_basic(self) -> None:
        """Test basic encryption."""
        cipher = CaesarCipher()
        result = cipher.encrypt("HELLO", key=3)
        assert result == "KHOOR"
    
    def test_encrypt_with_spaces(self) -> None:
        """Test encryption preserves spaces."""
        cipher = CaesarCipher()
        result = cipher.encrypt("HELLO WORLD", key=3)
        assert result == "KHOOR ZRUOG"
    
    def test_encrypt_mixed_case(self) -> None:
        """Test encryption preserves case."""
        cipher = CaesarCipher()
        result = cipher.encrypt("Hello World", key=5)
        assert result == "Mjqqt Btwqi"
    
    def test_encrypt_with_punctuation(self) -> None:
        """Test encryption preserves punctuation."""
        cipher = CaesarCipher()
        result = cipher.encrypt("Attack at dawn!", key=5)
        assert result == "Fyyfhp fy ifbs!"
    
    def test_encrypt_wrap_around(self) -> None:
        """Test encryption wraps around alphabet."""
        cipher = CaesarCipher()
        result = cipher.encrypt("XYZ", key=3)
        assert result == "ABC"
    
    def test_decrypt_basic(self) -> None:
        """Test basic decryption."""
        cipher = CaesarCipher()
        result = cipher.decrypt("KHOOR", key=3)
        assert result == "HELLO"
    
    def test_encrypt_decrypt_roundtrip(self) -> None:
        """Test encryption and decryption roundtrip."""
        cipher = CaesarCipher()
        original = "The quick brown fox jumps over the lazy dog"
        encrypted = cipher.encrypt(original, key=13)
        decrypted = cipher.decrypt(encrypted, key=13)
        assert decrypted == original
    
    def test_invalid_key_type(self) -> None:
        """Test that non-integer key raises error."""
        cipher = CaesarCipher()
        with pytest.raises(InvalidKeyError):
            cipher.encrypt("HELLO", key="invalid")
    
    def test_invalid_key_range(self) -> None:
        """Test that out-of-range key raises error."""
        cipher = CaesarCipher()
        with pytest.raises(InvalidKeyError):
            cipher.encrypt("HELLO", key=30)
    
    def test_invalid_data_type(self) -> None:
        """Test that bytes input raises error."""
        cipher = CaesarCipher()
        with pytest.raises(ValidationError):
            cipher.encrypt(b"HELLO", key=3)
    
    def test_crack_simple(self) -> None:
        """Test cracking simple Caesar cipher."""
        cipher = CaesarCipher()
        ciphertext = "KHOOR ZRUOG"
        result = cipher.crack(ciphertext)
        
        assert result['success'] is True
        assert result['key'] == 3
        assert result['plaintext'] == "HELLO WORLD"
        assert result['confidence'] > 0.5
    
    def test_crack_longer_text(self) -> None:
        """Test cracking with longer text."""
        cipher = CaesarCipher()
        plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        encrypted = cipher.encrypt(plaintext, key=7)
        result = cipher.crack(encrypted)
        
        assert result['success'] is True
        assert result['key'] == 7
        assert result['plaintext'] == plaintext
    
    def test_crack_returns_scores(self) -> None:
        """Test that crack returns chi-squared scores."""
        cipher = CaesarCipher()
        result = cipher.crack("KHOOR")
        
        assert 'scores' in result
        assert len(result['scores']) == 26


class TestVigenereCipher:
    """Test cases for Vigenère cipher."""
    
    def test_encrypt_basic(self) -> None:
        """Test basic encryption."""
        cipher = VigenereCipher()
        result = cipher.encrypt("ATTACKATDAWN", key="LEMON")
        assert result == "LXFOPVEFRNHR"
    
    def test_encrypt_key_repetition(self) -> None:
        """Test that key repeats correctly."""
        cipher = VigenereCipher()
        result = cipher.encrypt("AAAA", key="AB")
        assert result == "ABAB"
    
    def test_encrypt_preserves_case(self) -> None:
        """Test encryption preserves case."""
        cipher = VigenereCipher()
        result = cipher.encrypt("Hello", key="KEY")
        assert result == "Rijvs"
    
    def test_decrypt_basic(self) -> None:
        """Test basic decryption."""
        cipher = VigenereCipher()
        result = cipher.decrypt("LXFOPVEFRNHR", key="LEMON")
        assert result == "ATTACKATDAWN"
    
    def test_encrypt_decrypt_roundtrip(self) -> None:
        """Test encryption and decryption roundtrip."""
        cipher = VigenereCipher()
        original = "The quick brown fox"
        key = "SECRET"
        encrypted = cipher.encrypt(original, key=key)
        decrypted = cipher.decrypt(encrypted, key=key)
        assert decrypted == original
    
    def test_invalid_key_empty(self) -> None:
        """Test that empty key raises error."""
        cipher = VigenereCipher()
        with pytest.raises(InvalidKeyError):
            cipher.encrypt("HELLO", key="")
    
    def test_invalid_key_non_alpha(self) -> None:
        """Test that non-alphabetic key raises error."""
        cipher = VigenereCipher()
        with pytest.raises(InvalidKeyError):
            cipher.encrypt("HELLO", key="KEY123")
    
    def test_crack_short_text_fails(self) -> None:
        """Test that cracking very short text fails gracefully."""
        cipher = VigenereCipher()
        result = cipher.crack("ABC")
        assert result['success'] is False
    
    def test_crack_estimates_key_length(self) -> None:
        """Test that crack estimates key length."""
        cipher = VigenereCipher()
        plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG " * 3
        key = "LEMON"
        encrypted = cipher.encrypt(plaintext, key=key)
        result = cipher.crack(encrypted)
        
        # Should detect key length (may not be exact due to short text)
        assert 'key_length' in result


class TestXORCipher:
    """Test cases for XOR cipher."""
    
    def test_encrypt_string(self) -> None:
        """Test string encryption returns hex."""
        cipher = XORCipher()
        result = cipher.encrypt("HELLO", key=42)
        assert isinstance(result, str)
        assert len(result) == 10  # 5 bytes * 2 hex chars
    
    def test_encrypt_bytes(self) -> None:
        """Test bytes encryption returns bytes."""
        cipher = XORCipher()
        result = cipher.encrypt(b"HELLO", key=42)
        assert isinstance(result, bytes)
        assert len(result) == 5
    
    def test_decrypt_hex_string(self) -> None:
        """Test decrypting hex string."""
        cipher = XORCipher()
        encrypted = cipher.encrypt("HELLO", key=42)
        decrypted = cipher.decrypt(encrypted, key=42)
        assert decrypted == "HELLO"
    
    def test_decrypt_bytes(self) -> None:
        """Test decrypting bytes."""
        cipher = XORCipher()
        encrypted = cipher.encrypt(b"HELLO", key=42)
        decrypted = cipher.decrypt(encrypted, key=42)
        assert decrypted == b"HELLO"
    
    def test_xor_is_symmetric(self) -> None:
        """Test that XOR is symmetric operation."""
        cipher = XORCipher()
        data = "Test message"
        key = 123
        
        encrypted = cipher.encrypt(data, key=key)
        decrypted = cipher.decrypt(encrypted, key=key)
        assert decrypted == data
    
    def test_multi_byte_key(self) -> None:
        """Test encryption with multi-byte key."""
        cipher = XORCipher()
        result = cipher.encrypt("HELLO", key=b"KEY")
        assert isinstance(result, str)
    
    def test_string_key(self) -> None:
        """Test encryption with string key."""
        cipher = XORCipher()
        result = cipher.encrypt("HELLO", key="SECRET")
        decrypted = cipher.decrypt(result, key="SECRET")
        assert decrypted == "HELLO"
    
    def test_invalid_key_range(self) -> None:
        """Test that integer key out of range raises error."""
        cipher = XORCipher()
        with pytest.raises(InvalidKeyError):
            cipher.encrypt("HELLO", key=256)
    
    def test_crack_single_byte(self) -> None:
        """Test cracking with single-byte key."""
        cipher = XORCipher()
        plaintext = "the quick brown fox jumps"
        key = 42
        encrypted = cipher.encrypt(plaintext, key=key)
        result = cipher.crack(encrypted)
        
        assert result['success'] is True
        assert result['key'] == key
        assert result['plaintext'] == plaintext
    
    def test_crack_returns_scores(self) -> None:
        """Test that crack returns scores for all keys."""
        cipher = XORCipher()
        encrypted = cipher.encrypt("HELLO", key=42)
        result = cipher.crack(encrypted)
        
        assert 'scores' in result
        assert len(result['scores']) == 256


class TestSubstitutionCipher:
    """Test cases for Substitution cipher."""
    
    def test_encrypt_basic(self) -> None:
        """Test basic encryption."""
        cipher = SubstitutionCipher()
        key = "QWERTYUIOPASDFGHJKLZXCVBNM"
        result = cipher.encrypt("HELLO", key=key)
        assert result == "ITSSG"
    
    def test_decrypt_basic(self) -> None:
        """Test basic decryption."""
        cipher = SubstitutionCipher()
        key = "QWERTYUIOPASDFGHJKLZXCVBNM"
        result = cipher.decrypt("ITSSG", key=key)
        assert result == "HELLO"
    
    def test_encrypt_decrypt_roundtrip(self) -> None:
        """Test encryption and decryption roundtrip."""
        cipher = SubstitutionCipher()
        key = "QWERTYUIOPASDFGHJKLZXCVBNM"
        original = "The Quick Brown Fox"
        encrypted = cipher.encrypt(original, key=key)
        decrypted = cipher.decrypt(encrypted, key=key)
        assert decrypted == original
    
    def test_preserves_case(self) -> None:
        """Test that case is preserved."""
        cipher = SubstitutionCipher()
        key = "QWERTYUIOPASDFGHJKLZXCVBNM"
        result = cipher.encrypt("Hello World", key=key)
        assert result == "Itssg Vgksr"
    
    def test_invalid_key_length(self) -> None:
        """Test that wrong length key raises error."""
        cipher = SubstitutionCipher()
        with pytest.raises(InvalidKeyError):
            cipher.encrypt("HELLO", key="SHORT")
    
    def test_invalid_key_duplicates(self) -> None:
        """Test that key with duplicates raises error."""
        cipher = SubstitutionCipher()
        key = "ABCDEFGHIJKLMNOPQRSTUVWXAA"  # Has duplicates
        with pytest.raises(InvalidKeyError):
            cipher.encrypt("HELLO", key=key)
    
    def test_invalid_key_non_alpha(self) -> None:
        """Test that non-alphabetic key raises error."""
        cipher = SubstitutionCipher()
        key = "QWERTYUIOP123DFGHJKLZXCVB"
        with pytest.raises(InvalidKeyError):
            cipher.encrypt("HELLO", key=key)
    
    def test_crack_short_text_fails(self) -> None:
        """Test that cracking very short text fails."""
        cipher = SubstitutionCipher()
        result = cipher.crack("HI")
        assert result['success'] is False
    
    def test_crack_attempts_hill_climbing(self) -> None:
        """Test that crack uses hill climbing."""
        cipher = SubstitutionCipher()
        # Use longer text for better cracking
        plaintext = "the quick brown fox jumps over the lazy dog " * 5
        key = "QWERTYUIOPASDFGHJKLZXCVBNM"
        encrypted = cipher.encrypt(plaintext, key=key)
        result = cipher.crack(encrypted)
        
        assert 'attempts' in result
        assert result['attempts'] > 100  # Should try many swaps


class TestMorseHandler:
    """Test cases for Morse code handler."""
    
    def test_encrypt_basic(self) -> None:
        """Test basic encoding."""
        morse = MorseHandler()
        result = morse.encrypt("SOS", key=None)
        assert "..." in result
        assert "---" in result
    
    def test_encrypt_full_word(self) -> None:
        """Test encoding a word."""
        morse = MorseHandler()
        result = morse.encrypt("HELLO", key=None)
        assert "...." in result  # H
        assert "." in result      # E
        assert ".-.." in result   # L
        assert "---" in result    # O
    
    def test_encrypt_with_spaces(self) -> None:
        """Test encoding multiple words."""
        morse = MorseHandler()
        result = morse.encrypt("HELLO WORLD", key=None)
        assert "/" in result  # Word separator
    
    def test_decrypt_basic(self) -> None:
        """Test basic decoding."""
        morse = MorseHandler()
        result = morse.decrypt("... --- ... ", key=None)
        assert result == "SOS"
    
    def test_encrypt_decrypt_roundtrip(self) -> None:
        """Test encoding and decoding roundtrip."""
        morse = MorseHandler()
        original = "HELLO WORLD"
        encoded = morse.encrypt(original, key=None)
        decoded = morse.decrypt(encoded, key=None)
        assert decoded == original
    
    def test_encrypt_numbers(self) -> None:
        """Test encoding numbers."""
        morse = MorseHandler()
        result = morse.encrypt("123", key=None)
        assert ".----" in result  # 1
        assert "..---" in result  # 2
        assert "...--" in result  # 3
    
    def test_encrypt_punctuation(self) -> None:
        """Test encoding punctuation."""
        morse = MorseHandler()
        result = morse.encrypt("SOS!", key=None)
        assert "-.-.--" in result  # !
    
    def test_decrypt_unknown_sequence(self) -> None:
        """Test decoding handles unknown sequences."""
        morse = MorseHandler()
        result = morse.decrypt("... .... .....", key=None)
        # Should handle gracefully (may include ?)
        assert isinstance(result, str)
    
    def test_crack_is_decode(self) -> None:
        """Test that crack just decodes."""
        morse = MorseHandler()
        encoded = morse.encrypt("SOS", key=None)
        result = morse.crack(encoded)
        
        assert result['success'] is True
        assert result['key'] is None
        assert result['plaintext'] == "SOS"
        assert result['confidence'] == 1.0
    
    def test_encode_to_audio_pattern(self) -> None:
        """Test audio pattern generation."""
        morse = MorseHandler()
        pattern = morse.encode_to_audio_pattern("SOS")
        
        assert len(pattern) > 0
        assert all(isinstance(p, tuple) for p in pattern)
        assert all(p[0] in ['dit', 'dah', 'gap'] for p in pattern)
    
    def test_empty_string(self) -> None:
        """Test handling empty string."""
        morse = MorseHandler()
        result = morse.encrypt("", key=None)
        assert result == ""
        
        result = morse.decrypt("", key=None)
        assert result == ""


class TestCipherIntegration:
    """Integration tests across multiple ciphers."""
    
    def test_all_ciphers_implement_interface(self) -> None:
        """Test that all ciphers implement required methods."""
        ciphers = [
            CaesarCipher(),
            VigenereCipher(),
            XORCipher(),
            SubstitutionCipher(),
            MorseHandler()
        ]
        
        for cipher in ciphers:
            assert hasattr(cipher, 'encrypt')
            assert hasattr(cipher, 'decrypt')
            assert hasattr(cipher, 'crack')
    
    def test_all_ciphers_have_repr(self) -> None:
        """Test that all ciphers have string representation."""
        ciphers = [
            CaesarCipher(),
            VigenereCipher(),
            XORCipher(),
            SubstitutionCipher(),
            MorseHandler()
        ]
        
        for cipher in ciphers:
            repr_str = repr(cipher)
            assert isinstance(repr_str, str)
            assert len(repr_str) > 0
    
    def test_caesar_vs_vigenere_with_single_char_key(self) -> None:
        """Test that Vigenère with single char key equals Caesar."""
        plaintext = "HELLO"
        shift = 3
        
        caesar = CaesarCipher()
        vigenere = VigenereCipher()
        
        caesar_result = caesar.encrypt(plaintext, key=shift)
        # Convert shift to letter: 3 -> 'D'
        vigenere_result = vigenere.encrypt(plaintext, key=chr(shift + ord('A')))
        
        assert caesar_result == vigenere_result
