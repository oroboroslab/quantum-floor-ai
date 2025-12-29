#!/bin/bash
# Build AXIS-7B-C Ollama Docker Image
# Quantum-Floor AI

set -e

echo "========================================"
echo "AXIS-7B-C Docker Build"
echo "========================================"

IMAGE_NAME="quantum-floor-ai/axis-7b-c"
VERSION="1.0.0"

cd "$(dirname "$0")/.."

if [ ! -f "ENCRYPTED_DISTRIBUTION/axis_7b_c.bin.enc" ]; then
    echo "Running encryption first..."
    ./BUILD_SCRIPTS/encrypt_axis.sh
fi

echo "Building Docker image..."
docker build \
    -t $IMAGE_NAME:$VERSION \
    -t $IMAGE_NAME:latest \
    -f OLLAMA_INTEGRATION/Dockerfile.axis \
    .

echo "========================================"
echo "Build complete!"
echo "Image: $IMAGE_NAME:$VERSION"
echo ""
echo "Run: docker run -e AXIS_LICENSE_KEY=<key> -p 11434:11434 $IMAGE_NAME"
echo "========================================"
