# CryptoSentinel Project Structure

**Author:** saisrujanmurthy@gmail.com  
**Status:** ✅ Foundation Complete

## Project Overview

CryptoSentinel is a production-grade cryptographic framework built with Python 3.10+ that unifies 10 cryptographic and security tools into a single professional application.

## ✅ Completed Components

### 1. Directory Structure
```
CryptoSentinel/
├── crypto_sentinel/          # Main source package
│   ├── __init__.py          # Package initialization
│   ├── core/                # Abstract base classes
│   │   ├── __init__.py
│   │   ├── exceptions.py    # ✅ Custom exception hierarchy
│   │   ├── base_cipher.py   # ✅ CipherInterface ABC
│   │   ├── base_hasher.py   # ✅ HasherInterface ABC
│   │   └── base_analyzer.py # ✅ AnalyzerInterface ABC
│   ├── ciphers/             # Classical ciphers (TODO)
│   │   └── __init__.py
│   ├── hashing/             # Hash functions (TODO)
│   │   └── __init__.py
│   ├── security/            # Security tools (TODO)
│   │   └── __init__.py
│   ├── utils/               # Utility functions
│   │   ├── __init__.py
│   │   └── math_helpers.py  # ✅ Mathematical operations
│   └── ui/                  # User interface (TODO)
│       └── __init__.py
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_core/
│   │   ├── __init__.py
│   │   └── test_exceptions.py  # ✅ Exception tests
│   ├── test_utils/
│   │   ├── __init__.py
│   │   └── test_math_helpers.py  # ✅ Math utility tests
│   └── test_*/ (other test modules)
├── docs/                    # Documentation
│   └── README.md
├── README.md               # ✅ Project documentation
├── requirements.txt        # ✅ Dependencies
├── setup.py               # ✅ Setup configuration
├── pyproject.toml         # ✅ Modern Python config
├── LICENSE                # ✅ MIT License
└── .gitignore            # ✅ Git ignore rules
```

## 🎯 Core Architecture

### Abstract Base Classes (ABCs)

#### 1. CipherInterface
Location: `crypto_sentinel/core/base_cipher.py`

Defines the contract for all cipher implementations:
```python
class CipherInterface(ABC):
    def encrypt(data: str | bytes, key: Any) -> str | bytes
    def decrypt(data: str | bytes, key: Any) -> str | bytes
    def crack(data: str | bytes) -> dict[str, Any]
```

**Crack Result Format:**
```python
{
    'success': bool,
    'key': Any,
    'plaintext': str | bytes,
    'confidence': float,  # 0.0 to 1.0
    'method': str,
    'attempts': int
}
```

#### 2. HasherInterface
Location: `crypto_sentinel/core/base_hasher.py`

Defines the contract for hashing algorithms:
```python
class HasherInterface(ABC):
    def hash_string(text: str) -> str
    def hash_file(filepath: str | Path) -> str
    
    @property
    def algorithm_name() -> str
    
    @property
    def digest_size() -> int
```

**Features:**
- Streaming file support for large files
- Built-in verification method
- Extensible for custom hashers

#### 3. AnalyzerInterface
Location: `crypto_sentinel/core/base_analyzer.py`

Defines the contract for security analyzers:
```python
class AnalyzerInterface(ABC):
    def analyze(data: str | bytes) -> dict[str, Any]
    def validate(data: str | bytes) -> bool
    
    @property
    def analyzer_name() -> str
    
    @property
    def version() -> str
```

**Analysis Result Format:**
```python
{
    'valid': bool,
    'score': float,  # 0.0 to 1.0
    'warnings': list[str],
    'recommendations': list[str],
    'details': dict[str, Any]
}
```

### Exception Hierarchy

Location: `crypto_sentinel/core/exceptions.py`

```
Exception
└── CryptoSentinelError (base)
    ├── EncryptionError
    ├── DecryptionError
    ├── InvalidKeyError
    ├── HashingError
    ├── FileOperationError
    ├── ValidationError
    └── CrackingError
```

**Features:**
- Rich error context with details dict
- Formatted string representations
- Graceful error handling support

### Mathematical Utilities

Location: `crypto_sentinel/utils/math_helpers.py`

#### Functions:

1. **`gcd(a: int, b: int) -> int`**
   - Euclidean algorithm
   - Handles negative numbers
   - O(log(min(a, b))) complexity

2. **`modular_inverse(a: int, m: int) -> int`**
   - Extended Euclidean algorithm
   - Returns smallest positive inverse
   - Critical for affine/substitution ciphers

3. **`calculate_ioc(text: str) -> float`**
   - Index of Coincidence for cryptanalysis
   - English text: ~0.065-0.068
   - Random/cipher text: ~0.038-0.045

4. **`is_coprime(a: int, b: int) -> bool`**
   - Quick coprimality check
   - Key validation utility

5. **`factorial(n: int) -> int`**
   - Standard factorial
   - Used in permutation calculations

6. **`chi_squared(observed, expected) -> float`**
   - Statistical goodness-of-fit
   - Frequency analysis tool
   - Lower values = better match

## 📊 Code Quality Standards

### Type Hints
- Python 3.10+ syntax (`str | bytes` instead of `Union[str, bytes]`)
- All function signatures typed
- Return types specified
- Generic types where appropriate

### Documentation
- Google-style docstrings
- Args, Returns, Raises sections
- Usage examples in docstrings
- Author attribution in module headers

### Testing
- Pytest framework
- Organized by module structure
- Comprehensive test coverage
- Edge case handling

## 🚀 Next Steps

### Immediate Priorities

1. **Implement Caesar Cipher**
   - Simple shift cipher
   - Brute force cracking (26 attempts)
   - Frequency analysis scoring

2. **Implement Vigenère Cipher**
   - Polyalphabetic substitution
   - Kasiski examination
   - IoC-based key length detection

3. **Implement MD5 Hasher**
   - Use hashlib
   - Streaming file support
   - Collision warning in docs

4. **Implement SHA-256 Hasher**
   - Modern secure hash
   - Streaming file support
   - Benchmark performance

5. **Implement Password Analyzer**
   - Strength scoring algorithm
   - Common password detection
   - Entropy calculation

### Cipher Implementation Template

```python
"""
[Cipher Name] implementation.

Author: saisrujanmurthy@gmail.com
"""

from typing import Any, Union
from crypto_sentinel.core.base_cipher import CipherInterface
from crypto_sentinel.core.exceptions import EncryptionError, DecryptionError


class [CipherName]Cipher(CipherInterface):
    """
    [Description]
    
    [Algorithm details]
    """
    
    def encrypt(self, data: Union[str, bytes], key: Any) -> Union[str, bytes]:
        """Encrypt using [cipher name]."""
        # Implementation
        pass
    
    def decrypt(self, data: Union[str, bytes], key: Any) -> Union[str, bytes]:
        """Decrypt using [cipher name]."""
        # Implementation
        pass
    
    def crack(self, data: Union[str, bytes]) -> dict[str, Any]:
        """Crack [cipher name] using [method]."""
        # Implementation
        pass
```

### Hasher Implementation Template

```python
"""
[Hash Algorithm] implementation.

Author: saisrujanmurthy@gmail.com
"""

import hashlib
from pathlib import Path
from typing import Union
from crypto_sentinel.core.base_hasher import HasherInterface
from crypto_sentinel.core.exceptions import HashingError


class [HashName]Hasher(HasherInterface):
    """
    [Description]
    """
    
    CHUNK_SIZE = 8192  # For streaming
    
    @property
    def algorithm_name(self) -> str:
        return "[ALGORITHM_NAME]"
    
    @property
    def digest_size(self) -> int:
        return [SIZE_IN_BYTES]
    
    def hash_string(self, text: str) -> str:
        """Hash string using [algorithm]."""
        # Implementation
        pass
    
    def hash_file(self, filepath: Union[str, Path]) -> str:
        """Hash file using [algorithm] with streaming."""
        # Implementation with chunked reading
        pass
```

## 📝 Development Workflow

### Running Tests
```bash
# All tests
pytest tests/ -v

# Specific module
pytest tests/test_core/ -v

# With coverage
pytest tests/ --cov=crypto_sentinel --cov-report=html
```

### Code Quality Checks
```bash
# Type checking
mypy crypto_sentinel/

# Linting
ruff check crypto_sentinel/

# Formatting
black crypto_sentinel/

# Import sorting
isort crypto_sentinel/
```

### Adding New Cipher

1. Create file in `crypto_sentinel/ciphers/`
2. Inherit from `CipherInterface`
3. Implement all abstract methods
4. Add comprehensive docstrings
5. Create test file in `tests/test_ciphers/`
6. Update `crypto_sentinel/ciphers/__init__.py`

### Adding New Hasher

1. Create file in `crypto_sentinel/hashing/`
2. Inherit from `HasherInterface`
3. Implement streaming file support
4. Add test file in `tests/test_hashing/`
5. Update `crypto_sentinel/hashing/__init__.py`

## 📖 Resources

### Cryptanalysis References
- [Frequency Analysis](https://en.wikipedia.org/wiki/Frequency_analysis)
- [Index of Coincidence](https://en.wikipedia.org/wiki/Index_of_coincidence)
- [Kasiski Examination](https://en.wikipedia.org/wiki/Kasiski_examination)

### Python Resources
- [Type Hints](https://docs.python.org/3/library/typing.html)
- [ABC Module](https://docs.python.org/3/library/abc.html)
- [Pytest](https://docs.pytest.org/)

## 🎓 Design Patterns Used

1. **Abstract Factory Pattern** - Interface definitions
2. **Strategy Pattern** - Pluggable algorithms
3. **Template Method** - Base class convenience methods
4. **Factory Pattern** - Future CLI/UI instantiation

## ✉️ Contact

**Sai Srujan Murthy**  
Email: saisrujanmurthy@gmail.com

---

**Status:** Foundation Complete ✅  
**Next Milestone:** Implement first 3 ciphers and 2 hashers  
**Target:** 10 unified cryptographic tools
