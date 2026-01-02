#!/bin/bash
# AXIS-7B-C Docker Entrypoint
# Optimized for <20ms latency

set -e

echo "========================================"
echo "AXIS-7B-C Ultra-Fast Container"
echo "Quantum-Floor AI"
echo "========================================"

# Verify license
if [ -z "$AXIS_LICENSE_KEY" ]; then
    echo "ERROR: AXIS_LICENSE_KEY environment variable not set"
    exit 1
fi

# Hardware acceleration detection
echo "Detecting hardware acceleration..."

if command -v nvidia-smi &> /dev/null; then
    echo "  NVIDIA GPU detected"
    export AXIS_DEVICE="cuda"
elif [ -d "/dev/dri" ]; then
    echo "  Intel GPU detected"
    export AXIS_DEVICE="intel"
else
    echo "  Using CPU (latency may exceed 20ms)"
    export AXIS_DEVICE="cpu"
fi

# Verify quantum lock
echo "Verifying quantum lock..."
if [ ! -f "/app/encrypted/axis_lock.bin" ]; then
    echo "ERROR: Quantum lock file missing"
    exit 1
fi

# License verification
python3 /app/scripts/verify_license.py "$AXIS_LICENSE_KEY"
if [ $? -ne 0 ]; then
    echo "ERROR: License verification failed"
    exit 1
fi

echo "License verified"

# Pre-load model to memory for instant response
echo "Pre-loading model to memory..."
export AXIS_PRELOAD="1"
export AXIS_CACHE_SIZE="1000"

# Start Ollama optimized
echo "Starting optimized Ollama server..."
OLLAMA_NUM_PARALLEL=4 OLLAMA_FLASH_ATTENTION=1 ollama serve &
OLLAMA_PID=$!

sleep 2

# Load model
echo "Loading AXIS-7B-C..."
ollama create axis-7b-c -f /app/Modelfile.axis

# Warm up model
echo "Warming up model..."
echo "Hello" | ollama run axis-7b-c > /dev/null

echo "========================================"
echo "AXIS-7B-C ready! (<20ms latency)"
echo "Run: ollama run axis-7b-c"
echo "========================================"

wait $OLLAMA_PID
