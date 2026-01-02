#!/bin/bash
# Push AXIS-7B-C to Ollama Library
# Quantum-Floor AI

set -e

echo "========================================"
echo "AXIS-7B-C Ollama Library Push"
echo "========================================"

MODEL_NAME="oroboroslab/axis-7b-c"
VERSION="1.0.0"

if ! ollama list &> /dev/null; then
    echo "ERROR: Not logged into Ollama"
    exit 1
fi

cd "$(dirname "$0")/.."

echo "Creating local model..."
ollama create $MODEL_NAME -f OLLAMA_INTEGRATION/Modelfile.axis

echo "Tagging..."
ollama cp $MODEL_NAME $MODEL_NAME:$VERSION
ollama cp $MODEL_NAME $MODEL_NAME:latest

echo "Pushing..."
ollama push $MODEL_NAME:$VERSION
ollama push $MODEL_NAME:latest

echo "========================================"
echo "Done! Run: ollama run $MODEL_NAME"
echo "========================================"
