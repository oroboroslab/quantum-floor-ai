#!/bin/bash
# Build REGIS-7B-C Ollama Docker Image
# Quantum-Floor AI

set -e

echo "========================================"
echo "REGIS-7B-C Docker Build"
echo "========================================"

# Configuration
IMAGE_NAME="quantum-floor-ai/regis-7b-c"
VERSION="1.0.0"

cd "$(dirname "$0")/.."

# Check for encrypted files
if [ ! -f "ENCRYPTED_DISTRIBUTION/regis_7b_c.bin.enc" ]; then
    echo "Encrypted files not found. Running encryption first..."
    ./BUILD_SCRIPTS/encrypt_regis.sh
fi

# Build Docker image
echo "Building Docker image..."
docker build \
    -t $IMAGE_NAME:$VERSION \
    -t $IMAGE_NAME:latest \
    -f OLLAMA_INTEGRATION/Dockerfile.regis \
    .

echo "========================================"
echo "Build complete!"
echo ""
echo "Image: $IMAGE_NAME:$VERSION"
echo ""
echo "To run:"
echo "  docker run -e REGIS_LICENSE_KEY=<key> -p 11434:11434 $IMAGE_NAME"
echo "========================================"
