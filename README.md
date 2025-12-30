# CryptoSentinel

**A Production-Grade Cryptographic Framework**

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

## Overview

CryptoSentinel is a highly advanced, object-oriented framework that unifies 10 cryptographic and security tools into a single professional application. Built with production-grade code quality, comprehensive type hints, and modular architecture for maximum scalability.

## Author

**Sai Srujan Murthy**  
📧 saisrujanmurthy@gmail.com

## Features

### 🔐 Classical Ciphers
- **Caesar Cipher** - Simple shift cipher with brute force cracking
- **Vigenère Cipher** - Polyalphabetic substitution with key length analysis
- **XOR Cipher** - Bitwise encryption with key reuse detection
- **Substitution Cipher** - Monoalphabetic replacement with frequency analysis
- **Morse Code** - International Morse encoding/decoding

### 🔒 Cryptographic Hashing
- **MD5** - Legacy hash function with collision awareness
- **SHA-256** - Secure hash algorithm with streaming support
- **Checksum Validators** - File integrity verification

### 🛡️ Security Tools
- **Password Strength Analyzer** - Comprehensive password evaluation
- **Base64 Encoder/Decoder** - Standard encoding utilities

### 🧮 Advanced Utilities
- **Mathematical Helpers** - GCD, modular inverse, IoC calculation
- **File I/O Operations** - Streaming support for large files
- **Text Processing** - Frequency analysis and pattern detection

## Architecture

```
CryptoSentinel/
├── crypto_sentinel/          # Main source code
│   ├── core/                # Abstract base classes
│   │   ├── base_cipher.py   # CipherInterface ABC
│   │   ├── base_hasher.py   # HasherInterface ABC
│   │   ├── base_analyzer.py # AnalyzerInterface ABC
│   │   └── exceptions.py    # Custom exceptions
│   ├── ciphers/             # Classical encryption implementations
│   ├── hashing/             # Hash function implementations
│   ├── security/            # Security analysis tools
│   ├── utils/               # Utility functions
│   │   └── math_helpers.py  # Mathematical operations
│   └── ui/                  # Rich CLI interface
├── tests/                   # Comprehensive test suite
├── docs/                    # Documentation assets
└── README.md               # This file
```

## Requirements

- Python 3.10 or higher
- Type hints throughout
- Google-style docstrings
- Production-grade error handling

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd CryptoSentinel

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

## 🎨 Interactive CLI

**NEW!** Experience CryptoSentinel through our stunning terminal interface powered by the Rich library:

```bash
# Launch interactive CLI
python cli.py

# Or run a non-interactive demo
python demo_ui.py
```

### CLI Features
✨ **Beautiful ASCII banner** with colored panels  
✨ **Interactive menus** with emoji icons and tables  
✨ **Animated progress bars** and spinners  
✨ **Colored output** (cyan/green/red/yellow theme)  
✨ **Side-by-side comparisons** for encrypt/decrypt operations  
✨ **Password strength visualization** with colored bars  
✨ **Graceful error handling** - no crashes, only friendly panels  
✨ **Ctrl+C support** - exit anytime with style  

See [CLI_IMPLEMENTATION.md](CLI_IMPLEMENTATION.md) for full documentation.

## Quick Start

### Command Line Interface (Recommended)

```bash
python cli.py
```

Then navigate through menus to:
- Encrypt/decrypt with 5 classical ciphers
- Hash text or files with MD5/SHA-256
- Validate file checksums
- Analyze password strength
- Encode/decode Base64

### Programmatic Usage

```python
from crypto_sentinel.ciphers import CaesarCipher
from crypto_sentinel.hashing import SHA256Hasher
from crypto_sentinel.security import PasswordAnalyzer

# Encrypt with Caesar cipher
cipher = CaesarCipher()
encrypted = cipher.encrypt("HELLO WORLD", key=3)
print(f"Encrypted: {encrypted}")

# Hash with SHA-256
hasher = SHA256Hasher()
hash_value = hasher.hash_string("sensitive data")
print(f"Hash: {hash_value}")

# Analyze password strength
analyzer = PasswordAnalyzer()
result = analyzer.analyze("MyP@ssw0rd123")
print(f"Password Score: {result['score']}")
```

## Design Principles

### 1. **Interface Segregation**
All modules implement well-defined abstract base classes ensuring consistent APIs across the framework.

### 2. **Type Safety**
Comprehensive type hints using Python 3.10+ features for enhanced IDE support and early error detection.

### 3. **Error Handling**
Custom exception hierarchy derived from `CryptoSentinelError` for graceful error management.

### 4. **Modularity**
Each component is self-contained and can be used independently or as part of the larger framework.

### 5. **Scalability**
Designed to accommodate new cryptographic algorithms and security tools without breaking existing code.

## Core Interfaces

### CipherInterface
```python
class CipherInterface(ABC):
    @abstractmethod
    def encrypt(self, data: str | bytes, key: Any) -> str | bytes: ...
    
    @abstractmethod
    def decrypt(self, data: str | bytes, key: Any) -> str | bytes: ...
    
    @abstractmethod
    def crack(self, data: str | bytes) -> dict: ...
```

### HasherInterface
```python
class HasherInterface(ABC):
    @abstractmethod
    def hash_string(self, text: str) -> str: ...
    
    @abstractmethod
    def hash_file(self, filepath: str) -> str: ...
```

### AnalyzerInterface
```python
class AnalyzerInterface(ABC):
    @abstractmethod
    def analyze(self, data: str | bytes) -> dict[str, Any]: ...
    
    @abstractmethod
    def validate(self, data: str | bytes) -> bool: ...
```

## Mathematical Utilities

The framework includes robust mathematical functions essential for cryptographic operations:

- **`gcd(a, b)`** - Greatest Common Divisor using Euclidean algorithm
- **`modular_inverse(a, m)`** - Modular multiplicative inverse for affine ciphers
- **`calculate_ioc(text)`** - Index of Coincidence for cryptanalysis
- **`is_coprime(a, b)`** - Check if two numbers are relatively prime
- **`chi_squared(observed, expected)`** - Statistical analysis for frequency attacks

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test module
pytest tests/test_core/ -v

# Run with coverage
pytest tests/ --cov=crypto_sentinel
```

## Contributing

Contributions are welcome! Please ensure:

1. All code includes type hints
2. Google-style docstrings for all public APIs
3. Comprehensive unit tests (>90% coverage)
4. Code passes `mypy` type checking
5. Follows PEP 8 style guidelines

## License

MIT License - See LICENSE file for details

## Roadmap

- [ ] Implement remaining cipher classes
- [ ] Add RSA encryption support
- [ ] Build Rich CLI interface
- [ ] Add web API endpoints
- [ ] Create comprehensive documentation site
- [ ] Add performance benchmarks
- [ ] Docker containerization

## Contact

For questions, suggestions, or contributions:

**Sai Srujan Murthy**  
📧 saisrujanmurthy@gmail.com

---

**Built with ❤️ for the security community**
