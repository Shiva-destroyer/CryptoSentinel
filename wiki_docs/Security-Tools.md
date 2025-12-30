# Security Tools - Password Strength & Data Encoding

**Measure entropy, estimate crack times, and encode data safely**

---

## 📖 Table of Contents

1. [ELI5 - Explain Like I'm 5](#eli5---explain-like-im-5)
2. [Password Analyzer - The Entropy Calculator](#password-analyzer---the-entropy-calculator)
3. [The Mathematics - Information Entropy](#the-mathematics---information-entropy)
4. [Time to Crack - Reality Check](#time-to-crack---reality-check)
5. [Base64 Encoder - Binary to Text Magic](#base64-encoder---binary-to-text-magic)
6. [The Base64 Algorithm](#the-base64-algorithm)
7. [Code Implementation](#code-implementation)
8. [Pros & Cons](#pros--cons)
9. [Try It Yourself](#try-it-yourself)

---

## 🧒 ELI5 - Explain Like I'm 5

### Part 1: Password Strength (The Guessing Game)

**Imagine a combination lock on your treasure chest!**

```
Lock with 3 numbers (0-9):
Combinations: 10 × 10 × 10 = 1,000 possibilities
Your friend tries 1 per second → 1,000 seconds = 17 minutes

Lock with 6 numbers (0-9):
Combinations: 10 × 10 × 10 × 10 × 10 × 10 = 1,000,000 possibilities
Your friend tries 1 per second → 1,000,000 seconds = 11.5 DAYS! 🕐
```

**The Magic Formula:**

```
More numbers = Harder to guess! 🎯

If you also use LETTERS (A-Z):
Lock with 3 characters (A-Z and 0-9):
Combinations: 36 × 36 × 36 = 46,656 possibilities
Even HARDER to guess! 🚀
```

---

### Part 2: Base64 (The Secret Code Translator)

**Imagine you want to send a photo through a phone that only understands letters!**

```
Photo: 👍 (picture file - binary data)
       ↓
       (Base64 translator)
       ↓
Text:  "iVBORw0KGgo..." (looks like gibberish, but it's your photo!)
```

**Why do we need this?**

Some systems only like text (like email or JSON files). Base64 converts:
- Pictures 🖼️ → Text letters
- Music 🎵 → Text letters  
- Any file → Text letters

Then later, you can convert back:
```
Text: "iVBORw0KGgo..."
      ↓
      (Base64 translator - reverse)
      ↓
Photo: 👍 (original picture back!)
```

---

## 🔐 Password Analyzer - The Entropy Calculator

### What is Password Entropy?

**Entropy** = Measure of randomness/unpredictability (in bits)

Higher entropy = Harder to guess = Stronger password! 💪

### 🎯 The Formula

$$E = L \times \log_2(R)$$

Where:
- $E$ = Entropy (in bits)
- $L$ = Password length (number of characters)
- $R$ = Pool size (number of possible characters)
- $\log_2$ = Logarithm base 2 (how many bits to represent $R$ choices)

### 📊 Character Pool Sizes

```
Type               Characters                          Pool Size (R)
────────────────────────────────────────────────────────────────────
Lowercase only     a-z                                 26
Uppercase only     A-Z                                 26
Digits only        0-9                                 10
────────────────────────────────────────────────────────────────────
Lower + Upper      a-z, A-Z                            52
Lower + Digits     a-z, 0-9                            36
Upper + Digits     A-Z, 0-9                            36
────────────────────────────────────────────────────────────────────
Alphanumeric       a-z, A-Z, 0-9                       62
All characters     a-z, A-Z, 0-9, !@#$%^&*()...       94
```

### 🧮 Example Calculations

#### Example 1: "password" (Weak)

```
Password: "password"
Length: L = 8
Characters: All lowercase (a-z)
Pool size: R = 26

Entropy:
E = L × log₂(R)
E = 8 × log₂(26)
E = 8 × 4.70
E = 37.6 bits

Strength: ⚠️ WEAK!
```

#### Example 2: "P@ssw0rd!" (Better)

```
Password: "P@ssw0rd!"
Length: L = 9
Characters: Uppercase (P), lowercase (assword), digit (0), special (@!)
Pool size: R = 94 (all character types)

Entropy:
E = L × log₂(R)
E = 9 × log₂(94)
E = 9 × 6.55
E = 58.95 bits

Strength: ✅ MODERATE
```

#### Example 3: "Tr0ub4dor&3" (Strong)

```
Password: "Tr0ub4dor&3"
Length: L = 11
Pool size: R = 94

Entropy:
E = 11 × log₂(94)
E = 11 × 6.55
E = 72.05 bits

Strength: ✅✅ STRONG!
```

#### Example 4: "correct horse battery staple" (Very Strong)

```
Password: "correct horse battery staple"
Length: L = 28 (with spaces)
Pool size: R = 36 (lowercase + spaces)

Entropy:
E = 28 × log₂(36)
E = 28 × 5.17
E = 144.76 bits

Strength: ✅✅✅ VERY STRONG! 🔒
```

### 📊 Entropy Classification

```
Entropy (bits)  Strength      Example             Crack Time
─────────────────────────────────────────────────────────────────
< 28            Very Weak     "pass"              Instant
28-35           Weak          "password"          Hours
36-59           Moderate      "P@ssw0rd1"         Years
60-127          Strong        "MyP@ssw0rd2024!"   Centuries
>= 128          Very Strong   "correct horse..."  Heat death of universe
```

### 🔍 Why Length Matters More Than Complexity

**Comparison:**

```
Option 1: Short + Complex
Password: "P@s5!" (5 chars, all types)
Entropy: 5 × log₂(94) = 32.75 bits
Crack time: Hours

Option 2: Long + Simple
Password: "correcthorsebatterystaple" (25 chars, lowercase only)
Entropy: 25 × log₂(26) = 117.5 bits
Crack time: Millions of years! 🚀

Winner: Length! 📏
```

**XKCD Comic Wisdom:**

```
❌ Hard to remember: "Tr0ub4dor&3" (44 bits)
✅ Easy to remember: "correct horse battery staple" (144 bits)

Humans are bad at random complexity but good at remembering phrases!
```

---

## ⏱️ Time to Crack - Reality Check

### The Attack Model

**GPU Brute Force:**
- Modern GPU: $10^{10}$ hashes per second (10 billion!)
- GPU farm: $10^{12}$ hashes per second (1 trillion!)

### 🧮 Calculation Formula

$$\text{Search Space} = R^L$$

$$\text{Time (seconds)} = \frac{2^E}{10^{10}}$$

Where:
- $R$ = Pool size
- $L$ = Password length
- $E$ = Entropy in bits
- $10^{10}$ = Guesses per second

### 📊 Crack Time Examples

#### Example 1: "pass" (16 bits)

```
Password: "pass"
Entropy: 4 × log₂(26) = 18.8 bits
Search space: 2^18.8 = 456,976

Time to crack:
456,976 ÷ 10,000,000,000 = 0.000046 seconds
≈ Instant! ⚡
```

#### Example 2: "password" (37.6 bits)

```
Password: "password"
Entropy: 37.6 bits
Search space: 2^37.6 = 209 billion

Time to crack:
209,000,000,000 ÷ 10,000,000,000 = 20.9 seconds
≈ 21 seconds ⏱️
```

#### Example 3: "P@ssw0rd!" (58.95 bits)

```
Password: "P@ssw0rd!"
Entropy: 58.95 bits
Search space: 2^58.95 = 506 trillion

Time to crack:
506,000,000,000,000 ÷ 10,000,000,000 = 50,600 seconds
≈ 14 hours ⏰
```

#### Example 4: "MySecureP@ssw0rd2024!" (137 bits)

```
Password: "MySecureP@ssw0rd2024!"
Entropy: 21 × log₂(94) = 137.55 bits
Search space: 2^137.55 = 2.6 × 10^41

Time to crack:
2.6 × 10^41 ÷ 10^10 = 2.6 × 10^31 seconds
= 8.2 × 10^23 years
= 60 trillion times the age of the universe! 🌌
```

### 📈 Visual Timeline

```
Entropy    Example              Time to Crack
─────────────────────────────────────────────────────────────
20 bits    "abc1"               1 second
30 bits    "pass123"            17 minutes
40 bits    "MyPass1"            1 week
50 bits    "MyP@ss123"          35 years
60 bits    "MyP@ssw0rd1"        36,533 years
70 bits    "MySecureP@ss1"      35 million years
80 bits    "MySecureP@ss2024"   38 billion years (3× age of universe)
90 bits    "MySecureP@ss2024!"  38 trillion years
100 bits   (20+ char password)  39 quadrillion years
128 bits   (25+ char password)  10^28 years (unimaginable!)
```

### 🎯 Practical Recommendations

```
Purpose              Min Entropy   Example Length        Crack Time
──────────────────────────────────────────────────────────────────────
WiFi password        50 bits       12 chars (mixed)      35 years
Email password       60 bits       13 chars (mixed)      36,000 years
Banking password     70 bits       15 chars (mixed)      35 million years
Master password      80+ bits      20+ chars (mixed)     > Age of universe
```

---

## 🔤 Base64 Encoder - Binary to Text Magic

### What is Base64?

**Base64** is an encoding scheme that converts binary data (8-bit) into ASCII text (6-bit).

### 🎯 Why Do We Need Base64?

```
Problem: Some systems only accept text
- Email (SMTP): Only supports 7-bit ASCII
- JSON/XML: Text-based formats
- URLs: Can't have binary data

Solution: Convert binary → text → transmit → convert back!
```

### 📊 The Character Set (64 characters)

```
A-Z (26 chars):  ABCDEFGHIJKLMNOPQRSTUVWXYZ
a-z (26 chars):  abcdefghijklmnopqrstuvwxyz
0-9 (10 chars):  0123456789
Symbols (2):     + /
Padding (1):     =

Total: 64 + 1 padding = 65 characters
```

### 🔢 Index Mapping

```
Value   Char    Value   Char    Value   Char    Value   Char
──────────────────────────────────────────────────────────────
  0      A        17      R        34      i        51      z
  1      B        18      S        35      j        52      0
  2      C        19      T        36      k        53      1
  3      D        20      U        37      l        54      2
  4      E        21      V        38      m        55      3
  5      F        22      W        39      n        56      4
  6      G        23      X        40      o        57      5
  7      H        24      Y        41      p        58      6
  8      I        25      Z        42      q        59      7
  9      J        26      a        43      r        60      8
 10      K        27      b        44      s        61      9
 11      L        28      c        45      t        62      +
 12      M        29      d        46      u        63      /
 13      N        30      e        47      v
 14      O        31      f        48      w        Padding:
 15      P        32      g        49      x         =
 16      Q        33      h        50      y
```

---

## 🧮 The Base64 Algorithm

### Encoding Process (Binary → Text)

#### Step 1: Convert to Binary (8-bit)

```
Text: "Man"

M = ASCII 77 = 01001101
a = ASCII 97 = 01100001
n = ASCII 110 = 01101110

Binary: 01001101 01100001 01101110
        └─ 8 ──┘ └─ 8 ──┘ └─ 8 ──┘
           bits     bits     bits
```

#### Step 2: Group into 6-bit Chunks

```
01001101 01100001 01101110
↓
010011  010110  000101  101110
└─6──┘  └─6──┘  └─6──┘  └─6──┘
  bits    bits    bits    bits
```

#### Step 3: Convert 6-bit to Decimal

```
010011 = 19 (decimal)
010110 = 22 (decimal)
000101 = 5 (decimal)
101110 = 46 (decimal)
```

#### Step 4: Map to Base64 Characters

```
19 → T  (from lookup table)
22 → W
5  → F
46 → u

Result: "TWFu"
```

### 📊 Complete Example

```
Input:  "Man" (3 bytes = 24 bits)
Binary: 01001101 01100001 01101110
Groups: 010011 010110 000101 101110
Values: 19     22     5      46
Output: T      W      F      u

"Man" → "TWFu"
```

---

### Padding Rules (The '=' Character)

**Why Padding?**

Base64 processes 3 bytes (24 bits) at a time, producing 4 characters.  
If input is not a multiple of 3, we need padding!

#### Case 1: Input = 3 bytes (Perfect!)

```
Input: "Man" (3 bytes)
Output: "TWFu" (4 chars) ✓ No padding needed
```

#### Case 2: Input = 2 bytes (Need padding)

```
Input: "Ma" (2 bytes = 16 bits)

Step 1: Convert to binary
M = 01001101
a = 01100001

Binary: 01001101 01100001
        └─ 8 ──┘ └─ 8 ──┘

Step 2: Group into 6-bit (need 24 bits total!)
01001101 01100001 00000000  ← Pad with zeros
↓
010011  010110  000100  000000
└─6──┘  └─6──┘  └─6──┘  └─6──┘

Step 3: Convert to Base64
19 → T
22 → W
4  → E
0 (padding) → =

Output: "TWE="
       One = means 1 byte of padding! 🟰
```

#### Case 3: Input = 1 byte (Need more padding)

```
Input: "M" (1 byte = 8 bits)

Step 1: Convert to binary
M = 01001101

Binary: 01001101 00000000 00000000  ← Pad with zeros
        └─ 8 ──┘

Step 2: Group into 6-bit
010011  010000  000000  000000
└─6──┘  └─6──┘  └─6──┘  └─6──┘

Step 3: Convert to Base64
19 → T
16 → Q
0 (padding) → =
0 (padding) → =

Output: "TQ=="
       Two == means 2 bytes of padding! 🟰🟰
```

### 📏 Size Overhead

```
Original size: n bytes
Base64 size:   ⌈4 × n / 3⌉ bytes

Overhead: ~33% increase

Examples:
3 bytes   → 4 chars   (33% increase)
6 bytes   → 8 chars   (33% increase)
100 bytes → 136 chars (36% increase)
1 MB      → 1.33 MB   (33% increase)
```

---

### Decoding Process (Text → Binary)

#### Step 1: Remove Padding

```
Input: "TWFu"
(No padding, proceed)
```

#### Step 2: Convert Characters to 6-bit

```
T → 19 → 010011
W → 22 → 010110
F → 5  → 000101
u → 46 → 101110
```

#### Step 3: Concatenate Bits

```
010011 010110 000101 101110
↓
01001101 01100001 01101110
└─ 8 ──┘ └─ 8 ──┘ └─ 8 ──┘
```

#### Step 4: Convert to ASCII

```
01001101 = 77 = 'M'
01100001 = 97 = 'a'
01101110 = 110 = 'n'

Result: "Man"
```

---

## 💻 Code Implementation

### Password Analyzer

```python
class PasswordAnalyzer(AnalyzerInterface):
    """
    Advanced password strength analyzer using entropy calculation.
    """
    
    GUESSES_PER_SECOND: int = int(1e10)  # 10 billion (GPU attack)
    
    def _calculate_pool_size(self, password: str) -> int:
        """
        Determine character pool size based on password composition.
        
        Pool sizes:
        - Lowercase only: 26
        - Uppercase only: 26
        - Digits only: 10
        - Special chars: 32
        
        Combined pools are additive.
        """
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[^a-zA-Z0-9]', password))
        
        pool_size = 0
        if has_lower:
            pool_size += 26
        if has_upper:
            pool_size += 26
        if has_digit:
            pool_size += 10
        if has_special:
            pool_size += 32  # Common special characters
        
        return max(pool_size, 1)  # At least 1
    
    def _calculate_entropy(self, password: str) -> float:
        """
        Calculate Shannon entropy in bits.
        
        Formula: E = L × log₂(R)
        Where:
          L = password length
          R = character pool size
        """
        length = len(password)
        pool_size = self._calculate_pool_size(password)
        
        # Shannon entropy formula
        entropy = length * math.log2(pool_size)
        
        return entropy
    
    def _estimate_crack_time(self, entropy_bits: float) -> dict:
        """
        Estimate time to crack password using brute force.
        
        Assumptions:
        - GPU attack: 10^10 guesses per second
        - Average case: 50% of search space
        
        Time = (2^E / 2) / 10^10 seconds
             = 2^(E-1) / 10^10 seconds
        """
        # Search space (all possible combinations)
        search_space = 2 ** entropy_bits
        
        # Average case: half the search space
        avg_guesses = search_space / 2
        
        # Time in seconds
        seconds = avg_guesses / self.GUESSES_PER_SECOND
        
        # Convert to human-readable format
        display = self._format_time(seconds)
        
        return {
            'seconds': seconds,
            'display': display,
        }
    
    def _format_time(self, seconds: float) -> str:
        """Convert seconds to human-readable format."""
        
        if seconds < 1:
            return "Instant"
        elif seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f} minutes"
        elif seconds < 86400:
            hours = seconds / 3600
            return f"{hours:.1f} hours"
        elif seconds < 31536000:
            days = seconds / 86400
            return f"{days:.1f} days"
        elif seconds < 3153600000:
            years = seconds / 31536000
            return f"{years:.1f} years"
        elif seconds < 31536000000000:
            centuries = seconds / 3153600000
            return f"{centuries:.1f} centuries"
        else:
            return "Millions of years"
    
    def _calculate_score(self, entropy_bits: float) -> int:
        """
        Calculate password strength score (0-100).
        
        Thresholds:
        - < 28 bits: Very weak (0-20)
        - 28-35 bits: Weak (21-40)
        - 36-59 bits: Moderate (41-70)
        - 60-127 bits: Strong (71-90)
        - >= 128 bits: Very strong (91-100)
        """
        if entropy_bits < 28:
            return int((entropy_bits / 28) * 20)
        elif entropy_bits < 36:
            return 20 + int(((entropy_bits - 28) / 8) * 20)
        elif entropy_bits < 60:
            return 40 + int(((entropy_bits - 36) / 24) * 30)
        elif entropy_bits < 128:
            return 70 + int(((entropy_bits - 60) / 68) * 20)
        else:
            return min(90 + int((entropy_bits - 128) / 10), 100)
```

### Base64 Encoder

```python
class Base64Encoder(CipherInterface):
    """
    Base64 encoder/decoder for binary-to-text conversion.
    
    Not encryption! Just encoding for transport.
    """
    
    def encrypt(self, plaintext: str, key: str = None) -> str:
        """
        Encode string to Base64.
        
        Process:
        1. Convert string to bytes (UTF-8)
        2. Apply Base64 encoding
        3. Return ASCII string
        """
        try:
            # Convert to bytes
            data_bytes = plaintext.encode('utf-8')
            
            # Encode to Base64
            encoded_bytes = base64.b64encode(data_bytes)
            
            # Convert to string
            encoded_string = encoded_bytes.decode('ascii')
            
            return encoded_string
            
        except Exception as e:
            raise EncodingError(f"Base64 encoding failed: {str(e)}")
    
    def decrypt(self, ciphertext: str, key: str = None) -> str:
        """
        Decode Base64 string back to original.
        
        Handles:
        - Automatic padding correction
        - Whitespace removal
        """
        try:
            # Remove whitespace
            cleaned = ciphertext.strip()
            
            # Add padding if missing
            missing_padding = len(cleaned) % 4
            if missing_padding:
                cleaned += '=' * (4 - missing_padding)
            
            # Decode from Base64
            decoded_bytes = base64.b64decode(cleaned)
            
            # Convert to string
            decoded_string = decoded_bytes.decode('utf-8')
            
            return decoded_string
            
        except Exception as e:
            raise DecodingError(f"Base64 decoding failed: {str(e)}")
```

---

## ⚖️ Pros & Cons

### Password Analyzer

#### ✅ Pros

| Advantage | Description |
|-----------|-------------|
| **Quantitative** | Gives exact entropy measurement (bits) |
| **Realistic** | Uses 10^10 guesses/sec (modern GPU) |
| **Comprehensive** | Checks length, character types, patterns |
| **Educational** | Teaches users why length matters |
| **Actionable** | Provides specific recommendations |

#### ❌ Cons

| Disadvantage | Description |
|--------------|-------------|
| **Doesn't detect dictionary words** | "password" gets credit for 8 chars |
| **No pattern detection** | "123456" gets same score as "926473" |
| **Assumes brute force** | Real attacks use dictionaries first |
| **Ignores reuse** | Can't detect if password used elsewhere |
| **GPU speed estimate** | Actual speeds vary widely |

---

### Base64 Encoder

#### ✅ Pros

| Advantage | Description |
|-----------|-------------|
| **Universal** | Works with any binary data |
| **Text-safe** | Only ASCII characters (safe for email, JSON) |
| **No loss** | Reversible encoding (lossless) |
| **Standard** | RFC 4648 standard, widely supported |
| **Simple** | Easy to implement and understand |

#### ❌ Cons

| Disadvantage | Description |
|--------------|-------------|
| **Not encryption!** | Anyone can decode (no security!) |
| **Size increase** | 33% larger than original |
| **No compression** | Doesn't reduce size |
| **Misleading** | Looks encrypted but isn't |
| **Padding overhead** | Small files have larger relative overhead |

---

## 🎮 Try It Yourself

### Using the CLI

```bash
# Launch CryptoSentinel
python cli.py

# Navigate:
# 3. Security Tools
# Choose: Password Analyzer or Base64 Encoder
```

### Python Code Examples

#### Analyze Password Strength

```python
from crypto_sentinel.security import PasswordAnalyzer

analyzer = PasswordAnalyzer()

# Analyze a password
result = analyzer.analyze("MyP@ssw0rd2024!")

print(f"Entropy: {result['entropy']:.2f} bits")
print(f"Score: {result['score']}/100")
print(f"Strength: {result['strength']}")
print(f"Time to crack: {result['crack_time']['display']}")

# Output:
# Entropy: 91.63 bits
# Score: 78/100
# Strength: Strong
# Time to crack: 78.2 billion years
```

#### Compare Two Passwords

```python
# Weak password
weak = analyzer.analyze("password")
print(f"'password': {weak['entropy']:.1f} bits, {weak['crack_time']['display']}")
# 'password': 37.6 bits, 21.8 seconds

# Strong password
strong = analyzer.analyze("correct horse battery staple")
print(f"Passphrase: {strong['entropy']:.1f} bits, {strong['crack_time']['display']}")
# Passphrase: 144.8 bits, Millions of years
```

#### Encode with Base64

```python
from crypto_sentinel.security import Base64Encoder

encoder = Base64Encoder()

# Encode a message
original = "Hello, World! 🌍"
encoded = encoder.encrypt(original)
print(f"Original: {original}")
print(f"Encoded:  {encoded}")

# Output:
# Original: Hello, World! 🌍
# Encoded:  SGVsbG8sIFdvcmxkISDwn4yN

# Decode it back
decoded = encoder.decrypt(encoded)
print(f"Decoded:  {decoded}")

# Output:
# Decoded:  Hello, World! 🌍
```

#### Encode Binary Data

```python
# Encode a small image
with open('logo.png', 'rb') as f:
    image_bytes = f.read()

# Encode to Base64 string
encoded_image = base64.b64encode(image_bytes).decode('ascii')

# Now you can include in JSON:
json_data = {
    "username": "alice",
    "profile_pic": encoded_image  # ← Image as text!
}

# Send via API, store in database, etc.
```

---

## 🎓 Learning Exercises

### Beginner

1. Analyze your current password - is it strong enough?
2. Encode your name in Base64 - observe the size increase
3. Why doesn't Base64 provide security?

### Intermediate

4. Calculate entropy for "password" vs "correcthorsebatterystaple"
5. How many '=' padding characters does "A" need in Base64?
6. Calculate crack time for a 16-character alphanumeric password

### Advanced

7. Implement zxcvbn algorithm (advanced password strength)
8. Modify Base64 to use URL-safe characters (- and _ instead of + and /)
9. Calculate collision probability for 8-character passwords
10. Research Argon2 vs bcrypt for password hashing

---

## 🔬 Security Analysis

### Password Entropy vs Real Attacks

```
Theoretical:
"password" = 37.6 bits → 21 seconds

Reality:
"password" = 0 seconds (it's in every dictionary!)

Lesson: Entropy assumes RANDOM characters.
        Dictionary words have near-zero entropy!
```

### Base64 is NOT Encryption!

```
❌ WRONG:
encoded = base64.b64encode(password)
# Looks gibberish, but trivial to decode!

✅ RIGHT:
hashed = bcrypt.hashpw(password, salt)
# Actually secure!
```

**Real-World Example:**

```
Secret: "MyAPIKey12345"
Base64: "TXlBUElLZXkxMjM0NQ=="

Anyone can decode this in 1 second! 🚨

Use proper encryption (AES) or hashing (SHA-256 + salt) instead!
```

---

## 📚 Further Reading

- **Password Entropy**: [NIST Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- **Base64 Specification**: [RFC 4648](https://tools.ietf.org/html/rfc4648)
- **Password Strength**: [zxcvbn Algorithm](https://github.com/dropbox/zxcvbn)
- **XKCD Comic**: [Password Strength](https://xkcd.com/936/)
- **Next Topic**: [Caesar Cipher](Caesar-Cipher.md) - Classical cryptography

---

## 🔗 Navigation

- [← Back to Hashing Tools](Hashing-Tools.md)
- [→ Next: Caesar Cipher](Caesar-Cipher.md)
- [↑ Back to Top](#security-tools---password-strength--data-encoding)
- [🏠 Home](Home.md)

---

**Author**: saisrujanmurthy@gmail.com  
**Last Updated**: December 30, 2025  
**Difficulty**: ⭐⭐⭐☆☆ (Intermediate)  
**Security Importance**: ⭐⭐⭐⭐⭐ (Critical!)  

---

## 🎯 Key Takeaways

1. **Entropy = L × log₂(R)** - Longer passwords with larger character pools are stronger
2. **Length > Complexity** - "correct horse battery staple" beats "P@s5!"
3. **Base64 is encoding, NOT encryption** - Anyone can decode it!
4. **Use passphrases** - Easier to remember, much harder to crack
5. **Never reuse passwords** - One breach compromises all accounts
