#!/usr/bin/env python3
"""
Quantum Lock Test Suite
=======================

Tests quantum lock functionality.
"""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from CORE_LOCK.quantum_lock import QuantumLock
from CORE_LOCK.fernet_manager import FernetManager
from CORE_LOCK.license_check import LicenseChecker, verify_license
from CORE_LOCK.integrity_verifier import IntegrityVerifier


def test_lock_generation():
    """Test lock file generation."""
    print("Testing lock generation...")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as f:
        lock_path = f.name

    try:
        key = QuantumLock.generate_lock(lock_path)

        assert os.path.exists(lock_path), "Lock file not created"
        assert len(key) > 0, "Key is empty"

        # Verify format
        with open(lock_path, "rb") as f:
            data = f.read()
        assert data.startswith(b"QUANTUM_LOCK_V1:"), "Invalid lock format"

        print("  [PASS] Lock generation")
        return True

    finally:
        os.unlink(lock_path)


def test_encryption_decryption():
    """Test encryption and decryption."""
    print("Testing encryption/decryption...")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as f:
        lock_path = f.name

    try:
        # Generate lock
        key = QuantumLock.generate_lock(lock_path)

        # Create lock instance
        lock = QuantumLock(lock_path, "test_model")

        # Verify with any license key (for testing)
        assert lock.verify_license("TEST-LICENSE-KEY"), "License verification failed"

        # Test data
        test_data = b"This is secret model data" * 1000

        # Encrypt
        encrypted = lock.encrypt(test_data)
        assert encrypted != test_data, "Data not encrypted"

        # Decrypt
        decrypted = lock.decrypt(encrypted)
        assert decrypted == test_data, "Decryption failed"

        print("  [PASS] Encryption/decryption")
        return True

    finally:
        os.unlink(lock_path)


def test_license_verification():
    """Test license verification."""
    print("Testing license verification...")

    # Test valid trial license
    valid_key = "REGIS-7B-C-LICENSE-TRIAL-2025"
    assert verify_license(valid_key), "Valid license rejected"

    # Test standard license
    standard_key = "REGIS-7B-C-LICENSE-STANDARD-2025"
    assert verify_license(standard_key), "Standard license rejected"

    # Test expired license
    expired_key = "REGIS-7B-C-LICENSE-TRIAL-2020"
    assert not verify_license(expired_key), "Expired license accepted"

    print("  [PASS] License verification")
    return True


def test_integrity_verification():
    """Test integrity verification."""
    print("Testing integrity verification...")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as f:
        test_file = f.name
        f.write(b"Test file content")

    try:
        verifier = IntegrityVerifier()

        # Calculate hash
        hash1 = verifier.calculate_hash(test_file)
        assert len(hash1) == 64, "Invalid hash length"

        # Verify same hash
        hash2 = verifier.calculate_hash(test_file)
        assert hash1 == hash2, "Hash mismatch for same file"

        # Modify file
        with open(test_file, "ab") as f:
            f.write(b"Modified")

        hash3 = verifier.calculate_hash(test_file)
        assert hash1 != hash3, "Hash unchanged after modification"

        print("  [PASS] Integrity verification")
        return True

    finally:
        os.unlink(test_file)


def test_fernet_manager():
    """Test Fernet manager."""
    print("Testing Fernet manager...")

    manager = FernetManager()

    # Generate key
    key = manager.generate_key()
    assert len(key) > 0, "Key generation failed"

    # Test encryption
    data = b"Secret data"
    encrypted = manager.encrypt(data)
    assert encrypted != data, "Encryption failed"

    # Test decryption
    decrypted = manager.decrypt(encrypted)
    assert decrypted == data, "Decryption failed"

    # Test key derivation from password
    manager2 = FernetManager()
    derived_key, salt = manager2.derive_key_from_password("my_password")

    encrypted2 = manager2.encrypt(data)
    decrypted2 = manager2.decrypt(encrypted2)
    assert decrypted2 == data, "Password-derived encryption failed"

    print("  [PASS] Fernet manager")
    return True


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("QUANTUM LOCK TEST SUITE")
    print("=" * 50)
    print()

    tests = [
        test_lock_generation,
        test_encryption_decryption,
        test_license_verification,
        test_integrity_verification,
        test_fernet_manager,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  [FAIL] {test.__name__}: {e}")
            failed += 1

    print()
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
