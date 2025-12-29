#!/bin/bash
# ==============================================================================
# QUANTUM-FLOOR AI - TEST ALL COMPONENTS
# ==============================================================================

set -e

echo "========================================"
echo "QUANTUM-FLOOR AI - TEST SUITE"
echo "========================================"
echo ""

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
PASSED=0
FAILED=0

run_test() {
    local name="$1"
    local cmd="$2"

    echo -n "Testing $name... "
    if eval "$cmd" > /dev/null 2>&1; then
        echo "PASSED"
        ((PASSED++))
    else
        echo "FAILED"
        ((FAILED++))
    fi
}

# Test directory structure
echo "=== Directory Structure ==="
run_test "REGIS-7B-C exists" "[ -d '$PROJECT_DIR/REGIS-7B-C_COMPLETE' ]"
run_test "AXIS-7B-C exists" "[ -d '$PROJECT_DIR/AXIS-7B-C_COMPLETE' ]"
run_test "Quantum Lock exists" "[ -d '$PROJECT_DIR/QUANTUM_LOCK_SYSTEM' ]"
run_test "Connection-Core exists" "[ -d '$PROJECT_DIR/CONNECTION-CORE_PUBLIC' ]"
run_test "Landing Pages exist" "[ -d '$PROJECT_DIR/LANDING_PAGES' ]"
echo ""

# Test key files
echo "=== Key Files ==="
run_test "README.md" "[ -f '$PROJECT_DIR/README.md' ]"
run_test "API_REFERENCE.md" "[ -f '$PROJECT_DIR/API_REFERENCE.md' ]"
run_test "QUICK_START.md" "[ -f '$PROJECT_DIR/QUICK_START.md' ]"
run_test "BENCHMARKS.md" "[ -f '$PROJECT_DIR/BENCHMARKS.md' ]"
run_test "LICENSE_COMMERCIAL.md" "[ -f '$PROJECT_DIR/LICENSE_COMMERCIAL.md' ]"
echo ""

# Test REGIS files
echo "=== REGIS-7B-C Files ==="
run_test "regis_api.py" "[ -f '$PROJECT_DIR/REGIS-7B-C_COMPLETE/PUBLIC_API/regis_api.py' ]"
run_test "ethics.py" "[ -f '$PROJECT_DIR/REGIS-7B-C_COMPLETE/PUBLIC_API/ethics.py' ]"
run_test "Modelfile" "[ -f '$PROJECT_DIR/REGIS-7B-C_COMPLETE/OLLAMA_INTEGRATION/Modelfile.regis' ]"
run_test "Dockerfile" "[ -f '$PROJECT_DIR/REGIS-7B-C_COMPLETE/OLLAMA_INTEGRATION/Dockerfile.regis' ]"
echo ""

# Test AXIS files
echo "=== AXIS-7B-C Files ==="
run_test "axis_api.py" "[ -f '$PROJECT_DIR/AXIS-7B-C_COMPLETE/PUBLIC_API/axis_api.py' ]"
run_test "ethics.py" "[ -f '$PROJECT_DIR/AXIS-7B-C_COMPLETE/PUBLIC_API/ethics.py' ]"
run_test "Modelfile" "[ -f '$PROJECT_DIR/AXIS-7B-C_COMPLETE/OLLAMA_INTEGRATION/Modelfile.axis' ]"
run_test "Dockerfile" "[ -f '$PROJECT_DIR/AXIS-7B-C_COMPLETE/OLLAMA_INTEGRATION/Dockerfile.axis' ]"
echo ""

# Test Quantum Lock files
echo "=== Quantum Lock Files ==="
run_test "quantum_lock.py" "[ -f '$PROJECT_DIR/QUANTUM_LOCK_SYSTEM/CORE_LOCK/quantum_lock.py' ]"
run_test "fernet_manager.py" "[ -f '$PROJECT_DIR/QUANTUM_LOCK_SYSTEM/CORE_LOCK/fernet_manager.py' ]"
run_test "license_check.py" "[ -f '$PROJECT_DIR/QUANTUM_LOCK_SYSTEM/CORE_LOCK/license_check.py' ]"
run_test "license_generator.py" "[ -f '$PROJECT_DIR/QUANTUM_LOCK_SYSTEM/LICENSING/license_generator.py' ]"
echo ""

# Test Connection-Core files
echo "=== Connection-Core Files ==="
run_test "connection_core.py" "[ -f '$PROJECT_DIR/CONNECTION-CORE_PUBLIC/SOURCE_CODE/connection_core.py' ]"
run_test "memory_engine.py" "[ -f '$PROJECT_DIR/CONNECTION-CORE_PUBLIC/SOURCE_CODE/memory_engine.py' ]"
run_test "api.py" "[ -f '$PROJECT_DIR/CONNECTION-CORE_PUBLIC/SOURCE_CODE/api.py' ]"
run_test "MIT License" "[ -f '$PROJECT_DIR/CONNECTION-CORE_PUBLIC/DOCUMENTATION/LICENSE_MIT.txt' ]"
echo ""

# Test Landing Pages
echo "=== Landing Pages ==="
run_test "index.html" "[ -f '$PROJECT_DIR/LANDING_PAGES/index.html' ]"
run_test "style.css" "[ -f '$PROJECT_DIR/LANDING_PAGES/assets/css/style.css' ]"
run_test "particles.js" "[ -f '$PROJECT_DIR/LANDING_PAGES/assets/js/particles.js' ]"
run_test "main.js" "[ -f '$PROJECT_DIR/LANDING_PAGES/assets/js/main.js' ]"
echo ""

# Test build scripts
echo "=== Build Scripts ==="
run_test "build_all.sh" "[ -f '$PROJECT_DIR/build_all.sh' ]"
run_test "create_complete_package.sh" "[ -f '$PROJECT_DIR/create_complete_package.sh' ]"
echo ""

# Summary
echo "========================================"
echo "TEST SUMMARY"
echo "========================================"
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "ALL TESTS PASSED!"
    exit 0
else
    echo "SOME TESTS FAILED"
    exit 1
fi
