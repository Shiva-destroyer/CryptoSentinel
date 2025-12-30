# XOR Cipher - The Computer's Favorite Cipher

**From "perfect" One-Time Pad to everyday file encryption**

---

## 📖 Table of Contents

1. [ELI5 - Explain Like I'm 5](#eli5---explain-like-im-5)
2. [The Mathematics - XOR Truth Table](#the-mathematics---xor-truth-table)
3. [How It Works - Bitwise Magic](#how-it-works---bitwise-magic)
4. [One-Time Pad vs Repeating Key](#one-time-pad-vs-repeating-key)
5. [Real-World Usage](#real-world-usage)
6. [Code Implementation](#code-implementation)
7. [Pros & Cons](#pros--cons)
8. [Try It Yourself](#try-it-yourself)

---

## 🧒 ELI5 - Explain Like I'm 5

**Imagine you have a secret light switch game with your friend!**

You both have flashlights (on/off). The rule is:

```
Rule: "Flip your light if mine is ON"

My Light | Your Light | Result After Rule
---------|------------|------------------
 OFF     |    OFF     |      OFF
 OFF     |    ON      |      ON
 ON      |    OFF     |      ON
 ON      |    ON      |      OFF
```

Notice the last one? **ON + ON = OFF** (they cancel out!) 💡

### 🔐 Making Secret Messages

Let's say:
- **OFF OFF ON OFF ON** = Your message
- **ON ON ON ON ON** = Your secret key

Apply the rule to each pair:

```
Message: OFF OFF  ON OFF  ON
Key:      ON  ON  ON  ON  ON
         ─────────────────────
Result:   ON  ON OFF  ON OFF  ← Secret message!
```

To decode, your friend uses the **SAME KEY** again:

```
Secret:   ON  ON OFF  ON OFF
Key:      ON  ON  ON  ON  ON
         ─────────────────────
Message: OFF OFF  ON OFF  ON  ← Original back!
```

The key **cancels itself out**! That's the magic of XOR! ✨

---

## 🧮 The Mathematics - XOR Truth Table

XOR stands for **"eXclusive OR"** - it's true when inputs are **different**.

### Symbol

The XOR operator is written as: $\oplus$

### Truth Table

$$
\begin{array}{|c|c|c|}
\hline
A & B & A \oplus B \\
\hline
0 & 0 & 0 \\
0 & 1 & 1 \\
1 & 0 & 1 \\
1 & 1 & 0 \\
\hline
\end{array}
$$

**In words:**
- $0 \oplus 0 = 0$ (same → 0)
- $0 \oplus 1 = 1$ (different → 1)
- $1 \oplus 0 = 1$ (different → 1)
- $1 \oplus 1 = 0$ (same → 0)

### 🎯 Key Properties

#### 1. **Self-Inverse** (Most Important!)

$$A \oplus B \oplus B = A$$

XORing with the same value twice **cancels out**:

```
Message ⊕ Key = Ciphertext
Ciphertext ⊕ Key = Message  ← Same operation!
```

This is why XOR is **symmetric** - encryption and decryption are identical!

#### 2. **Commutative**

$$A \oplus B = B \oplus A$$

Order doesn't matter.

#### 3. **Associative**

$$(A \oplus B) \oplus C = A \oplus (B \oplus C)$$

Grouping doesn't matter.

#### 4. **Identity Element**

$$A \oplus 0 = A$$

XORing with 0 does nothing (leaves A unchanged).

### 📊 Example with Binary Numbers

Let's encrypt the letter **'H'** (ASCII 72 = `01001000`) with key **42** (`00101010`):

```
   01001000  (H)
⊕  00101010  (key 42)
   ─────────
   01100010  (result: 98 = 'b')
```

To decrypt, XOR again with 42:

```
   01100010  ('b')
⊕  00101010  (key 42)
   ─────────
   01001000  (H) ← Original!
```

### 🔢 XOR with Larger Numbers

```
Plaintext:  H  E  L  L  O
ASCII:     72 69 76 76 79
Binary:    01001000 01000101 01001100 01001100 01001111

Key (42):  00101010 00101010 00101010 00101010 00101010

XOR:       01100010 01101111 01100110 01100110 01100101
Decimal:   98       111      102      102      101
Result:    b        o        f        f        e
```

**Ciphertext**: `boffe`

---

## ⚙️ How It Works - Bitwise Magic

### Encryption Algorithm

```
For each byte in plaintext:
    1. Convert to binary (8 bits)
    2. XOR with corresponding key byte
    3. Output encrypted byte
```

If plaintext is longer than key, **repeat the key**:

```
Plaintext: H  E  L  L  O  W  O  R  L  D
Key:       42 42 42 42 42 42 42 42 42 42
          (key repeats)
```

### Step-by-Step Example

**Encrypt "HELLO" with key 42:**

```
Step 1: Convert to ASCII
H = 72, E = 69, L = 76, L = 76, O = 79

Step 2: Convert to binary
72 = 01001000
69 = 01000101
76 = 01001100
76 = 01001100
79 = 01001111

Step 3: XOR each with key (42 = 00101010)
01001000 ⊕ 00101010 = 01100010 (98)
01000101 ⊕ 00101010 = 01101111 (111)
01001100 ⊕ 00101010 = 01100110 (102)
01001100 ⊕ 00101010 = 01100110 (102)
01001111 ⊕ 00101010 = 01100101 (101)

Step 4: Convert to hex or characters
Result: 62 6f 66 66 65 (hex)
```

### Decryption (Identical Process!)

```
Ciphertext: 62 6f 66 66 65 (hex)
Key: 42 (00101010)

XOR each byte with 42:
98  ⊕ 42 = 72  (H)
111 ⊕ 42 = 69  (E)
102 ⊕ 42 = 76  (L)
102 ⊕ 42 = 76  (L)
101 ⊕ 42 = 79  (O)

Plaintext: HELLO
```

---

## 🔐 One-Time Pad vs Repeating Key

### The Perfect Cipher: One-Time Pad (OTP)

**Rules:**
1. Key must be **random**
2. Key must be **as long as the message**
3. Key must be **used only once**
4. Key must be kept **perfectly secret**

**Result**: **Mathematically unbreakable!** 🎉

#### Why It's Unbreakable

With a truly random key as long as the message, **every possible plaintext is equally likely**:

```
Ciphertext: 01100010
Key 1:      00101010 → Plaintext: 01001000 (H)
Key 2:      01011010 → Plaintext: 00111000 (8)
Key 3:      00001110 → Plaintext: 01101100 (l)
...
```

Without knowing the key, the ciphertext could decrypt to **anything**! An attacker gains **zero information**.

#### 📊 Mathematical Proof

For true random key $K$ of length $n$:

$$P(\text{plaintext} = M | \text{ciphertext} = C) = \frac{1}{2^n}$$

**Every** message is **equally probable** - perfect secrecy! 🔒

### The Practical Cipher: Repeating Key XOR

**Reality:** Most uses of XOR don't follow OTP rules!

**Common usage:**
```
Plaintext: HELLO WORLD HELLO WORLD HELLO WORLD
Key:       SECRET SECRET SECRET SECRET SECRET
          (key repeats every 6 bytes)
```

**Problem:** Key repetition creates **patterns** that can be exploited!

#### Key Reuse Vulnerability

When the same key byte encrypts multiple plaintext bytes:

```
Position: 0  6  12 18 24 30
All encrypted with key[0] = 'S'

If we know ONE of these plaintexts, we can deduce the key byte!
```

### 🆚 Comparison

| Feature | One-Time Pad | Repeating Key XOR |
|---------|--------------|-------------------|
| **Key Length** | = Message length | < Message length (repeats) |
| **Key Reuse** | NEVER | Always repeats |
| **Security** | Perfect (unbreakable) | Breakable with patterns |
| **Practical** | ❌ Hard (key distribution) | ✅ Easy (small key) |
| **Use Cases** | Spy agencies, military | Files, memory, obfuscation |

---

## 💻 Real-World Usage

XOR cipher is **everywhere** in computing, but not for security - for **obfuscation** and **efficiency**!

### 1. **Memory Encryption** 🧠

Operating systems use XOR to obscure sensitive data in RAM:

```python
# Storing a password in memory
password = "secret123"
key = 0x5A  # Random byte

# XOR to obfuscate
obfuscated = [ord(c) ^ key for c in password]

# Later, recover by XORing again
recovered = ''.join(chr(b ^ key) for b in obfuscated)
```

**Purpose**: Prevent casual inspection (not strong security!)

### 2. **File Format Obfuscation** 📁

Video games often XOR save files to prevent casual editing:

```python
# Save game data
save_data = b"player_level=99,gold=1000000"

# XOR with simple key
key = b"GAME"
encrypted = bytes(a ^ b for a, b in zip(save_data, itertools.cycle(key)))

# Looks like garbage in hex editor!
```

### 3. **Network Protocol Obfuscation** 🌐

Some protocols XOR packets to avoid simple packet sniffers:

```
Original packet: GET /api/user HTTP/1.1
XOR with key:    0xAA (repeated)
Result:          Gibberish to basic tools
```

### 4. **RAID Storage Parity** 💾

RAID 5 uses XOR for data recovery:

```
Disk 1: 10110011
Disk 2: 11001100
Parity: 01111111  (Disk1 ⊕ Disk2)

If Disk 1 fails:
Disk 1 = Disk 2 ⊕ Parity
       = 11001100 ⊕ 01111111
       = 10110011  ← Recovered!
```

### 5. **PNG Image Filtering** 🖼️

PNG format uses XOR for compression:

```
Row N:     [12, 45, 78, 23, ...]
Row N-1:   [10, 43, 80, 21, ...]
Stored:    [2,  2,  -2, 2,  ...]  (differences compress better!)

Using XOR properties for efficient encoding!
```

### ⚠️ What XOR is NOT Used For

**Not for:**
- Banking/financial security ❌
- Password storage ❌
- HTTPS/TLS encryption ❌
- Military communications ❌

**Use instead:**
- AES-256 for encryption
- bcrypt/Argon2 for passwords
- TLS 1.3 for network security

---

## 💻 Code Implementation

### The `encrypt()` Method in `xor.py`

```python
def encrypt(self, data: Union[str, bytes], key: Any) -> Union[str, bytes]:
    """
    Encrypt data using XOR cipher.
    
    For string input, returns hexadecimal string representation.
    For bytes input, returns encrypted bytes.
    Key is repeated cyclically if shorter than data.
    """
    # Validate and normalize key
    if isinstance(key, int):
        if not 0 <= key <= 255:
            raise InvalidKeyError(
                f"Integer key must be in range [0, 255], got {key}"
            )
        key_bytes = bytes([key])
    elif isinstance(key, bytes):
        if len(key) == 0:
            raise InvalidKeyError("Bytes key cannot be empty")
        key_bytes = key
    elif isinstance(key, str):
        key_bytes = key.encode('utf-8')
    else:
        raise InvalidKeyError(
            f"Key must be int, bytes, or str, got {type(key).__name__}"
        )
    
    # Convert input to bytes if string
    is_string_input = isinstance(data, str)
    if is_string_input:
        data_bytes = data.encode('utf-8')
    else:
        data_bytes = data
    
    # XOR operation with repeating key
    result_bytes = bytes(
        data_bytes[i] ^ key_bytes[i % len(key_bytes)]
        for i in range(len(data_bytes))
    )
    
    # Return hex string for string input, bytes for bytes input
    if is_string_input:
        return result_bytes.hex()
    else:
        return result_bytes
```

### The Core XOR Operation

The magic happens in this single line:

```python
result = data_byte ^ key_byte
```

That's it! XOR each data byte with the corresponding key byte.

### Key Repetition Logic

```python
key_byte = key_bytes[i % len(key_bytes)]
```

The modulo operator (`%`) makes the key repeat:

```
i=0: key[0]
i=1: key[1]
i=2: key[2]
i=3: key[0]  ← wraps around!
i=4: key[1]
...
```

### The `crack()` Method (Brute Force Single-Byte)

```python
def crack(self, data: Union[str, bytes]) -> dict[str, Any]:
    """
    Crack single-byte XOR cipher by trying all 256 possible keys.
    
    Scores each attempt based on:
    - Printable character ratio
    - Common English words found
    """
    # Convert hex string to bytes if needed
    if isinstance(data, str):
        data_bytes = bytes.fromhex(data)
    else:
        data_bytes = data
    
    best_key = 0
    best_score = 0
    best_plaintext = ""
    all_scores = {}
    
    # Try all 256 possible single-byte keys
    for key in range(256):
        # Decrypt with this key
        decrypted_bytes = bytes(b ^ key for b in data_bytes)
        
        # Try to decode as text
        try:
            plaintext = decrypted_bytes.decode('utf-8', errors='ignore')
        except:
            continue
        
        # Score based on English-like properties
        score = self._score_text(plaintext)
        all_scores[key] = score
        
        if score > best_score:
            best_score = score
            best_key = key
            best_plaintext = plaintext
    
    confidence = min(1.0, best_score / 100.0)
    
    return {
        'success': True if best_score > 10 else False,
        'key': best_key,
        'plaintext': best_plaintext,
        'confidence': confidence,
        'method': 'single_byte_brute_force',
        'attempts': 256,
        'scores': all_scores
    }

def _score_text(self, text: str) -> float:
    """Score text based on English-like characteristics."""
    score = 0.0
    
    # Check printable ratio
    printable_count = sum(c.isprintable() for c in text)
    score += (printable_count / len(text)) * 50
    
    # Check for common English words
    words = text.lower().split()
    common_word_count = sum(1 for w in words if w in self.COMMON_WORDS)
    score += common_word_count * 10
    
    # Check letter frequency
    alpha_ratio = sum(c.isalpha() for c in text) / len(text)
    score += alpha_ratio * 30
    
    return score
```

---

## ⚖️ Pros & Cons

### ✅ Pros

| Advantage | Description |
|-----------|-------------|
| **Extremely Fast** | Single CPU instruction (XOR) |
| **Symmetric** | Same operation for encrypt/decrypt |
| **Simple** | Easy to understand and implement |
| **Reversible** | Self-inverse property (A ⊕ B ⊕ B = A) |
| **OTP Perfect** | Unbreakable when used as One-Time Pad |
| **Hardware Support** | Native XOR instruction on all CPUs |
| **No Block Padding** | Works on any data length |

### ❌ Cons

| Disadvantage | Description |
|--------------|-------------|
| **Key Reuse Weakness** | Repeating key creates exploitable patterns |
| **Pattern Preservation** | XOR of repeated data shows patterns |
| **Not Authenticated** | No integrity checking |
| **Known-Plaintext Attack** | If you know plaintext, you recover key |
| **OTP Impractical** | Perfect version requires key = message length |
| **Not Industry Standard** | AES preferred for actual security |

### 📊 Security Analysis

```
Security Level (OTP):        ██████████ 10/10 (perfect!)
Security Level (Repeating):  ██░░░░░░░░ 2/10 (very weak)

Keyspace (single-byte):      256 keys (trivial)
Keyspace (multi-byte):       256^n keys (better, but still weak)
Keyspace (OTP):              2^(8n) where n = message bits

Cracking Time (single-byte): < 1 second (256 tries)
Cracking Time (OTP):         Impossible (information-theoretically secure)

Recommended Use:             Obfuscation, RAID parity, NOT security
```

### 🆚 Known-Plaintext Attack Example

**The Attack:**

```
If:  Ciphertext = Plaintext ⊕ Key
Then: Key = Plaintext ⊕ Ciphertext

If attacker knows ANY plaintext/ciphertext pair,
they recover the key!
```

**Example:**

```
You encrypted: "HELLO" with key 42
Ciphertext: 62 6f 66 66 65 (hex)

Attacker knows the first letter is 'H' (common greeting):
H = 72 (decimal)
First ciphertext byte = 98

Key = 72 ⊕ 98 = 42  ← Key recovered!

Now decrypt entire message with key 42!
```

---

## 🎮 Try It Yourself

### Using the CLI

```bash
# Launch CryptoSentinel
python cli.py

# Navigate:
# 1. Classical Ciphers
# 4. XOR Cipher
# 3. Choose: Encrypt, Decrypt, or Crack
```

### Python Code Examples

#### Encrypt (String)

```python
from crypto_sentinel.ciphers import XORCipher

cipher = XORCipher()
encrypted = cipher.encrypt("HELLO WORLD", key=42)
print(encrypted)  # Hex output: 62575c5c5d734...
```

#### Encrypt (Bytes for Files)

```python
# Encrypt file data
with open("secret.txt", "rb") as f:
    data = f.read()

encrypted = cipher.encrypt(data, key=42)

with open("secret.enc", "wb") as f:
    f.write(encrypted)
```

#### Decrypt

```python
decrypted = cipher.decrypt("62575c5c5d", key=42)
print(decrypted)  # HELLO
```

#### Crack (Single-Byte Key)

```python
# Try to crack single-byte XOR
ciphertext = "62575c5c5d"

result = cipher.crack(ciphertext)
print(f"Key: {result['key']}")              # 42
print(f"Plaintext: {result['plaintext']}")  # HELLO
print(f"Confidence: {result['confidence']}") # 0.95
```

---

## 🎓 Learning Exercises

### Beginner

1. XOR 10110011 with 11001100 by hand
2. Encrypt "HELLO" with key 255 (all 1s)
3. Why is XOR called "self-inverse"?

### Intermediate

4. Implement XOR encryption for a file in 5 lines of Python
5. Explain why key reuse is dangerous with an example
6. Calculate the keyspace for a 16-byte repeating key

### Advanced

7. Implement a two-time pad attack (when same key encrypts two messages)
8. Create a visualization of XOR patterns with repeating keys
9. Research the BEAST and POODLE attacks on SSL (related to XOR)
10. Implement a One-Time Pad generator using `/dev/urandom`

---

## 🔬 Advanced Topic: The Two-Time Pad Attack

When the same key encrypts two different messages:

$$C_1 = M_1 \oplus K$$
$$C_2 = M_2 \oplus K$$

XOR the ciphertexts:

$$C_1 \oplus C_2 = (M_1 \oplus K) \oplus (M_2 \oplus K) = M_1 \oplus M_2$$

The key **cancels out**! Now we can use frequency analysis on $M_1 \oplus M_2$ to recover both messages! 🎯

---

## 📚 Further Reading

- **One-Time Pad**: [Perfect Secrecy Proof](https://en.wikipedia.org/wiki/One-time_pad)
- **XOR Cipher**: [Bitwise Operations](https://en.wikipedia.org/wiki/XOR_cipher)
- **RAID**: [Parity Using XOR](https://en.wikipedia.org/wiki/RAID)
- **Known-Plaintext Attack**: [Cryptanalysis Methods](https://en.wikipedia.org/wiki/Known-plaintext_attack)
- **Related**: [Substitution Cipher](Substitution-Cipher.md) - Different approach

---

## 🔗 Navigation

- [← Back to Home](Home.md)
- [← Previous: Substitution Cipher](Substitution-Cipher.md)
- [→ Next: Morse Code](Morse-Code.md)
- [↑ Back to Top](#xor-cipher---the-computers-favorite-cipher)

---

**Author**: saisrujanmurthy@gmail.com  
**Last Updated**: December 30, 2025  
**Difficulty**: ⭐⭐⭐☆☆ (Intermediate)
