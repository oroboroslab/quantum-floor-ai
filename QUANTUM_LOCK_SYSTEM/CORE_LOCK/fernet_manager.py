"""
Fernet Encryption Manager
=========================

Manages Fernet encryption/decryption operations for Quantum Lock.
"""

import os
import base64
from typing import Optional, Tuple
from pathlib import Path

from cryptography.fernet import Fernet, MultiFernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class FernetManager:
    """
    Manages Fernet encryption operations.

    Supports:
    - Single key encryption
    - Key rotation (MultiFernet)
    - Password-based key derivation
    - Secure key generation
    """

    def __init__(self):
        self._fernet: Optional[Fernet] = None
        self._multi_fernet: Optional[MultiFernet] = None
        self._key: Optional[bytes] = None

    def generate_key(self) -> bytes:
        """Generate a new Fernet key."""
        self._key = Fernet.generate_key()
        self._fernet = Fernet(self._key)
        return self._key

    def load_key(self, key: bytes) -> None:
        """Load an existing Fernet key."""
        self._key = key
        self._fernet = Fernet(key)

    def load_key_from_file(self, key_path: str) -> None:
        """Load key from file."""
        with open(key_path, "rb") as f:
            self.load_key(f.read())

    def save_key_to_file(self, key_path: str) -> None:
        """Save key to file."""
        if self._key is None:
            raise ValueError("No key loaded")

        with open(key_path, "wb") as f:
            f.write(self._key)

    def derive_key_from_password(
        self,
        password: str,
        salt: Optional[bytes] = None
    ) -> Tuple[bytes, bytes]:
        """
        Derive a Fernet key from a password.

        Args:
            password: Password to derive from
            salt: Optional salt (generated if not provided)

        Returns:
            Tuple of (key, salt)
        """
        if salt is None:
            salt = os.urandom(16)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,  # OWASP recommended
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.load_key(key)

        return key, salt

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data."""
        if self._fernet is None:
            raise ValueError("No key loaded")

        return self._fernet.encrypt(data)

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Decrypt data."""
        if self._fernet is None:
            raise ValueError("No key loaded")

        return self._fernet.decrypt(encrypted_data)

    def encrypt_file(self, input_path: str, output_path: str) -> None:
        """Encrypt a file."""
        with open(input_path, "rb") as f:
            data = f.read()

        encrypted = self.encrypt(data)

        with open(output_path, "wb") as f:
            f.write(encrypted)

    def decrypt_file(self, input_path: str, output_path: str) -> None:
        """Decrypt a file."""
        with open(input_path, "rb") as f:
            encrypted = f.read()

        decrypted = self.decrypt(encrypted)

        with open(output_path, "wb") as f:
            f.write(decrypted)

    def decrypt_to_memory(self, input_path: str) -> bytes:
        """Decrypt file to memory only (never written to disk)."""
        with open(input_path, "rb") as f:
            encrypted = f.read()

        return self.decrypt(encrypted)

    # Key rotation support
    def setup_key_rotation(self, new_key: bytes, old_keys: list) -> None:
        """
        Setup key rotation with MultiFernet.

        Args:
            new_key: New primary key
            old_keys: List of old keys (for decryption only)
        """
        all_keys = [Fernet(new_key)] + [Fernet(k) for k in old_keys]
        self._multi_fernet = MultiFernet(all_keys)
        self._key = new_key
        self._fernet = Fernet(new_key)

    def rotate_encrypt(self, encrypted_data: bytes) -> bytes:
        """Re-encrypt data with the new key."""
        if self._multi_fernet is None:
            raise ValueError("Key rotation not configured")

        return self._multi_fernet.rotate(encrypted_data)

    def clear(self) -> None:
        """Securely clear all keys from memory."""
        self._fernet = None
        self._multi_fernet = None
        self._key = None


# Convenience functions
def encrypt_model(model_path: str, output_path: str, key: Optional[bytes] = None) -> bytes:
    """
    Encrypt a model file.

    Args:
        model_path: Path to model file
        output_path: Path for encrypted output
        key: Optional key (generated if not provided)

    Returns:
        The encryption key
    """
    manager = FernetManager()

    if key is None:
        key = manager.generate_key()
    else:
        manager.load_key(key)

    manager.encrypt_file(model_path, output_path)

    return key


def decrypt_model_to_memory(encrypted_path: str, key: bytes) -> bytes:
    """
    Decrypt a model file to memory only.

    Args:
        encrypted_path: Path to encrypted file
        key: Decryption key

    Returns:
        Decrypted model data
    """
    manager = FernetManager()
    manager.load_key(key)
    return manager.decrypt_to_memory(encrypted_path)
