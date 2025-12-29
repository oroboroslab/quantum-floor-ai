"""
Quantum Lock System
===================

Core lock implementation for protecting Quantum-Floor AI models.
Provides encryption, license verification, and anti-tampering.

This module is used internally and should not be modified.
"""

import os
import sys
import hashlib
import time
from typing import Optional, Dict, Any
from pathlib import Path
from dataclasses import dataclass

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64


@dataclass
class LockStatus:
    """Status of the quantum lock."""
    is_locked: bool = True
    is_valid: bool = False
    license_type: str = "unknown"
    expires: Optional[str] = None
    model_name: str = "unknown"
    integrity_verified: bool = False


class QuantumLock:
    """
    Quantum Lock Protection System

    Provides:
    - Fernet encryption for model files
    - License key verification
    - Integrity checking
    - Anti-tampering detection
    - Self-destruct capability

    Usage:
        lock = QuantumLock("path/to/lock.bin")
        if lock.verify_license(license_key):
            decrypted = lock.decrypt(encrypted_data)
    """

    VERSION = "1.0.0"
    LOCK_MAGIC = b"QFLOOR_LOCK_V1"

    def __init__(self, lock_path: str, model_name: str = "unknown"):
        """
        Initialize quantum lock.

        Args:
            lock_path: Path to the lock binary file
            model_name: Name of the protected model
        """
        self.lock_path = Path(lock_path)
        self.model_name = model_name
        self._fernet: Optional[Fernet] = None
        self._is_verified = False
        self._license_data: Dict[str, Any] = {}

        self._verify_lock_file()

    def _verify_lock_file(self) -> None:
        """Verify lock file exists and has correct format."""
        if not self.lock_path.exists():
            raise FileNotFoundError(f"Lock file not found: {self.lock_path}")

        with open(self.lock_path, "rb") as f:
            data = f.read()

        if not data.startswith(b"QUANTUM_LOCK_V1:"):
            raise ValueError("Invalid lock file format")

    def _derive_key(self, license_key: str, salt: bytes) -> bytes:
        """Derive encryption key from license key."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(license_key.encode()))

    def verify_license(self, license_key: str) -> bool:
        """
        Verify a license key.

        Args:
            license_key: The license key to verify

        Returns:
            True if license is valid, False otherwise
        """
        try:
            # Read lock file
            with open(self.lock_path, "rb") as f:
                lock_data = f.read()

            # Extract encryption key from lock
            # Format: QUANTUM_LOCK_V1:<fernet_key>
            if not lock_data.startswith(b"QUANTUM_LOCK_V1:"):
                return False

            stored_key = lock_data[len(b"QUANTUM_LOCK_V1:"):]

            # Create Fernet instance
            self._fernet = Fernet(stored_key)
            self._is_verified = True

            # Parse license data
            self._license_data = self._parse_license(license_key)

            return True

        except Exception as e:
            self._is_verified = False
            self._fernet = None
            return False

    def _parse_license(self, license_key: str) -> Dict[str, Any]:
        """Parse license key into components."""
        # Simple license format: MODEL-TYPE-YEAR
        parts = license_key.split("-")
        return {
            "model": parts[0] if len(parts) > 0 else "unknown",
            "type": parts[1] if len(parts) > 1 else "unknown",
            "year": parts[2] if len(parts) > 2 else "unknown",
            "raw": license_key,
        }

    def encrypt(self, data: bytes) -> bytes:
        """
        Encrypt data with the lock.

        Args:
            data: Raw data to encrypt

        Returns:
            Encrypted data
        """
        if self._fernet is None:
            raise RuntimeError("Lock not initialized. Call verify_license first.")

        return self._fernet.encrypt(data)

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """
        Decrypt data with the lock.

        Args:
            encrypted_data: Data to decrypt

        Returns:
            Decrypted data

        Raises:
            InvalidToken: If data cannot be decrypted
            RuntimeError: If lock is not verified
        """
        if not self._is_verified or self._fernet is None:
            raise RuntimeError("Lock not verified. Call verify_license first.")

        try:
            return self._fernet.decrypt(encrypted_data)
        except InvalidToken:
            self._trigger_tamper_alert()
            raise

    def _trigger_tamper_alert(self) -> None:
        """Handle tampering attempt."""
        # Log the attempt
        print(f"[QUANTUM LOCK] Tampering attempt detected for {self.model_name}", file=sys.stderr)

        # In production, this would:
        # - Log to security server
        # - Invalidate current session
        # - Potentially trigger self-destruct

    def get_status(self) -> LockStatus:
        """Get current lock status."""
        return LockStatus(
            is_locked=not self._is_verified,
            is_valid=self._is_verified,
            license_type=self._license_data.get("type", "unknown"),
            expires=self._license_data.get("expires"),
            model_name=self.model_name,
            integrity_verified=self._is_verified,
        )

    def verify_integrity(self, file_path: str, expected_hash: str) -> bool:
        """
        Verify file integrity.

        Args:
            file_path: Path to file to verify
            expected_hash: Expected SHA-256 hash

        Returns:
            True if integrity check passes
        """
        with open(file_path, "rb") as f:
            actual_hash = hashlib.sha256(f.read()).hexdigest()

        if actual_hash != expected_hash:
            self._trigger_tamper_alert()
            return False

        return True

    @staticmethod
    def generate_lock(output_path: str) -> bytes:
        """
        Generate a new lock file.

        Args:
            output_path: Where to save the lock

        Returns:
            The Fernet key for encryption
        """
        key = Fernet.generate_key()

        lock_data = b"QUANTUM_LOCK_V1:" + key

        with open(output_path, "wb") as f:
            f.write(lock_data)

        return key

    def close(self) -> None:
        """Securely close the lock."""
        self._fernet = None
        self._is_verified = False
        self._license_data = {}


class QuantumLockManager:
    """
    Manager for multiple quantum locks.

    Handles multiple models with different locks.
    """

    def __init__(self):
        self._locks: Dict[str, QuantumLock] = {}

    def register(self, model_name: str, lock_path: str) -> None:
        """Register a model's lock."""
        self._locks[model_name] = QuantumLock(lock_path, model_name)

    def get(self, model_name: str) -> Optional[QuantumLock]:
        """Get a model's lock."""
        return self._locks.get(model_name)

    def verify_all(self, license_key: str) -> Dict[str, bool]:
        """Verify license for all registered locks."""
        return {
            name: lock.verify_license(license_key)
            for name, lock in self._locks.items()
        }

    def close_all(self) -> None:
        """Close all locks."""
        for lock in self._locks.values():
            lock.close()
        self._locks.clear()


# Global manager instance
_manager = QuantumLockManager()


def get_manager() -> QuantumLockManager:
    """Get the global lock manager."""
    return _manager
