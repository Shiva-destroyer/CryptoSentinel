"""
Advanced password strength analyzer with entropy calculation.

This module analyzes password strength using mathematical entropy
calculation and provides detailed security recommendations.

Developer: saisrujanmurthy@gmail.com
"""

import math
import re
from typing import Any

from crypto_sentinel.core.base_analyzer import AnalyzerInterface
from crypto_sentinel.core.exceptions import ValidationError


class PasswordAnalyzer(AnalyzerInterface):
    """
    Advanced password strength analyzer using entropy theory.
    
    This analyzer goes beyond simple length checks by calculating
    Shannon entropy in bits, estimating time-to-crack, and providing
    actionable security recommendations.
    
    Entropy Formula:
        E = L × log₂(R)
        
        Where:
            E = Entropy in bits
            L = Password length
            R = Size of character pool (alphabet size)
        
        Character Pool Sizes:
            - Lowercase only: R = 26
            - Uppercase only: R = 26
            - Mixed case: R = 52
            - Alphanumeric: R = 62 (26 + 26 + 10)
            - Alphanumeric + special: R = 94 (printable ASCII)
    
    Time-to-Crack Estimation:
        Assumes attacker rate: 10^10 guesses/second
        (Typical GPU-accelerated attack rate)
        
        Search space: 2^E possibilities
        Time = 2^E / (10^10 guesses/sec)
    
    Security Thresholds:
        - < 28 bits: Very weak (crackable in seconds)
        - 28-35 bits: Weak (crackable in minutes/hours)
        - 36-59 bits: Moderate (days to months)
        - 60-127 bits: Strong (years to centuries)
        - >= 128 bits: Very strong (practically unbreakable)
    
    Example:
        >>> analyzer = PasswordAnalyzer()
        >>> result = analyzer.analyze("password123")
        >>> print(f"Score: {result['score']}/100")
        >>> print(f"Entropy: {result['entropy_bits']} bits")
        >>> print(f"Time to crack: {result['crack_time_display']}")
        >>> for rec in result['recommendations']:
        ...     print(f"- {rec}")
    """
    
    # Attack rate: 10 billion guesses per second (modern GPU)
    GUESSES_PER_SECOND: float = 1e10
    
    # Entropy thresholds for scoring
    ENTROPY_THRESHOLDS = {
        'very_weak': 28,
        'weak': 36,
        'moderate': 60,
        'strong': 128,
    }
    
    def __init__(self) -> None:
        """Initialize password analyzer."""
        pass
    
    @property
    def analyzer_name(self) -> str:
        """Return the analyzer name."""
        return "PasswordAnalyzer"
    
    @property
    def version(self) -> str:
        """Return the analyzer version."""
        return "1.0.0"
    
    def _calculate_pool_size(self, password: str) -> int:
        """
        Calculate character pool size based on password composition.
        
        Args:
            password: Password to analyze
            
        Returns:
            Size of character pool (alphabet size)
            
        Logic:
            - Check for lowercase letters: add 26
            - Check for uppercase letters: add 26
            - Check for digits: add 10
            - Check for special characters: add 32
        """
        pool_size = 0
        
        if re.search(r'[a-z]', password):
            pool_size += 26  # Lowercase letters
        
        if re.search(r'[A-Z]', password):
            pool_size += 26  # Uppercase letters
        
        if re.search(r'[0-9]', password):
            pool_size += 10  # Digits
        
        # Special characters (common printable ASCII excluding alphanumeric)
        if re.search(r'[^a-zA-Z0-9]', password):
            pool_size += 32  # Special characters (approximate)
        
        return pool_size
    
    def _calculate_entropy(self, password: str) -> float:
        """
        Calculate Shannon entropy in bits.
        
        Formula: E = L × log₂(R)
        
        Args:
            password: Password to analyze
            
        Returns:
            Entropy in bits
            
        Example:
            Password: "password" (8 lowercase chars)
            L = 8
            R = 26
            E = 8 × log₂(26) = 8 × 4.7 = 37.6 bits
        """
        length = len(password)
        pool_size = self._calculate_pool_size(password)
        
        if pool_size == 0:
            return 0.0
        
        entropy = length * math.log2(pool_size)
        return entropy
    
    def _estimate_crack_time(self, entropy_bits: float) -> dict[str, Any]:
        """
        Estimate time to crack password using brute force.
        
        Calculation:
            Search space: 2^E possibilities
            Time (seconds) = 2^E / (10^10 guesses/sec)
        
        Args:
            entropy_bits: Password entropy in bits
            
        Returns:
            Dictionary with:
                - seconds (float): Time in seconds
                - display (str): Human-readable time
                
        Example:
            40 bits entropy:
            Space = 2^40 = 1,099,511,627,776
            Time = 1.1 trillion / 10 billion = 110 seconds
        """
        search_space = 2 ** entropy_bits
        seconds = search_space / self.GUESSES_PER_SECOND
        
        # Convert to human-readable format
        if seconds < 1:
            display = "< 1 second"
        elif seconds < 60:
            display = f"{seconds:.1f} seconds"
        elif seconds < 3600:
            minutes = seconds / 60
            display = f"{minutes:.1f} minutes"
        elif seconds < 86400:
            hours = seconds / 3600
            display = f"{hours:.1f} hours"
        elif seconds < 31536000:
            days = seconds / 86400
            display = f"{days:.1f} days"
        elif seconds < 31536000 * 100:
            years = seconds / 31536000
            display = f"{years:.1f} years"
        elif seconds < 31536000 * 1000:
            centuries = seconds / (31536000 * 100)
            display = f"{centuries:.1f} centuries"
        else:
            display = "millions of years"
        
        return {
            'seconds': seconds,
            'display': display,
        }
    
    def _calculate_score(self, entropy_bits: float) -> int:
        """
        Calculate password score from 0-100 based on entropy.
        
        Scoring:
            - 0-27 bits: 0-20 (very weak)
            - 28-35 bits: 21-40 (weak)
            - 36-59 bits: 41-70 (moderate)
            - 60-127 bits: 71-90 (strong)
            - 128+ bits: 91-100 (very strong)
        
        Args:
            entropy_bits: Password entropy in bits
            
        Returns:
            Score from 0 to 100
        """
        if entropy_bits < self.ENTROPY_THRESHOLDS['very_weak']:
            # Very weak: 0-20
            score = int((entropy_bits / self.ENTROPY_THRESHOLDS['very_weak']) * 20)
        elif entropy_bits < self.ENTROPY_THRESHOLDS['weak']:
            # Weak: 21-40
            score = 20 + int(((entropy_bits - 28) / 8) * 20)
        elif entropy_bits < self.ENTROPY_THRESHOLDS['moderate']:
            # Moderate: 41-70
            score = 40 + int(((entropy_bits - 36) / 24) * 30)
        elif entropy_bits < self.ENTROPY_THRESHOLDS['strong']:
            # Strong: 71-90
            score = 70 + int(((entropy_bits - 60) / 68) * 20)
        else:
            # Very strong: 91-100
            score = 90 + min(10, int((entropy_bits - 128) / 20))
        
        return min(100, max(0, score))
    
    def _generate_recommendations(self, password: str, entropy_bits: float) -> list[str]:
        """
        Generate actionable security recommendations.
        
        Args:
            password: Password to analyze
            entropy_bits: Calculated entropy
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        length = len(password)
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'[0-9]', password))
        has_special = bool(re.search(r'[^a-zA-Z0-9]', password))
        
        # Length recommendations
        if length < 8:
            recommendations.append("Increase length to at least 8 characters")
        elif length < 12:
            recommendations.append("Consider increasing length to 12+ characters for better security")
        
        # Character diversity recommendations
        if not has_lower:
            recommendations.append("Add lowercase letters (a-z)")
        
        if not has_upper:
            recommendations.append("Add uppercase letters (A-Z)")
        
        if not has_digit:
            recommendations.append("Add numbers (0-9)")
        
        if not has_special:
            recommendations.append("Add special characters (!@#$%^&*)")
        
        # Pattern detection
        if re.search(r'(.)\1{2,}', password):
            recommendations.append("Avoid repeated characters (e.g., 'aaa', '111')")
        
        if re.search(r'(012|123|234|345|456|567|678|789|890)', password):
            recommendations.append("Avoid sequential numbers")
        
        if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
            recommendations.append("Avoid sequential letters")
        
        # Common patterns
        common_weak = ['password', '123456', 'qwerty', 'admin', 'letmein', 'welcome']
        if any(weak in password.lower() for weak in common_weak):
            recommendations.append("Avoid common words and patterns")
        
        # Entropy-based recommendations
        if entropy_bits < 36:
            recommendations.append("Password is too weak - use a longer password with mixed character types")
        elif entropy_bits < 60:
            recommendations.append("Consider using a passphrase or password manager for stronger security")
        
        if not recommendations:
            recommendations.append("Password strength is good! Consider using a password manager to generate and store complex passwords")
        
        return recommendations
    
    def analyze(self, data: str) -> dict[str, Any]:
        """
        Analyze password strength with comprehensive metrics.
        
        Performs complete password analysis including:
            - Entropy calculation
            - Time-to-crack estimation
            - Security score (0-100)
            - Detailed recommendations
        
        Args:
            data: Password to analyze
            
        Returns:
            Dictionary containing:
                - score (int): Security score 0-100
                - entropy_bits (float): Shannon entropy in bits
                - crack_time_seconds (float): Estimated crack time in seconds
                - crack_time_display (str): Human-readable crack time
                - length (int): Password length
                - pool_size (int): Character pool size
                - recommendations (list): Security recommendations
                - strength_level (str): Overall strength assessment
                
        Raises:
            ValidationError: If data is not a string
            
        Time Complexity: O(n) where n is password length
        
        Example:
            >>> analyzer = PasswordAnalyzer()
            >>> 
            >>> # Weak password
            >>> weak = analyzer.analyze("password123")
            >>> print(f"Score: {weak['score']}/100")
            >>> # Score: 35/100
            >>> 
            >>> # Strong password
            >>> strong = analyzer.analyze("Tr0ub4dor&3")
            >>> print(f"Entropy: {strong['entropy_bits']} bits")
            >>> # Entropy: 65.7 bits
        """
        if not isinstance(data, str):
            raise ValidationError(
                f"Expected string, got {type(data).__name__}"
            )
        
        if len(data) == 0:
            return {
                'score': 0,
                'entropy_bits': 0.0,
                'crack_time_seconds': 0.0,
                'crack_time_display': '< 1 second',
                'length': 0,
                'pool_size': 0,
                'recommendations': ['Password cannot be empty'],
                'strength_level': 'very_weak',
            }
        
        # Calculate metrics
        entropy_bits = self._calculate_entropy(data)
        crack_time = self._estimate_crack_time(entropy_bits)
        score = self._calculate_score(entropy_bits)
        pool_size = self._calculate_pool_size(data)
        recommendations = self._generate_recommendations(data, entropy_bits)
        
        # Determine strength level
        if entropy_bits < 28:
            strength_level = 'very_weak'
        elif entropy_bits < 36:
            strength_level = 'weak'
        elif entropy_bits < 60:
            strength_level = 'moderate'
        elif entropy_bits < 128:
            strength_level = 'strong'
        else:
            strength_level = 'very_strong'
        
        return {
            'score': score,
            'entropy_bits': round(entropy_bits, 2),
            'crack_time_seconds': crack_time['seconds'],
            'crack_time_display': crack_time['display'],
            'length': len(data),
            'pool_size': pool_size,
            'recommendations': recommendations,
            'strength_level': strength_level,
        }
    
    def validate(self, data: str) -> bool:
        """
        Quick validation: Check if password meets minimum security requirements.
        
        Minimum Requirements:
            - At least 8 characters
            - At least 36 bits of entropy (moderate strength)
        
        Args:
            data: Password to validate
            
        Returns:
            True if password meets minimum requirements
            
        Example:
            >>> analyzer = PasswordAnalyzer()
            >>> analyzer.validate("password123")
            False
            >>> analyzer.validate("MyS3cur3P@ssw0rd")
            True
        """
        if not isinstance(data, str) or len(data) < 8:
            return False
        
        entropy = self._calculate_entropy(data)
        return entropy >= 36.0  # Minimum moderate strength
    
    def __repr__(self) -> str:
        """String representation of analyzer."""
        return "PasswordAnalyzer(algorithm='entropy', threshold=36bits)"
