"""
Abstract base class for cipher implementations.

This module defines the CipherInterface ABC that all cipher implementations
must inherit from, ensuring consistent API across all encryption algorithms.

Author: saisrujanmurthy@gmail.com
"""

from abc import ABC, abstractmethod
from typing import Any, Union


class CipherInterface(ABC):
    """
    Abstract base class defining the interface for all cipher implementations.
    
    All concrete cipher classes (Caesar, Vigenère, XOR, etc.) must inherit
    from this class and implement its abstract methods to ensure a consistent
    API across the framework.
    
    The interface enforces three core operations:
    - encrypt: Transform plaintext to ciphertext
    - decrypt: Transform ciphertext back to plaintext
    - crack: Attempt automated cryptanalysis
    """
    
    @abstractmethod
    def encrypt(
        self, 
        data: Union[str, bytes], 
        key: Any
    ) -> Union[str, bytes]:
        """
        Encrypt the provided data using the specified key.
        
        This method must be implemented by all concrete cipher classes to
        transform plaintext data into encrypted ciphertext.
        
        Args:
            data: The plaintext to encrypt (string or bytes)
            key: The encryption key (type depends on cipher algorithm)
        
        Returns:
            The encrypted ciphertext (string or bytes)
        
        Raises:
            EncryptionError: If encryption fails
            InvalidKeyError: If the provided key is invalid
            ValidationError: If input data is invalid
        
        Examples:
            >>> cipher = CaesarCipher()
            >>> cipher.encrypt("HELLO", key=3)
            'KHOOR'
        """
        pass
    
    @abstractmethod
    def decrypt(
        self, 
        data: Union[str, bytes], 
        key: Any
    ) -> Union[str, bytes]:
        """
        Decrypt the provided ciphertext using the specified key.
        
        This method must be implemented by all concrete cipher classes to
        transform encrypted ciphertext back into plaintext.
        
        Args:
            data: The ciphertext to decrypt (string or bytes)
            key: The decryption key (type depends on cipher algorithm)
        
        Returns:
            The decrypted plaintext (string or bytes)
        
        Raises:
            DecryptionError: If decryption fails
            InvalidKeyError: If the provided key is invalid
            ValidationError: If input data is invalid
        
        Examples:
            >>> cipher = CaesarCipher()
            >>> cipher.decrypt("KHOOR", key=3)
            'HELLO'
        """
        pass
    
    @abstractmethod
    def crack(
        self, 
        data: Union[str, bytes]
    ) -> dict[str, Any]:
        """
        Attempt automated cryptanalysis on the provided ciphertext.
        
        This method must be implemented to provide automated cracking
        capabilities. The implementation should attempt various techniques
        (frequency analysis, brute force, etc.) to recover the key and plaintext.
        
        Args:
            data: The ciphertext to analyze and crack
        
        Returns:
            Dictionary containing cracking results with keys:
                - 'success': bool indicating if crack was successful
                - 'key': The recovered key (if successful)
                - 'plaintext': The decrypted plaintext (if successful)
                - 'confidence': float between 0-1 indicating confidence level
                - 'method': str describing the cracking method used
                - 'attempts': int number of attempts made
        
        Raises:
            CrackingError: If cracking process encounters an error
            ValidationError: If input data is invalid
        
        Examples:
            >>> cipher = CaesarCipher()
            >>> result = cipher.crack("KHOOR")
            >>> result
            {
                'success': True,
                'key': 3,
                'plaintext': 'HELLO',
                'confidence': 0.95,
                'method': 'frequency_analysis',
                'attempts': 26
            }
        """
        pass
    
    def __repr__(self) -> str:
        """
        Return string representation of the cipher instance.
        
        Returns:
            Developer-friendly representation
        """
        return f"{self.__class__.__name__}()"
