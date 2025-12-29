#!/usr/bin/env python3
"""
Model Encryption Tool
=====================

Encrypts model files with Quantum Lock protection.
"""

import os
import sys
import argparse
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from CORE_LOCK.fernet_manager import FernetManager
from CORE_LOCK.quantum_lock import QuantumLock
from CORE_LOCK.integrity_verifier import IntegrityVerifier


def encrypt_model(
    source_path: str,
    output_path: str,
    lock_path: str,
    model_name: str = "model"
) -> dict:
    """
    Encrypt a model file with Quantum Lock.

    Args:
        source_path: Path to source model file
        output_path: Path for encrypted output
        lock_path: Path to save lock file
        model_name: Name for the model

    Returns:
        Dictionary with encryption details
    """
    print(f"Encrypting {model_name}...")
    print(f"  Source: {source_path}")
    print(f"  Output: {output_path}")
    print(f"  Lock: {lock_path}")

    # Generate lock file and get key
    print("\nGenerating quantum lock...")
    key = QuantumLock.generate_lock(lock_path)

    # Encrypt model
    print("Encrypting model file...")
    manager = FernetManager()
    manager.load_key(key)

    with open(source_path, "rb") as f:
        source_data = f.read()

    encrypted_data = manager.encrypt(source_data)

    with open(output_path, "wb") as f:
        f.write(encrypted_data)

    # Calculate hashes for integrity verification
    print("Calculating integrity hashes...")
    verifier = IntegrityVerifier()
    source_hash = verifier.calculate_hash(source_path)
    output_hash = verifier.calculate_hash(output_path)
    lock_hash = verifier.calculate_hash(lock_path)

    result = {
        "model_name": model_name,
        "source_path": source_path,
        "source_size": os.path.getsize(source_path),
        "source_hash": source_hash,
        "output_path": output_path,
        "output_size": os.path.getsize(output_path),
        "output_hash": output_hash,
        "lock_path": lock_path,
        "lock_hash": lock_hash,
        "encryption": "Fernet (AES-128-CBC)",
    }

    print("\nEncryption complete!")
    print(f"  Source size: {result['source_size']:,} bytes")
    print(f"  Encrypted size: {result['output_size']:,} bytes")

    return result


def encrypt_directory(
    source_dir: str,
    output_dir: str,
    lock_path: str,
    patterns: list = None
) -> list:
    """
    Encrypt all matching files in a directory.

    Args:
        source_dir: Source directory
        output_dir: Output directory
        lock_path: Path for lock file
        patterns: File patterns to match

    Returns:
        List of encryption results
    """
    import glob

    if patterns is None:
        patterns = ["*.bin", "*.gguf", "*.pt", "*.pth", "*.safetensors"]

    source_path = Path(source_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Find all matching files
    files = []
    for pattern in patterns:
        files.extend(glob.glob(str(source_path / pattern)))

    if not files:
        print(f"No files found matching patterns: {patterns}")
        return []

    # Generate single lock for all files
    key = QuantumLock.generate_lock(lock_path)

    manager = FernetManager()
    manager.load_key(key)

    results = []
    for file_path in files:
        file_name = Path(file_path).name
        enc_path = output_path / f"{file_name}.enc"

        print(f"Encrypting {file_name}...")

        with open(file_path, "rb") as f:
            data = f.read()

        encrypted = manager.encrypt(data)

        with open(enc_path, "wb") as f:
            f.write(encrypted)

        results.append({
            "source": file_path,
            "output": str(enc_path),
            "source_size": os.path.getsize(file_path),
            "output_size": os.path.getsize(enc_path),
        })

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Encrypt model files with Quantum Lock"
    )

    parser.add_argument(
        "source",
        help="Source file or directory"
    )
    parser.add_argument(
        "output",
        help="Output file or directory"
    )
    parser.add_argument(
        "--lock",
        default="quantum_lock.bin",
        help="Path for lock file (default: quantum_lock.bin)"
    )
    parser.add_argument(
        "--name",
        default="model",
        help="Model name for logging"
    )
    parser.add_argument(
        "--directory",
        "-d",
        action="store_true",
        help="Encrypt entire directory"
    )
    parser.add_argument(
        "--patterns",
        nargs="+",
        default=["*.bin", "*.gguf"],
        help="File patterns for directory mode"
    )

    args = parser.parse_args()

    if args.directory:
        results = encrypt_directory(
            args.source,
            args.output,
            args.lock,
            args.patterns
        )
        print(f"\nEncrypted {len(results)} files")
    else:
        result = encrypt_model(
            args.source,
            args.output,
            args.lock,
            args.name
        )

    print("\nDone!")


if __name__ == "__main__":
    main()
