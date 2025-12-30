"""
Unit tests for mathematical utility functions.

Author: saisrujanmurthy@gmail.com
"""

import pytest
from crypto_sentinel.utils.math_helpers import (
    gcd,
    modular_inverse,
    calculate_ioc,
    is_coprime,
    factorial,
    chi_squared,
)


class TestGCD:
    """Test cases for greatest common divisor function."""
    
    def test_gcd_basic(self) -> None:
        """Test GCD with basic inputs."""
        assert gcd(48, 18) == 6
        assert gcd(17, 19) == 1
        assert gcd(100, 50) == 50
    
    def test_gcd_with_zero(self) -> None:
        """Test GCD when one number is zero."""
        assert gcd(0, 5) == 5
        assert gcd(10, 0) == 10
    
    def test_gcd_negative_numbers(self) -> None:
        """Test GCD with negative numbers."""
        assert gcd(-48, 18) == 6
        assert gcd(48, -18) == 6
        assert gcd(-48, -18) == 6
    
    def test_gcd_both_zero_raises(self) -> None:
        """Test that GCD raises ValueError when both args are zero."""
        with pytest.raises(ValueError, match="undefined for both arguments being zero"):
            gcd(0, 0)


class TestModularInverse:
    """Test cases for modular multiplicative inverse."""
    
    def test_modular_inverse_basic(self) -> None:
        """Test modular inverse with basic coprime numbers."""
        assert modular_inverse(3, 11) == 4
        assert modular_inverse(7, 26) == 15
        assert modular_inverse(15, 26) == 7
    
    def test_modular_inverse_verify(self) -> None:
        """Verify that (a * inverse) % m == 1."""
        a, m = 7, 26
        inv = modular_inverse(a, m)
        assert (a * inv) % m == 1
    
    def test_modular_inverse_non_coprime_raises(self) -> None:
        """Test that non-coprime numbers raise ValueError."""
        with pytest.raises(ValueError, match="must be coprime"):
            modular_inverse(12, 18)
    
    def test_modular_inverse_zero_raises(self) -> None:
        """Test that zero raises ValueError."""
        with pytest.raises(ValueError, match="does not exist for 0"):
            modular_inverse(0, 11)
    
    def test_modular_inverse_negative_modulus_raises(self) -> None:
        """Test that negative modulus raises ValueError."""
        with pytest.raises(ValueError, match="Modulus must be positive"):
            modular_inverse(3, -11)


class TestCalculateIOC:
    """Test cases for Index of Coincidence calculation."""
    
    def test_ioc_uniform_distribution(self) -> None:
        """Test IoC with uniform letter distribution."""
        text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ioc = calculate_ioc(text)
        # Should be close to 1/26 ≈ 0.0385
        assert 0.035 < ioc < 0.042
    
    def test_ioc_repeated_letters(self) -> None:
        """Test IoC with highly repeated letters."""
        text = "AAAAABBBBBCCCCC"
        ioc = calculate_ioc(text)
        # Should be higher than uniform distribution
        assert ioc > 0.15
    
    def test_ioc_case_insensitive(self) -> None:
        """Test that IoC is case-insensitive."""
        text1 = "HELLO WORLD"
        text2 = "hello world"
        assert calculate_ioc(text1) == calculate_ioc(text2)
    
    def test_ioc_ignores_non_alpha(self) -> None:
        """Test that IoC ignores non-alphabetic characters."""
        text1 = "HELLO WORLD"
        text2 = "H3LL0 W0RLD!!!"
        # Should be similar since non-alpha chars are filtered
        assert abs(calculate_ioc(text1) - calculate_ioc(text2)) < 0.01
    
    def test_ioc_insufficient_chars_raises(self) -> None:
        """Test that text with < 2 chars raises ValueError."""
        with pytest.raises(ValueError, match="at least 2 alphabetic characters"):
            calculate_ioc("A")
        
        with pytest.raises(ValueError, match="at least 2 alphabetic characters"):
            calculate_ioc("123")


class TestIsCoprime:
    """Test cases for coprimality checking."""
    
    def test_coprime_basic(self) -> None:
        """Test basic coprime number pairs."""
        assert is_coprime(15, 28) is True
        assert is_coprime(7, 11) is True
    
    def test_not_coprime(self) -> None:
        """Test non-coprime number pairs."""
        assert is_coprime(12, 18) is False
        assert is_coprime(10, 15) is False


class TestFactorial:
    """Test cases for factorial function."""
    
    def test_factorial_basic(self) -> None:
        """Test factorial with basic inputs."""
        assert factorial(0) == 1
        assert factorial(1) == 1
        assert factorial(5) == 120
        assert factorial(10) == 3628800
    
    def test_factorial_negative_raises(self) -> None:
        """Test that negative input raises ValueError."""
        with pytest.raises(ValueError, match="not defined for negative numbers"):
            factorial(-5)


class TestChiSquared:
    """Test cases for chi-squared statistic."""
    
    def test_chi_squared_perfect_match(self) -> None:
        """Test chi-squared with perfect match."""
        observed = [10, 15, 12]
        expected = [10.0, 15.0, 12.0]
        assert chi_squared(observed, expected) == 0.0
    
    def test_chi_squared_basic(self) -> None:
        """Test chi-squared with slight deviation."""
        observed = [10, 15, 12]
        expected = [12.0, 14.0, 11.0]
        result = chi_squared(observed, expected)
        assert result > 0
        assert result < 2.0  # Should be relatively small
    
    def test_chi_squared_different_lengths_raises(self) -> None:
        """Test that different length lists raise ValueError."""
        with pytest.raises(ValueError, match="must have same length"):
            chi_squared([1, 2, 3], [1.0, 2.0])
    
    def test_chi_squared_zero_expected_raises(self) -> None:
        """Test that zero in expected frequencies raises ValueError."""
        with pytest.raises(ValueError, match="cannot contain zero"):
            chi_squared([1, 2, 3], [1.0, 0.0, 3.0])
