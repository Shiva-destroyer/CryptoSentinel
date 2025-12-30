# CryptoSentinel - Advanced Security Framework

**A Production-Grade Cryptographic Framework for Education and Security Analysis**

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

---

## 📚 Welcome to CryptoSentinel

CryptoSentinel is a comprehensive, production-grade framework that unifies **10 cryptographic and security tools** into a single, professionally designed application. Built with modern software engineering principles, it serves as both an educational resource and a practical security toolkit.

### 🎯 What Makes CryptoSentinel Unique?

- **Educational**: Each module includes detailed mathematical explanations, cryptanalysis techniques, and interactive demonstrations
- **Professional**: Type-hinted code, comprehensive docstrings, and production-ready error handling
- **Interactive**: Beautiful CLI interface powered by Rich library with animations and colored output
- **Modular**: Clean OOP architecture with abstract base classes and dependency injection
- **Tested**: Comprehensive test suite covering edge cases and security scenarios

---

## 🔐 Included Cryptographic Tools

### Classical Ciphers (5 Implementations)

1. **[Caesar Cipher](Caesar-Cipher.md)** - Shift cipher with frequency analysis cracking
2. **[Vigenère Cipher](Vigenere-Cipher.md)** - Polyalphabetic cipher with IoC-based key detection
3. **XOR Cipher** - Bitwise encryption with key reuse detection
4. **Substitution Cipher** - Monoalphabetic replacement with frequency analysis
5. **Morse Code** - International standard encoding/decoding

### Hashing Functions (3 Implementations)

6. **MD5 Hasher** - Legacy hash function with collision awareness
7. **SHA-256 Hasher** - Secure hash algorithm with streaming support
8. **Checksum Validator** - File integrity verification tool

### Security Tools (2 Implementations)

9. **Password Analyzer** - Comprehensive strength evaluation with entropy calculation
10. **Base64 Encoder** - Standard encoding/decoding utilities

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Shiva-destroyer/CryptoSentinel.git
cd CryptoSentinel

# Install dependencies
pip install -r requirements.txt

# Launch interactive CLI
python cli.py
```

### First Steps

1. **Try the Interactive CLI** - Run `python cli.py` for a beautiful terminal experience
2. **Run the Demo** - Execute `python demo_ui.py` for a non-interactive showcase
3. **Explore the Code** - Navigate to `crypto_sentinel/` to see the implementations
4. **Read the Wiki** - Start with [Caesar Cipher](Caesar-Cipher.md) to understand the fundamentals

---

## 📖 Documentation Structure

### Getting Started
- **[Home](Home.md)** - You are here!
- **[Installation Guide](#installation)** - Setup instructions
- **[CLI Usage](../CLI_IMPLEMENTATION.md)** - Interactive interface documentation

### Cipher Deep Dives
- **[Caesar Cipher](Caesar-Cipher.md)** - ELI5, Math, Frequency Analysis, Chi-Squared Test
- **[Vigenère Cipher](Vigenere-Cipher.md)** - Polyalphabetic encryption, Friedman Test, Kasiski Examination
- **XOR Cipher** _(Coming Soon)_ - Bitwise operations, key reuse attacks
- **Substitution Cipher** _(Coming Soon)_ - Letter mapping, frequency analysis
- **Morse Code** _(Coming Soon)_ - Timing-based encoding

### Hashing & Security
- **MD5 & SHA-256** _(Coming Soon)_ - Hash functions, collision resistance
- **Password Analysis** _(Coming Soon)_ - Entropy calculation, strength metrics
- **Base64 Encoding** _(Coming Soon)_ - Standard encoding schemes

### Advanced Topics
- **Cryptanalysis Techniques** _(Coming Soon)_ - Breaking classical ciphers
- **Frequency Analysis** _(Coming Soon)_ - Statistical attack methods
- **Mathematical Foundations** _(Coming Soon)_ - Number theory, modular arithmetic

---

## 🎨 Interactive CLI Features

CryptoSentinel includes a stunning terminal interface with:

✨ **ASCII Art Banner** - Eye-catching cyan-colored header  
✨ **Rich Tables** - Organized menus with emoji icons  
✨ **Progress Bars** - Animated processing indicators  
✨ **Color Coding** - Cyan (info), Green (success), Red (errors), Yellow (warnings)  
✨ **Side-by-Side Comparisons** - Input vs Output tables  
✨ **Password Strength Visualization** - Colored bars based on score  
✨ **Graceful Error Handling** - No crashes, only friendly panels  
✨ **Keyboard Shortcuts** - Ctrl+C exits gracefully  

See the [CLI Documentation](../CLI_IMPLEMENTATION.md) for screenshots and detailed usage.

---

## 🏗️ Architecture Overview

```
CryptoSentinel/
├── crypto_sentinel/              # Main source code
│   ├── core/                     # Abstract base classes
│   │   ├── base_cipher.py        # CipherInterface ABC
│   │   ├── base_hasher.py        # HasherInterface ABC
│   │   ├── base_analyzer.py      # AnalyzerInterface ABC
│   │   └── exceptions.py         # Custom exception hierarchy
│   ├── ciphers/                  # Classical encryption
│   │   ├── caesar.py             # Caesar cipher + frequency analysis
│   │   ├── vigenere.py           # Vigenère + IoC analysis
│   │   ├── xor.py                # XOR cipher
│   │   ├── substitution.py       # Substitution cipher
│   │   └── morse.py              # Morse code
│   ├── hashing/                  # Hash functions
│   │   ├── md5_hasher.py         # MD5 implementation
│   │   ├── sha256_hasher.py      # SHA-256 implementation
│   │   └── checksum.py           # File checksum validator
│   ├── security/                 # Security tools
│   │   ├── password_analyzer.py  # Password strength analysis
│   │   └── base64_encoder.py     # Base64 encoding
│   ├── utils/                    # Utility functions
│   │   └── math_helpers.py       # GCD, modular inverse, IoC, chi-squared
│   └── ui/                       # Rich CLI interface
│       └── console_ui.py         # Terminal UI implementation
├── tests/                        # Comprehensive test suite
├── wiki_docs/                    # GitHub Wiki documentation (you are here!)
└── cli.py                        # Main entry point
```

---

## 🧮 Mathematical Foundations

CryptoSentinel is built on solid mathematical principles:

- **Modular Arithmetic** - Used in Caesar, Vigenère, and XOR ciphers
- **Frequency Analysis** - Statistical cryptanalysis technique
- **Chi-Squared Test** - Measures deviation from expected English letter distribution
- **Index of Coincidence (IoC)** - Detects key length in polyalphabetic ciphers
- **Kasiski Examination** - Finds repeated patterns to determine key length
- **Entropy Calculation** - Measures password randomness

Each module's wiki page includes detailed mathematical explanations with LaTeX formulas.

---

## 👨‍💻 Author

**Sai Srujan Murthy**  
📧 **Email**: saisrujanmurthy@gmail.com  
🐙 **GitHub**: [Shiva-destroyer](https://github.com/Shiva-destroyer)

Built with ❤️ for students, educators, and security enthusiasts.

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](../LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Whether you're:
- Adding new ciphers or algorithms
- Improving documentation
- Writing more tests
- Fixing bugs
- Enhancing the CLI

Please feel free to submit issues and pull requests.

---

## 🎓 Educational Use

CryptoSentinel is designed for **educational purposes**. It demonstrates:
- How classical ciphers work and why they're broken
- Modern cryptanalysis techniques
- Software engineering best practices
- Type-safe Python programming
- Test-driven development

**⚠️ Important**: Do NOT use these classical ciphers for real-world security. They are easily crackable and serve only as learning tools. For production security, use modern algorithms like AES-256 and bcrypt.

---

## 📞 Support

- **Documentation**: Browse the wiki pages for detailed guides
- **Issues**: Report bugs on [GitHub Issues](https://github.com/Shiva-destroyer/CryptoSentinel/issues)
- **Email**: Contact saisrujanmurthy@gmail.com for questions

---

## 🗺️ Wiki Navigation

📌 **Start Here**
- [Home](Home.md) ← You are here
- [Installation Guide](#installation)

🔐 **Cipher Modules**
- [Caesar Cipher](Caesar-Cipher.md) - Beginner-friendly shift cipher
- [Vigenère Cipher](Vigenere-Cipher.md) - Advanced polyalphabetic encryption

🧰 **Tools & Utilities**
- [CLI Usage](../CLI_IMPLEMENTATION.md) - Interactive terminal interface
- [Testing Guide](../tests/) - Running the test suite

📚 **Learning Resources**
- [Mathematical Foundations](#mathematical-foundations) - Number theory basics
- [Cryptanalysis Techniques](#) - Breaking ciphers systematically

---

**Last Updated**: December 30, 2025  
**Version**: 1.0.0  
**Status**: ✅ Active Development
