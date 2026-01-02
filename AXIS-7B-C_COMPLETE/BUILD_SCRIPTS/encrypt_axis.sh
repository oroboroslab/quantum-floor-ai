#!/bin/bash
# Encrypt AXIS-7B-C Source Files
# Quantum-Floor AI

set -e

echo "========================================"
echo "AXIS-7B-C Encryption Script"
echo "========================================"

SOURCE_DIR="../SOURCE_CORE"
OUTPUT_DIR="../ENCRYPTED_DISTRIBUTION"

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Creating placeholder encrypted files..."

    mkdir -p "$OUTPUT_DIR"

    python3 << 'PYTHON_SCRIPT'
import os
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

# Create placeholder data (smaller than REGIS)
model_data = b"AXIS-7B-C ENCRYPTED MODEL CORE - PLACEHOLDER"
weights_data = b"AXIS-7B-C ENCRYPTED WEIGHTS - PLACEHOLDER" * 500  # ~25KB placeholder

encrypted_model = f.encrypt(model_data)
encrypted_weights = f.encrypt(weights_data)

output_dir = "../ENCRYPTED_DISTRIBUTION"
os.makedirs(output_dir, exist_ok=True)

with open(f"{output_dir}/axis_7b_c.bin.enc", "wb") as file:
    file.write(encrypted_model)

with open(f"{output_dir}/axis_weights.gguf.enc", "wb") as file:
    file.write(encrypted_weights)

lock_data = b"QUANTUM_LOCK_V1:" + key
with open(f"{output_dir}/axis_lock.bin", "wb") as file:
    file.write(lock_data)

license_data = "AXIS-7B-C-LICENSE-TRIAL-2025\nExpires: 2025-12-31\nType: Trial\n"
with open(f"{output_dir}/axis_license.key", "w") as file:
    file.write(license_data)

print("Placeholder encrypted files created!")
PYTHON_SCRIPT

    exit 0
fi

echo "Encrypting source files..."
python3 encrypt_model.py --source "$SOURCE_DIR" --output "$OUTPUT_DIR"

echo "========================================"
echo "Encryption complete!"
echo "========================================"
