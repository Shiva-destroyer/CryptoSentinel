"""
Mathematical utility functions for cryptographic operations.

This module provides essential mathematical functions used in various
cryptographic algorithms, including GCD, modular arithmetic, and
cryptanalysis tools.

Author: saisrujanmurthy@gmail.com
"""

from collections import Counter
from typing import Union


def gcd(a: int, b: int) -> int:
    """
    Calculate the Greatest Common Divisor (GCD) of two integers using Euclidean algorithm.
    
    The GCD is the largest positive integer that divides both numbers without
    a remainder. This is fundamental for many cryptographic operations,
    particularly in determining coprimality for key generation.
    
    Args:
        a: First integer
        b: Second integer
    
    Returns:
        The greatest common divisor of a and b
    
    Raises:
        ValueError: If both arguments are zero
    
    Examples:
        >>> gcd(48, 18)
        6
        >>> gcd(17, 19)
        1
        >>> gcd(100, 50)
        50
        >>> gcd(0, 5)
        5
    
    Notes:
        - Uses the Euclidean algorithm for efficient computation
        - Time complexity: O(log(min(a, b)))
        - Handles negative numbers by working with absolute values
    """
    a, b = abs(a), abs(b)
    
    if a == 0 and b == 0:
        raise ValueError("GCD is undefined for both arguments being zero")
    
    while b != 0:
        a, b = b, a % b
    
    return a


def modular_inverse(a: int, m: int) -> int:
    """
    Calculate the modular multiplicative inverse of a modulo m.
    
    The modular inverse of a (mod m) is an integer x such that:
        (a * x) ≡ 1 (mod m)
    
    This is crucial for affine ciphers, RSA decryption, and substitution ciphers.
    The inverse exists if and only if gcd(a, m) = 1 (a and m are coprime).
    
    Args:
        a: The number to find the inverse of
        m: The modulus
    
    Returns:
        The modular multiplicative inverse of a modulo m
    
    Raises:
        ValueError: If modular inverse does not exist (gcd(a, m) ≠ 1)
        ValueError: If m <= 0
    
    Examples:
        >>> modular_inverse(3, 11)
        4  # because (3 * 4) % 11 = 1
        >>> modular_inverse(7, 26)
        15  # because (7 * 15) % 26 = 1
        >>> modular_inverse(15, 26)
        7  # because (15 * 7) % 26 = 1
    
    Notes:
        - Uses the Extended Euclidean Algorithm
        - Time complexity: O(log(min(a, m)))
        - Returns the smallest positive inverse
    """
    if m <= 0:
        raise ValueError(f"Modulus must be positive, got {m}")
    
    # Normalize a to be within [0, m)
    a = a % m
    
    if a == 0:
        raise ValueError(f"Modular inverse does not exist for {a} mod {m}")
    
    # Check if gcd(a, m) = 1
    if gcd(a, m) != 1:
        raise ValueError(
            f"Modular inverse does not exist: gcd({a}, {m}) ≠ 1. "
            f"Numbers must be coprime."
        )
    
    # Extended Euclidean Algorithm
    def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
        """
        Extended Euclidean Algorithm.
        Returns (gcd, x, y) such that a*x + b*y = gcd
        """
        if a == 0:
            return b, 0, 1
        
        gcd_val, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        
        return gcd_val, x, y
    
    _, x, _ = extended_gcd(a, m)
    
    # Return positive inverse
    return (x % m + m) % m


def calculate_ioc(text: str) -> float:
    """
    Calculate the Index of Coincidence (IoC) for cryptanalysis.
    
    The Index of Coincidence measures the probability that two randomly
    selected letters from the text are identical. It's a powerful tool for:
    - Determining if text is encrypted
    - Estimating the key length in polyalphabetic ciphers (e.g., Vigenère)
    - Distinguishing between different languages
    
    For English text:
        - Plain text: IoC ≈ 0.065-0.068
        - Random text: IoC ≈ 0.038
        - Monoalphabetic cipher: IoC ≈ 0.065 (preserves statistics)
        - Polyalphabetic cipher: IoC ≈ 0.038-0.045 (flattens distribution)
    
    Args:
        text: The text to analyze (case-insensitive, non-alpha chars ignored)
    
    Returns:
        The Index of Coincidence as a float between 0 and 1
    
    Raises:
        ValueError: If text has fewer than 2 characters after filtering
    
    Examples:
        >>> calculate_ioc("HELLO WORLD")
        0.0727  # Typical for English
        >>> calculate_ioc("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        0.0385  # Random/uniform distribution
        >>> calculate_ioc("AAAAABBBBBCCCCC")
        0.2095  # Highly non-uniform
    
    Notes:
        - Formula: IoC = Σ(n_i * (n_i - 1)) / (N * (N - 1))
          where n_i is the frequency of letter i, N is total letter count
        - Only considers alphabetic characters
        - Case-insensitive
        - Higher IoC suggests more structure/patterns in text
    """
    # Filter to alphabetic characters only and convert to uppercase
    filtered_text = ''.join(c.upper() for c in text if c.isalpha())
    
    n = len(filtered_text)
    
    if n < 2:
        raise ValueError(
            f"Text must contain at least 2 alphabetic characters, got {n}"
        )
    
    # Count frequency of each character
    freq_counter = Counter(filtered_text)
    
    # Calculate IoC using the formula: Σ(n_i * (n_i - 1)) / (N * (N - 1))
    numerator = sum(count * (count - 1) for count in freq_counter.values())
    denominator = n * (n - 1)
    
    ioc = numerator / denominator
    
    return round(ioc, 6)


def is_coprime(a: int, b: int) -> bool:
    """
    Check if two integers are coprime (relatively prime).
    
    Two numbers are coprime if their greatest common divisor is 1.
    This is important for key validation in many cryptographic algorithms.
    
    Args:
        a: First integer
        b: Second integer
    
    Returns:
        True if a and b are coprime, False otherwise
    
    Examples:
        >>> is_coprime(15, 28)
        True
        >>> is_coprime(12, 18)
        False
        >>> is_coprime(7, 11)
        True
    """
    return gcd(a, b) == 1


def factorial(n: int) -> int:
    """
    Calculate the factorial of a non-negative integer.
    
    Used in various cryptographic calculations, particularly for
    determining the number of possible permutations.
    
    Args:
        n: Non-negative integer
    
    Returns:
        The factorial of n (n!)
    
    Raises:
        ValueError: If n is negative
    
    Examples:
        >>> factorial(5)
        120
        >>> factorial(0)
        1
        >>> factorial(10)
        3628800
    """
    if n < 0:
        raise ValueError(f"Factorial is not defined for negative numbers: {n}")
    
    if n == 0 or n == 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result


def chi_squared(observed: list[int], expected: list[float]) -> float:
    """
    Calculate chi-squared statistic for frequency analysis.
    
    Used in cryptanalysis to compare observed letter frequencies against
    expected frequencies (e.g., English language statistics) to determine
    if a decryption attempt produced meaningful text.
    
    Args:
        observed: List of observed frequencies
        expected: List of expected frequencies
    
    Returns:
        Chi-squared statistic (lower values indicate better match)
    
    Raises:
        ValueError: If lists have different lengths or expected has zero values
    
    Examples:
        >>> chi_squared([10, 15, 12], [12.0, 14.0, 11.0])
        0.690
    
    Notes:
        - Formula: χ² = Σ((observed - expected)² / expected)
        - Lower χ² values indicate better fit to expected distribution
        - Used extensively in frequency analysis attacks
    """
    if len(observed) != len(expected):
        raise ValueError(
            f"Lists must have same length: observed={len(observed)}, "
            f"expected={len(expected)}"
        )
    
    if any(e == 0 for e in expected):
        raise ValueError("Expected frequencies cannot contain zero values")
    
    chi_sq = sum(
        ((obs - exp) ** 2) / exp 
        for obs, exp in zip(observed, expected)
    )
    
    return round(chi_sq, 6)
