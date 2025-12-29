# Quick Start Guide

Get started with Quantum-Floor AI models in minutes.

## Installation

### Option 1: Ollama (Easiest)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Run REGIS-7B-C
ollama run oroboroslab/regis-7b-c

# Run AXIS-7B-C
ollama run oroboroslab/axis-7b-c
```

### Option 2: Python Package

```bash
# Install packages
pip install regis-7b-c axis-7b-c connection-core

# Set license key (required for REGIS and AXIS)
export REGIS_LICENSE_KEY="your-license-key"
export AXIS_LICENSE_KEY="your-license-key"
```

### Option 3: Docker

```bash
# REGIS-7B-C
docker pull oroboroslab/regis-7b-c
docker run -e REGIS_LICENSE_KEY=<key> -p 11434:11434 oroboroslab/regis-7b-c

# AXIS-7B-C
docker pull oroboroslab/axis-7b-c
docker run -e AXIS_LICENSE_KEY=<key> -p 11434:11434 oroboroslab/axis-7b-c
```

## REGIS-7B-C Examples

### Basic Chat

```python
from regis_api import RegisModel

# Initialize and load
model = RegisModel()
model.load()

# Generate text
response = model.generate("What is machine learning?")
print(response)

# Chat mode
messages = [
    {"role": "user", "content": "Hello!"},
]
response = model.chat(messages)
print(response)
```

### Voice Synthesis

```python
from regis_api import RegisModel

model = RegisModel()
model.load()

# Text to speech
text = "Welcome to Quantum-Floor AI!"
audio = model.text_to_speech(text, output_path="welcome.wav")

# Page to speech
audio = model.page_to_speech(
    "https://example.com/article",
    output_path="article.wav",
    summarize=True
)
```

### Streaming

```python
from regis_api import RegisModel

model = RegisModel()
model.load()

# Stream output
for chunk in model.generate_stream("Write a story about AI"):
    print(chunk, end="", flush=True)
```

## AXIS-7B-C Examples

### Instant Speech (<20ms)

```python
from axis_api import AxisModel, instant_speech

# Using convenience function
audio = instant_speech("Click!")  # <20ms latency

# Or with model instance
model = AxisModel()
audio = model.instant_speech("Button pressed!")
print(f"Latency: {model.last_latency_ms}ms")
```

### Pre-warming Cache

```python
from axis_api import AxisModel

model = AxisModel()

# Pre-cache common UI phrases
common_phrases = [
    "Loading...",
    "Done!",
    "Error",
    "Success",
    "Please wait",
]
model.warm_cache(common_phrases)

# Now these are instant
audio = model.instant_speech("Loading...")  # <5ms from cache
```

### Selection to Speech

```python
from axis_api import AxisModel

model = AxisModel()

def on_text_selected(text):
    """Called when user selects text"""
    audio = model.selection_to_speech(text)
    play_audio(audio)  # Your audio playback function

# Integration example (pseudo-code)
document.on_selection_change(on_text_selected)
```

## Connection-Core Examples

### Basic Memory

```python
from connection_core import MemoryEngine

# Initialize
memory = MemoryEngine()

# Add memories
memory.add("User's name is Alice")
memory.add("User prefers dark mode", importance=0.8)
memory.add("User is a Python developer", tags=["profession"])

# Recall relevant memories
results = memory.recall("What does the user prefer?")
for m in results:
    print(f"[{m.importance:.2f}] {m.content}")
```

### Conversation Memory

```python
from connection_core import MemoryEngine
from connection_core.memory_engine import ConversationMemory

engine = MemoryEngine()
conversation = ConversationMemory(engine)

# Add conversation turns
conversation.add_turn("user", "Hello!")
conversation.add_turn("assistant", "Hi there! How can I help?")
conversation.add_turn("user", "What's the weather?")

# Get recent history
history = conversation.get_recent(5)
for turn in history:
    print(f"{turn.role}: {turn.content}")
```

### Semantic Memory

```python
from connection_core import MemoryEngine
from connection_core.memory_engine import SemanticMemory

engine = MemoryEngine()
semantic = SemanticMemory(engine)

# Store concepts
semantic.add_concept("user.name", "Alice")
semantic.add_concept("user.preferences.theme", "dark")
semantic.add_concept("user.preferences.language", "Python")

# Retrieve concepts
name = semantic.get_concept("user.name")
print(f"User: {name}")

# List all preferences
prefs = semantic.list_concepts("user.preferences")
print(f"Preferences: {prefs}")
```

### REST API Server

```bash
# Start server
python -m connection_core.api --port 8000
```

```python
import requests

# Add memory
requests.post("http://localhost:8000/memories", json={
    "content": "Important fact to remember",
    "importance": 0.9
})

# Recall memories
response = requests.post("http://localhost:8000/recall", json={
    "query": "important facts",
    "limit": 5
})
memories = response.json()["memories"]
```

## License Setup

### Trial License

Trial licenses are included for evaluation:

```python
# Set environment variable
export REGIS_LICENSE_KEY="REGIS-7B-C-LICENSE-TRIAL-2025"
export AXIS_LICENSE_KEY="AXIS-7B-C-LICENSE-TRIAL-2025"
```

Trial limitations:
- 1,000 API calls
- Expires December 31, 2025
- Evaluation use only

### Commercial License

For commercial use:
1. Visit https://quantum-floor.ai/pricing
2. Purchase appropriate license
3. Set license key in environment or code

```python
from regis_api import RegisModel

# Via constructor
model = RegisModel(license_key="YOUR-COMMERCIAL-KEY")

# Or via environment
export QUANTUM_FLOOR_LICENSE="YOUR-COMMERCIAL-KEY"
```

## Troubleshooting

### "License verification failed"
- Check license key is correct
- Ensure license hasn't expired
- Contact support if issue persists

### "Model files not found"
- Ensure complete distribution is downloaded
- Check file paths are correct
- Re-download if files are corrupted

### "CUDA out of memory"
- Use `device="cpu"` for CPU inference
- Reduce `max_tokens` setting
- Close other GPU applications

### "Latency exceeds target"
- Enable hardware acceleration
- Pre-warm cache for common phrases
- Check for background processes

## Next Steps

- [API Reference](API_REFERENCE.md) - Complete API documentation
- [Benchmarks](BENCHMARKS.md) - Performance data
- [Examples](examples/) - More code examples
- [License](LICENSE_COMMERCIAL.md) - License terms

## Support

- Email: oroboros.lab.q@gmail.com
- GitHub: github.com/oroboroslab
- Docs: https://oroboroslab.github.io
