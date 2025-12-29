# API Reference

Complete API documentation for Quantum-Floor AI models.

## REGIS-7B-C API

### RegisModel

```python
from regis_api import RegisModel, RegisConfig

model = RegisModel(config=None, license_key=None)
```

**Parameters:**
- `config` (RegisConfig, optional): Model configuration
- `license_key` (str, optional): License key (uses env var if not provided)

### RegisConfig

```python
config = RegisConfig(
    max_tokens=2048,       # Maximum tokens to generate
    temperature=0.7,       # Sampling temperature (0-1)
    top_p=0.9,            # Nucleus sampling threshold
    top_k=40,             # Top-k sampling
    repetition_penalty=1.1,# Repetition penalty
    voice_enabled=True,    # Enable voice synthesis
    voice_speed=1.0,      # Voice speed (0.5-2.0)
    voice_pitch=1.0,      # Voice pitch (0.5-2.0)
    stream=False,         # Enable streaming
    device="auto",        # Device: "auto", "cuda", "cpu"
)
```

### Methods

#### load()
```python
model.load(device=None) -> RegisModel
```
Load model into memory.

#### generate()
```python
model.generate(
    prompt: str,
    max_tokens: int = None,
    temperature: float = None,
    stream: bool = None,
    **kwargs
) -> str
```
Generate text from prompt.

#### generate_stream()
```python
model.generate_stream(prompt: str, **kwargs) -> Generator[str, None, None]
```
Generate text with streaming output.

#### chat()
```python
model.chat(
    messages: List[Dict[str, str]],
    **kwargs
) -> str
```
Multi-turn chat interface.

**messages format:**
```python
[
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi there!"},
    {"role": "user", "content": "How are you?"}
]
```

#### text_to_speech()
```python
model.text_to_speech(
    text: str,
    output_path: str = None,
    speed: float = None,
    pitch: float = None
) -> bytes
```
Convert text to speech audio (WAV format).

#### page_to_speech()
```python
model.page_to_speech(
    url: str,
    output_path: str = None,
    summarize: bool = True
) -> bytes
```
Convert webpage content to speech.

#### unload()
```python
model.unload() -> None
```
Unload model from memory.

### Convenience Functions

```python
from regis_api import generate, chat, text_to_speech

# Quick generation
response = generate("Hello, how are you?")

# Quick chat
response = chat([{"role": "user", "content": "Hi!"}])

# Quick TTS
audio = text_to_speech("Hello world")
```

---

## AXIS-7B-C API

### AxisModel

```python
from axis_api import AxisModel, AxisConfig

model = AxisModel(config=None, license_key=None)
```

### AxisConfig

```python
config = AxisConfig(
    preload=True,              # Keep model in memory
    hardware_acceleration=True, # Use GPU/NPU
    cache_size=1000,           # Cache recent outputs
    batch_processing=False,    # Batch mode
    voice_speed=1.0,          # Voice speed
    voice_pitch=1.0,          # Voice pitch
    voice_quality="balanced", # "fast", "balanced", "quality"
    target_latency_ms=20,     # Target latency
    max_latency_ms=50,        # Max acceptable latency
    device="auto",            # Device selection
)
```

### Methods

#### instant_speech()
```python
model.instant_speech(
    text: str,
    output_path: str = None,
    **kwargs
) -> bytes
```
Convert text to speech with <20ms latency.

#### selection_to_speech()
```python
model.selection_to_speech(
    text: str,
    callback: Callable[[bytes], None] = None
) -> bytes
```
Instantly speak selected text.

#### batch_speech()
```python
model.batch_speech(
    texts: List[str],
    parallel: bool = True
) -> List[bytes]
```
Generate speech for multiple texts.

#### warm_cache()
```python
model.warm_cache(common_phrases: List[str]) -> None
```
Pre-generate audio for common phrases.

#### get_stats()
```python
model.get_stats() -> dict
```
Get performance statistics.

### Convenience Functions

```python
from axis_api import instant_speech, selection_to_speech

# Instant speech (<20ms)
audio = instant_speech("Click!")

# Selection to speech
audio = selection_to_speech("Selected text")
```

---

## Connection-Core API

### MemoryEngine

```python
from connection_core import MemoryEngine, MemoryConfig

engine = MemoryEngine(config=None)
```

### MemoryConfig

```python
config = MemoryConfig(
    storage_path="memory.db",    # SQLite database path
    max_memories=10000,          # Maximum memories to store
    default_importance=0.5,      # Default importance (0-1)
    decay_rate=0.001,           # Daily importance decay
    min_importance=0.1,         # Minimum importance threshold
    embedding_enabled=False,    # Enable semantic embeddings
)
```

### Methods

#### add()
```python
engine.add(
    content: str,
    importance: float = None,
    tags: List[str] = None,
    metadata: Dict[str, Any] = None
) -> Memory
```
Add a new memory.

#### recall()
```python
engine.recall(
    query: str,
    limit: int = 5,
    min_importance: float = None,
    tags: List[str] = None
) -> List[Memory]
```
Recall memories relevant to query.

#### get()
```python
engine.get(memory_id: str) -> Optional[Memory]
```
Get a specific memory by ID.

#### update()
```python
engine.update(
    memory_id: str,
    content: str = None,
    importance: float = None,
    tags: List[str] = None,
    metadata: Dict[str, Any] = None
) -> Optional[Memory]
```
Update an existing memory.

#### delete()
```python
engine.delete(memory_id: str) -> bool
```
Delete a memory.

#### clear()
```python
engine.clear() -> int
```
Clear all memories. Returns count deleted.

#### count()
```python
engine.count() -> int
```
Get total memory count.

#### get_stats()
```python
engine.get_stats() -> Dict[str, Any]
```
Get memory statistics.

#### export()
```python
engine.export(output_path: str) -> int
```
Export memories to JSON file.

#### import_memories()
```python
engine.import_memories(input_path: str) -> int
```
Import memories from JSON file.

### Memory Object

```python
@dataclass
class Memory:
    id: str
    content: str
    created_at: float
    importance: float
    tags: List[str]
    metadata: Dict[str, Any]
    access_count: int
    last_accessed: Optional[float]
```

### Extended Memory Classes

#### ConversationMemory
```python
from connection_core import ConversationMemory

conv = ConversationMemory(engine, max_turns=100)
conv.add_turn("user", "Hello!")
conv.add_turn("assistant", "Hi there!")
history = conv.get_recent(10)
```

#### SemanticMemory
```python
from connection_core import SemanticMemory

semantic = SemanticMemory(engine)
semantic.add_concept("user.name", "Alice")
name = semantic.get_concept("user.name")
```

---

## REST API

Connection-Core includes a REST API server.

### Start Server
```bash
python -m connection_core.api --port 8000
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| GET | /stats | Memory statistics |
| GET | /memories | List memories |
| GET | /memories/:id | Get memory |
| POST | /memories | Create memory |
| POST | /recall | Recall memories |
| PUT | /memories/:id | Update memory |
| DELETE | /memories/:id | Delete memory |
| DELETE | /memories | Clear all |

### Examples

```bash
# Create memory
curl -X POST http://localhost:8000/memories \
  -H "Content-Type: application/json" \
  -d '{"content": "User prefers dark mode", "importance": 0.8}'

# Recall memories
curl -X POST http://localhost:8000/recall \
  -H "Content-Type: application/json" \
  -d '{"query": "user preferences", "limit": 5}'
```

---

## Environment Variables

| Variable | Model | Description |
|----------|-------|-------------|
| REGIS_LICENSE_KEY | REGIS | License key |
| AXIS_LICENSE_KEY | AXIS | License key |
| QUANTUM_FLOOR_LICENSE | Both | Universal license key |

---

## Error Handling

All APIs raise specific exceptions:

```python
from regis_api import RegisModel

try:
    model = RegisModel()
    model.load()
except RuntimeError as e:
    if "license" in str(e).lower():
        print("Invalid license")
    elif "missing" in str(e).lower():
        print("Model files missing")
```

---

## Performance Tips

### REGIS-7B-C
- Use GPU for best performance
- Enable streaming for long generations
- Cache common responses

### AXIS-7B-C
- Pre-warm cache with common phrases
- Keep model loaded (preload=True)
- Use hardware acceleration

### Connection-Core
- Set appropriate max_memories limit
- Use tags for efficient filtering
- Call decay_importance() periodically
