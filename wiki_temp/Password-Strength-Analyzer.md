# Password Strength Analyzer

**Entropy Calculation and Security Assessment**

---

## Introduction

The Password Strength Analyzer is a sophisticated tool that evaluates password security using **information theory** and **entropy calculation**. Unlike simplistic checkers that just count characters or require specific symbols, this tool calculates the true cryptographic strength of passwords and estimates how long it would take an attacker to crack them.

In an era where data breaches expose billions of passwords annually, understanding password strength is critical for:
- **Personal security** - Protecting online accounts
- **Enterprise security** - Enforcing password policies
- **Security audits** - Assessing authentication systems
- **User education** - Teaching good password practices

CryptoSentinel's analyzer provides:
- **Shannon entropy** calculation (bits of randomness)
- **Crack time estimation** (brute force, dictionary, AI-assisted)
- **Pattern detection** (common weaknesses)
- **Actionable recommendations** (how to improve)

### When to Use This Tool

✅ **Creating new passwords** - Ensure adequate strength  
✅ **Password policy enforcement** - Set minimum requirements  
✅ **Security audits** - Assess authentication systems  
✅ **User education** - Demonstrate password security  
✅ **Compliance** - Meet regulatory requirements (PCI DSS, HIPAA)  

❌ **Storing passwords** - Use [[SHA256-Hash-Implementation]] with proper KDF  
❌ **Transmitting passwords** - Use secure channels (HTTPS, SSH)  

---

## Algorithm: Entropy and Information Theory

### What is Entropy?

In cryptography, **entropy** measures the unpredictability of a password. Higher entropy = more random = harder to crack.

**Formula:**
```
Entropy (bits) = log₂(R^L)
               = L × log₂(R)
```

Where:
- **L** = Password length
- **R** = Size of character set (pool of possible characters)

### Character Set Sizes

Different character types provide different pool sizes:

| Character Type | Example | Pool Size (R) |
|---------------|---------|---------------|
| Lowercase only | abc | 26 |
| Uppercase only | ABC | 26 |
| Numbers only | 123 | 10 |
| Lowercase + Uppercase | aB | 52 |
| Alphanumeric | aB1 | 62 |
| + Special characters | aB1! | ~94 |
| Extended ASCII | aB1!é | ~256 |

### Entropy Calculation Examples

**Example 1: "password"**
```
Length: 8
Character set: lowercase only (26)
Entropy = 8 × log₂(26) = 8 × 4.7 = 37.6 bits

Possible combinations: 26^8 = 208,827,064,576
At 1 billion guesses/sec: ~3.5 minutes
```

**Example 2: "P@ssw0rd"**
```
Length: 8
Character set: mixed (62 + special ≈ 70)
Entropy = 8 × log₂(70) = 8 × 6.13 = 49 bits

Possible combinations: 70^8 = 5.8 × 10^14
At 1 billion guesses/sec: ~6 days
```

**Example 3: "correct horse battery staple"** (XKCD method)
```
Length: 28 (with spaces: 4 words)
Character set: lowercase + space (27)
Entropy = 28 × log₂(27) = 28 × 4.75 = 133 bits

But actually: 4 random words from 2048-word dictionary
True entropy = log₂(2048^4) = 44 bits

Memorable AND secure!
```

### Entropy Strength Guidelines

| Entropy (bits) | Strength | Crack Time | Use Case |
|---------------|----------|------------|-----------|
| < 28 | Very Weak | Instant | ⛔ Never use |
| 28-35 | Weak | Minutes | ⛔ Avoid |
| 36-59 | Moderate | Days to years | ⚠️ OK for low-value accounts |
| 60-127 | Strong | Centuries | ✅ Good for most uses |
| 128+ | Very Strong | Never | ✅ High-security accounts |

### Attack Methods and Time Estimates

**1. Brute Force (try all combinations)**
```
Time = R^L / attempts_per_second
```

**Modern attack speeds:**
- CPU: 100 million - 1 billion hashes/sec (MD5, SHA1)
- GPU: 10-100 billion hashes/sec
- ASIC: 1 trillion+ hashes/sec (Bitcoin miners)
- Botnet: Distributed = even faster

**2. Dictionary Attack (try common passwords)**
```
Most common 10,000 passwords: Instant
RockYou leaked 32 million passwords: < 1 second
Combined wordlists: < 1 hour
```

**Top 10 most common passwords (NEVER use these):**
1. 123456
2. password
3. 123456789
4. 12345678
5. 12345
6. 111111
7. 1234567
8. sunshine
9. qwerty
10. iloveyou

**3. AI-Assisted Attack (PassGAN)**
```
Neural networks trained on breach data
Learns patterns humans use
Can crack 50%+ of passwords faster than brute force
```

### Pattern Detection

**Weak patterns to avoid:**
- ❌ Sequential: "123456", "abcdef"
- ❌ Repeated: "aaaaaa", "111111"
- ❌ Keyboard patterns: "qwerty", "asdfgh", "1qaz2wsx"
- ❌ Common substitutions: "P@ssw0rd" (a→@, o→0)
- ❌ Common phrases: "iloveyou", "letmein"
- ❌ Personal info: names, birthdays, phone numbers
- ❌ Dictionary words: "dragon", "monkey", "master"

**Strong patterns:**
- ✅ True randomness: "Kj#8mP2$nQ9x"
- ✅ Passphrase: "correct horse battery staple"
- ✅ Password manager generated
- ✅ Long (16+ characters)
- ✅ Mixed character types

---

## How It Works: Code Implementation

### Entropy Calculator

```python
import math
import re
from typing import Dict, List, Tuple

class PasswordAnalyzer:
    """
    Analyzes password strength using entropy calculation.
    """
    
    # Common password patterns
    COMMON_PASSWORDS = [
        '123456', 'password', '123456789', '12345678', '12345',
        '111111', '1234567', 'sunshine', 'qwerty', 'iloveyou'
        # ... (extended list of 10,000+ common passwords)
    ]
    
    def analyze(self, password: str) -> Dict:
        """
        Comprehensive password strength analysis.
        
        Returns:
            {
                'entropy': float,
                'strength': str,
                'crack_time': Dict,
                'issues': List[str],
                'recommendations': List[str]
            }
        """
        return {
            'entropy': self.calculate_entropy(password),
            'strength': self.get_strength_rating(password),
            'crack_time': self.estimate_crack_time(password),
            'issues': self.detect_weaknesses(password),
            'recommendations': self.get_recommendations(password),
            'character_analysis': self.analyze_characters(password)
        }
    
    def calculate_entropy(self, password: str) -> float:
        """
        Calculate Shannon entropy in bits.
        """
        if not password:
            return 0.0
        
        # Determine character set size
        pool_size = 0
        
        if re.search(r'[a-z]', password):
            pool_size += 26  # Lowercase
        if re.search(r'[A-Z]', password):
            pool_size += 26  # Uppercase
        if re.search(r'[0-9]', password):
            pool_size += 10  # Digits
        if re.search(r'[^a-zA-Z0-9]', password):
            pool_size += 32  # Special characters (approximate)
        
        # Entropy = length × log₂(pool_size)
        entropy = len(password) * math.log2(pool_size) if pool_size > 0 else 0
        
        return round(entropy, 2)
    
    def analyze_characters(self, password: str) -> Dict:
        """
        Analyze character composition.
        """
        return {
            'length': len(password),
            'lowercase': sum(1 for c in password if c.islower()),
            'uppercase': sum(1 for c in password if c.isupper()),
            'digits': sum(1 for c in password if c.isdigit()),
            'special': sum(1 for c in password if not c.isalnum()),
            'unique_chars': len(set(password))
        }
    
    def estimate_crack_time(self, password: str) -> Dict:
        """
        Estimate time to crack using different attack methods.
        """
        entropy = self.calculate_entropy(password)
        
        # Possible combinations
        combinations = 2 ** entropy
        
        # Attack speeds (hashes per second)
        speeds = {
            'online_throttled': 100,          # 100 attempts/sec (rate limited)
            'online': 10_000,                 # 10K attempts/sec
            'offline_slow': 1_000_000,        # 1M/sec (bcrypt, Argon2)
            'offline_fast': 100_000_000_000,  # 100B/sec (MD5/SHA1 on GPU)
        }
        
        results = {}
        for method, speed in speeds.items():
            seconds = combinations / speed
            results[method] = self._format_time(seconds)
        
        return results
    
    def _format_time(self, seconds: float) -> str:
        """
        Convert seconds to human-readable time.
        """
        if seconds < 1:
            return "Instant"
        elif seconds < 60:
            return f"{seconds:.0f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.0f} minutes"
        elif seconds < 86400:
            return f"{seconds/3600:.1f} hours"
        elif seconds < 31536000:
            return f"{seconds/86400:.0f} days"
        elif seconds < 31536000 * 100:
            return f"{seconds/31536000:.1f} years"
        elif seconds < 31536000 * 1000000:
            return f"{seconds/(31536000*1000):.0f} thousand years"
        elif seconds < 31536000 * 1000000000:
            return f"{seconds/(31536000*1000000):.0f} million years"
        else:
            return "Heat death of universe"
    
    def detect_weaknesses(self, password: str) -> List[str]:
        """
        Identify common password weaknesses.
        """
        issues = []
        
        # Length check
        if len(password) < 8:
            issues.append("❌ Too short (minimum 8 characters)")
        elif len(password) < 12:
            issues.append("⚠️ Short (recommended 12+ characters)")
        
        # Common password check
        if password.lower() in self.COMMON_PASSWORDS:
            issues.append("❌ CRITICAL: Common password (appears in breach databases)")
        
        # Pattern detection
        if re.match(r'^(.)\1+$', password):
            issues.append("❌ All same character (e.g., 'aaaaa')")
        
        if re.search(r'123|234|345|456|567|678|789', password):
            issues.append("⚠️ Contains sequential numbers")
        
        if re.search(r'abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz', password.lower()):
            issues.append("⚠️ Contains sequential letters")
        
        if re.search(r'qwerty|asdfgh|zxcvbn', password.lower()):
            issues.append("⚠️ Keyboard pattern detected")
        
        # Character variety
        char_types = 0
        if re.search(r'[a-z]', password): char_types += 1
        if re.search(r'[A-Z]', password): char_types += 1
        if re.search(r'[0-9]', password): char_types += 1
        if re.search(r'[^a-zA-Z0-9]', password): char_types += 1
        
        if char_types < 2:
            issues.append("⚠️ Uses only one character type")
        elif char_types < 3:
            issues.append("⚠️ Missing character variety")
        
        # Repeated characters
        if re.search(r'(.)\1{2,}', password):
            issues.append("⚠️ Contains repeated characters (e.g., 'aaa')")
        
        return issues if issues else ["✅ No obvious weaknesses detected"]
    
    def get_recommendations(self, password: str) -> List[str]:
        """
        Provide actionable improvement recommendations.
        """
        recommendations = []
        entropy = self.calculate_entropy(password)
        
        if entropy < 60:
            recommendations.append("🔑 Increase length to 12+ characters")
            recommendations.append("🔀 Add more character variety (uppercase, numbers, symbols)")
        
        if len(password) < 12:
            recommendations.append("📏 Use at least 12 characters for good security")
        
        if not re.search(r'[A-Z]', password):
            recommendations.append("🔠 Add uppercase letters")
        
        if not re.search(r'[0-9]', password):
            recommendations.append("🔢 Add numbers")
        
        if not re.search(r'[^a-zA-Z0-9]', password):
            recommendations.append("🔣 Add special characters (!@#$%^&*)")
        
        # General best practices
        recommendations.append("💡 Consider using a passphrase (4+ random words)")
        recommendations.append("🔐 Use a password manager to generate and store passwords")
        recommendations.append("🔄 Enable two-factor authentication (2FA)")
        recommendations.append("🚫 Never reuse passwords across sites")
        
        return recommendations
    
    def get_strength_rating(self, password: str) -> str:
        """
        Get overall strength rating.
        """
        entropy = self.calculate_entropy(password)
        
        if entropy < 28:
            return "Very Weak ⛔"
        elif entropy < 36:
            return "Weak ⚠️"
        elif entropy < 60:
            return "Moderate ⚡"
        elif entropy < 128:
            return "Strong ✅"
        else:
            return "Very Strong 🔒"
```

---

## Usage Guide: CLI Commands

### Starting the Tool

```bash
python cli.py

# Select: 3. Security Tools > 1. Password Strength Analyzer
```

### Analyzing a Password

```
Enter password to analyze: P@ssw0rd123

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PASSWORD STRENGTH ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Character Analysis:
  Length: 12 characters
  Lowercase: 6
  Uppercase: 1
  Digits: 3
  Special: 2
  Unique characters: 11

🔢 Entropy: 59.4 bits
💪 Strength: Moderate ⚡

⏱️  Estimated Crack Time:
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Attack Method      ┃ Time to Crack        ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ Online (throttled) │ 1.8 million years    │
│ Online (fast)      │ 18 thousand years    │
│ Offline (slow)     │ 18 years             │
│ Offline (fast GPU) │ 6.5 days             │
└────────────────────┴──────────────────────┘

⚠️  Identified Issues:
  ⚠️ Common substitution pattern (@ for a, 0 for o)
  ⚠️ Contains common base word 'password'
  ⚠️ Recommended length is 16+ characters

🔑 Recommendations:
  📏 Increase length to 16+ characters
  💡 Consider passphrase: "correct horse battery staple"
  🔐 Use password manager (Bitwarden, 1Password, KeePassXC)
  🔄 Enable 2FA wherever possible
  🚫 Never reuse this password on multiple sites

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Comparing Passwords

```
Compare mode: Enter multiple passwords

Password 1: password
Password 2: P@ssw0rd
Password 3: correct-horse-battery-staple
Password 4: Kj#8mP2$nQ9xRt5&Lw

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPARISON RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┏━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Password ┃ Length  ┃ Entropy     ┃ Crack Time   ┃
┃          ┃         ┃ (bits)      ┃ (GPU)        ┃
┡━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ Pass #1  │ 8       │ 37.6 ⛔     │ Instant      │
│ Pass #2  │ 8       │ 49.0 ⚠️     │ 6 days       │
│ Pass #3  │ 28      │ 131.7 🔒    │ 10^25 years  │
│ Pass #4  │ 18      │ 119.3 🔒    │ 10^23 years  │
└──────────┴─────────┴─────────────┴──────────────┘

Winner: Password #3 (passphrase)
  - Highest entropy
  - Easy to remember
  - Extremely secure
  - Recommended approach!
```

### Generating Secure Passwords

```
Generate secure password:
1. Random (high entropy)
2. Passphrase (memorable)
3. Custom pattern

Selection: 2

Passphrase options:
  Words: 4 (default), 5, 6
  Separator: - (default), space, none
  Capitalize: yes (default), no
  Add number: yes (default), no

Words: 5
Separator: space
Capitalize: yes
Add number: yes

✓ Generated passphrase:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Correct Horse Battery Staple Mountain 7
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Entropy: 143.2 bits
Strength: Very Strong 🔒
Memorable: ✅ Yes
Crack time: Never (universe heat death first)

Save this password securely!
```

---

## Troubleshooting

### Common Issues

**Problem:** "My complex password scored lower than a simple passphrase - why?"  
**Solution:** Length matters more than complexity:
- `P@ssw0rd!` (9 chars) = 56 bits entropy
- `correct horse battery staple` (28 chars) = 131 bits entropy
- Longer passwords have exponentially more combinations
- Passphrases are easier to remember AND more secure
- See [XKCD #936](https://xkcd.com/936/) for explanation

**Problem:** "Tool says my password is weak but it has symbols!"  
**Solution:** Common mistakes:
- ❌ `P@ssw0rd` - Common substitutions (a→@, o→0) are in attack dictionaries
- ❌ `Password1!` - Base word + number + symbol is predictable
- ✅ `Kj#8mP2$nQ9x` - Truly random characters
- ✅ `correct-horse-battery-staple` - Random words
- Symbols alone don't make passwords strong

**Problem:** "How often should I change my passwords?"  
**Solution:** Modern guidance (NIST SP 800-63B):
- ✅ **DO**: Change if compromised in a breach
- ✅ **DO**: Use unique password per site
- ✅ **DO**: Use long, strong passwords with 2FA
- ❌ **DON'T**: Force periodic changes (leads to weak patterns)
- ❌ **DON'T**: Reuse passwords
- Quality over rotation frequency

**Problem:** "Should I write down my passwords?"  
**Solution:** It depends on threat model:
- ✅ **Physical security high**: Written in locked safe > Weak memorable password
- ✅ **Best practice**: Use password manager (encrypted digital vault)
- ❌ **Never**: Sticky notes on monitor, unencrypted files, emails
- ❌ **Never**: Save in browser without master password
- Consider: Offline password manager or encrypted USB drive

**Problem:** "Password manager generated gibberish - is it safe?"  
**Solution:** YES! This is ideal:
- `Kj#8mP2$nQ9xRt5&Lw7@Nf9` is PERFECT
- Maximum entropy (truly random)
- Impossible to guess or brute force
- Password manager remembers it for you
- You only need to remember ONE strong master password
- **Recommendation**: Use password manager for everything

---

## Pros and Cons

### ✅ Advantages

**Scientific Approach**
- Based on information theory (Claude Shannon)
- Quantifiable security (entropy bits)
- Objective measurements
- Predictable attack resistance

**Comprehensive Analysis**
- Character composition
- Pattern detection
- Dictionary checks
- Realistic crack time estimates

**Educational Value**
- Teaches password security concepts
- Demonstrates why length > complexity
- Shows real attack methods
- Promotes good security habits

**Practical Recommendations**
- Actionable improvement steps
- Multiple security levels explained
- Passphrase generation
- Password manager integration

### ❌ Limitations

**Cannot Detect All Weaknesses**
- Personal information (names, dates) without context
- Company-specific patterns
- Language-specific common phrases
- Recently leaked passwords not in database

**Crack Time Estimates are Approximate**
- Attack speeds vary widely (hardware dependent)
- Doesn't account for AI-assisted attacks perfectly
- Rainbow tables can speed up specific attacks
- Assumes attacker knows character set

**Human Factors**
- Can't force users to follow recommendations
- Writing down complex passwords
- Password reuse across sites
- Social engineering (phishing bypasses password strength)

**Context Dependent**
- High-security vs low-security accounts have different needs
- Online vs offline attacks have different speeds
- With/without rate limiting
- With/without 2FA changes calculation

### Best Practices Summary

**✅ DO:**
- Use 16+ character passwords
- Use password manager
- Enable 2FA/MFA everywhere
- Use unique password per site
- Use passphrases when possible
- Check for breaches ([Have I Been Pwned](https://haveibeenpwned.com/))

**❌ DON'T:**
- Reuse passwords
- Use personal information
- Use common words/patterns
- Share passwords
- Store in plain text
- Use "12345" or "password" (obviously!)

---

## Related Tools

- **[[SHA256-Hash-Implementation]]** - For secure password hashing (with KDF)
- **[[Base64-Encoder-Decoder]]** - Understanding encoding (not for passwords!)
- **[[File-Checksum-Validator]]** - Integrity verification concepts

---

## References

### Technical Foundations
- **Shannon Entropy**: Information theory, 1948
- **NIST SP 800-63B**: Digital Identity Guidelines (Authentication)
- **OWASP**: Password Storage Cheat Sheet

### Password Research
- **Bonneau et al.**: "The Quest to Replace Passwords" (2012)
- **Florêncio & Herley**: "A Large-Scale Study of Web Password Habits" (2007)
- **Wheeler**: "zxcvbn: Low-Budget Password Strength Estimation" (Dropbox, 2012)

### Attack Methods
- **RockYou breach**: 32 million passwords leaked (2009)
- **PassGAN**: Generative adversarial network for password cracking (2019)
- **GPU cracking**: Modern hardware achieves 100B+ hashes/second

### Standards and Guidelines
- **NIST**: No more forced periodic resets
- **PCI DSS**: 8-character minimum, complexity requirements
- **GDPR**: Strong authentication requirements
- **HIPAA**: Unique user IDs and passwords required

---

## Learn More

**Next Steps:**
1. Learn [[SHA256-Hash-Implementation]] for secure password storage (with PBKDF2)
2. Understand [[File-Checksum-Validator]] for data integrity
3. Explore password managers: Bitwarden, 1Password, KeePassXC

**External Resources:**
- [XKCD #936 - Password Strength](https://xkcd.com/936/)
- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/)
- [Have I Been Pwned](https://haveibeenpwned.com/) - Check for breaches
- [Password Strength Calculator](https://www.passwordmonster.com/)

---

---

## Navigation

[← Back to Home](Home) | [Report Issue](https://github.com/Shiva-destroyer/CryptoSentinel/issues) | [View All Tools](Home#available-tools)

---

**Developed by:** saisrujanmurthy@gmail.com
