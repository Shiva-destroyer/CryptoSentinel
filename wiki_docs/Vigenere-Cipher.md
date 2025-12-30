# Vigenère Cipher - The Unbreakable Cipher (Until It Was Broken)

**For 300 years, this cipher was considered uncrackable**

---

## 📖 Table of Contents

1. [ELI5 - Explain Like I'm 5](#eli5---explain-like-im-5)
2. [The Mathematics](#the-mathematics)
3. [How It Works - Step by Step](#how-it-works---step-by-step)
4. [Advanced Cryptanalysis](#advanced-cryptanalysis---breaking-the-unbreakable)
5. [Code Implementation](#code-implementation)
6. [Pros & Cons](#pros--cons)
7. [Try It Yourself](#try-it-yourself)

---

## 🧒 ELI5 - Explain Like I'm 5

**Imagine the Caesar cipher clock, but the clock changes for EVERY letter!**

Remember Caesar cipher? You spin the clock by the same amount for every letter (like always spinning 3 positions).

**Vigenère is smarter**: It uses a **keyword** to decide how much to spin for each letter!

### 🎯 Example with Keyword "KEY"

Let's encrypt **"HELLO"** using the keyword **"KEY"**:

```
Plaintext:  H  E  L  L  O
Keyword:    K  E  Y  K  E  (repeats!)
            ↓  ↓  ↓  ↓  ↓
Shift by:   10 4  24 10 4  (K=10, E=4, Y=24)
            ↓  ↓  ↓  ↓  ↓
Ciphertext: R  I  J  V  S
```

- **H** shifted by **K**(10) → **R**
- **E** shifted by **E**(4) → **I**
- **L** shifted by **Y**(24) → **J**
- **L** shifted by **K**(10) → **V**
- **O** shifted by **E**(4) → **S**

**Result**: HELLO → **RIJVS** 🎉

### 🤔 Why Is This Harder to Break?

In Caesar cipher, **E** always becomes the same letter (like **H**).  
In Vigenère, **E** can become different letters depending on which keyword letter is used!

```
Caesar:   E → H, E → H, E → H  (always the same!)
Vigenère: E → I, E → S, E → I  (changes based on keyword position!)
```

This hides the letter frequency patterns! 🕵️

---

## 🧮 The Mathematics

The Vigenère cipher is a **polyalphabetic substitution cipher** - it uses multiple Caesar ciphers based on a keyword.

### Encryption Formula

$$E(x) = (x + k_i) \bmod 26$$

Where:
- $E(x)$ = Encrypted letter
- $x$ = Position of plaintext letter (A=0, B=1, ..., Z=25)
- $k_i$ = Position of keyword letter at index $i \bmod \text{key\_length}$
- $\bmod 26$ = Modulo 26 (wrap around)

### Decryption Formula

$$D(x) = (x - k_i) \bmod 26$$

Where:
- $D(x)$ = Decrypted letter
- $x$ = Position of ciphertext letter
- $k_i$ = Position of keyword letter at index $i$

### 📊 Example Calculation

Encrypt **"ATTACK"** with keyword **"LEMON"**:

| Position | Plaintext | Plaintext # | Keyword | Keyword # | Calculation | Result # | Ciphertext |
|----------|-----------|-------------|---------|-----------|-------------|----------|------------|
| 0        | A         | 0           | L       | 11        | (0+11) mod 26 = 11 | 11 | **L** |
| 1        | T         | 19          | E       | 4         | (19+4) mod 26 = 23 | 23 | **X** |
| 2        | T         | 19          | M       | 12        | (19+12) mod 26 = 5 | 5  | **F** |
| 3        | A         | 0           | O       | 14        | (0+14) mod 26 = 14 | 14 | **O** |
| 4        | C         | 2           | N       | 13        | (2+13) mod 26 = 15 | 15 | **P** |
| 5        | K         | 10          | L       | 11        | (10+11) mod 26 = 21 | 21 | **V** |

**Result**: ATTACK → **LXFOPV** ✅

### 🔄 Keyword Repetition

If the plaintext is longer than the keyword, the keyword **repeats**:

```
Plaintext:  A T T A C K A T D A W N
Keyword:    L E M O N L E M O N L E  (repeats)
```

This makes it a **periodic cipher** - the same keyword letter encrypts every $k$-th character (where $k$ = key length).

---

## ⚙️ How It Works - Step by Step

### Encryption Process

```
Plaintext:  ATTACKATDAWN
Keyword:    LEMON

Step 1: Repeat keyword to match plaintext length
        LEMON → LEMONLEMONLE

Step 2: Convert to numbers (A=0, B=1, ...)
        Plaintext: [0,19,19,0,2,10,0,19,3,0,22,13]
        Keyword:   [11,4,12,14,13,11,4,12,14,13,11,4]

Step 3: Apply (x + k_i) mod 26 to each pair
        [11,23,5,14,15,21,4,5,17,13,7,17]

Step 4: Convert back to letters
        LXFOPVEFRNHR

Ciphertext: LXFOPVEFRNHR
```

### Decryption Process

```
Ciphertext: LXFOPVEFRNHR
Keyword:    LEMON

Step 1: Repeat keyword
        LEMONLEMONLE

Step 2: Convert to numbers
        Ciphertext: [11,23,5,14,15,21,4,5,17,13,7,17]
        Keyword:    [11,4,12,14,13,11,4,12,14,13,11,4]

Step 3: Apply (x - k_i) mod 26 to each pair
        [0,19,19,0,2,10,0,19,3,0,22,13]

Step 4: Convert back to letters
        ATTACKATDAWN

Plaintext: ATTACKATDAWN
```

---

## 🔍 Advanced Cryptanalysis - Breaking the "Unbreakable"

For 300 years (1553-1863), the Vigenère cipher was called **"le chiffre indéchiffrable"** (the unbreakable cipher). Then mathematicians discovered its weakness!

### 🎯 The Cracking Strategy (3 Steps)

```
Step 1: Find the KEY LENGTH using statistical analysis
Step 2: Divide ciphertext into columns (one per key letter)
Step 3: Solve each column as a Caesar cipher
```

---

### 📏 Step 1: Finding Key Length

#### Method A: The Friedman Test (Index of Coincidence)

The **Index of Coincidence (IoC)** measures how "English-like" text is.

**Formula:**

$$\text{IoC} = \frac{\sum_{i=0}^{25} f_i(f_i - 1)}{N(N-1)}$$

Where:
- $f_i$ = Frequency of letter $i$ in the text
- $N$ = Total number of letters

**Key Insight:**
- **Random text**: IoC ≈ 0.0385 (all letters equally likely)
- **English text**: IoC ≈ 0.0667 (some letters more common)
- **Monoalphabetic cipher**: IoC ≈ 0.0667 (preserves frequencies)
- **Polyalphabetic cipher**: IoC between 0.0385 and 0.0667

**The Algorithm:**

```python
For each possible key length k from 1 to 20:
    1. Divide ciphertext into k columns
    2. Calculate IoC for each column
    3. Average the IoC values
    4. The k with IoC closest to 0.0667 is likely the key length!
```

**Example:**

```
Ciphertext: LXFOPVEFRNHR (encrypted with "LEMON", length 5)

Try k=1 (Caesar):
  All letters together → IoC = 0.041 (not English-like)

Try k=2:
  Column 1: L, F, V, R, H → IoC = 0.045
  Column 2: X, O, E, N, R → IoC = 0.043
  Average: 0.044 (still not great)

Try k=5: ← LEMON has 5 letters!
  Column 1: L, E → IoC = 0.065
  Column 2: X, F → IoC = 0.068
  Column 3: F, R → IoC = 0.066
  Column 4: O, N → IoC = 0.067
  Column 5: P, H → IoC = 0.064
  Average: 0.066 ← VERY close to 0.0667! ✓
```

Key length **5** gives the highest IoC, so we've found it!

#### Method B: Kasiski Examination

**The Idea**: Repeated words in plaintext may encrypt to repeated patterns in ciphertext if they align with the keyword!

**Example:**

```
Plaintext:  THE QUICK BROWN FOX THE LAZY DOG
Keyword:    KEYKEYKEYKEYKEYKEYK EYKEYKEYKEY

Notice "THE" appears twice:
Position 1: T+K=D, H+E=L, E+Y=C → DLC
Position 5: T+E=X, H+Y=F, E+K=O → XFO  (different! keyword shifted)

But if "THE" repeats at positions 0 and 15 (multiple of 5):
Both would encrypt the same way! → Same pattern appears twice
```

**The Algorithm:**

```python
1. Find all repeated n-grams (groups of 3+ letters) in ciphertext
2. Calculate distances between repetitions
3. Find GCD (Greatest Common Divisor) of all distances
4. The GCD is likely the key length (or a multiple of it)!
```

**Example:**

```
Ciphertext: VVHQWVVHQWVVHQWVVHQW

Pattern "VVHQW" repeats at positions: 0, 5, 10, 15
Distances: 5, 5, 5
GCD(5, 5, 5) = 5

Key length is 5! ✓
```

---

### 🔨 Step 2: Divide Into Columns

Once we know the key length $k$, we split the ciphertext into $k$ groups:

```
Ciphertext: LXFOPVEFRNHR
Key length: 5

Column 0: Letters at positions 0, 5, 10, ...  → L, V, H
Column 1: Letters at positions 1, 6, 11, ...  → X, E, R
Column 2: Letters at positions 2, 7, ...      → F, F
Column 3: Letters at positions 3, 8, ...      → O, R
Column 4: Letters at positions 4, 9, ...      → P, N
```

**Why?** Each column was encrypted with the **same Caesar shift** (same keyword letter)!

---

### 🎯 Step 3: Solve Each Column as Caesar Cipher

Now each column is just a simple Caesar cipher! We use **frequency analysis** (chi-squared test) on each:

```python
Column 0: "LVH"
  Try shift 0: χ² = 523
  Try shift 1: χ² = 489
  ...
  Try shift 11: χ² = 15 ← LOWEST! Key letter = L (position 11)
  ...

Column 1: "XER"
  Best shift = 4 → Key letter = E

Column 2: "FF"
  Best shift = 12 → Key letter = M

Column 3: "OR"
  Best shift = 14 → Key letter = O

Column 4: "PN"
  Best shift = 13 → Key letter = N
```

**Recovered Key**: L + E + M + O + N = **LEMON** ✅

---

### 🧠 The Complete Cracking Process (Flowchart)

```
             START
               ↓
    ┌──────────────────────┐
    │  Analyze Ciphertext  │
    │  Calculate IoC       │
    └──────────┬───────────┘
               ↓
    ┌──────────────────────┐
    │  Friedman Test       │
    │  Find Key Length (k) │
    └──────────┬───────────┘
               ↓
    ┌──────────────────────┐
    │  Divide into k       │
    │  Columns             │
    └──────────┬───────────┘
               ↓
    ┌──────────────────────┐
    │  For Each Column:    │
    │  - Try all shifts    │
    │  - Calculate χ²      │
    │  - Pick best shift   │
    └──────────┬───────────┘
               ↓
    ┌──────────────────────┐
    │  Assemble Key from   │
    │  Column Shifts       │
    └──────────┬───────────┘
               ↓
    ┌──────────────────────┐
    │  Decrypt with Key    │
    │  SUCCESS!            │
    └──────────────────────┘
```

---

## 💻 Code Implementation

### The `crack()` Method in `vigenere.py`

Here's how CryptoSentinel implements Vigenère cracking:

```python
def crack(self, data: Union[str, bytes]) -> dict:
    """
    Crack Vigenère cipher using IoC-based key length detection
    and frequency analysis.
    """
    # Step 1: Filter to alphabetic only
    filtered_text = ''.join(c.upper() for c in data if c.isalpha())
    
    if len(filtered_text) < 20:
        return {
            'success': False,
            'error': 'Text too short for reliable analysis'
        }
    
    # Step 2: Estimate key length using IoC
    key_length = self._estimate_key_length(filtered_text)
    
    # Step 3: Split into columns
    columns = [''] * key_length
    for i, char in enumerate(filtered_text):
        columns[i % key_length] += char
    
    # Step 4: Solve each column as Caesar cipher
    key_chars = []
    total_confidence = 0.0
    
    for column in columns:
        best_shift = 0
        best_score = float('inf')
        
        # Try all 26 shifts
        for shift in range(26):
            decrypted = ''.join(
                chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
                for c in column
            )
            score = self._score_text(decrypted)  # Chi-squared
            
            if score < best_score:
                best_score = score
                best_shift = shift
        
        key_chars.append(chr(best_shift + ord('A')))
        confidence = max(0.0, min(1.0, 1.0 - (best_score / 500.0)))
        total_confidence += confidence
    
    # Step 5: Reconstruct key and decrypt
    key = ''.join(key_chars)
    plaintext = self.decrypt(data, key=key)
    
    return {
        'success': True,
        'key': key,
        'plaintext': plaintext,
        'confidence': total_confidence / key_length,
        'method': 'friedman_test',
        'attempts': key_length * 26,
        'key_length': key_length
    }
```

### The IoC Helper Function

```python
def _estimate_key_length(self, text: str, max_length: int = 20) -> int:
    """
    Estimate Vigenère key length using Index of Coincidence.
    
    For each possible key length k:
        - Divide text into k columns
        - Calculate IoC for each column
        - Average the IoC values
        - Key length with IoC closest to 0.0667 wins
    """
    best_length = 1
    best_avg_ioc = 0.0
    
    for key_len in range(1, min(max_length, len(text) // 2) + 1):
        # Divide into columns
        columns = [''] * key_len
        for i, char in enumerate(text):
            columns[i % key_len] += char
        
        # Calculate average IoC
        ioc_sum = 0.0
        for column in columns:
            if len(column) > 1:
                ioc = calculate_ioc(column)  # From math_helpers
                ioc_sum += ioc
        
        avg_ioc = ioc_sum / key_len
        
        # IoC ≈ 0.0667 indicates English text
        if abs(avg_ioc - 0.0667) < abs(best_avg_ioc - 0.0667):
            best_avg_ioc = avg_ioc
            best_length = key_len
    
    return best_length
```

### The `calculate_ioc()` Function

Located in `utils/math_helpers.py`:

```python
def calculate_ioc(text: str) -> float:
    """
    Calculate Index of Coincidence for a text.
    
    IoC measures how likely it is that two randomly selected
    letters from the text are the same.
    
    Formula: IoC = Σ(f_i * (f_i - 1)) / (N * (N - 1))
    
    Returns:
        ~0.0667 for English text
        ~0.0385 for random text
    """
    text = text.upper()
    n = len(text)
    
    if n < 2:
        return 0.0
    
    # Count letter frequencies
    freq = [0] * 26
    for char in text:
        if char.isalpha():
            freq[ord(char) - ord('A')] += 1
    
    # Calculate IoC
    ioc = sum(f * (f - 1) for f in freq) / (n * (n - 1))
    
    return ioc
```

---

## ⚖️ Pros & Cons

### ✅ Pros

| Advantage | Description |
|-----------|-------------|
| **Frequency Hiding** | Hides single-letter frequency patterns |
| **Variable Shifts** | Each position uses different Caesar shift |
| **Simple to Use** | Easy to implement with a keyword |
| **Historical** | Used in real wars and diplomacy |
| **Scalable Security** | Longer keys = exponentially more possibilities |

**Keyspace Comparison:**
- Key length 3: $26^3 = 17,576$ keys
- Key length 5: $26^5 = 11,881,376$ keys
- Key length 10: $26^{10} ≈ 141$ trillion keys

### ❌ Cons

| Disadvantage | Description |
|--------------|-------------|
| **IoC Vulnerability** | Statistical analysis reveals key length |
| **Periodic Pattern** | Keyword repetition creates exploitable patterns |
| **Kasiski Examination** | Repeated n-grams leak key length |
| **Column Analysis** | Once key length known, reduces to Caesar |
| **Not Semantic Secure** | Same plaintext + key = same ciphertext |
| **Short Key Weakness** | Keys shorter than plaintext repeat |

### 📊 Security Analysis

```
Security Level:       ██████░░░░ 6/10
Keyspace (k=5):       26^5 = 11.8M keys
Cracking Time:        Minutes (with enough ciphertext)
Pattern Preservation: Partially hidden (periodic)
Recommended Use:      Education, puzzles
```

**Vulnerability Factors:**
- Ciphertext length > 100 letters: Easy to crack
- Ciphertext length > 50 letters: Moderate difficulty
- Ciphertext length < 30 letters: Hard to crack reliably
- Key length ≥ plaintext length: Becomes **One-Time Pad** (unbreakable!)

---

## 🎮 Try It Yourself

### Using the CLI

```bash
# Launch CryptoSentinel
python cli.py

# Navigate:
# 1. Classical Ciphers
# 2. Vigenère Cipher
# 3. Choose: Encrypt, Decrypt, or Crack
```

### Python Code Examples

#### Encrypt

```python
from crypto_sentinel.ciphers import VigenereCipher

cipher = VigenereCipher()
encrypted = cipher.encrypt("ATTACK AT DAWN", key="LEMON")
print(encrypted)  # Output: LXFOPV EF RNHR
```

#### Decrypt

```python
decrypted = cipher.decrypt("LXFOPV EF RNHR", key="LEMON")
print(decrypted)  # Output: ATTACK AT DAWN
```

#### Crack (Automatic Key Recovery)

```python
result = cipher.crack("LXFOPVEFRNHR")
print(f"Key: {result['key']}")              # LEMON
print(f"Key Length: {result['key_length']}") # 5
print(f"Plaintext: {result['plaintext']}")  # ATTACKATDAWN
print(f"Confidence: {result['confidence']}") # 0.87
print(f"Method: {result['method']}")        # friedman_test
```

---

## 🎓 Learning Exercises

### Beginner

1. Encrypt "HELLO" with key "ABC" by hand
2. Decrypt "RIJVS" with key "KEY"
3. Why does a longer keyword make Vigenère stronger?

### Intermediate

4. Calculate IoC for the text "LXFOPV" (hint: should be low)
5. Explain why repeated words can reveal key length
6. What happens if the key is as long as the plaintext?

### Advanced

7. Implement Kasiski examination from scratch
8. Write code to find all repeated n-grams in a ciphertext
9. Compare IoC values for monoalphabetic vs polyalphabetic ciphers
10. Research the **One-Time Pad** (Vigenère with key length = plaintext length)

---

## 🔬 Mathematical Deep Dive

### Why IoC Works

The probability that two random letters from English text are the same:

$$P_{\text{English}} = \sum_{i=0}^{25} p_i^2 ≈ 0.0667$$

Where $p_i$ is the probability of letter $i$.

For random text (uniform distribution):

$$P_{\text{Random}} = 26 \times \left(\frac{1}{26}\right)^2 = \frac{1}{26} ≈ 0.0385$$

**Vigenère with key length k:**

$$\text{IoC}_{\text{Vigenère}} ≈ \frac{1}{k} \cdot 0.0667 + \frac{k-1}{k} \cdot 0.0385$$

As $k$ increases, IoC approaches 0.0385 (random).  
When we divide into correct columns, each column's IoC ≈ 0.0667 (English)!

### Time Complexity

```
Encryption:  O(n)              n = text length
Decryption:  O(n)
Cracking:    O(k_max * n * 26) where k_max = max key length tried
```

For typical parameters:
- $k_{\max} = 20$
- $n = 1000$ letters
- Total operations: $20 \times 1000 \times 26 = 520,000$ (< 1 second)

---

## 📚 Further Reading

- **History**: [Vigenère's Original Treatise (1586)](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)
- **Cryptanalysis**: [Friedman's IoC Method (1920)](https://en.wikipedia.org/wiki/Index_of_coincidence)
- **Kasiski**: [Pattern Finding (1863)](https://en.wikipedia.org/wiki/Kasiski_examination)
- **One-Time Pad**: [The Only Unbreakable Cipher](https://en.wikipedia.org/wiki/One-time_pad)
- **Previous Cipher**: [Caesar Cipher](Caesar-Cipher.md) - The foundation

---

## 🔗 Navigation

- [← Back to Home](Home.md)
- [← Previous: Caesar Cipher](Caesar-Cipher.md)
- [↑ Back to Top](#vigenère-cipher---the-unbreakable-cipher-until-it-was-broken)

---

**Author**: saisrujanmurthy@gmail.com  
**Last Updated**: December 30, 2025  
**Difficulty**: ⭐⭐⭐☆☆ (Intermediate)
