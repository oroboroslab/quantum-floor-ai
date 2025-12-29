#!/bin/bash
# Create AXIS-7B-C Release Package
# Quantum-Floor AI

set -e

echo "========================================"
echo "AXIS-7B-C Release Package Builder"
echo "========================================"

VERSION="${1:-1.0.0}"
cd "$(dirname "$0")/.."

./BUILD_SCRIPTS/test_speed.sh

RELEASE_DIR="dist/axis-7b-c-v$VERSION"
rm -rf "$RELEASE_DIR"
mkdir -p "$RELEASE_DIR"

echo "Creating release package..."

cp -r ENCRYPTED_DISTRIBUTION "$RELEASE_DIR/"
cp -r PUBLIC_API "$RELEASE_DIR/"
cp -r DOCUMENTATION "$RELEASE_DIR/"

mkdir -p "$RELEASE_DIR/ollama"
cp OLLAMA_INTEGRATION/Modelfile.axis "$RELEASE_DIR/ollama/"
cp OLLAMA_INTEGRATION/Dockerfile.axis "$RELEASE_DIR/ollama/"

cat > "$RELEASE_DIR/install.sh" << 'EOF'
#!/bin/bash
echo "Installing AXIS-7B-C..."
cd PUBLIC_API && pip install -e . && cd ..
echo "Done! Usage: from axis_api import AxisModel"
EOF
chmod +x "$RELEASE_DIR/install.sh"

cd dist
zip -r "axis-7b-c-v$VERSION.zip" "axis-7b-c-v$VERSION"
tar -czf "axis-7b-c-v$VERSION.tar.gz" "axis-7b-c-v$VERSION"
cd ..

echo "========================================"
echo "Release created!"
ls -lh dist/axis-7b-c-v$VERSION.*
echo "========================================"
