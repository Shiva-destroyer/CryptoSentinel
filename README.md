# CryptoSentinel Framework

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Status](https://img.shields.io/badge/status-production-success.svg)

**A comprehensive cryptographic toolkit featuring classical and modern cipher implementations, hashing algorithms, and security analysis tools with a beautiful CLI interface.**

---

## 📋 Overview

CryptoSentinel is a production-ready Python framework designed for cryptographic operations, security analysis, and educational purposes. Built with clean architecture and SOLID principles, it provides both powerful functionality and an intuitive user experience.

**Repository:** https://github.com/Shiva-destroyer/CryptoSentinel.git

---

## ✨ Features

### 🔐 Classical Ciphers
- **Caesar Cipher** - Shift-based encryption with frequency analysis
- **Vigenère Cipher** - Polyalphabetic substitution with IoC & Kasiski examination
- **Substitution Cipher** - Monoalphabetic substitution with hill climbing cryptanalysis
- **XOR Cipher** - Bitwise XOR encryption with key detection

### 📡 Encoding Tools
- **Morse Code** - Binary tree-based encoding/decoding

### 🔒 Hashing & Security
- **MD5 & SHA-256** - Cryptographic hash functions with streaming support for large files
- **Checksum Validator** - File integrity verification and corruption detection
- **Password Analyzer** - Entropy calculation and strength assessment with crack-time estimation
- **Base64 Encoder** - Binary-to-text conversion for safe data transport

### 🎨 Beautiful CLI
- Rich library integration with color-coded output
- Interactive menus and progress bars
- Formatted tables and panels
- Comprehensive help system

---

## 🚀 Installation

### Clone Repository
```bash
git clone https://github.com/Shiva-destroyer/CryptoSentinel.git
cd CryptoSentinel
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Install Package (Optional)
```bash
pip install -e .
```

---

## 💻 Usage

### Launch Interactive CLI
```bash
python cli.py
```

### Quick Examples

#### Caesar Cipher Encryption
```python
from crypto_sentinel.ciphers import CaesarCipher

cipher = CaesarCipher()
encrypted = cipher.encrypt("Hello World", key=3)
print(encrypted)  # "Khoor Zruog"
```

#### SHA-256 File Hashing
```python
from crypto_sentinel.hashing import SHA256Hasher

hasher = SHA256Hasher()
file_hash = hasher.hash_file("document.pdf")
print(file_hash)  # 64-character hex digest
```

#### Password Strength Analysis
```python
from crypto_sentinel.security import PasswordAnalyzer

analyzer = PasswordAnalyzer()
result = analyzer.analyze("MyP@ssw0rd2024!")
print(f"Entropy: {result['entropy']:.1f} bits")
print(f"Strength: {result['strength']}")
print(f"Time to crack: {result['crack_time']['display']}")
```

---

## 📚 Documentation

### **[📖 Read the Full Documentation in the Project Wiki](https://github.com/Shiva-destroyer/CryptoSentinel/wiki)**

The comprehensive wiki includes:
- **Detailed Algorithm Explanations** - ELI5 through advanced mathematics
- **Cryptanalysis Techniques** - Frequency analysis, IoC, Kasiski examination
- **Code Examples & Tutorials** - Step-by-step guides
- **Security Best Practices** - Password entropy, hashing guidelines
- **Mathematical Foundations** - Chi-squared tests, Friedman tests, entropy calculations

---

## 🧪 Testing

Run the complete test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=crypto_sentinel
```

---

## 📦 Package Structure

```
crypto_sentinel/
├── ciphers/           # Cipher implementations
├── hashing/           # Hash functions and validators
├── security/          # Security analysis tools
├── core/              # Base classes and exceptions
├── ui/                # CLI interface components
└── utils/             # Helper utilities

tests/                 # Comprehensive test suite
docs/                  # Developer documentation
cli.py                 # Main CLI application
```

---

## 🛠️ Requirements

- **Python**: 3.8 or higher
- **Dependencies**: 
  - `rich>=13.0.0` - CLI formatting
  - `pytest>=7.0.0` - Testing framework

---

## 🎯 Use Cases

✅ **Educational** - Learn cryptography concepts interactively  
✅ **Security Analysis** - Analyze password strength and entropy  
✅ **File Integrity** - Verify file checksums and detect corruption  
✅ **Data Encoding** - Convert binary data for safe transport  
✅ **Development** - Integrate cryptographic operations into projects  

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest features.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**saisrujanmurthy@gmail.com**

- GitHub: [@Shiva-destroyer](https://github.com/Shiva-destroyer)
- Repository: https://github.com/Shiva-destroyer/CryptoSentinel.git

---

## 🌟 Acknowledgments

- Built with ❤️ using Python and the Rich library
- Inspired by classical cryptography and modern security principles
- Comprehensive documentation written for learners at all levels

---

## 📊 Project Status

✅ **Production Ready** - Fully tested and documented  
✅ **Active Development** - Regular updates and improvements  
✅ **Comprehensive Testing** - 50+ test cases with pytest  
✅ **Professional Documentation** - 5,900+ lines in wiki  

---

<div align="center">

**⭐ Star this repository if you find it useful! ⭐**

[Documentation](https://github.com/Shiva-destroyer/CryptoSentinel/wiki) • [Issues](https://github.com/Shiva-destroyer/CryptoSentinel/issues) • [Repository](https://github.com/Shiva-destroyer/CryptoSentinel)

</div>
