"""
Comprehensive tests for hashing implementations.

Tests MD5, SHA256 hashers and checksum validator with various scenarios
including temporary file operations.

Author: saisrujanmurthy@gmail.com
"""

import tempfile
import os
from pathlib import Path
import pytest

from crypto_sentinel.hashing import MD5Hasher, SHA256Hasher, ChecksumValidator
from crypto_sentinel.core.exceptions import (
    FileOperationError,
    HashingError,
    ValidationError,
)


class TestMD5Hasher:
    """Test cases for MD5 hasher."""
    
    def test_hash_string_basic(self) -> None:
        """Test basic string hashing."""
        hasher = MD5Hasher()
        result = hasher.hash_string("Hello World")
        assert result == "b10a8db164e0754105b7a99be72e3fe5"
    
    def test_hash_string_empty(self) -> None:
        """Test hashing empty string."""
        hasher = MD5Hasher()
        result = hasher.hash_string("")
        assert result == "d41d8cd98f00b204e9800998ecf8427e"
    
    def test_hash_string_unicode(self) -> None:
        """Test hashing Unicode characters."""
        hasher = MD5Hasher()
        result = hasher.hash_string("Hello 世界")
        assert len(result) == 32  # MD5 always 32 hex chars
        assert all(c in '0123456789abcdef' for c in result)
    
    def test_hash_string_invalid_type(self) -> None:
        """Test that non-string input raises error."""
        hasher = MD5Hasher()
        with pytest.raises(ValidationError):
            hasher.hash_string(12345)
    
    def test_hash_file_temp(self) -> None:
        """Test hashing a temporary file."""
        hasher = MD5Hasher()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Test content for hashing")
            temp_path = f.name
        
        try:
            # Hash the file
            file_hash = hasher.hash_file(temp_path)
            
            # Verify it matches string hash
            string_hash = hasher.hash_string("Test content for hashing")
            assert file_hash == string_hash
            
        finally:
            # Cleanup
            os.unlink(temp_path)
    
    def test_hash_file_large(self) -> None:
        """Test hashing large file with streaming."""
        hasher = MD5Hasher()
        
        # Create large temporary file (1MB)
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            # Write 1MB of data
            data = b"A" * (1024 * 1024)
            f.write(data)
            temp_path = f.name
        
        try:
            # Hash the file (should use streaming)
            file_hash = hasher.hash_file(temp_path)
            
            # Verify hash is correct length
            assert len(file_hash) == 32
            
        finally:
            os.unlink(temp_path)
    
    def test_hash_file_not_found(self) -> None:
        """Test that non-existent file raises error."""
        hasher = MD5Hasher()
        with pytest.raises(FileOperationError):
            hasher.hash_file("/nonexistent/file.txt")
    
    def test_hash_file_directory(self) -> None:
        """Test that directory path raises error."""
        hasher = MD5Hasher()
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(FileOperationError):
                hasher.hash_file(tmpdir)
    
    def test_repr(self) -> None:
        """Test string representation."""
        hasher = MD5Hasher()
        repr_str = repr(hasher)
        assert "MD5" in repr_str
        assert "md5" in repr_str


class TestSHA256Hasher:
    """Test cases for SHA-256 hasher."""
    
    def test_hash_string_basic(self) -> None:
        """Test basic string hashing."""
        hasher = SHA256Hasher()
        result = hasher.hash_string("Hello World")
        assert result == "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"
    
    def test_hash_string_empty(self) -> None:
        """Test hashing empty string."""
        hasher = SHA256Hasher()
        result = hasher.hash_string("")
        assert result == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    
    def test_hash_length(self) -> None:
        """Test that SHA-256 always produces 64-character hash."""
        hasher = SHA256Hasher()
        result = hasher.hash_string("Test")
        assert len(result) == 64
        assert all(c in '0123456789abcdef' for c in result)
    
    def test_hash_deterministic(self) -> None:
        """Test that same input produces same hash."""
        hasher = SHA256Hasher()
        hash1 = hasher.hash_string("Test message")
        hash2 = hasher.hash_string("Test message")
        assert hash1 == hash2
    
    def test_hash_different_inputs(self) -> None:
        """Test that different inputs produce different hashes."""
        hasher = SHA256Hasher()
        hash1 = hasher.hash_string("Message A")
        hash2 = hasher.hash_string("Message B")
        assert hash1 != hash2
    
    def test_hash_file_temp(self) -> None:
        """Test hashing a temporary file matches string hash."""
        hasher = SHA256Hasher()
        
        content = "SHA-256 test content"
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            # Hash file and string
            file_hash = hasher.hash_file(temp_path)
            string_hash = hasher.hash_string(content)
            
            # Should match
            assert file_hash == string_hash
            
        finally:
            os.unlink(temp_path)
    
    def test_hash_file_binary(self) -> None:
        """Test hashing binary file."""
        hasher = SHA256Hasher()
        
        # Create binary file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b"\x00\x01\x02\x03\xff\xfe\xfd")
            temp_path = f.name
        
        try:
            file_hash = hasher.hash_file(temp_path)
            assert len(file_hash) == 64
            
        finally:
            os.unlink(temp_path)
    
    def test_hash_file_streaming(self) -> None:
        """Test that streaming works for files larger than chunk size."""
        hasher = SHA256Hasher()
        
        # Create file larger than chunk size (64KB)
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            # Write 128KB (2 chunks)
            data = b"B" * (128 * 1024)
            f.write(data)
            temp_path = f.name
        
        try:
            file_hash = hasher.hash_file(temp_path)
            assert len(file_hash) == 64
            
        finally:
            os.unlink(temp_path)
    
    def test_repr(self) -> None:
        """Test string representation."""
        hasher = SHA256Hasher()
        repr_str = repr(hasher)
        assert "SHA256" in repr_str


class TestChecksumValidator:
    """Test cases for checksum validator."""
    
    def test_compare_identical_files(self) -> None:
        """Test comparing two identical files."""
        validator = ChecksumValidator()
        
        # Create two identical temp files
        content = "Identical content"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f1:
            f1.write(content)
            path1 = f1.name
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f2:
            f2.write(content)
            path2 = f2.name
        
        try:
            result = validator.compare_files(path1, path2)
            
            assert result['match'] is True
            assert result['hash1'] == result['hash2']
            assert result['algorithm'] == 'sha256'
            
        finally:
            os.unlink(path1)
            os.unlink(path2)
    
    def test_compare_different_files(self) -> None:
        """Test comparing two different files."""
        validator = ChecksumValidator()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f1:
            f1.write("Content A")
            path1 = f1.name
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f2:
            f2.write("Content B")
            path2 = f2.name
        
        try:
            result = validator.compare_files(path1, path2)
            
            assert result['match'] is False
            assert result['hash1'] != result['hash2']
            
        finally:
            os.unlink(path1)
            os.unlink(path2)
    
    def test_compare_with_md5(self) -> None:
        """Test comparing files with MD5 algorithm."""
        validator = ChecksumValidator()
        
        content = "MD5 test"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f1:
            f1.write(content)
            path1 = f1.name
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f2:
            f2.write(content)
            path2 = f2.name
        
        try:
            result = validator.compare_files(path1, path2, algorithm='md5')
            
            assert result['match'] is True
            assert result['algorithm'] == 'md5'
            assert len(result['hash1']) == 32
            
        finally:
            os.unlink(path1)
            os.unlink(path2)
    
    def test_validate_file_match(self) -> None:
        """Test validating file against correct hash."""
        validator = ChecksumValidator()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Test content")
            path = f.name
        
        try:
            # Get the actual hash first
            hasher = SHA256Hasher()
            expected_hash = hasher.hash_string("Test content")
            
            # Validate
            result = validator.validate_file(path, expected_hash)
            
            assert result['match'] is True
            assert result['computed_hash'] == expected_hash
            
        finally:
            os.unlink(path)
    
    def test_validate_file_mismatch(self) -> None:
        """Test validating file against incorrect hash."""
        validator = ChecksumValidator()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Test content")
            path = f.name
        
        try:
            # Use wrong hash
            wrong_hash = "0" * 64
            
            result = validator.validate_file(path, wrong_hash)
            
            assert result['match'] is False
            assert result['expected_hash'] == wrong_hash
            
        finally:
            os.unlink(path)
    
    def test_validate_file_invalid_hash_length(self) -> None:
        """Test that invalid hash length raises error."""
        validator = ChecksumValidator()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Test")
            path = f.name
        
        try:
            with pytest.raises(ValidationError):
                validator.validate_file(path, "too_short")
        finally:
            os.unlink(path)
    
    def test_validate_file_invalid_hash_chars(self) -> None:
        """Test that non-hex hash raises error."""
        validator = ChecksumValidator()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Test")
            path = f.name
        
        try:
            with pytest.raises(ValidationError):
                validator.validate_file(path, "z" * 64)
        finally:
            os.unlink(path)
    
    def test_unsupported_algorithm(self) -> None:
        """Test that unsupported algorithm raises error."""
        validator = ChecksumValidator()
        
        with pytest.raises(ValidationError):
            validator.compare_files("file1", "file2", algorithm='sha512')
    
    def test_generate_report(self) -> None:
        """Test generating comprehensive hash report."""
        validator = ChecksumValidator()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Report test")
            path = f.name
        
        try:
            report = validator.generate_report(path)
            
            assert 'file' in report
            assert 'size' in report
            assert 'hashes' in report
            assert 'md5' in report['hashes']
            assert 'sha256' in report['hashes']
            assert len(report['hashes']['md5']) == 32
            assert len(report['hashes']['sha256']) == 64
            
        finally:
            os.unlink(path)
    
    def test_generate_report_single_algorithm(self) -> None:
        """Test generating report with single algorithm."""
        validator = ChecksumValidator()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Report test")
            path = f.name
        
        try:
            report = validator.generate_report(path, algorithms=['md5'])
            
            assert 'md5' in report['hashes']
            assert 'sha256' not in report['hashes']
            
        finally:
            os.unlink(path)
    
    def test_repr(self) -> None:
        """Test string representation."""
        validator = ChecksumValidator()
        repr_str = repr(validator)
        assert "ChecksumValidator" in repr_str


class TestHashingIntegration:
    """Integration tests across hashing components."""
    
    def test_md5_vs_sha256_same_input(self) -> None:
        """Test that MD5 and SHA-256 produce different hashes for same input."""
        md5 = MD5Hasher()
        sha256 = SHA256Hasher()
        
        data = "Same input"
        
        md5_hash = md5.hash_string(data)
        sha256_hash = sha256.hash_string(data)
        
        assert md5_hash != sha256_hash
        assert len(md5_hash) == 32
        assert len(sha256_hash) == 64
    
    def test_file_integrity_workflow(self) -> None:
        """Test complete file integrity verification workflow."""
        # Create original file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Important data")
            original_path = f.name
        
        try:
            # Compute checksum
            hasher = SHA256Hasher()
            original_hash = hasher.hash_file(original_path)
            
            # Simulate file copy
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                f.write("Important data")
                copy_path = f.name
            
            try:
                # Verify copy
                validator = ChecksumValidator()
                result = validator.validate_file(copy_path, original_hash)
                
                assert result['match'] is True
                
            finally:
                os.unlink(copy_path)
        finally:
            os.unlink(original_path)
