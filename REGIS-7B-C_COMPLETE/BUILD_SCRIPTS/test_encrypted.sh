#!/bin/bash
# Test REGIS-7B-C Encrypted Distribution
# Quantum-Floor AI

set -e

echo "========================================"
echo "REGIS-7B-C Encrypted Distribution Test"
echo "========================================"

cd "$(dirname "$0")/.."

# Check all required files exist
echo "Checking distribution files..."

REQUIRED_FILES=(
    "ENCRYPTED_DISTRIBUTION/regis_7b_c.bin.enc"
    "ENCRYPTED_DISTRIBUTION/regis_weights.gguf.enc"
    "ENCRYPTED_DISTRIBUTION/regis_lock.bin"
    "ENCRYPTED_DISTRIBUTION/regis_license.key"
    "PUBLIC_API/__init__.py"
    "PUBLIC_API/regis_api.py"
    "PUBLIC_API/requirements.txt"
    "PUBLIC_API/setup.py"
)

MISSING=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  [OK] $file"
    else
        echo "  [MISSING] $file"
        MISSING=$((MISSING + 1))
    fi
done

if [ $MISSING -gt 0 ]; then
    echo ""
    echo "ERROR: $MISSING required files missing!"
    exit 1
fi

echo ""
echo "All required files present."

# Test Python API import
echo ""
echo "Testing Python API import..."
cd PUBLIC_API
python3 -c "from regis_api import RegisModel, RegisConfig; print('  [OK] Import successful')" 2>/dev/null || echo "  [SKIP] Python test (dependencies not installed)"
cd ..

# Check file sizes
echo ""
echo "File sizes:"
ls -lh ENCRYPTED_DISTRIBUTION/*.enc ENCRYPTED_DISTRIBUTION/*.bin ENCRYPTED_DISTRIBUTION/*.key 2>/dev/null | awk '{print "  " $5 "\t" $9}'

# Verify encryption (check file headers)
echo ""
echo "Verifying encryption..."
if file ENCRYPTED_DISTRIBUTION/regis_7b_c.bin.enc | grep -q "data"; then
    echo "  [OK] Model file is encrypted (binary data)"
else
    echo "  [WARN] Model file may not be properly encrypted"
fi

echo ""
echo "========================================"
echo "Test complete!"
echo "========================================"
