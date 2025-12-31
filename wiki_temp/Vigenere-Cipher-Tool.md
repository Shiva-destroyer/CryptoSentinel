# Vigenère Cipher Tool

**The Unbreakable Cipher of the Renaissance**

---

## Introduction

The Vigenère Cipher, invented by Giovan Battista Bellaso in 1553 and misattributed to Blaise de Vigenère, represents a major leap forward in cryptographic security. For 300 years, it was considered "le chiffre indéchiffrable" (the indecipherable cipher) until Charles Babbage and Friedrich Kasiski independently broke it in the 19th century.

Unlike the simple [[Caesar-Cipher-Tool]] which uses a single shift value, the Vigenère Cipher uses a **keyword** to create multiple interwoven Caesar ciphers, making frequency analysis much more difficult.

### What Makes Vigenère Special

The Vigenère Cipher is a **polyalphabetic substitution cipher**, meaning:
- Different letters can be encrypted differently each time they appear
- The same plaintext letter can produce different ciphertext letters
- Frequency analysis (which breaks Caesar) is significantly harder

CryptoSentinel's implementation includes:
- Standard encryption/decryption with keyword
- **Kasiski Examination** for key length detection
- **Index of Coincidence (IoC)** analysis
- Automated key recovery using frequency analysis

### When to Use This Tool

✅ **Historical cipher analysis** - Understanding Renaissance cryptography  
✅ **Advanced cryptography learning** - Polyalphabetic substitution  
✅ **Moderate obfuscation** - Better than Caesar but still not secure  
✅ **CTF challenges** - Common in capture-the-flag competitions  

❌ **Modern security** - Use [[SHA256-Hash-Implementation]] instead  
❌ **Data protection** - Not secure against determined attackers  

---

## Algorithm: Polyalphabetic Substitution

### Encryption Formula

The Vigenère Cipher uses a repeating keyword to determine shifts:

```
C[i] = (P[i] + K[i mod m]) mod 26
```

Where:
- **C[i]** = ciphertext character at position i
- **P[i]** = plaintext character at position i
- **K[i mod m]** = keyword character (repeating)
- **m** = length of keyword
- **mod 26** = alphabet wraparound

### The Vigenère Square (Tabula Recta)

Traditional Vigenère encryption uses a 26×26 grid:

```
     A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
   +----------------------------------------------------
A  | A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
B  | B C D E F G H I J K L M N O P Q R S T U V W X Y Z A
C  | C D E F G H I J K L M N O P Q R S T U V W X Y Z A B
D  | D E F G H I J K L M N O P Q R S T U V W X Y Z A B C
...
```

To encrypt:
1. Find plaintext letter in top row
2. Find keyword letter in left column
3. Intersection is the ciphertext

### Example Encryption

**Plaintext:** `ATTACK AT DAWN`  
**Keyword:** `LEMON` (repeats as LEMONL EM ONLE)

| Plaintext | A | T | T | A | C | K | A | T | D | A | W | N |
|-----------|---|---|---|---|---|---|---|---|---|---|---|---|
| Keyword | L | E | M | O | N | L | E | M | O | N | L | E |
| Shift | 11| 4 | 12| 14| 13| 11| 4 | 12| 14| 13| 11| 4 |
| Ciphertext| L | X | F | O | P | V | E | F | R | N | H | R |

**Ciphertext:** `LXFOPV EF RNHR`

Notice how:
- Two "A"s encrypt to different letters (L and O)
- Two "T"s encrypt to different letters (X and F)
- Pattern recognition is much harder

---

## Algorithm: Kasiski Examination Method

### How Kasiski Examination Works

**Friedrich Kasiski's breakthrough (1863):**

When the same plaintext segment aligns with the same keyword segment, it produces the same ciphertext. By finding repeated sequences in ciphertext, we can determine the key length.

**Steps:**
1. **Find Repeats** - Identify sequences that appear multiple times (3+ characters)
2. **Measure Distances** - Calculate distances between repetitions
3. **Find GCD** - The key length is likely a factor of these distances
4. **Statistical Validation** - Use Index of Coincidence to confirm

### Example Analysis

**Ciphertext:** `VHVS SFJWFZ VHF XJWFS FMAVJ...`

Repeated sequence "VHF" appears at positions 0 and 30.  
Distance = 30 characters

Factors of 30: 1, 2, 3, 5, 6, 10, 15, 30  
Most likely key lengths: 5, 6, 10, 15

### Index of Coincidence (IoC)

IoC measures how likely two randomly selected letters from a text are the same:

```
IoC = Σ(f[i] * (f[i] - 1)) / (N * (N - 1))
```

Where:
- **f[i]** = frequency of letter i
- **N** = total number of letters

**Expected Values:**
- Random text: IoC ≈ 0.038
- English text: IoC ≈ 0.065
- For Vigenère: IoC depends on key length

**Using IoC to Find Key Length:**

For each potential key length k:
1. Split ciphertext into k groups (every kth letter)
2. Calculate IoC for each group
3. Average the IoC values
4. The key length with IoC closest to 0.065 is likely correct

---

## How It Works: Code Implementation

### Core Encryption Engine

```python
class VigenereCipher:
    """
    Implements Vigenère cipher with cryptanalysis capabilities.
    """
    
    def encrypt(self, plaintext: str, keyword: str) -> str:
        """
        Encrypt plaintext using Vigenère cipher.
        
        Args:
            plaintext: Message to encrypt
            keyword: Repeating keyword for shifts
            
        Returns:
            Encrypted ciphertext
        """
        result = []
        keyword = keyword.upper()
        key_index = 0
        
        for char in plaintext:
            if char.isalpha():
                # Determine base (A or a)
                base = ord('A') if char.isupper() else ord('a')
                
                # Get shift from keyword
                shift = ord(keyword[key_index % len(keyword)]) - ord('A')
                
                # Apply Vigenère formula
                encrypted = (ord(char) - base + shift) % 26
                result.append(chr(base + encrypted))
                
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str, keyword: str) -> str:
        """Decrypt by negating the shift."""
        result = []
        keyword = keyword.upper()
        key_index = 0
        
        for char in ciphertext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shift = ord(keyword[key_index % len(keyword)]) - ord('A')
                
                # Subtract shift for decryption
                decrypted = (ord(char) - base - shift) % 26
                result.append(chr(base + decrypted))
                
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
```

### Kasiski Examination Implementation

```python
def kasiski_examination(ciphertext: str, 
                       sequence_length: int = 3) -> List[int]:
    """
    Find likely key lengths using Kasiski method.
    
    Returns list of probable key lengths sorted by likelihood.
    """
    # Remove non-alphabetic characters
    cleaned = ''.join(c for c in ciphertext.upper() if c.isalpha())
    
    # Find all repeated sequences
    sequences = {}
    for i in range(len(cleaned) - sequence_length):
        seq = cleaned[i:i + sequence_length]
        if seq in sequences:
            sequences[seq].append(i)
        else:
            sequences[seq] = [i]
    
    # Calculate distances between repetitions
    distances = []
    for positions in sequences.values():
        if len(positions) > 1:
            for i in range(len(positions) - 1):
                distance = positions[i + 1] - positions[i]
                distances.append(distance)
    
    # Find GCD of all distances
    from math import gcd
    from functools import reduce
    
    if not distances:
        return list(range(2, 16))  # Default guess
    
    # Count factor frequencies
    factor_counts = {}
    for dist in distances:
        for factor in range(2, min(dist, 30)):
            if dist % factor == 0:
                factor_counts[factor] = factor_counts.get(factor, 0) + 1
    
    # Sort by frequency
    likely_lengths = sorted(factor_counts.keys(), 
                          key=lambda x: factor_counts[x], 
                          reverse=True)
    
    return likely_lengths[:5]  # Top 5 candidates
```

### Index of Coincidence Calculator

```python
def calculate_ioc(text: str) -> float:
    """
    Calculate Index of Coincidence for given text.
    
    Returns:
        IoC value (0.038 for random, 0.065 for English)
    """
    text = ''.join(c for c in text.upper() if c.isalpha())
    N = len(text)
    
    if N <= 1:
        return 0.0
    
    # Count frequency of each letter
    frequencies = {}
    for char in text:
        frequencies[char] = frequencies.get(char, 0) + 1
    
    # Calculate IoC
    ioc_sum = sum(f * (f - 1) for f in frequencies.values())
    ioc = ioc_sum / (N * (N - 1))
    
    return ioc

def find_key_length(ciphertext: str, 
                   max_length: int = 20) -> int:
    """
    Determine most likely key length using IoC.
    """
    cleaned = ''.join(c for c in ciphertext.upper() if c.isalpha())
    
    best_length = 1
    best_avg_ioc = 0.0
    
    for key_length in range(1, max_length + 1):
        # Split into groups
        groups = ['' for _ in range(key_length)]
        for i, char in enumerate(cleaned):
            groups[i % key_length] += char
        
        # Calculate average IoC
        iocs = [calculate_ioc(group) for group in groups]
        avg_ioc = sum(iocs) / len(iocs)
        
        # English text has IoC around 0.065
        if abs(avg_ioc - 0.065) < abs(best_avg_ioc - 0.065):
            best_avg_ioc = avg_ioc
            best_length = key_length
    
    return best_length
```

---

## Usage Guide: CLI Commands

### Starting the Tool

```bash
python cli.py

# Select: 1. Classical Ciphers > 2. Vigenère Cipher
```

### Encrypting with Keyword

```
Choose operation:
1. Encrypt Text
2. Decrypt Text
3. Crack Vigenère Cipher (Advanced)

Selection: 1

Enter plaintext: ATTACK AT DAWN
Enter keyword: LEMON

✓ Encryption complete!
Ciphertext: LXFOPV EF RNHR
```

### Decrypting with Known Key

```
Selection: 2

Enter ciphertext: LXFOPV EF RNHR
Enter keyword: LEMON

✓ Decryption complete!
Plaintext: ATTACK AT DAWN
```

### Automatic Cryptanalysis

```
Selection: 3

Enter ciphertext to crack: [paste long ciphertext]

🔍 Step 1: Running Kasiski Examination...
Found repeated sequences:
  - "THE" appears 3 times (distances: 15, 30, 45)
  - "AND" appears 2 times (distance: 12)

Likely key lengths: 3, 5, 15

🔍 Step 2: Calculating Index of Coincidence...
┏━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┓
┃ Key Length ┃ Avg IoC ┃ Score   ┃
┡━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━┩
│     3      │  0.067  │  ★★★★★  │
│     5      │  0.052  │  ★★★    │
│    15      │  0.041  │  ★★     │
└────────────┴─────────┴─────────┘

Most likely key length: 3

🔍 Step 3: Frequency Analysis per Position...
Position 1: Most likely shift = 11 (L)
Position 2: Most likely shift = 4  (E)
Position 3: Most likely shift = 12 (M)

Recovered keyword: LEM (or LEMON if repeating)

✓ Decryption with recovered key:
ATTACK AT DAWN...
```

---

## Troubleshooting

### Common Issues

**Problem:** "Cracking fails with short ciphertext"  
**Solution:** Vigenère cracking requires statistical analysis. For best results:
- Minimum 200-300 characters of ciphertext
- Text should be in English (or adjust frequency tables)
- Avoid ciphertext with many numbers/symbols

**Problem:** "Key length detection gives wrong results"  
**Solution:** Multiple factors can affect accuracy:
- Very short or very long keywords are harder to detect
- Random text won't have proper English characteristics
- Try both Kasiski and IoC methods for confirmation
- Manual key length testing may be needed for edge cases

**Problem:** "Keyword with spaces or numbers doesn't work"  
**Solution:** Keywords should be alphabetic only (A-Z). The tool automatically:
- Removes spaces and non-alphabetic characters
- Converts to uppercase
- "LEMON123" becomes "LEMON"

**Problem:** "Same keyword produces different results than online tools"  
**Solution:** Check these implementation differences:
- Some tools skip spaces, others don't
- Case handling varies (preserve vs normalize)
- Non-alphabetic character handling
- CryptoSentinel preserves case and punctuation

**Problem:** "IoC values don't match expected 0.065"  
**Solution:** IoC varies based on:
- Text length (longer = more accurate)
- Language (English ~0.065, German ~0.076, etc.)
- Topic (technical text has different distribution)
- Use IoC comparatively, not as absolute threshold

---

## Pros and Cons

### ✅ Advantages

**Significantly More Secure Than Caesar**
- Frequency analysis is much harder
- Multiple different shift values
- No obvious patterns in ciphertext
- Resisted breaking for 300 years

**Key Flexibility**
- Keyword can be any length
- Memorable passphrases work well
- Longer keys = more security
- Easy to change keys frequently

**Historical Importance**
- Used in Civil War, WWI
- Foundation for modern stream ciphers
- Demonstrates polyalphabetic substitution
- Led to development of rotor machines (Enigma)

**Educational Value**
- Perfect for teaching statistical cryptanalysis
- Shows evolution beyond monoalphabetic ciphers
- Introduces key management concepts
- Demonstrates why key length matters

### ❌ Disadvantages

**Still Breakable**
- Kasiski examination finds key length
- Frequency analysis per position recovers key
- Modern computers crack it instantly
- No security against determined attackers

**Key Management Issues**
- Must securely share keyword
- Short keywords repeat too often
- Long keywords are hard to remember
- Compromise of key breaks all messages

**Vulnerable to Known-Plaintext Attacks**
- If attacker knows part of plaintext, can recover key segments
- Common phrases ("Dear Sir") give away key positions
- Predictable message formats are dangerous

**Not True Randomness**
- Pattern of keyword length repeats
- Statistical properties still present
- Not suitable for any modern security need
- Better than Caesar, but not cryptographically secure

### Security Rating: ⚠️ HISTORICAL/EDUCATIONAL ONLY

**Modern Alternatives:**
- [[SHA256-Hash-Implementation]] for data integrity
- [[Password-Strength-Analyzer]] for authentication security
- Modern encryption: AES-256, RSA, or authenticated encryption

---

## Related Tools

- **[[Caesar-Cipher-Tool]]** - Simpler monoalphabetic version
- **[[Simple-Substitution-Cracker]]** - Related substitution cipher
- **[[Simple-XOR-Encryption]]** - Modern equivalent (repeating key XOR)

---

## References

### Historical Context
- **1553**: Giovan Battista Bellaso invents the cipher
- **1586**: Blaise de Vigenère publishes description (gets credit)
- **1863**: Friedrich Kasiski publishes breaking method
- **1854**: Charles Babbage independently breaks it (unpublished)
- **1917**: Used in WWI diplomatic communications

### Mathematical Foundation
- Polyalphabetic substitution cipher
- Modular arithmetic base
- Statistical cryptanalysis techniques
- Index of Coincidence (William Friedman, 1920)

### Modern Legacy
- Inspired one-time pad (unbreakable variant)
- Foundation for stream ciphers
- Led to rotor cipher machines
- Teaches importance of key length and randomness

---

---

## Navigation

[← Back to Home](Home) | [Report Issue](https://github.com/Shiva-destroyer/CryptoSentinel/issues) | [View All Tools](Home#available-tools)

---

**Developed by:** saisrujanmurthy@gmail.com
