#!/usr/bin/env python3
"""
Demonstration script for CryptoSentinel hashing and security modules.

Shows all implemented features including MD5/SHA256 hashing, file checksums,
password analysis with entropy calculation, and Base64 encoding.

Developer: saisrujanmurthy@gmail.com
"""

from crypto_sentinel.hashing import MD5Hasher, SHA256Hasher, ChecksumValidator
from crypto_sentinel.security import PasswordAnalyzer, Base64Encoder
import tempfile
import os


def demo_hashing():
    """Demonstrate hashing functionality."""
    print("\n" + "="*70)
    print("HASHING MODULE DEMONSTRATION")
    print("="*70)
    
    # MD5 Hasher
    print("\n1. MD5 Hasher")
    print("-" * 70)
    md5 = MD5Hasher()
    test_string = "CryptoSentinel Framework"
    hash_result = md5.hash_string(test_string)
    print(f"Input: '{test_string}'")
    print(f"MD5 Hash: {hash_result}")
    print(f"Properties: {md5.algorithm_name}, {md5.digest_size} bytes")
    
    # SHA-256 Hasher
    print("\n2. SHA-256 Hasher")
    print("-" * 70)
    sha256 = SHA256Hasher()
    hash_result = sha256.hash_string(test_string)
    print(f"Input: '{test_string}'")
    print(f"SHA-256 Hash: {hash_result}")
    print(f"Properties: {sha256.algorithm_name}, {sha256.digest_size} bytes")
    
    # File Hashing with Streaming
    print("\n3. File Hashing with Streaming (64KB chunks)")
    print("-" * 70)
    
    # Create temp file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        content = "Large file content that would be read in chunks..."
        f.write(content)
        temp_path = f.name
    
    try:
        file_hash = sha256.hash_file(temp_path)
        string_hash = sha256.hash_string(content)
        print(f"File path: {temp_path}")
        print(f"File hash:   {file_hash}")
        print(f"String hash: {string_hash}")
        print(f"Match: {file_hash == string_hash} ✓")
    finally:
        os.unlink(temp_path)
    
    # Checksum Validator
    print("\n4. Checksum Validator")
    print("-" * 70)
    validator = ChecksumValidator()
    
    # Create two files
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f1:
        f1.write("File content A")
        path1 = f1.name
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f2:
        f2.write("File content A")
        path2 = f2.name
    
    try:
        result = validator.compare_files(path1, path2, algorithm='sha256')
        print(f"File 1: {path1}")
        print(f"File 2: {path2}")
        print(f"Algorithm: {result['algorithm'].upper()}")
        print(f"Match: {result['match']} ✓")
        print(f"Hash 1: {result['hash1'][:32]}...")
        print(f"Hash 2: {result['hash2'][:32]}...")
    finally:
        os.unlink(path1)
        os.unlink(path2)
    
    # Generate comprehensive report
    print("\n5. Comprehensive Hash Report")
    print("-" * 70)
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("Report test file")
        temp_path = f.name
    
    try:
        report = validator.generate_report(temp_path)
        print(f"File: {report['file']}")
        print(f"Size: {report['size']} bytes")
        print(f"MD5:    {report['hashes']['md5']}")
        print(f"SHA256: {report['hashes']['sha256']}")
    finally:
        os.unlink(temp_path)


def demo_password_analyzer():
    """Demonstrate password analysis with entropy calculation."""
    print("\n" + "="*70)
    print("PASSWORD ANALYZER DEMONSTRATION")
    print("="*70)
    
    analyzer = PasswordAnalyzer()
    
    passwords = [
        ("password123", "Very weak - common pattern"),
        ("Password123", "Weak - needs special chars"),
        ("Tr0ub4dor&3", "Strong - good mix"),
        ("Correct-Horse-Battery-Staple", "Very strong - passphrase"),
    ]
    
    print(f"\nAnalyzer: {analyzer.analyzer_name} v{analyzer.version}")
    print(f"Entropy Formula: E = L × log₂(R)")
    print(f"Attack Rate: {analyzer.GUESSES_PER_SECOND:.0e} guesses/second\n")
    
    for i, (pwd, desc) in enumerate(passwords, 1):
        print(f"\n{i}. Password: '{pwd}' ({desc})")
        print("-" * 70)
        
        result = analyzer.analyze(pwd)
        
        print(f"Score:       {result['score']}/100")
        print(f"Strength:    {result['strength_level'].upper()}")
        print(f"Length:      {result['length']} characters")
        print(f"Pool Size:   {result['pool_size']} (character types used)")
        print(f"Entropy:     {result['entropy_bits']} bits")
        print(f"Crack Time:  {result['crack_time_display']}")
        
        if result['recommendations']:
            print(f"\nRecommendations:")
            for rec in result['recommendations'][:3]:  # Show first 3
                print(f"  • {rec}")


def demo_base64_encoder():
    """Demonstrate Base64 encoding with auto-padding."""
    print("\n" + "="*70)
    print("BASE64 ENCODER DEMONSTRATION")
    print("="*70)
    
    encoder = Base64Encoder()
    
    # String encoding
    print("\n1. String Encoding/Decoding")
    print("-" * 70)
    text = "Hello, CryptoSentinel!"
    encoded = encoder.encrypt(text)
    decoded = encoder.decrypt(encoded)
    print(f"Original:  '{text}'")
    print(f"Encoded:   '{encoded}'")
    print(f"Decoded:   '{decoded}'")
    print(f"Match:     {text == decoded} ✓")
    
    # Auto-padding correction
    print("\n2. Auto-Padding Correction")
    print("-" * 70)
    malformed = "SGVsbG8"  # Missing padding
    corrected = encoder._fix_padding(malformed)
    decoded = encoder.decrypt(malformed)
    print(f"Malformed:  '{malformed}' (missing padding)")
    print(f"Corrected:  '{corrected}'")
    print(f"Decoded:    '{decoded}' ✓")
    
    # Binary data
    print("\n3. Binary Data Encoding")
    print("-" * 70)
    binary = b"\x00\x01\x02\xff\xfe\xfd"
    encoded = encoder.encode_bytes(binary)
    decoded_bytes = encoder.decode_bytes(encoded)
    print(f"Binary:    {binary.hex()}")
    print(f"Encoded:   '{encoded}'")
    print(f"Decoded:   {decoded_bytes.hex()}")
    print(f"Match:     {binary == decoded_bytes} ✓")
    
    # Validation
    print("\n4. Base64 Validation")
    print("-" * 70)
    valid_b64 = "SGVsbG8="
    invalid_b64 = "Not Base64!"
    print(f"'{valid_b64}' is valid: {encoder.is_valid_base64(valid_b64)} ✓")
    print(f"'{invalid_b64}' is valid: {encoder.is_valid_base64(invalid_b64)}")


def main():
    """Run all demonstrations."""
    print("\n" + "#"*70)
    print("#" + " "*20 + "CRYPTOSENTINEL DEMO" + " "*21 + "#")
    print("#" + " "*12 + "Hashing & Security Modules" + " "*21 + "#")
    print("#"*70)
    
    demo_hashing()
    demo_password_analyzer()
    demo_base64_encoder()
    
    print("\n" + "="*70)
    print("✅ ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
    print("="*70)
    print("\nImplemented Features:")
    print("  ✓ MD5 & SHA-256 hashers with streaming file support (64KB chunks)")
    print("  ✓ Checksum validator for file integrity verification")
    print("  ✓ Password analyzer with Shannon entropy calculation")
    print("  ✓ Time-to-crack estimation (10^10 guesses/sec)")
    print("  ✓ Base64 encoder with automatic padding correction")
    print("  ✓ Comprehensive error handling and validation")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
