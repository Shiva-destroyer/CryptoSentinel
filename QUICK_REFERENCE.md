# 🚀 CryptoSentinel Quick Reference

**Author:** saisrujanmurthy@gmail.com  
**Location:** `/home/shivansh/Vs Code/Github projects/CryptoSentinel`

---

## ⚡ Quick Commands

```bash
# Navigate to project
cd "/home/shivansh/Vs Code/Github projects/CryptoSentinel"

# Setup (one-time)
python3.10 -m venv venv && source venv/bin/activate
make install-dev

# Development workflow
make validate    # ✓ Check installation
make test       # 🧪 Run tests
make check      # 🔍 Format, lint, typecheck
make coverage   # 📊 Test coverage
make help       # 📚 See all commands
```

---

## 📁 Key Locations

| What | Where |
|------|-------|
| Core ABCs | `crypto_sentinel/core/` |
| Math utils | `crypto_sentinel/utils/math_helpers.py` |
| Exceptions | `crypto_sentinel/core/exceptions.py` |
| Tests | `tests/` |
| Docs | `docs/` |

---

## 🏗️ Interface Templates

### Cipher
```python
from crypto_sentinel.core.base_cipher import CipherInterface

class MyCipher(CipherInterface):
    def encrypt(self, data: str | bytes, key: Any) -> str | bytes: ...
    def decrypt(self, data: str | bytes, key: Any) -> str | bytes: ...
    def crack(self, data: str | bytes) -> dict[str, Any]: ...
```

### Hasher
```python
from crypto_sentinel.core.base_hasher import HasherInterface

class MyHasher(HasherInterface):
    @property
    def algorithm_name(self) -> str: ...
    @property
    def digest_size(self) -> int: ...
    def hash_string(self, text: str) -> str: ...
    def hash_file(self, filepath: str | Path) -> str: ...
```

### Analyzer
```python
from crypto_sentinel.core.base_analyzer import AnalyzerInterface

class MyAnalyzer(AnalyzerInterface):
    @property
    def analyzer_name(self) -> str: ...
    @property
    def version(self) -> str: ...
    def analyze(self, data: str | bytes) -> dict[str, Any]: ...
    def validate(self, data: str | bytes) -> bool: ...
```

---

## 🧮 Math Functions

```python
from crypto_sentinel.utils.math_helpers import *

gcd(48, 18)                    # → 6
modular_inverse(7, 26)         # → 15
calculate_ioc("HELLO WORLD")   # → ~0.0727
is_coprime(15, 28)            # → True
factorial(5)                   # → 120
chi_squared([10,15,12], [12.0,14.0,11.0])  # → 0.69
```

---

## 🎯 Next Implementations

1. **Caesar Cipher** → `crypto_sentinel/ciphers/caesar.py`
2. **Vigenère Cipher** → `crypto_sentinel/ciphers/vigenere.py`
3. **MD5 Hasher** → `crypto_sentinel/hashing/md5.py`
4. **SHA256 Hasher** → `crypto_sentinel/hashing/sha256.py`
5. **Password Analyzer** → `crypto_sentinel/security/password.py`

---

## 📝 Testing Pattern

```python
import pytest
from crypto_sentinel.ciphers.my_cipher import MyCipher

class TestMyCipher:
    def test_basic_operation(self) -> None:
        cipher = MyCipher()
        result = cipher.encrypt("test", key=3)
        assert result == "expected"
    
    def test_invalid_input_raises(self) -> None:
        cipher = MyCipher()
        with pytest.raises(ValidationError):
            cipher.encrypt("", key=3)
```

---

## 🔧 Common Makefile Commands

| Command | Action |
|---------|--------|
| `make help` | Show all commands |
| `make validate` | Quick health check |
| `make test` | Run all tests |
| `make coverage` | Tests + coverage |
| `make format` | Format code |
| `make lint` | Check code quality |
| `make typecheck` | Type checking |
| `make check` | All quality checks |
| `make clean` | Remove artifacts |
| `make all` | Everything |

---

## 📚 Documentation

- **README.md** - Project overview
- **docs/PROJECT_STRUCTURE.md** - Architecture reference
- **docs/DEVELOPER_GUIDE.md** - Development handbook
- **INITIALIZATION_COMPLETE.md** - Setup summary

---

## ✉️ Contact

**Sai Srujan Murthy**  
saisrujanmurthy@gmail.com

---

**Status:** ✅ Foundation Complete | 🚀 Ready for Development
