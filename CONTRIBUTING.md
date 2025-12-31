# Contributing to CryptoSentinel

Thank you for your interest in contributing to CryptoSentinel! This educational cryptography framework welcomes contributions from developers of all skill levels.

## 🌟 Ways to Contribute

### 1. **Code Contributions**
- Implement new cryptographic algorithms
- Improve existing tool implementations
- Add new features or enhancements
- Fix bugs and issues

### 2. **Documentation**
- Improve Wiki pages
- Add code examples
- Write tutorials
- Translate documentation

### 3. **Testing**
- Write unit tests
- Report bugs
- Suggest improvements
- Test on different platforms

### 4. **Educational Content**
- Create learning resources
- Add algorithm explanations
- Develop practice challenges
- Share use cases

## 🚀 Getting Started

### Fork and Clone

1. **Fork the repository:**
   ```bash
   # Click "Fork" on GitHub
   ```

2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/CryptoSentinel.git
   cd CryptoSentinel
   ```

3. **Add upstream remote:**
   ```bash
   git remote add upstream https://github.com/Shiva-destroyer/CryptoSentinel.git
   ```

### Set Up Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_caesar.py
```

## 📝 Contribution Guidelines

### Code Style

- **PEP 8:** Follow Python's style guide
- **Type Hints:** Use type annotations for functions
- **Docstrings:** Document all classes and functions (Google style)
- **Formatting:** Use `black` for code formatting

```bash
# Format code
black src/ tests/

# Check style
flake8 src/ tests/

# Type checking
mypy src/
```

### Commit Messages

Use clear, descriptive commit messages:

```
Add SHA-512 hash implementation

- Implement SHA-512 algorithm following FIPS 180-4
- Add comprehensive unit tests
- Update documentation with usage examples
```

**Format:**
- **First line:** Brief summary (50 chars max)
- **Body:** Detailed explanation (wrap at 72 chars)
- **Footer:** Issue references (e.g., "Fixes #42")

### Branch Naming

- `feature/algorithm-name` - New features
- `fix/issue-description` - Bug fixes
- `docs/topic` - Documentation updates
- `test/component` - Test additions

Example: `feature/rsa-encryption`

## 🔄 Pull Request Process

### Before Submitting

1. **Update from upstream:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests:**
   ```bash
   pytest
   ```

3. **Check code style:**
   ```bash
   black --check src/ tests/
   flake8 src/ tests/
   ```

4. **Update documentation:**
   - Update README.md if needed
   - Add/update Wiki pages
   - Include docstrings

### Submit Pull Request

1. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request:**
   - Go to GitHub and click "New Pull Request"
   - Select your fork and branch
   - Fill out the PR template

3. **PR Title Format:**
   ```
   [Type] Brief description
   
   Examples:
   [Feature] Add RSA encryption algorithm
   [Fix] Correct Vigenère key length detection
   [Docs] Update Caesar cipher Wiki page
   ```

4. **PR Description Should Include:**
   - What changes were made
   - Why the changes are necessary
   - How to test the changes
   - Related issues (if any)

### Review Process

- Maintainers will review your PR within 3-7 days
- Address any requested changes
- Once approved, your PR will be merged

## 🎯 What to Contribute

### High-Priority Areas

- **Classical Ciphers:** Playfair, Four-Square, Bifid
- **Modern Algorithms:** RSA, AES, DES
- **Cryptanalysis Tools:** Frequency analysis, pattern detection
- **Hash Functions:** SHA-512, BLAKE2, RIPEMD
- **Encoding Schemes:** URL encoding, Hex encoding
- **Test Coverage:** Increase test coverage to >90%

### Educational Focus

Remember, CryptoSentinel is educational:
- **Explain Algorithms:** Add detailed comments
- **Show Vulnerabilities:** Demonstrate weaknesses
- **Compare Methods:** Show multiple approaches
- **Educational Value:** Prioritize learning over performance

## 🐛 Reporting Issues

### Bug Reports

Include:
- **Description:** Clear summary of the bug
- **Steps to Reproduce:** Exact steps
- **Expected Behavior:** What should happen
- **Actual Behavior:** What actually happens
- **Environment:** OS, Python version, dependencies
- **Logs:** Error messages or stack traces

### Feature Requests

Include:
- **Description:** What feature you'd like
- **Use Case:** Why it's needed
- **Proposed Solution:** How it could work
- **Alternatives:** Other approaches considered

## 📜 Code of Conduct

### Our Standards

- **Be Respectful:** Treat everyone with kindness
- **Be Constructive:** Provide helpful feedback
- **Be Patient:** Remember everyone is learning
- **Be Professional:** Keep discussions on-topic

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Spam or self-promotion
- Sharing others' private information

## 📞 Communication

- **Issues:** For bugs and feature requests
- **Discussions:** For questions and ideas
- **Email:** saisrujanmurthy@gmail.com

## 🏆 Recognition

Contributors will be:
- Listed in README.md
- Credited in release notes
- Acknowledged in Wiki pages

## 📚 Resources

- **Project Wiki:** [CryptoSentinel Wiki](https://github.com/Shiva-destroyer/CryptoSentinel/wiki)
- **Python Docs:** [Python.org](https://docs.python.org/3/)
- **Cryptography:** [Handbook of Applied Cryptography](http://cacr.uwaterloo.ca/hac/)
- **PEP 8:** [Style Guide](https://pep8.org/)

## ❓ Questions?

Don't hesitate to ask! Open an issue with the `question` label or email directly.

---

**Thank you for contributing to CryptoSentinel!**

**Developed by:** saisrujanmurthy@gmail.com  
**Repository:** [https://github.com/Shiva-destroyer/CryptoSentinel](https://github.com/Shiva-destroyer/CryptoSentinel)
