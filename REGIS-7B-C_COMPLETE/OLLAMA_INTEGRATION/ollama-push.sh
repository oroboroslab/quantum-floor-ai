#!/bin/bash
# Push REGIS-7B-C to Ollama Library
# Quantum-Floor AI

set -e

echo "========================================"
echo "REGIS-7B-C Ollama Library Push"
echo "========================================"

# Configuration
MODEL_NAME="oroboroslab/regis-7b-c"
VERSION="1.0.0"

# Check Ollama login
if ! ollama list &> /dev/null; then
    echo "ERROR: Not logged into Ollama. Run 'ollama login' first."
    exit 1
fi

# Build the model
echo "Building model for distribution..."
cd "$(dirname "$0")/.."

# Create the model locally first
echo "Creating local model..."
ollama create $MODEL_NAME -f OLLAMA_INTEGRATION/Modelfile.regis

# Tag with version
echo "Tagging version $VERSION..."
ollama cp $MODEL_NAME $MODEL_NAME:$VERSION
ollama cp $MODEL_NAME $MODEL_NAME:latest

# Push to library
echo "Pushing to Ollama library..."
ollama push $MODEL_NAME:$VERSION
ollama push $MODEL_NAME:latest

echo "========================================"
echo "Push complete!"
echo ""
echo "Users can now run:"
echo "  ollama run $MODEL_NAME"
echo "========================================"
