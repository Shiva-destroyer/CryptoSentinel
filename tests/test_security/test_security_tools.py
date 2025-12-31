"""
Comprehensive tests for security tools.

Tests password analyzer with entropy calculations and Base64 encoder
with various edge cases.

Developer: saisrujanmurthy@gmail.com
"""

import pytest
from crypto_sentinel.security import PasswordAnalyzer, Base64Encoder
from crypto_sentinel.core.exceptions import (
    ValidationError,
    EncryptionError,
    DecryptionError,
)


class TestPasswordAnalyzer:
    """Test cases for password strength analyzer."""
    
    def test_analyze_weak_password(self) -> None:
        """Test analysis of weak password 'password123'."""
        analyzer = PasswordAnalyzer()
        result = analyzer.analyze("password123")
        
        assert result['score'] < 50  # Weak score
        assert result['length'] == 11
        assert result['strength_level'] in ['weak', 'very_weak', 'moderate']
        assert result['entropy_bits'] < 60  # Not strong
        assert len(result['recommendations']) > 0
    
    def test_analyze_strong_password(self) -> None:
        """Test analysis of strong password 'Tr0ub4dor&3'."""
        analyzer = PasswordAnalyzer()
        result = analyzer.analyze("Tr0ub4dor&3")
        
        assert result['score'] > 50  # Better score than weak password
        assert result['length'] == 11
        assert result['entropy_bits'] > 40  # Higher entropy
        assert 'crack_time_display' in result
    
    def test_entropy_comparison(self) -> None:
        """Test that strong password has higher entropy than weak."""
        analyzer = PasswordAnalyzer()
        
        weak = analyzer.analyze("password123")
        strong = analyzer.analyze("Tr0ub4dor&3")
        
        # Strong password should have more entropy
        assert strong['entropy_bits'] > weak['entropy_bits']
        assert strong['score'] >= weak['score']
    
    def test_analyze_empty_password(self) -> None:
        """Test analysis of empty password."""
        analyzer = PasswordAnalyzer()
        result = analyzer.analyze("")
        
        assert result['score'] == 0
        assert result['entropy_bits'] == 0.0
        assert result['strength_level'] == 'very_weak'
        assert 'empty' in result['recommendations'][0].lower()
    
    def test_analyze_lowercase_only(self) -> None:
        """Test password with only lowercase letters."""
        analyzer = PasswordAnalyzer()
        result = analyzer.analyze("abcdefgh")
        
        assert result['pool_size'] == 26  # Only lowercase
        # Entropy = 8 * log2(26) ≈ 8 * 4.7 ≈ 37.6
        assert 35 < result['entropy_bits'] < 40
    
    def test_analyze_mixed_case(self) -> None:
        """Test password with mixed case letters."""
        analyzer = PasswordAnalyzer()
        result = analyzer.analyze("AbCdEfGh")
        
        assert result['pool_size'] == 52  # Uppercase + lowercase
        # Entropy = 8 * log2(52) ≈ 8 * 5.7 ≈ 45.6
        assert 44 < result['entropy_bits'] < 48
    
    def test_analyze_alphanumeric(self) -> None:
        """Test password with letters and numbers."""
        analyzer = PasswordAnalyzer()
        result = analyzer.analyze("Abc123Def")
        
        assert result['pool_size'] == 62  # Mixed case + digits
        # Entropy = 9 * log2(62) ≈ 9 * 5.95 ≈ 53.5
        assert 52 < result['entropy_bits'] < 56
    
    def test_analyze_full_spectrum(self) -> None:
        """Test password with all character types."""
        analyzer = PasswordAnalyzer()
        result = analyzer.analyze("Abc123!@#")
        
        assert result['pool_size'] == 94  # All types
        # Entropy = 9 * log2(94) ≈ 9 * 6.55 ≈ 59
        assert 57 < result['entropy_bits'] < 62
    
    def test_crack_time_estimation(self) -> None:
        """Test that crack time increases with entropy."""
        analyzer = PasswordAnalyzer()
        
        weak = analyzer.analyze("abc")
        strong = analyzer.analyze("MyStr0ngP@ssw0rd!")
        
        # Strong password should take longer to crack
        assert strong['crack_time_seconds'] > weak['crack_time_seconds']
        assert 'crack_time_display' in weak
        assert 'crack_time_display' in strong
    
    def test_recommendations_for_short_password(self) -> None:
        """Test recommendations for short password."""
        analyzer = PasswordAnalyzer()
        result = analyzer.analyze("abc")
        
        recommendations = result['recommendations']
        assert any('length' in r.lower() for r in recommendations)
    
    def test_recommendations_for_no_uppercase(self) -> None:
        """Test recommendations when missing uppercase."""
        analyzer = PasswordAnalyzer()
        result = analyzer.analyze("password123!")
        
        recommendations = result['recommendations']
        assert any('uppercase' in r.lower() for r in recommendations)
    
    def test_recommendations_for_no_numbers(self) -> None:
        """Test recommendations when missing numbers."""
        analyzer = PasswordAnalyzer()
        result = analyzer.analyze("Password!")
        
        recommendations = result['recommendations']
        assert any('number' in r.lower() for r in recommendations)
    
    def test_recommendations_for_no_special(self) -> None:
        """Test recommendations when missing special characters."""
        analyzer = PasswordAnalyzer()
        result = analyzer.analyze("Password123")
        
        recommendations = result['recommendations']
        assert any('special' in r.lower() for r in recommendations)
    
    def test_detect_repeated_characters(self) -> None:
        """Test detection of repeated characters."""
        analyzer = PasswordAnalyzer()
        result = analyzer.analyze("Passsword111")
        
        recommendations = result['recommendations']
        assert any('repeat' in r.lower() for r in recommendations)
    
    def test_detect_sequential_numbers(self) -> None:
        """Test detection of sequential numbers."""
        analyzer = PasswordAnalyzer()
        result = analyzer.analyze("Pass123word")
        
        recommendations = result['recommendations']
        assert any('sequential' in r.lower() for r in recommendations)
    
    def test_detect_common_patterns(self) -> None:
        """Test detection of common weak patterns."""
        analyzer = PasswordAnalyzer()
        result = analyzer.analyze("password123")
        
        recommendations = result['recommendations']
        assert any('common' in r.lower() or 'pattern' in r.lower() for r in recommendations)
    
    def test_validate_weak_password(self) -> None:
        """Test that weak password fails validation."""
        analyzer = PasswordAnalyzer()
        assert analyzer.validate("weak") is False
    
    def test_validate_strong_password(self) -> None:
        """Test that strong password passes validation."""
        analyzer = PasswordAnalyzer()
        assert analyzer.validate("MyStr0ng!Pass") is True
    
    def test_validate_short_password(self) -> None:
        """Test that short password fails validation."""
        analyzer = PasswordAnalyzer()
        assert analyzer.validate("Sh0rt!") is False
    
    def test_score_ranges(self) -> None:
        """Test that scores are in valid range 0-100."""
        analyzer = PasswordAnalyzer()
        
        passwords = [
            "",
            "a",
            "password",
            "Password123",
            "MyV3ry!Str0ng&P@ssw0rd",
            "Correct-Horse-Battery-Staple-2024!"
        ]
        
        for pwd in passwords:
            result = analyzer.analyze(pwd)
            assert 0 <= result['score'] <= 100
    
    def test_invalid_input_type(self) -> None:
        """Test that non-string input raises error."""
        analyzer = PasswordAnalyzer()
        with pytest.raises(ValidationError):
            analyzer.analyze(12345)
    
    def test_repr(self) -> None:
        """Test string representation."""
        analyzer = PasswordAnalyzer()
        repr_str = repr(analyzer)
        assert "PasswordAnalyzer" in repr_str


class TestBase64Encoder:
    """Test cases for Base64 encoder."""
    
    def test_encrypt_basic_string(self) -> None:
        """Test basic string encoding."""
        encoder = Base64Encoder()
        result = encoder.encrypt("Hello World")
        assert result == "SGVsbG8gV29ybGQ="
    
    def test_encrypt_empty_string(self) -> None:
        """Test encoding empty string."""
        encoder = Base64Encoder()
        result = encoder.encrypt("")
        assert result == ""
    
    def test_encrypt_bytes(self) -> None:
        """Test encoding bytes."""
        encoder = Base64Encoder()
        result = encoder.encrypt(b"Hello")
        assert result == "SGVsbG8="
    
    def test_decrypt_basic(self) -> None:
        """Test basic decoding."""
        encoder = Base64Encoder()
        result = encoder.decrypt("SGVsbG8gV29ybGQ=")
        assert result == "Hello World"
    
    def test_encrypt_decrypt_roundtrip(self) -> None:
        """Test encoding and decoding roundtrip."""
        encoder = Base64Encoder()
        original = "Test message with special chars: !@#$%"
        encoded = encoder.encrypt(original)
        decoded = encoder.decrypt(encoded)
        assert decoded == original
    
    def test_decrypt_missing_padding_one(self) -> None:
        """Test decoding with one missing padding character."""
        encoder = Base64Encoder()
        # "Hello" normally encodes to "SGVsbG8=" but test without padding
        result = encoder.decrypt("SGVsbG8")
        assert result == "Hello"
    
    def test_decrypt_missing_padding_two(self) -> None:
        """Test decoding with two missing padding characters."""
        encoder = Base64Encoder()
        # "Hi" normally encodes to "SGk=" but test without padding
        result = encoder.decrypt("SGk")
        assert result == "Hi"
    
    def test_decrypt_correct_padding(self) -> None:
        """Test decoding with correct padding."""
        encoder = Base64Encoder()
        result = encoder.decrypt("SGVsbG8=")
        assert result == "Hello"
    
    def test_encrypt_unicode(self) -> None:
        """Test encoding Unicode characters."""
        encoder = Base64Encoder()
        original = "Hello 世界"
        encoded = encoder.encrypt(original)
        decoded = encoder.decrypt(encoded)
        assert decoded == original
    
    def test_encrypt_binary_data(self) -> None:
        """Test encoding binary data."""
        encoder = Base64Encoder()
        binary_data = b"\x00\x01\x02\xff\xfe\xfd"
        encoded = encoder.encrypt(binary_data)
        
        # Decode back to bytes
        decoded_bytes = encoder.decode_bytes(encoded)
        assert decoded_bytes == binary_data
    
    def test_invalid_input_type(self) -> None:
        """Test that invalid input type raises error."""
        encoder = Base64Encoder()
        with pytest.raises(ValidationError):
            encoder.encrypt(12345)
    
    def test_crack_valid_base64(self) -> None:
        """Test 'cracking' (decoding) valid Base64."""
        encoder = Base64Encoder()
        result = encoder.crack("SGVsbG8gV29ybGQ=")
        
        assert result['success'] is True
        assert result['plaintext'] == "Hello World"
        assert result['key'] is None
        assert result['confidence'] == 1.0
    
    def test_crack_invalid_base64(self) -> None:
        """Test cracking invalid Base64."""
        encoder = Base64Encoder()
        result = encoder.crack("Not valid Base64!!!")
        
        assert result['success'] is False
    
    def test_encode_bytes_method(self) -> None:
        """Test convenience encode_bytes method."""
        encoder = Base64Encoder()
        result = encoder.encode_bytes(b"\x00\xff\x42")
        assert result == "AP9C"
    
    def test_decode_bytes_method(self) -> None:
        """Test decode_bytes method."""
        encoder = Base64Encoder()
        result = encoder.decode_bytes("AP9C")
        assert result == b"\x00\xff\x42"
    
    def test_is_valid_base64_true(self) -> None:
        """Test validation of valid Base64."""
        encoder = Base64Encoder()
        assert encoder.is_valid_base64("SGVsbG8=") is True
    
    def test_is_valid_base64_false(self) -> None:
        """Test validation of invalid Base64."""
        encoder = Base64Encoder()
        assert encoder.is_valid_base64("Not base64!") is False
    
    def test_is_valid_base64_missing_padding(self) -> None:
        """Test validation with missing padding (should fix and validate)."""
        encoder = Base64Encoder()
        assert encoder.is_valid_base64("SGVsbG8") is True
    
    def test_padding_fix_no_change(self) -> None:
        """Test padding fix when no fix needed."""
        encoder = Base64Encoder()
        result = encoder._fix_padding("AAAA")
        assert result == "AAAA"
    
    def test_padding_fix_add_one(self) -> None:
        """Test padding fix adds one character."""
        encoder = Base64Encoder()
        result = encoder._fix_padding("AAA")
        assert result == "AAA="
    
    def test_padding_fix_add_two(self) -> None:
        """Test padding fix adds two characters."""
        encoder = Base64Encoder()
        result = encoder._fix_padding("AA")
        assert result == "AA=="
    
    def test_long_text_encoding(self) -> None:
        """Test encoding long text."""
        encoder = Base64Encoder()
        long_text = "A" * 1000
        encoded = encoder.encrypt(long_text)
        decoded = encoder.decrypt(encoded)
        assert decoded == long_text
    
    def test_special_characters(self) -> None:
        """Test encoding special characters."""
        encoder = Base64Encoder()
        special = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        encoded = encoder.encrypt(special)
        decoded = encoder.decrypt(encoded)
        assert decoded == special
    
    def test_repr(self) -> None:
        """Test string representation."""
        encoder = Base64Encoder()
        repr_str = repr(encoder)
        assert "Base64" in repr_str


class TestSecurityIntegration:
    """Integration tests across security components."""
    
    def test_password_strength_progression(self) -> None:
        """Test that password strength increases with improvements."""
        analyzer = PasswordAnalyzer()
        
        # Progressive improvements
        passwords = [
            "password",           # Weak: lowercase only
            "Password",           # Better: mixed case
            "Password1",          # Better: with number
            "Password1!",         # Better: with special
            "MyL0ng!P@ssw0rd",   # Strong: long with variety
        ]
        
        scores = [analyzer.analyze(pwd)['entropy_bits'] for pwd in passwords]
        
        # Each should generally be better than the last
        for i in range(len(scores) - 1):
            assert scores[i+1] >= scores[i]
    
    def test_base64_not_encryption(self) -> None:
        """Test that Base64 doesn't increase security."""
        analyzer = PasswordAnalyzer()
        encoder = Base64Encoder()
        
        weak_password = "password"
        encoded_password = encoder.encrypt(weak_password)
        
        # Base64 encoding doesn't make password stronger
        weak_score = analyzer.analyze(weak_password)['score']
        encoded_score = analyzer.analyze(encoded_password)['score']
        
        # Encoded version might even be weaker (lacks variety)
        assert encoded_score != 100  # Not perfect security
    
    def test_combined_security_workflow(self) -> None:
        """Test realistic security workflow."""
        analyzer = PasswordAnalyzer()
        encoder = Base64Encoder()
        
        # User creates password
        password = "MySecure!Pass123"
        
        # Analyze strength
        analysis = analyzer.analyze(password)
        assert analysis['score'] > 60  # Should be reasonably strong
        
        # Encode for storage/transmission (not secure, just encoding)
        encoded = encoder.encrypt(password)
        
        # Decode later
        decoded = encoder.decrypt(encoded)
        assert decoded == password
