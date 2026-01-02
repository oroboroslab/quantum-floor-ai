#!/usr/bin/env python3
"""
Quantum Lock Creation Tool
==========================

Creates quantum lock files for new models.
"""

import os
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from CORE_LOCK.quantum_lock import QuantumLock
from CORE_LOCK.integrity_verifier import IntegrityVerifier


def create_lock(
    output_path: str,
    model_name: str = "model"
) -> dict:
    """
    Create a new quantum lock.

    Args:
        output_path: Where to save the lock file
        model_name: Name of the model being protected

    Returns:
        Dictionary with lock details
    """
    print(f"Creating quantum lock for {model_name}...")

    # Generate lock
    key = QuantumLock.generate_lock(output_path)

    # Calculate hash
    verifier = IntegrityVerifier()
    lock_hash = verifier.calculate_hash(output_path)

    result = {
        "model_name": model_name,
        "lock_path": output_path,
        "lock_size": os.path.getsize(output_path),
        "lock_hash": lock_hash,
        "key_length": len(key),
    }

    print(f"\nQuantum lock created!")
    print(f"  Path: {output_path}")
    print(f"  Size: {result['lock_size']} bytes")
    print(f"  Hash: {lock_hash[:16]}...")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Create quantum lock for model protection"
    )

    parser.add_argument(
        "output",
        help="Output path for lock file"
    )
    parser.add_argument(
        "--name",
        default="model",
        help="Model name"
    )

    args = parser.parse_args()

    create_lock(args.output, args.name)
    print("\nDone!")


if __name__ == "__main__":
    main()
