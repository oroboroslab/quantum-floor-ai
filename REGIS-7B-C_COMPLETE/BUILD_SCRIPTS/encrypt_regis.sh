#!/bin/bash
# Encrypt REGIS-7B-C Source Files
# Quantum-Floor AI

set -e

echo "========================================"
echo "REGIS-7B-C Encryption Script"
echo "========================================"

# Configuration
SOURCE_DIR="../SOURCE_CORE"
OUTPUT_DIR="../ENCRYPTED_DISTRIBUTION"
KEY_FILE="../QUANTUM_LOCK_SYSTEM/master.key"

# Check for source files
if [ ! -d "$SOURCE_DIR" ]; then
    echo "WARNING: Source directory not found. Creating placeholder encrypted files."

    mkdir -p "$OUTPUT_DIR"

    # Create placeholder encrypted files
    echo "Creating placeholder encrypted model..."
    python3 << 'PYTHON_SCRIPT'
import os
from cryptography.fernet import Fernet

# Generate key
key = Fernet.generate_key()
f = Fernet(key)

# Create placeholder model data
model_data = b"REGIS-7B-C ENCRYPTED MODEL CORE - PLACEHOLDER"
weights_data = b"REGIS-7B-C ENCRYPTED WEIGHTS - PLACEHOLDER" * 1000  # ~50KB placeholder

# Encrypt
encrypted_model = f.encrypt(model_data)
encrypted_weights = f.encrypt(weights_data)

# Write encrypted files
output_dir = "../ENCRYPTED_DISTRIBUTION"
os.makedirs(output_dir, exist_ok=True)

with open(f"{output_dir}/regis_7b_c.bin.enc", "wb") as file:
    file.write(encrypted_model)

with open(f"{output_dir}/regis_weights.gguf.enc", "wb") as file:
    file.write(encrypted_weights)

# Create lock file
lock_data = b"QUANTUM_LOCK_V1:" + key
with open(f"{output_dir}/regis_lock.bin", "wb") as file:
    file.write(lock_data)

# Create license key
license_data = f"REGIS-7B-C-LICENSE-TRIAL-2025\nExpires: 2025-12-31\nType: Trial\n"
with open(f"{output_dir}/regis_license.key", "w") as file:
    file.write(license_data)

print("Placeholder encrypted files created successfully!")
PYTHON_SCRIPT

    exit 0
fi

# Actual encryption (when source files exist)
echo "Encrypting source files..."
python3 encrypt_model.py \
    --source "$SOURCE_DIR" \
    --output "$OUTPUT_DIR" \
    --key "$KEY_FILE"

echo "========================================"
echo "Encryption complete!"
echo "Output: $OUTPUT_DIR"
echo "========================================"
