# Simple XOR Encryption

**Bitwise XOR Logic and Stream Cipher Fundamentals**

---

## Introduction

XOR (Exclusive OR) encryption is one of the most fundamental encryption techniques in computer science, using the XOR bitwise operation to encrypt and decrypt data. While simple, it forms the mathematical foundation for many modern stream ciphers and demonstrates core cryptographic concepts.

**XOR Properties:**
- `A XOR B XOR B = A` (reversible)
- `A XOR 0 = A` (identity)
- `A XOR A = 0` (self-inverse)
- `A XOR B = B XOR A` (commutative)

CryptoSentinel's XOR Encryption tool provides:
- **Single-byte XOR** - Simple key encryption
- **Multi-byte XOR** - Repeating key encryption (similar to [[Vigenere-Cipher-Tool]])
- **Key length detection** - Cryptanalysis using Hamming distance
- **Frequency analysis** - Breaking weak keys

### When to Use This Tool

✅ **Educational purposes** - Understanding bitwise operations  
✅ **CTF challenges** - Common in capture-the-flag competitions  
✅ **Understanding stream ciphers** - Foundation for ChaCha20, AES-CTR  
✅ **Quick obfuscation** - Non-security data hiding  

❌ **Secure communications** - Use AES-256-GCM instead  
❌ **Production systems** - Not cryptographically secure alone  
❌ **Password storage** - Use [[SHA256-Hash-Implementation]] with KDF  

---

## Algorithm: Binary XOR Logic

### XOR Truth Table

The XOR operation returns 1 when inputs differ, 0 when they match:

```
A | B | A XOR B
--|---|--------
0 | 0 |   0
0 | 1 |   1
1 | 0 |   1
1 | 1 |   0
```

### Why XOR for Encryption?

**Perfect reversibility:**
```
Plaintext:  01001000  (H)
Key:        01010101  (U)
───────────────────── XOR
Ciphertext: 00011101

Ciphertext: 00011101
Key:        01010101  (U)
───────────────────── XOR
Plaintext:  01001000  (H)  ← Original recovered!
```

### Single-Byte XOR

Encrypt entire message with one byte key (0-255):

```
Plaintext: "HELLO"
Key: 0x55 (85 decimal, 01010101 binary)

H = 0x48 = 01001000
    XOR    01010101
           ─────────
           00011101 = 0x1D

E = 0x45 = 01000101
    XOR    01010101
           ─────────
           00010000 = 0x10

L = 0x4C = 01001100
    XOR    01010101
           ─────────
           00011001 = 0x19

L = 0x4C = 00011001 = 0x19 (same as above)

O = 0x4F = 01001111
    XOR    01010101
           ─────────
           00011010 = 0x1A

Ciphertext: 1D 10 19 19 1A
```

**Weakness:** Only 256 possible keys - trivial brute force!

### Multi-Byte (Repeating Key) XOR

Use a longer key that repeats:

```
Plaintext: "ATTACK AT DAWN"
Key: "ICE" (repeats: ICEICEICEICE...)

A T T A C K   A T   D A W N
I C E I C E I C E I C E I C

A XOR I, T XOR C, T XOR E, A XOR I, C XOR C, K XOR E...
```

This is essentially [[Vigenere-Cipher-Tool]] in binary form!

**Example with hex:**
```
Plaintext:  41 54 54 41 43 4B 20 41 54 20 44 41 57 4E
Key (ICE):  49 43 45 49 43 45 49 43 45 49 43 45 49 43
            ──────────────────────────────────────────── XOR
Ciphertext: 08 17 31 08 00 0E 69 02 31 69 07 04 1E 0D
```

### One-Time Pad: Unbreakable XOR

**The only provably unbreakable encryption:**

Requirements:
1. **Key length = Message length** (no repetition)
2. **Truly random key** (not pseudorandom)
3. **Key used only once** (never reused)
4. **Key kept perfectly secret**

```
Message: "HELLO" (5 bytes)
Key: 0xA7, 0x3F, 0x9C, 0x2D, 0xF1 (5 random bytes)

Perfect security - no statistical attack possible!
```

**Why it's unbreakable:**
- Any plaintext of equal length is equally likely
- "HELLO" XOR key = ciphertext
- "WORLD" XOR different key = same ciphertext
- Attacker cannot determine which is correct

**Why it's rarely used:**
- Key distribution problem (need to securely share huge keys)
- Key storage problem (key as large as all messages)
- One-time use only (waste of key material)

---

## Algorithm: Breaking XOR - Cryptanalysis

### Method 1: Single-Byte XOR Brute Force

Only 256 possible keys - try them all!

```python
def break_single_byte_xor(ciphertext: bytes) -> List[Tuple[int, str, float]]:
    """
    Try all 256 possible keys and score results.
    """
    candidates = []
    
    for key in range(256):
        # Decrypt with this key
        decrypted = bytes([b ^ key for b in ciphertext])
        
        # Score based on English character frequency
        score = calculate_english_score(decrypted)
        
        try:
            text = decrypted.decode('ascii')
            candidates.append((key, text, score))
        except UnicodeDecodeError:
            pass
    
    # Sort by score
    return sorted(candidates, key=lambda x: x[2], reverse=True)
```

### Method 2: Hamming Distance for Key Length

**Hamming distance** = Number of differing bits between two strings

```
String 1: "this"
String 2: "that"

t = 01110100    t = 01110100
h = 01101000    h = 01101000
i = 01101001    a = 01100001  ← Differ in 3 bits
s = 01110011    t = 01110100  ← Differ in 3 bits

Hamming distance: 6 bits
```

**Finding key length:**

```
1. Try different key lengths (1-40)
2. For each key length:
   a. Split ciphertext into blocks of that length
   b. Calculate Hamming distance between blocks
   c. Normalize by key length (bits per byte)
3. Smallest normalized distance = likely key length
```

**Why this works:**
- When key length is correct, blocks are encrypted with same key
- Similar plaintext blocks → similar ciphertext blocks
- Lower Hamming distance indicates correct key length

### Method 3: Frequency Analysis per Position

Once key length is known:

```
1. Split ciphertext by key position
   Position 0: bytes 0, 3, 6, 9, ... (encrypted with key[0])
   Position 1: bytes 1, 4, 7, 10, ... (encrypted with key[1])
   Position 2: bytes 2, 5, 8, 11, ... (encrypted with key[2])

2. Each position is single-byte XOR!
3. Brute force each position independently
4. Combine to recover full key
```

---

## How It Works: Code Implementation

### Core XOR Operations

```python
class XORCipher:
    """
    XOR encryption with single-byte or repeating-key.
    """
    
    def encrypt_single_byte(self, plaintext: bytes, key: int) -> bytes:
        """
        Encrypt with single-byte key (0-255).
        
        Args:
            plaintext: Data to encrypt
            key: Single byte (0-255)
            
        Returns:
            Encrypted ciphertext
        """
        return bytes([b ^ key for b in plaintext])
    
    def encrypt_repeating_key(self, plaintext: bytes, key: bytes) -> bytes:
        """
        Encrypt with repeating multi-byte key.
        
        Args:
            plaintext: Data to encrypt
            key: Key bytes (repeats if shorter than plaintext)
            
        Returns:
            Encrypted ciphertext
        """
        result = []
        key_len = len(key)
        
        for i, byte in enumerate(plaintext):
            result.append(byte ^ key[i % key_len])
        
        return bytes(result)
    
    def decrypt_single_byte(self, ciphertext: bytes, key: int) -> bytes:
        """
        Decrypt with single-byte key.
        XOR is symmetric: encrypt and decrypt are same operation!
        """
        return self.encrypt_single_byte(ciphertext, key)
    
    def decrypt_repeating_key(self, ciphertext: bytes, key: bytes) -> bytes:
        """
        Decrypt with repeating key.
        XOR is symmetric: encrypt and decrypt are same operation!
        """
        return self.encrypt_repeating_key(ciphertext, key)
```

### Hamming Distance Calculator

```python
def hamming_distance(bytes1: bytes, bytes2: bytes) -> int:
    """
    Calculate Hamming distance (number of differing bits).
    """
    distance = 0
    
    for b1, b2 in zip(bytes1, bytes2):
        # XOR gives 1 for differing bits
        xor = b1 ^ b2
        
        # Count 1 bits (population count)
        distance += bin(xor).count('1')
    
    return distance

def find_key_length(ciphertext: bytes, max_keysize: int = 40) -> int:
    """
    Find most likely key length using Hamming distance.
    """
    distances = []
    
    for keysize in range(2, max_keysize + 1):
        # Take first few blocks
        blocks = [
            ciphertext[i:i+keysize] 
            for i in range(0, min(len(ciphertext), keysize * 4), keysize)
        ]
        
        if len(blocks) < 2:
            continue
        
        # Calculate average Hamming distance
        total_distance = 0
        comparisons = 0
        
        for i in range(len(blocks) - 1):
            dist = hamming_distance(blocks[i], blocks[i+1])
            total_distance += dist
            comparisons += 1
        
        # Normalize by keysize
        normalized = total_distance / comparisons / keysize
        distances.append((keysize, normalized))
    
    # Sort by distance (smallest = most likely)
    distances.sort(key=lambda x: x[1])
    
    return distances[0][0]  # Return most likely key length
```

### Full Cryptanalysis Engine

```python
def break_repeating_key_xor(ciphertext: bytes) -> Tuple[bytes, bytes]:
    """
    Break repeating-key XOR cipher.
    
    Returns:
        (recovered_key, decrypted_plaintext)
    """
    # Step 1: Find key length
    keysize = find_key_length(ciphertext)
    print(f"🔍 Detected key length: {keysize}")
    
    # Step 2: Split by key position
    blocks = [[] for _ in range(keysize)]
    for i, byte in enumerate(ciphertext):
        blocks[i % keysize].append(byte)
    
    # Step 3: Break each position (single-byte XOR)
    key = []
    for block in blocks:
        block_bytes = bytes(block)
        
        # Try all 256 keys
        best_key = 0
        best_score = 0
        
        for k in range(256):
            decrypted = bytes([b ^ k for b in block_bytes])
            score = calculate_english_score(decrypted)
            
            if score > best_score:
                best_score = score
                best_key = k
        
        key.append(best_key)
    
    key = bytes(key)
    
    # Step 4: Decrypt with recovered key
    plaintext = bytes([b ^ key[i % len(key)] for i, b in enumerate(ciphertext)])
    
    return key, plaintext

def calculate_english_score(text: bytes) -> float:
    """
    Score text based on English character frequency.
    """
    # English letter frequencies
    freq = {
        'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97,
        'n': 6.75, 's': 6.33, 'h': 6.09, 'r': 5.99, ' ': 15.0
    }
    
    score = 0
    try:
        text_str = text.decode('ascii').lower()
        for char in text_str:
            score += freq.get(char, 0)
    except UnicodeDecodeError:
        return 0
    
    return score
```

---

## Usage Guide: CLI Commands

### Starting the Tool

```bash
python cli.py

# Select: 1. Classical Ciphers > 4. Simple XOR Encryption
```

### Single-Byte XOR Encryption

```
Choose operation:
1. Single-byte XOR
2. Repeating-key XOR
3. Break XOR cipher

Selection: 1

Enter plaintext: Hello, World!
Enter key (0-255): 42

✓ Encrypted (hex):
62 67 6E 6E 69 58 54 49 69 74 6E 66 55

✓ Encrypted (base64):
YmdubmlYVElpdG5mVQ==

Decrypt: XOR with same key (42)
```

### Repeating-Key XOR

```
Selection: 2

Enter plaintext: Attack at dawn
Enter key (text): ICE

Key bytes: 49 43 45 (repeats)

✓ Encrypted (hex):
08 17 31 08 00 0E 69 02 31 69 07 04 1E 0D

To decrypt: Use same key "ICE"
```

### Breaking XOR Cipher

```
Selection: 3

Enter ciphertext (hex): 08173108000E690231690704... [paste long ciphertext]

🔍 Analyzing ciphertext...
   Length: 487 bytes
   Detecting key length using Hamming distance...

🎯 Step 1: Key Length Detection
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ Key Length ┃ Normalized Distance┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│     3      │      2.14         │ ⭐ Most likely
│     6      │      2.67         │
│     9      │      3.12         │
└────────────┴───────────────────┘

Most likely key length: 3

🎯 Step 2: Breaking Each Key Position
Position 0: Testing 256 keys... Best: 0x49 (I)
Position 1: Testing 256 keys... Best: 0x43 (C)
Position 2: Testing 256 keys... Best: 0x45 (E)

✓ Recovered key: "ICE"

🎯 Step 3: Decryption
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ATTACK AT DAWN. BRING THREE BATTALIONS...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Confidence: ★★★★★ High (English text detected)
```

---

## Troubleshooting

### Common Issues

**Problem:** "Encryption seems to produce random garbage"  
**Solution:** This is correct!
- XOR output is binary data, not printable text
- Display as hexadecimal or Base64
- Binary ciphertext is expected behavior
- Only after XOR decryption with correct key do you get plaintext back

**Problem:** "Key detection gives wrong results"  
**Solution:** Key length detection requires:
- Sufficient ciphertext length (500+ bytes recommended)
- Plaintext must be English (or adjust frequency tables)
- Short keys (2-3 bytes) are harder to detect reliably
- Very long keys (30+ bytes) approach one-time pad security

**Problem:** "Breaking fails on short ciphertexts"  
**Solution:** Statistical attacks need data:
- Minimum 100-200 bytes for reliable breaking
- Short messages (< 50 bytes) may need manual analysis
- Single-byte XOR always breakable (only 256 keys)
- Consider known-plaintext attack for short messages

**Problem:** "Why is decryption the same as encryption?"  
**Solution:** XOR is **self-inverse**:
```
Encrypt: Plaintext XOR Key = Ciphertext
Decrypt: Ciphertext XOR Key = Plaintext

Because: (P XOR K) XOR K = P XOR (K XOR K) = P XOR 0 = P
```
This is a unique property of XOR!

**Problem:** "Is XOR secure for real applications?"  
**Solution:** Only with one-time pad:
- ✅ **Secure**: True OTP (random key, same length, used once)
- ⚠️ **Weak**: Repeating key (this tool) - breakable
- ❌ **Insecure**: Single-byte XOR - trivially breakable
- **Modern alternative**: Use AES-256-GCM or ChaCha20-Poly1305

---

## Pros and Cons

### ✅ Advantages

**Simplicity**
- Single bitwise operation
- Easy to understand and implement
- Fast (hardware-optimized)
- No complex mathematics

**Perfect Reversibility**
- Same operation for encrypt and decrypt
- No separate decryption algorithm needed
- Elegant mathematical property

**Foundation for Modern Crypto**
- Stream ciphers (ChaCha20, RC4)
- Block cipher modes (CTR, OFB)
- Many protocols use XOR operations
- Understanding XOR = understanding modern crypto

**Educational Value**
- Demonstrates core cryptographic concepts
- Shows why key reuse is dangerous
- Illustrates frequency analysis
- Perfect for learning cryptanalysis

### ❌ Disadvantages

**Repeating Key is Weak**
- Frequency analysis breaks it
- Hamming distance reveals key length
- Crib-dragging attacks possible
- Similar to [[Vigenere-Cipher-Tool]] weaknesses

**No Integrity Protection**
- Bit flipping attacks trivial
- Attacker can modify ciphertext predictably
- Example: Flip bit in ciphertext → flips bit in plaintext
- Need MAC/HMAC for authentication

**Key Reuse is Catastrophic**
```
C1 = P1 XOR K
C2 = P2 XOR K

C1 XOR C2 = (P1 XOR K) XOR (P2 XOR K)
          = P1 XOR P2

Keys cancel out! Attacker sees plaintext relationship!
```

**No Forward Secrecy**
- Same key for all messages
- Key compromise = all messages compromised
- No per-message key variation

**Malleability**
```
Ciphertext:  C = P XOR K
Flip bit:    C' = C XOR 00000100
Decrypt:     P' = C' XOR K = P XOR 00000100

Attacker can modify plaintext without knowing key!
```

### Security Rating by Variant

| Variant | Key | Security | Use Case |
|---------|-----|----------|----------|
| Single-byte XOR | 1 byte | ⛔ None | Educational only |
| Repeating-key XOR | 3-20 bytes | ⚠️ Weak | CTF, learning |
| One-time pad | Same length as message, truly random, used once | 🔒 Unbreakable | Diplomatic cables (rare) |
| Modern stream cipher | 256-bit key + nonce | 🔒 Strong | ChaCha20, AES-CTR |

---

## Related Tools

- **[[Vigenere-Cipher-Tool]]** - Similar repeating-key principle in text domain
- **[[Caesar-Cipher-Tool]]** - Simpler substitution cipher
- **[[SHA256-Hash-Implementation]]** - Modern cryptographic security

---

## References

### Technical Foundation
- **XOR properties**: Boolean algebra, De Morgan's laws
- **One-time pad**: Claude Shannon (1949) - proved unbreakable
- **Stream ciphers**: Modern variants (ChaCha20, Salsa20)

### Cryptanalysis Methods
- **Hamming distance**: Richard Hamming (1950)
- **Frequency analysis**: Statistical attack
- **Crib-dragging**: Known-plaintext XOR attack
- **Bit-flipping**: Malleability demonstration

### Real-World Applications
- **RC4**: Stream cipher (now deprecated due to weaknesses)
- **ChaCha20**: Modern secure stream cipher
- **AES-CTR**: Block cipher in counter mode (uses XOR)
- **Disk encryption**: XEX, XTS modes

### Historical Context
- **WWII**: One-time pads used for secure communications
- **Soviet spies**: Venona project broke reused OTP
- **Modern**: NSA uses OTP for highest classification levels

---

## Learn More

**Next Steps:**
1. Compare with [[Vigenere-Cipher-Tool]] - similar mathematical weakness
2. Learn [[SHA256-Hash-Implementation]] for modern security
3. Study modern stream ciphers: ChaCha20-Poly1305

**External Resources:**
- [XOR Wikipedia](https://en.wikipedia.org/wiki/XOR_cipher)
- [One-Time Pad](https://en.wikipedia.org/wiki/One-time_pad)
- [Stream Cipher Attacks](https://en.wikipedia.org/wiki/Stream_cipher_attacks)
- [ChaCha20 Specification](https://tools.ietf.org/html/rfc7539)

---

---

## Navigation

[← Back to Home](Home) | [Report Issue](https://github.com/Shiva-destroyer/CryptoSentinel/issues) | [View All Tools](Home#available-tools)

---

**Developed by:** saisrujanmurthy@gmail.com
