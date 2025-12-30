# CryptoSentinel Development Guide

**Author:** saisrujanmurthy@gmail.com

## Quick Start for Developers

### Initial Setup

```bash
# Navigate to project
cd "/home/shivansh/Vs Code/Github projects/CryptoSentinel"

# Create virtual environment
python3.10 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install -e ".[dev]"

# Verify installation
python -c "from crypto_sentinel.core import CipherInterface; print('✅ Setup successful!')"
```

### Running Tests

```bash
# Run all tests with coverage
pytest tests/ -v --cov=crypto_sentinel --cov-report=term-missing

# Run specific test file
pytest tests/test_utils/test_math_helpers.py -v

# Run tests matching pattern
pytest tests/ -k "test_gcd" -v

# Generate HTML coverage report
pytest tests/ --cov=crypto_sentinel --cov-report=html
open htmlcov/index.html
```

### Code Quality

```bash
# Type checking
mypy crypto_sentinel/

# Linting
ruff check crypto_sentinel/

# Auto-fix linting issues
ruff check --fix crypto_sentinel/

# Format code
black crypto_sentinel/

# Sort imports
isort crypto_sentinel/

# Run all checks
black crypto_sentinel/ && isort crypto_sentinel/ && ruff check crypto_sentinel/ && mypy crypto_sentinel/
```

## Implementation Guidelines

### 1. Adding a New Cipher

**Step 1:** Create the cipher file

```bash
touch crypto_sentinel/ciphers/caesar.py
```

**Step 2:** Implement the cipher

```python
"""
Caesar Cipher implementation.

Author: saisrujanmurthy@gmail.com
"""

from typing import Any, Union
from crypto_sentinel.core.base_cipher import CipherInterface
from crypto_sentinel.core.exceptions import (
    EncryptionError,
    DecryptionError,
    InvalidKeyError,
)


class CaesarCipher(CipherInterface):
    """
    Caesar Cipher implementation with frequency analysis cracking.
    
    The Caesar cipher shifts each letter by a fixed number of positions
    in the alphabet. It's a simple substitution cipher named after
    Julius Caesar.
    
    Attributes:
        ALPHABET_SIZE: Size of the alphabet (26 for English)
    """
    
    ALPHABET_SIZE = 26
    
    def encrypt(self, data: Union[str, bytes], key: Any) -> Union[str, bytes]:
        """
        Encrypt plaintext using Caesar cipher.
        
        Args:
            data: Plaintext string to encrypt
            key: Integer shift value (0-25)
        
        Returns:
            Encrypted ciphertext string
        
        Raises:
            InvalidKeyError: If key is not an integer or out of range
            EncryptionError: If encryption fails
        """
        # Implementation here
        pass
    
    def decrypt(self, data: Union[str, bytes], key: Any) -> Union[str, bytes]:
        """Decrypt ciphertext using Caesar cipher."""
        # Implementation here
        pass
    
    def crack(self, data: Union[str, bytes]) -> dict[str, Any]:
        """
        Crack Caesar cipher using brute force and frequency analysis.
        
        Returns:
            Dictionary with cracking results including best key and plaintext
        """
        # Implementation here
        pass
```

**Step 3:** Create test file

```bash
touch tests/test_ciphers/test_caesar.py
```

**Step 4:** Write comprehensive tests

```python
"""
Tests for Caesar cipher.

Author: saisrujanmurthy@gmail.com
"""

import pytest
from crypto_sentinel.ciphers.caesar import CaesarCipher


class TestCaesarCipher:
    
    def test_encrypt_basic(self) -> None:
        cipher = CaesarCipher()
        result = cipher.encrypt("HELLO", key=3)
        assert result == "KHOOR"
    
    def test_decrypt_basic(self) -> None:
        cipher = CaesarCipher()
        result = cipher.decrypt("KHOOR", key=3)
        assert result == "HELLO"
    
    def test_crack_simple(self) -> None:
        cipher = CaesarCipher()
        result = cipher.crack("KHOOR")
        assert result['success'] is True
        assert result['key'] == 3
```

**Step 5:** Update package exports

Edit `crypto_sentinel/ciphers/__init__.py`:
```python
from .caesar import CaesarCipher

__all__ = ["CaesarCipher"]
```

### 2. Adding a New Hasher

Similar process but inherit from `HasherInterface`:

```python
"""
SHA-256 hasher implementation.

Author: saisrujanmurthy@gmail.com
"""

import hashlib
from pathlib import Path
from typing import Union
from crypto_sentinel.core.base_hasher import HasherInterface


class SHA256Hasher(HasherInterface):
    """SHA-256 cryptographic hash function."""
    
    CHUNK_SIZE = 8192
    
    @property
    def algorithm_name(self) -> str:
        return "SHA256"
    
    @property
    def digest_size(self) -> int:
        return 32  # 256 bits = 32 bytes
    
    def hash_string(self, text: str) -> str:
        """Hash string using SHA-256."""
        hasher = hashlib.sha256()
        hasher.update(text.encode('utf-8'))
        return hasher.hexdigest()
    
    def hash_file(self, filepath: Union[str, Path]) -> str:
        """Hash file using SHA-256 with streaming."""
        hasher = hashlib.sha256()
        path = Path(filepath)
        
        with open(path, 'rb') as f:
            while chunk := f.read(self.CHUNK_SIZE):
                hasher.update(chunk)
        
        return hasher.hexdigest()
```

### 3. Adding a New Analyzer

Inherit from `AnalyzerInterface`:

```python
"""
Password strength analyzer.

Author: saisrujanmurthy@gmail.com
"""

from typing import Any, Union
from crypto_sentinel.core.base_analyzer import AnalyzerInterface


class PasswordAnalyzer(AnalyzerInterface):
    """Analyze password strength and provide recommendations."""
    
    @property
    def analyzer_name(self) -> str:
        return "PasswordStrengthAnalyzer"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    def analyze(self, data: Union[str, bytes]) -> dict[str, Any]:
        """
        Analyze password strength.
        
        Returns dictionary with:
        - valid: bool
        - score: float (0.0 to 1.0)
        - strength: str ("weak", "medium", "strong", "very_strong")
        - warnings: list[str]
        - recommendations: list[str]
        - details: dict with metrics
        """
        # Implementation
        pass
    
    def validate(self, data: Union[str, bytes]) -> bool:
        """Quick validation - is password acceptable?"""
        result = self.analyze(data)
        return result['score'] >= 0.5
```

## Best Practices

### Type Hints

✅ **Good:**
```python
def encrypt(self, data: str | bytes, key: int) -> str:
    """Encrypt data."""
    pass
```

❌ **Bad:**
```python
def encrypt(self, data, key):
    """Encrypt data."""
    pass
```

### Docstrings

✅ **Good:**
```python
def calculate_ioc(text: str) -> float:
    """
    Calculate the Index of Coincidence for cryptanalysis.
    
    The Index of Coincidence measures the probability that two
    randomly selected letters from the text are identical.
    
    Args:
        text: The text to analyze (case-insensitive)
    
    Returns:
        The Index of Coincidence as a float between 0 and 1
    
    Raises:
        ValueError: If text has fewer than 2 characters
    
    Examples:
        >>> calculate_ioc("HELLO WORLD")
        0.0727
    """
    pass
```

❌ **Bad:**
```python
def calculate_ioc(text: str) -> float:
    """Calculate IoC."""
    pass
```

### Error Handling

✅ **Good:**
```python
from crypto_sentinel.core.exceptions import InvalidKeyError

def encrypt(self, data: str, key: int) -> str:
    if not isinstance(key, int):
        raise InvalidKeyError(
            "Key must be an integer",
            details={"provided_type": type(key).__name__}
        )
    # Continue with encryption
```

❌ **Bad:**
```python
def encrypt(self, data: str, key: int) -> str:
    if not isinstance(key, int):
        raise Exception("Bad key")
```

### Testing

✅ **Good:**
```python
class TestCaesarCipher:
    """Comprehensive Caesar cipher tests."""
    
    def test_encrypt_uppercase(self) -> None:
        """Test encryption with uppercase letters."""
        cipher = CaesarCipher()
        assert cipher.encrypt("ABC", key=1) == "BCD"
    
    def test_encrypt_lowercase(self) -> None:
        """Test encryption with lowercase letters."""
        cipher = CaesarCipher()
        assert cipher.encrypt("abc", key=1) == "bcd"
    
    def test_invalid_key_raises(self) -> None:
        """Test that invalid key raises InvalidKeyError."""
        cipher = CaesarCipher()
        with pytest.raises(InvalidKeyError):
            cipher.encrypt("ABC", key="invalid")
```

❌ **Bad:**
```python
def test_caesar():
    cipher = CaesarCipher()
    assert cipher.encrypt("ABC", 1) == "BCD"
```

## Common Patterns

### Streaming File Operations

```python
def hash_file(self, filepath: Union[str, Path]) -> str:
    """Hash large files efficiently."""
    hasher = hashlib.sha256()
    path = Path(filepath)
    
    try:
        with open(path, 'rb') as f:
            while chunk := f.read(self.CHUNK_SIZE):
                hasher.update(chunk)
    except FileNotFoundError:
        raise FileOperationError(
            f"File not found: {path}",
            details={"filepath": str(path)}
        )
    except Exception as e:
        raise HashingError(
            f"Failed to hash file: {e}",
            details={"filepath": str(path), "error": str(e)}
        )
    
    return hasher.hexdigest()
```

### Frequency Analysis

```python
from collections import Counter

def analyze_frequency(text: str) -> dict[str, float]:
    """Analyze letter frequency in text."""
    # Filter to letters only
    letters = [c.upper() for c in text if c.isalpha()]
    total = len(letters)
    
    if total == 0:
        return {}
    
    # Count frequencies
    counts = Counter(letters)
    
    # Convert to percentages
    frequencies = {
        letter: (count / total) * 100
        for letter, count in counts.items()
    }
    
    return dict(sorted(frequencies.items()))
```

### Brute Force Cracking

```python
def crack(self, data: str) -> dict[str, Any]:
    """Crack cipher using brute force."""
    best_result = {
        'success': False,
        'key': None,
        'plaintext': None,
        'confidence': 0.0,
        'method': 'brute_force',
        'attempts': 0
    }
    
    for key in range(self.KEY_SPACE):
        try:
            plaintext = self.decrypt(data, key)
            score = self._score_plaintext(plaintext)
            
            if score > best_result['confidence']:
                best_result.update({
                    'success': True,
                    'key': key,
                    'plaintext': plaintext,
                    'confidence': score
                })
        except Exception:
            pass
        
        best_result['attempts'] += 1
    
    return best_result
```

## Troubleshooting

### Import Errors

If you see `ModuleNotFoundError`:
```bash
# Reinstall in development mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/home/shivansh/Vs Code/Github projects/CryptoSentinel"
```

### Type Checking Issues

If `mypy` complains about missing imports:
```bash
# Install type stubs
pip install types-all
```

### Test Failures

```bash
# Run with verbose output
pytest tests/ -vv

# Run specific failing test
pytest tests/test_core/test_exceptions.py::TestCryptoSentinelError::test_basic_exception -vv

# Run with print statements visible
pytest tests/ -s
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/add-caesar-cipher

# Stage changes
git add crypto_sentinel/ciphers/caesar.py
git add tests/test_ciphers/test_caesar.py

# Commit with descriptive message
git commit -m "feat: Add Caesar cipher implementation

- Implement encrypt/decrypt methods
- Add brute force cracking with frequency analysis
- Include comprehensive test suite
- Update package exports"

# Push to remote
git push origin feature/add-caesar-cipher
```

## Performance Considerations

### Large File Handling

Always use chunked reading:
```python
CHUNK_SIZE = 8192  # 8KB chunks

with open(filepath, 'rb') as f:
    while chunk := f.read(CHUNK_SIZE):
        process(chunk)
```

### Optimization Tips

1. Use `str.translate()` for character substitution
2. Pre-compile regex patterns as class attributes
3. Cache expensive calculations (e.g., frequency tables)
4. Use `itertools` for combinatorial operations
5. Consider `numpy` for large-scale numerical operations

## Resources

- **Type Hints:** https://peps.python.org/pep-0484/
- **Google Style Guide:** https://google.github.io/styleguide/pyguide.html
- **Pytest Docs:** https://docs.pytest.org/
- **Cryptography Theory:** https://crypto.stanford.edu/~dabo/courses/OnlineCrypto/

## Contact

**Sai Srujan Murthy**  
📧 saisrujanmurthy@gmail.com

Happy coding! 🚀
