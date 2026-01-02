# ⚡ QUANTUM-FLOOR AI by Oroboros Labs

**Breaking What Should Be Impossible**

[![License](https://img.shields.io/badge/License-Commercial-blue.svg)](LICENSE_COMMERCIAL.md)
[![MIT License](https://img.shields.io/badge/Connection--Core-MIT-green.svg)](https://github.com/oroboroslab/connection-core)
[![Website](https://img.shields.io/badge/Website-oroboroslab.github.io-purple.svg)](https://oroboroslab.github.io)
[![Connection-Core Docs](https://img.shields.io/badge/Memory%20Docs-connection--core-00d4aa.svg)](https://oroboroslab.github.io/connection-core/)

## THE BREAKTHROUGH

| Model | Size | vs Traditional | Latency | Status |
|-------|------|----------------|---------|--------|
| **REGIS-7B-C** | 220MB | **64X smaller** | <100ms | 🔒 Commercial |
| **AXIS-7B-C** | 48MB | **300X smaller** | <20ms | 🔒 Commercial |
| **Connection-Core** | <100KB | - | <50ms | 🎁 MIT |

### Size Visualization

```
Llama-7B (14GB)
████████████████████████████████████████████████████████████████████████

REGIS-7B-C (220MB) - 64X SMALLER
█

AXIS-7B-C (48MB) - 300X SMALLER
░
```

## WHY IT MATTERS

- **Run 7B AI on a Raspberry Pi** - No more GPU requirements
- **Instant voice response** - <20ms selection-to-speech
- **94% less energy consumption** - Sustainable AI
- **Free AI memory** - Connection-Core for any project (MIT)

## Quick Start

### Via Ollama (Recommended)

```bash
# REGIS-7B-C - Full LLM with voice synthesis
ollama run oroboroslabs/regis-7b-c

# AXIS-7B-C - Ultra-fast (<20ms) speech
ollama run oroboroslabs/axis-7b-c
```

### Via Python

```bash
# Install packages
pip install regis-7b-c axis-7b-c

# Connection-Core is FREE (MIT License)
pip install connection-core
```

```python
# REGIS-7B-C - Full Language Model
from regis_api import RegisModel

model = RegisModel()
response = model.generate("Explain quantum computing")
audio = model.text_to_speech(response)  # <100ms

# AXIS-7B-C - Instant Speech
from axis_api import instant_speech

audio = instant_speech("Hello world!")  # <20ms latency!

# Connection-Core - Free AI Memory
from connection_core import MemoryEngine

memory = MemoryEngine()
memory.add("User prefers dark mode")
relevant = memory.recall("What are user preferences?")
```

### Via Docker

```bash
# REGIS-7B-C
docker run -e REGIS_LICENSE_KEY=<key> -p 11434:11434 oroboroslab/regis-7b-c

# AXIS-7B-C
docker run -e AXIS_LICENSE_KEY=<key> -p 11434:11434 oroboroslab/axis-7b-c
```

## Technology

### 7-Level Architecture

Our proprietary compression technology achieves what was thought impossible:

- **Levels 1-3:** Efficient encoding layers
- **Levels 4-5:** Compressed attention mechanisms
- **Level 6:** Knowledge distillation core
- **Level 7:** Output optimization

*Architecture details are encrypted and protected by Quantum Lock.*

### Quantum Lock Protection

Enterprise-grade encryption protecting our intellectual property:
- Fernet (AES-128-CBC) encryption
- Runtime decryption only
- Anti-tampering detection
- License enforcement

## Models

### REGIS-7B-C

Full-featured language model with integrated voice synthesis.

- **Size:** 220MB (64x smaller than Llama-7B)
- **Performance:** Matches Llama-7B quality
- **Features:** 7-level architecture, voice synthesis, page-to-speech
- **Latency:** <100ms page-to-speech
- **License:** Commercial

### AXIS-7B-C

Ultra-fast model optimized for instant response.

- **Size:** 48MB (300x smaller than Llama-7B)
- **Performance:** 7B equivalent for speech tasks
- **Features:** Hardware acceleration, caching, <20ms latency
- **Latency:** <20ms selection-to-speech
- **License:** Commercial

### Connection-Core (Open Source Gift)

Lightweight memory engine - our gift to the AI community.

- **Size:** <100KB
- **Latency:** <50ms retrieval
- **Features:** Persistent memory, semantic search, conversation history
- **License:** MIT (fully open source)
- **Repository:** [github.com/oroboroslab/connection-core](https://github.com/oroboroslab/connection-core)
- **Documentation:** [oroboroslab.github.io/connection-core](https://oroboroslab.github.io/connection-core/)

## Documentation

- [API Reference](API_REFERENCE.md) - Complete API documentation
- [Quick Start Guide](QUICK_START.md) - Get started in minutes
- [Benchmarks](BENCHMARKS.md) - Performance data
- [Connection-Core Docs](https://oroboroslab.github.io/connection-core/) - Free memory engine documentation
- [Commercial License](LICENSE_COMMERCIAL.md) - License terms

## Contact

**Organization:** Oroboros Labs
**Email:** oroboros.lab.q@gmail.com
**Website:** https://oroboroslab.github.io
**GitHub:** https://github.com/oroboroslab

## License

- **REGIS-7B-C & AXIS-7B-C:** Commercial License (see [LICENSE_COMMERCIAL.md](LICENSE_COMMERCIAL.md))
- **Connection-Core:** MIT License (see [LICENSE_MIT.txt](CONNECTION-CORE_PUBLIC/DOCUMENTATION/LICENSE_MIT.txt))

---

<p align="center">
  <strong>⚡ Oroboros Labs</strong><br>
  <em>Making the impossible, possible since 2024.</em>
</p>
