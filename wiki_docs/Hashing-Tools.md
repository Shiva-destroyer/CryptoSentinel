# Hashing Tools - Digital Fingerprints for Data Integrity

**One-way functions that create unique signatures for any data**

---

## 📖 Table of Contents

1. [ELI5 - Explain Like I'm 5](#eli5---explain-like-im-5)
2. [What is a Hash Function?](#what-is-a-hash-function)
3. [The Mathematics - Merkle-Damgård Construction](#the-mathematics---merkle-damgård-construction)
4. [MD5 vs SHA-256](#md5-vs-sha-256)
5. [Streaming Large Files - The Chunking Magic](#streaming-large-files---the-chunking-magic)
6. [Checksum Validation](#checksum-validation)
7. [Code Implementation](#code-implementation)
8. [Pros & Cons](#pros--cons)
9. [Try It Yourself](#try-it-yourself)

---

## 🧒 ELI5 - Explain Like I'm 5

**Imagine you have a magic photo booth!**

You put anything inside (a picture, a book, a toy) and it takes a special "fingerprint photo" of it:

```
Input: Your teddy bear 🧸
↓ (magic photo booth)
Output: Photo ID #A1B2C3D4E5F6...

Input: Your DIFFERENT teddy bear 🧸
↓ (magic photo booth)
Output: DIFFERENT Photo ID #F6E5D4C3B2A1...
```

### 🎯 Three Magic Rules:

1. **Same thing always gives same photo** 
   - If you put the same teddy bear in twice, you get the exact same photo ID!

2. **Different things give different photos**
   - Even if you change ONE tiny thing, the photo looks completely different!

3. **You can't rebuild the toy from the photo** (ONE-WAY!)
   - If I show you photo #A1B2C3D4, you can't tell if it's a teddy bear, a book, or a car!
   - This is what makes hashing special - **you can't go backwards!** 🚫⬅️

### 📦 Real Example

```
Input: "Hello World"
↓ (SHA-256 hash function)
Output: "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"

Input: "Hello World!" (added one !)
↓ (SHA-256 hash function)
Output: "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069"
         ↑↑↑↑↑ Completely different! ↑↑↑↑↑
```

---

## 🔍 What is a Hash Function?

A **hash function** is a mathematical algorithm that converts data of any size into a fixed-size "fingerprint" (the hash).

### Properties of Good Hash Functions

```
1. DETERMINISTIC
   Hash("Hello") = abc123...
   Hash("Hello") = abc123...  ← Always the same!

2. FAST COMPUTATION
   Hash 1GB file in seconds

3. AVALANCHE EFFECT
   Change 1 bit → Hash changes ~50%
   
4. ONE-WAY (Pre-image Resistance)
   Given hash abc123..., cannot find original input
   
5. COLLISION RESISTANCE
   Hard to find two different inputs with same hash
```

### 📊 Visual Comparison

```
INPUT (any size)          HASH (fixed size)
┌──────────────────┐      ┌──────────────┐
│ "Hello"          │  →   │ b10a8db16... │ (128 bits)
│ (5 bytes)        │      └──────────────┘
└──────────────────┘

┌──────────────────┐      ┌──────────────┐
│ 10GB video file  │  →   │ c3f4e21a8... │ (128 bits)
│ (10,000,000 KB)  │      └──────────────┘
└──────────────────┘

Same size output regardless of input size!
```

---

## 🧮 The Mathematics - Merkle-Damgård Construction

Most modern hash functions (including MD5 and SHA-256) use the **Merkle-Damgård construction**.

### 🏗️ The Basic Idea (Simplified)

```
Step 1: PADDING
Add bits to make message length a multiple of block size

Step 2: SPLIT INTO BLOCKS
Divide padded message into fixed-size chunks

Step 3: ITERATIVE COMPRESSION
Process each block with a compression function

Step 4: FINALIZE
Output the final hash value
```

### 📐 The Algorithm

```
┌─────────────────────────────────────────────────────────┐
│                 Merkle-Damgård Construction             │
└─────────────────────────────────────────────────────────┘

Message: "Hello World" (88 bits)
         ↓
Padding: "Hello World" + padding bits → 512 bits (1 block)
         ↓
         ┌─────────────┐
Initial  │   IV        │  ← Initialization Vector (constant)
State:   │  (fixed)    │
         └──────┬──────┘
                ↓
         ┌──────────────────────────┐
Block 1: │  Compression Function    │ ← Process Block 1
         │  f(IV, Block1)           │
         └──────────┬───────────────┘
                    ↓
         ┌──────────────────────────┐
Block 2: │  Compression Function    │ ← Process Block 2
         │  f(State1, Block2)       │
         └──────────┬───────────────┘
                    ↓
                   ...
                    ↓
         ┌──────────────────────────┐
Final:   │  Hash Value              │
         │  b10a8db164e0754105...   │
         └──────────────────────────┘
```

### 🔬 The Compression Function

For SHA-256, each block processes:

$$H_{i+1} = f(H_i, M_i)$$

Where:
- $H_i$ = Current hash state (256 bits)
- $M_i$ = Message block $i$ (512 bits)
- $f$ = Compression function (64 rounds of bitwise operations)

### 🎯 Why This Design?

**Advantages:**
- ✅ **Efficient**: Process data sequentially (streaming)
- ✅ **Simple**: Same function repeated for each block
- ✅ **Secure**: Collision in any step affects final output

**The Security Proof:**
> "If the compression function is collision-resistant,  
> then the entire hash function is collision-resistant."

---

## 🆚 MD5 vs SHA-256

### MD5 (Message Digest Algorithm 5)

**Created:** 1991 by Ronald Rivest  
**Digest Size:** 128 bits (32 hex characters)  
**Status:** ⚠️ **BROKEN** - Do NOT use for security!

```
Hash("Hello World") = "b10a8db164e0754105b7a99be72e3fe5"
                       ↑                              ↑
                       32 hexadecimal characters
```

#### 💔 The Collision Vulnerability

In **2004**, researchers found that MD5 has **collision vulnerabilities**:

**What's a Collision?**

```
Collision = Two different inputs producing the SAME hash

Input A: "Hello World"     → Hash: abc123...
Input B: "Goodbye World"   → Hash: abc123...  ← SAME! 😱
```

**Why This Breaks Security:**

Imagine an attacker creates two files:
```
File 1: "I owe you $10"     → MD5: xyz789...
File 2: "I owe you $10000"  → MD5: xyz789... ← Same hash!
```

You sign File 1, but attacker can swap in File 2 later! 🚨

#### 🔓 Real-World Attacks

**2008: Flame Malware**
- Used MD5 collision to forge Microsoft certificates
- Allowed malware to appear legitimate
- Affected millions of computers

**Current Status:**
- ❌ Don't use for: Passwords, signatures, certificates
- ✅ Can use for: Non-security checksums (file corruption detection)

---

### SHA-256 (Secure Hash Algorithm 256)

**Created:** 2001 by NSA  
**Digest Size:** 256 bits (64 hex characters)  
**Status:** ✅ **SECURE** - Industry standard!

```
Hash("Hello World") = "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"
                       ↑                                                              ↑
                       64 hexadecimal characters
```

#### ✅ Why SHA-256 is the Standard

**Security Properties:**

1. **Pre-image Resistance** (One-way)
   - Given hash, cannot find original input
   - Would take: $2^{256}$ attempts (longer than age of universe!)

2. **Second Pre-image Resistance**
   - Given input A, cannot find different input B with same hash
   - Would take: $2^{256}$ attempts

3. **Collision Resistance**
   - Cannot find ANY two inputs with same hash
   - Would take: $2^{128}$ attempts (still impossible!)

**Comparison:**

| Feature | MD5 | SHA-256 |
|---------|-----|---------|
| **Bits** | 128 | 256 |
| **Collision Found?** | ✅ Yes (2004) | ❌ No |
| **Time to Break** | Seconds | $2^{128}$ operations |
| **Security** | Broken | Secure |
| **Use For Security?** | ❌ NO | ✅ YES |
| **Speed** | Fast | Slightly slower |

#### 🌍 SHA-256 in the Wild

**Bitcoin Blockchain:**
```
Each block's hash is computed with SHA-256 (twice!)
This secures billions of dollars in cryptocurrency
```

**SSL/TLS Certificates:**
```
Website certificates use SHA-256 for signatures
Every HTTPS connection relies on it
```

**Git Version Control:**
```
Git commit hashes are computed with SHA-256
Ensures code integrity across all developers
```

---

## 💾 Streaming Large Files - The Chunking Magic

### 🎯 The Problem

How do you hash a **10GB video file** without using 10GB of RAM?

```
❌ BAD: Load entire file into memory
   file_content = read_all(10GB_file)  ← Uses 10GB RAM!
   hash(file_content)

✅ GOOD: Read in small chunks
   for chunk in read_chunks(10GB_file, 64KB):  ← Uses only 64KB RAM!
       hash.update(chunk)
```

### 🔧 The Chunking Algorithm

```
CHUNK_SIZE = 65536  # 64KB = 64 * 1024 bytes

Step 1: Initialize hash object
hash_obj = hashlib.sha256()

Step 2: Open file in binary mode
with open(file, 'rb') as f:

    Step 3: Read and process chunks
    while True:
        chunk = f.read(CHUNK_SIZE)  ← Read 64KB
        
        if not chunk:  ← End of file?
            break
        
        hash_obj.update(chunk)  ← Update hash incrementally

Step 4: Get final hash
return hash_obj.hexdigest()
```

### 📊 Memory Usage Visualization

```
BAD APPROACH (Load All):
┌──────────────────────────────────┐
│  RAM Usage: 10GB                 │
│  ████████████████████████████    │
│                                  │
│  Peak: 10,000 MB                 │
└──────────────────────────────────┘

GOOD APPROACH (Streaming):
┌──────────────────────────────────┐
│  RAM Usage: 64KB                 │
│  █                               │
│                                  │
│  Peak: 0.0625 MB                 │
└──────────────────────────────────┘

156,250x less memory! 🚀
```

### ⚡ Performance Metrics

**10GB File Hashing:**

```
Hardware: Modern SSD (500 MB/s read speed)

Time to read file: 10,000 MB ÷ 500 MB/s = 20 seconds
Hashing overhead: ~2 seconds (CPU fast!)
Total time: ~22 seconds

Memory used: 64KB (constant, regardless of file size!)
```

**Why 64KB Chunks?**

```
Too small (4KB):   More read operations, slower
Too large (1MB):   Uses more RAM, diminishing returns
Just right (64KB): Optimal balance! ⚖️
```

### 🔬 The Math Behind Streaming

The hash function is **incremental**:

$$H(\text{File}) = H(M_1 \parallel M_2 \parallel ... \parallel M_n)$$

Where:
- $M_i$ = Chunk $i$ (64KB)
- $\parallel$ = Concatenation

**Key Property:**

$$H_i = f(H_{i-1}, M_i)$$

Each chunk updates the state, so we never need the full file in memory! 🎉

---

## ✅ Checksum Validation

### What is a Checksum?

A **checksum** is a hash value used to verify **data integrity**.

### 🎯 Use Cases

#### 1. **Downloaded File Verification**

```
Website: "Download ubuntu-22.04.iso"
Provided SHA-256: abc123def456...

You download the file:
1. Compute hash of downloaded file
2. Compare with provided hash
3. If match → File is intact! ✓
4. If mismatch → File corrupted or tampered! ✗
```

#### 2. **File Backup Verification**

```
Before backup:
  original.txt → SHA-256: xyz789...

After backup:
  backup.txt → SHA-256: xyz789... ← Match! ✓

Files are bit-identical!
```

#### 3. **Data Corruption Detection**

```
Store file + its hash:
  document.pdf     (1 MB)
  document.sha256  (64 bytes)

Later, check integrity:
  Compute hash(document.pdf)
  Compare with stored hash
  
  Match → No corruption ✓
  Mismatch → File damaged! ⚠️
```

### 📝 Common Checksum Formats

**MD5SUM file:**
```
b10a8db164e0754105b7a99be72e3fe5  file1.txt
c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8  file2.txt
```

**SHA256SUM file:**
```
a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e  ubuntu.iso
```

---

## 💻 Code Implementation

### The `hash_file()` Method

```python
class SHA256Hasher(HasherInterface):
    """
    SHA-256 hash generator with streaming support.
    """
    
    CHUNK_SIZE: int = 65536  # 64KB chunks
    
    def hash_file(self, filepath: str) -> str:
        """
        Generate SHA-256 hash of a file using streaming reads.
        
        This method reads the file in 64KB chunks to prevent memory
        exhaustion on large files (10GB+). The entire file is never
        loaded into memory at once.
        
        Time Complexity: O(n) where n is file size
        Space Complexity: O(1) - only 64KB buffer in memory
        """
        path = Path(filepath)
        
        # Validation
        if not path.exists():
            raise FileOperationError(f"File not found: {filepath}")
        
        if not path.is_file():
            raise FileOperationError(f"Path is not a file: {filepath}")
        
        try:
            # Initialize hash object
            hash_obj = hashlib.sha256()
            
            # Stream file in chunks
            with open(path, 'rb') as f:
                while True:
                    chunk = f.read(self.CHUNK_SIZE)
                    if not chunk:
                        break
                    hash_obj.update(chunk)
            
            # Return hex digest
            return hash_obj.hexdigest()
            
        except PermissionError as e:
            raise FileOperationError(
                f"Permission denied reading file: {filepath}"
            ) from e
        except Exception as e:
            raise HashingError(
                f"SHA-256 file hashing failed: {str(e)}"
            ) from e
```

### The `ChecksumValidator` Class

```python
class ChecksumValidator:
    """
    File integrity validator using cryptographic hashes.
    """
    
    def __init__(self):
        self.hashers = {
            'md5': MD5Hasher(),
            'sha256': SHA256Hasher(),
        }
    
    def compare_files(
        self,
        filepath1: str,
        filepath2: str,
        algorithm: str = "sha256"
    ) -> dict:
        """
        Compare two files by computing and comparing their hashes.
        
        Returns:
            - match (bool): True if files are identical
            - hash1, hash2 (str): Computed hashes
        """
        hasher = self.hashers[algorithm]
        
        # Compute both hashes
        hash1 = hasher.hash_file(filepath1)
        hash2 = hasher.hash_file(filepath2)
        
        # Compare
        match = (hash1 == hash2)
        
        return {
            'match': match,
            'algorithm': algorithm,
            'hash1': hash1,
            'hash2': hash2,
        }
    
    def validate_file(
        self,
        filepath: str,
        expected_hash: str,
        algorithm: str = "sha256"
    ) -> dict:
        """
        Validate a file against a known hash value.
        
        Common use: Verify downloaded files.
        """
        hasher = self.hashers[algorithm]
        
        # Compute file hash
        computed_hash = hasher.hash_file(filepath)
        
        # Compare (case-insensitive)
        match = computed_hash.lower() == expected_hash.lower()
        
        return {
            'match': match,
            'computed_hash': computed_hash,
            'expected_hash': expected_hash,
        }
```

---

## ⚖️ Pros & Cons

### ✅ Pros

| Advantage | Description |
|-----------|-------------|
| **One-Way** | Cannot reverse hash to get original data (security!) |
| **Fixed Size** | Any input → Same size output (256 bits for SHA-256) |
| **Fast** | Hash 10GB file in ~20 seconds |
| **Deterministic** | Same input always gives same hash |
| **Avalanche Effect** | 1-bit change → ~50% hash changes |
| **Collision Resistant** | Hard to find two inputs with same hash (SHA-256) |
| **Streaming** | Can hash files larger than RAM |

### ❌ Cons

| Disadvantage | Description |
|--------------|-------------|
| **Not Encryption** | Cannot decrypt hash back to data |
| **No Key** | Anyone can compute the hash |
| **Rainbow Tables** | Pre-computed hashes for common passwords |
| **MD5 Broken** | Collisions found, not secure |
| **Storage** | Need to store hash separately |
| **One-Way Only** | If you lose data, hash won't help recover it |

### 📊 Comparison Table

| Feature | MD5 | SHA-256 |
|---------|-----|---------|
| **Digest Size** | 128 bits | 256 bits |
| **Speed** | Very fast | Fast |
| **Security** | ❌ Broken | ✅ Secure |
| **Collisions** | ✅ Found | ❌ None known |
| **Use For Security?** | ❌ NO | ✅ YES |
| **Good For Checksums?** | ✅ Yes | ✅ Yes |
| **Memory (10GB file)** | 64KB | 64KB |
| **Bitcoin** | ❌ Not used | ✅ Core algorithm |

---

## 🎮 Try It Yourself

### Using the CLI

```bash
# Launch CryptoSentinel
python cli.py

# Navigate:
# 2. Hashing Tools
# Choose: MD5, SHA-256, or File Checksum
```

### Python Code Examples

#### Hash a String

```python
from crypto_sentinel.hashing import SHA256Hasher

hasher = SHA256Hasher()
hash_value = hasher.hash_string("Hello World")
print(hash_value)
# a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e
```

#### Hash a File (Even 10GB!)

```python
# Works efficiently on huge files!
hash_value = hasher.hash_file("/path/to/large_file.bin")
print(f"SHA-256: {hash_value}")
```

#### Compare Two Files

```python
from crypto_sentinel.hashing import ChecksumValidator

validator = ChecksumValidator()

result = validator.compare_files(
    "original.txt",
    "backup.txt",
    algorithm="sha256"
)

if result['match']:
    print("✓ Files are identical!")
else:
    print("✗ Files differ!")
    print(f"  File 1: {result['hash1']}")
    print(f"  File 2: {result['hash2']}")
```

#### Verify Downloaded File

```python
# Download ubuntu.iso
# Get official SHA-256 from ubuntu.com

result = validator.validate_file(
    "ubuntu-22.04.iso",
    "abc123def456...",  # Official hash
    algorithm="sha256"
)

if result['match']:
    print("✓ File integrity verified!")
else:
    print("⚠️ WARNING: File may be corrupted or tampered!")
```

---

## 🎓 Learning Exercises

### Beginner

1. Hash your name with MD5 and SHA-256 - compare the lengths
2. Change one letter and see how the entire hash changes
3. Why can't you "decrypt" a hash?

### Intermediate

4. Calculate how many possible SHA-256 hashes exist (2^256)
5. Explain why streaming uses O(1) memory
6. Research the "birthday paradox" and collision probability

### Advanced

7. Implement a simple hash function using XOR
8. Calculate the probability of an accidental SHA-256 collision
9. Research the "length extension attack" on SHA-256
10. Compare Merkle-Damgård to sponge construction (SHA-3)

---

## 🔬 Security Analysis

### Brute Force Resistance

```
MD5 (128 bits):
  Possible hashes: 2^128 = 3.4 × 10^38
  @ 10^12 hashes/sec: 10^13 years to try all

SHA-256 (256 bits):
  Possible hashes: 2^256 = 1.15 × 10^77
  @ 10^12 hashes/sec: 3.67 × 10^52 years
  
  (Universe is only 1.38 × 10^10 years old!)
```

### Why Hashing Passwords is Not Enough

```
❌ BAD:
  Store: hash("password123")
  
  Attacker pre-computes hashes of common passwords
  (Rainbow table attack)

✅ GOOD:
  Store: hash("password123" + random_salt)
  
  Salt makes each hash unique
  (Use bcrypt or Argon2 for passwords!)
```

---

## 📚 Further Reading

- **Hash Functions**: [Cryptographic Hash Functions](https://en.wikipedia.org/wiki/Cryptographic_hash_function)
- **Merkle-Damgård**: [Construction Details](https://en.wikipedia.org/wiki/Merkle%E2%80%93Damg%C3%A5rd_construction)
- **MD5 Collisions**: [The Attack That Broke MD5](https://en.wikipedia.org/wiki/MD5#Security)
- **SHA-256**: [Secure Hash Algorithm](https://en.wikipedia.org/wiki/SHA-2)
- **Next Topic**: [Security Tools](Security-Tools.md) - Password analysis

---

## 🔗 Navigation

- [← Back to Home](Home.md)
- [→ Next: Security Tools](Security-Tools.md)
- [↑ Back to Top](#hashing-tools---digital-fingerprints-for-data-integrity)

---

**Author**: saisrujanmurthy@gmail.com  
**Last Updated**: December 30, 2025  
**Difficulty**: ⭐⭐⭐☆☆ (Intermediate)  
**Security Importance**: ⭐⭐⭐⭐⭐ (Critical!)
