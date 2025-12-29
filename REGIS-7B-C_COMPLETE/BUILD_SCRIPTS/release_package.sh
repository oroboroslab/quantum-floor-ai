#!/bin/bash
# Create REGIS-7B-C Release Package
# Quantum-Floor AI

set -e

echo "========================================"
echo "REGIS-7B-C Release Package Builder"
echo "========================================"

VERSION="${1:-1.0.0}"
cd "$(dirname "$0")/.."

# Run tests first
echo "Running distribution tests..."
./BUILD_SCRIPTS/test_encrypted.sh

# Create release directory
RELEASE_DIR="dist/regis-7b-c-v$VERSION"
rm -rf "$RELEASE_DIR"
mkdir -p "$RELEASE_DIR"

echo ""
echo "Creating release package..."

# Copy encrypted distribution
cp -r ENCRYPTED_DISTRIBUTION "$RELEASE_DIR/"

# Copy public API
cp -r PUBLIC_API "$RELEASE_DIR/"

# Copy documentation
cp -r DOCUMENTATION "$RELEASE_DIR/"

# Copy Ollama files
mkdir -p "$RELEASE_DIR/ollama"
cp OLLAMA_INTEGRATION/Modelfile.regis "$RELEASE_DIR/ollama/"
cp OLLAMA_INTEGRATION/docker-entrypoint.sh "$RELEASE_DIR/ollama/"
cp OLLAMA_INTEGRATION/Dockerfile.regis "$RELEASE_DIR/ollama/"

# Create install script
cat > "$RELEASE_DIR/install.sh" << 'EOF'
#!/bin/bash
# REGIS-7B-C Quick Install

echo "Installing REGIS-7B-C..."

# Install Python package
cd PUBLIC_API
pip install -e .
cd ..

echo "Installation complete!"
echo "Usage: from regis_api import RegisModel"
EOF
chmod +x "$RELEASE_DIR/install.sh"

# Create zip archive
echo "Creating archive..."
cd dist
zip -r "regis-7b-c-v$VERSION.zip" "regis-7b-c-v$VERSION"
cd ..

# Create tar.gz archive
cd dist
tar -czf "regis-7b-c-v$VERSION.tar.gz" "regis-7b-c-v$VERSION"
cd ..

echo ""
echo "========================================"
echo "Release package created!"
echo ""
echo "Files:"
ls -lh dist/regis-7b-c-v$VERSION.* 2>/dev/null
echo ""
echo "Directory: dist/regis-7b-c-v$VERSION/"
echo "========================================"
