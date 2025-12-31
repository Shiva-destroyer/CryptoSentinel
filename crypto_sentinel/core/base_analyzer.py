"""
Abstract base class for security analyzer implementations.

This module defines the AnalyzerInterface ABC that all security analysis tools
must inherit from, ensuring consistent API for password strength, checksums, etc.

Developer: saisrujanmurthy@gmail.com
"""

from abc import ABC, abstractmethod
from typing import Any, Union


class AnalyzerInterface(ABC):
    """
    Abstract base class defining the interface for security analysis tools.
    
    All concrete analyzer classes (PasswordAnalyzer, ChecksumValidator, etc.)
    must inherit from this class and implement its abstract methods to ensure
    a consistent API across the framework.
    
    Analyzers are tools that inspect and evaluate data to provide security
    insights, strength metrics, or validation results.
    """
    
    @abstractmethod
    def analyze(self, data: Union[str, bytes]) -> dict[str, Any]:
        """
        Analyze the provided data and return comprehensive results.
        
        This method must be implemented by all concrete analyzer classes to
        perform security analysis and return structured results.
        
        Args:
            data: The data to analyze (string or bytes)
        
        Returns:
            Dictionary containing analysis results. Common keys include:
                - 'valid': bool indicating if data passes validation
                - 'score': float between 0-1 representing strength/quality
                - 'warnings': list of warning messages
                - 'recommendations': list of improvement suggestions
                - 'details': dict with detailed analysis metrics
        
        Raises:
            ValidationError: If input data format is invalid
            CryptoSentinelError: If analysis encounters an error
        
        Examples:
            >>> analyzer = PasswordAnalyzer()
            >>> result = analyzer.analyze("MyP@ssw0rd123")
            >>> result
            {
                'valid': True,
                'score': 0.75,
                'strength': 'strong',
                'warnings': ['Contains common words'],
                'recommendations': ['Consider using a passphrase'],
                'details': {
                    'length': 13,
                    'has_uppercase': True,
                    'has_lowercase': True,
                    'has_digits': True,
                    'has_special': True,
                    'entropy': 52.4
                }
            }
        """
        pass
    
    @abstractmethod
    def validate(self, data: Union[str, bytes]) -> bool:
        """
        Perform quick validation check on the provided data.
        
        This method provides a simple boolean validation result without
        the detailed analysis returned by analyze(). Useful for fast
        pass/fail checks.
        
        Args:
            data: The data to validate
        
        Returns:
            True if data passes validation, False otherwise
        
        Raises:
            ValidationError: If input data format is invalid
        
        Examples:
            >>> analyzer = PasswordAnalyzer()
            >>> analyzer.validate("weak")
            False
            >>> analyzer.validate("Str0ng!P@ssw0rd")
            True
        """
        pass
    
    @property
    @abstractmethod
    def analyzer_name(self) -> str:
        """
        Return the name of the analyzer.
        
        Returns:
            String identifier for the analyzer
        """
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """
        Return the version of the analyzer implementation.
        
        Returns:
            Version string (e.g., "1.0.0")
        """
        pass
    
    def get_recommendations(self, data: Union[str, bytes]) -> list[str]:
        """
        Get actionable recommendations based on analysis.
        
        This convenience method extracts recommendations from the full
        analysis results. Can be overridden for custom behavior.
        
        Args:
            data: The data to analyze
        
        Returns:
            List of recommendation strings
        
        Examples:
            >>> analyzer = PasswordAnalyzer()
            >>> analyzer.get_recommendations("password123")
            [
                'Increase length to at least 12 characters',
                'Add uppercase letters',
                'Add special characters',
                'Avoid common words'
            ]
        """
        result = self.analyze(data)
        return result.get('recommendations', [])
    
    def get_score(self, data: Union[str, bytes]) -> float:
        """
        Get numerical score from analysis.
        
        This convenience method extracts the score from full analysis
        results. Can be overridden for custom scoring.
        
        Args:
            data: The data to analyze
        
        Returns:
            Score value between 0.0 (worst) and 1.0 (best)
        
        Examples:
            >>> analyzer = PasswordAnalyzer()
            >>> analyzer.get_score("Str0ng!P@ssw0rd")
            0.85
        """
        result = self.analyze(data)
        return result.get('score', 0.0)
    
    def __repr__(self) -> str:
        """
        Return string representation of the analyzer instance.
        
        Returns:
            Developer-friendly representation
        """
        return f"{self.__class__.__name__}(name={self.analyzer_name}, version={self.version})"
