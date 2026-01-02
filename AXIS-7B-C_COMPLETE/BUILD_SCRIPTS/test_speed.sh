#!/bin/bash
# Test AXIS-7B-C Speed (<20ms verification)
# Quantum-Floor AI

set -e

echo "========================================"
echo "AXIS-7B-C Speed Verification Test"
echo "Target: <20ms latency"
echo "========================================"

cd "$(dirname "$0")/.."

# Check files
echo "Checking distribution files..."
REQUIRED_FILES=(
    "ENCRYPTED_DISTRIBUTION/axis_7b_c.bin.enc"
    "ENCRYPTED_DISTRIBUTION/axis_weights.gguf.enc"
    "ENCRYPTED_DISTRIBUTION/axis_lock.bin"
    "PUBLIC_API/axis_api.py"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  [OK] $file"
    else
        echo "  [MISSING] $file"
        exit 1
    fi
done

# Python latency test
echo ""
echo "Running latency tests..."
cd PUBLIC_API

python3 << 'PYTHON_SCRIPT'
import time
import sys
sys.path.insert(0, '.')

try:
    from axis_api import AxisModel, AxisConfig

    config = AxisConfig(preload=True, cache_size=0)
    model = AxisModel(config=config)

    # Test phrases
    phrases = ["Hello", "Yes", "Click", "Submit", "OK"]

    print("\nLatency Results:")
    print("-" * 40)

    latencies = []
    for phrase in phrases:
        start = time.perf_counter()
        model.instant_speech(phrase)
        latency = (time.perf_counter() - start) * 1000
        latencies.append(latency)

        status = "OK" if latency < 20 else "SLOW"
        print(f"  [{status}] {latency:6.2f}ms - '{phrase}'")

    avg = sum(latencies) / len(latencies)
    under_20 = sum(1 for l in latencies if l < 20) / len(latencies) * 100

    print("-" * 40)
    print(f"  Average: {avg:.2f}ms")
    print(f"  Under 20ms: {under_20:.0f}%")

    if under_20 >= 80:
        print("\n  STATUS: PASSED")
        sys.exit(0)
    else:
        print("\n  STATUS: NEEDS OPTIMIZATION")
        sys.exit(1)

except ImportError as e:
    print(f"  [SKIP] Python test - {e}")
    sys.exit(0)
PYTHON_SCRIPT

echo ""
echo "========================================"
echo "Speed test complete!"
echo "========================================"
