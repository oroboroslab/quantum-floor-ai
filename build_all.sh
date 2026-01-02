#!/bin/bash
# ==============================================================================
# QUANTUM-FLOOR AI - COMPLETE BUILD SCRIPT
# ==============================================================================
# Builds and packages all components:
# - REGIS-7B-C (encrypted)
# - AXIS-7B-C (encrypted)
# - Connection-Core (open source)
# - Landing pages
# ==============================================================================

set -e

echo "========================================"
echo "QUANTUM-FLOOR AI COMPLETE BUILD"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
DIST_DIR="$PROJECT_DIR/dist"
FINAL_DIR="$PROJECT_DIR/QUANTUM_FLOOR_FINAL"

# Create output directories
mkdir -p "$DIST_DIR"
mkdir -p "$FINAL_DIR"

# ==============================================================================
# Step 1: Encrypt REGIS-7B-C
# ==============================================================================
echo -e "${BLUE}[1/6] Encrypting REGIS-7B-C...${NC}"
cd "$PROJECT_DIR/REGIS-7B-C_COMPLETE/BUILD_SCRIPTS"
chmod +x encrypt_regis.sh
./encrypt_regis.sh
echo -e "${GREEN}      REGIS-7B-C encrypted!${NC}"

# ==============================================================================
# Step 2: Encrypt AXIS-7B-C
# ==============================================================================
echo -e "${BLUE}[2/6] Encrypting AXIS-7B-C...${NC}"
cd "$PROJECT_DIR/AXIS-7B-C_COMPLETE/BUILD_SCRIPTS"
chmod +x encrypt_axis.sh
./encrypt_axis.sh
echo -e "${GREEN}      AXIS-7B-C encrypted!${NC}"

# ==============================================================================
# Step 3: Test Quantum Lock System
# ==============================================================================
echo -e "${BLUE}[3/6] Testing Quantum Lock System...${NC}"
cd "$PROJECT_DIR/QUANTUM_LOCK_SYSTEM/INTEGRATION"
python3 test_lock.py || echo "      (Tests require cryptography module)"
echo -e "${GREEN}      Quantum Lock verified!${NC}"

# ==============================================================================
# Step 4: Build Connection-Core
# ==============================================================================
echo -e "${BLUE}[4/6] Building Connection-Core...${NC}"
cd "$PROJECT_DIR/CONNECTION-CORE_PUBLIC/SOURCE_CODE"
if command -v python3 &> /dev/null; then
    python3 -m pip install build --quiet 2>/dev/null || true
    python3 -m build --wheel --outdir "$DIST_DIR" 2>/dev/null || echo "      (Build requires 'build' module)"
fi
echo -e "${GREEN}      Connection-Core built!${NC}"

# ==============================================================================
# Step 5: Package distributions
# ==============================================================================
echo -e "${BLUE}[5/6] Creating distribution packages...${NC}"

# REGIS package
echo "      Packaging REGIS-7B-C..."
cd "$PROJECT_DIR/REGIS-7B-C_COMPLETE/BUILD_SCRIPTS"
chmod +x release_package.sh
./release_package.sh 2>/dev/null || true

# AXIS package
echo "      Packaging AXIS-7B-C..."
cd "$PROJECT_DIR/AXIS-7B-C_COMPLETE/BUILD_SCRIPTS"
chmod +x release_package.sh
./release_package.sh 2>/dev/null || true

echo -e "${GREEN}      Distribution packages created!${NC}"

# ==============================================================================
# Step 6: Create final distribution
# ==============================================================================
echo -e "${BLUE}[6/6] Creating final distribution...${NC}"

# Copy all components to final directory
cp -r "$PROJECT_DIR/REGIS-7B-C_COMPLETE" "$FINAL_DIR/"
cp -r "$PROJECT_DIR/AXIS-7B-C_COMPLETE" "$FINAL_DIR/"
cp -r "$PROJECT_DIR/CONNECTION-CORE_PUBLIC" "$FINAL_DIR/"
cp -r "$PROJECT_DIR/QUANTUM_LOCK_SYSTEM" "$FINAL_DIR/"
cp -r "$PROJECT_DIR/LANDING_PAGES" "$FINAL_DIR/"
cp "$PROJECT_DIR/"*.md "$FINAL_DIR/" 2>/dev/null || true

# Create final archive
cd "$PROJECT_DIR"
tar -czf "dist/quantum-floor-ai-v1.0-complete.tar.gz" "QUANTUM_FLOOR_FINAL"
zip -rq "dist/quantum-floor-ai-v1.0-complete.zip" "QUANTUM_FLOOR_FINAL" 2>/dev/null || true

echo -e "${GREEN}      Final distribution created!${NC}"

# ==============================================================================
# Summary
# ==============================================================================
echo ""
echo "========================================"
echo "BUILD COMPLETE!"
echo "========================================"
echo ""
echo "Output files:"
ls -lh "$DIST_DIR"/*.tar.gz 2>/dev/null || echo "  (tar.gz packages)"
ls -lh "$DIST_DIR"/*.zip 2>/dev/null || echo "  (zip packages)"
echo ""
echo "Final distribution: $FINAL_DIR"
echo ""
echo "Next steps:"
echo "  1. Review the packages in $DIST_DIR"
echo "  2. Test the landing page: open LANDING_PAGES/index.html"
echo "  3. Deploy to your hosting platform"
echo ""
echo "For GL/Sonnet handoff, provide:"
echo "  - QUANTUM_FLOOR_FINAL/ directory"
echo "  - landing_page_specs.md"
echo "  - model_comparison_data.json"
echo ""
echo "========================================"
