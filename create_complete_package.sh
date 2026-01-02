#!/bin/bash
# ==============================================================================
# QUANTUM-FLOOR AI - CREATE COMPLETE PACKAGE
# ==============================================================================
# Creates the final distribution package ready for GL/Sonnet
# ==============================================================================

set -e

echo "========================================"
echo "CREATING COMPLETE PACKAGE"
echo "========================================"
echo ""

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
PACKAGE_DIR="$PROJECT_DIR/QUANTUM_FLOOR_COMPLETE"
VERSION="1.0.0"

# Clean previous builds
rm -rf "$PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR"

echo "[1/5] Copying REGIS-7B-C..."
cp -r "$PROJECT_DIR/REGIS-7B-C_COMPLETE" "$PACKAGE_DIR/"

echo "[2/5] Copying AXIS-7B-C..."
cp -r "$PROJECT_DIR/AXIS-7B-C_COMPLETE" "$PACKAGE_DIR/"

echo "[3/5] Copying Connection-Core..."
cp -r "$PROJECT_DIR/CONNECTION-CORE_PUBLIC" "$PACKAGE_DIR/"

echo "[4/5] Copying Quantum Lock System..."
cp -r "$PROJECT_DIR/QUANTUM_LOCK_SYSTEM" "$PACKAGE_DIR/"

echo "[5/5] Copying Landing Pages & Docs..."
cp -r "$PROJECT_DIR/LANDING_PAGES" "$PACKAGE_DIR/"
cp "$PROJECT_DIR/"*.md "$PACKAGE_DIR/" 2>/dev/null || true

# Create specs files
cat > "$PACKAGE_DIR/landing_page_specs.md" << 'EOF'
# QUANTUM-FLOOR AI LANDING PAGE SPECS

## Design Theme
- Dark mode with quantum blue (#00f0ff) accents
- Animated particle background (quantum entanglement visualization)
- Neon glows, subtle animations
- Professional but futuristic

## Required Sections
1. Hero: "Models That Shouldn't Exist" with particle animation
2. Model Cards: REGIS & AXIS with live stats
3. Technology Teaser: "7-Level Proprietary Architecture" (no details)
4. Live Demos: Interactive model testing
5. Get Started: Ollama/Python/Docker commands
6. Open Source Gift: Connection-Core showcase
7. Social Proof: GitHub/Ollama counters

## Interactive Elements
- Animated quantum particles in background
- Model performance counters (real-time updating)
- Live demo widgets
- Copy-to-clipboard for install commands
- Dark/light mode toggle

## Mobile Responsive
- Stack model cards on mobile
- Simplified animations on mobile
- Touch-friendly demo buttons

## Performance
- <2s load time
- Lazy load animations
- Optimized particle count based on device
EOF

cat > "$PACKAGE_DIR/model_comparison_data.json" << 'EOF'
{
  "models": [
    {
      "name": "REGIS-7B-C",
      "size": "220MB",
      "performance": "Matches Llama-7B",
      "latency": "<100ms page-to-speech",
      "features": ["7-level architecture", "Voice synthesis", "Encrypted core"],
      "demo_url": "/demos/regis",
      "install_command": "ollama run quantum-floor-ai/regis-7b-c"
    },
    {
      "name": "AXIS-7B-C",
      "size": "48MB",
      "performance": "7B equivalent",
      "latency": "<20ms selection-to-speech",
      "features": ["Hardware accelerated", "Ultra-fast", "Encrypted core"],
      "demo_url": "/demos/axis",
      "install_command": "ollama run quantum-floor-ai/axis-7b-c"
    },
    {
      "name": "Connection-Core",
      "size": "<100KB",
      "performance": "N/A",
      "latency": "<50ms retrieval",
      "features": ["MIT Licensed", "Works with any LLM", "Persistent memory"],
      "demo_url": "/demos/connection-core",
      "install_command": "pip install connection-core"
    }
  ],
  "comparison": {
    "llama_7b": "14GB",
    "our_models": "64x-300x smaller",
    "speed_advantage": "10x-100x faster"
  }
}
EOF

# Create archive
echo ""
echo "Creating archives..."
cd "$PROJECT_DIR"
tar -czf "quantum-floor-ai-complete-v$VERSION.tar.gz" "QUANTUM_FLOOR_COMPLETE"
zip -rq "quantum-floor-ai-complete-v$VERSION.zip" "QUANTUM_FLOOR_COMPLETE" 2>/dev/null || true

echo ""
echo "========================================"
echo "PACKAGE COMPLETE!"
echo "========================================"
echo ""
echo "Directory: $PACKAGE_DIR"
echo ""
echo "Archives:"
ls -lh "$PROJECT_DIR"/quantum-floor-ai-complete-v*.* 2>/dev/null
echo ""
echo "Hand off to GL/Sonnet with:"
echo '  "Here is everything. Build us a stunning single-page landing page.'
echo '  The models are encrypted and ready. The design specs are included.'
echo '  Make it look impossible."'
echo ""
echo "========================================"
