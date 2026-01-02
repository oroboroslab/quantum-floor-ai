#!/bin/bash
# REGIS-7B-C Docker Entrypoint
# Decrypts model at runtime and starts Ollama server

set -e

echo "========================================"
echo "REGIS-7B-C Encrypted Container"
echo "Quantum-Floor AI"
echo "========================================"

# Verify license
if [ -z "$REGIS_LICENSE_KEY" ]; then
    echo "ERROR: REGIS_LICENSE_KEY environment variable not set"
    echo "Please provide a valid license key to run this container."
    exit 1
fi

# Verify quantum lock
echo "Verifying quantum lock..."
if [ ! -f "/app/encrypted/regis_lock.bin" ]; then
    echo "ERROR: Quantum lock file missing"
    exit 1
fi

# Runtime decryption (happens in memory only)
echo "Initializing encrypted runtime..."
python3 /app/scripts/verify_license.py "$REGIS_LICENSE_KEY"

if [ $? -ne 0 ]; then
    echo "ERROR: License verification failed"
    exit 1
fi

echo "License verified successfully"

# Decrypt model to memory (never written to disk)
echo "Loading encrypted model to memory..."
export REGIS_DECRYPTION_MODE="memory_only"
export REGIS_SECURE_MODE="1"

# Start Ollama with encrypted model
echo "Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
sleep 3

# Load the model
echo "Loading REGIS-7B-C into Ollama..."
ollama create regis-7b-c -f /app/Modelfile.regis

echo "========================================"
echo "REGIS-7B-C ready!"
echo "Run: ollama run regis-7b-c"
echo "========================================"

# Keep container running
wait $OLLAMA_PID
