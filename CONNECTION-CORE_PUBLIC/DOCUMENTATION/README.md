# Connection-Core

**Persistent Memory for AI - Our Gift to the Community**

A lightweight, open-source memory engine that gives any AI persistent memory.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE_MIT.txt)
[![PyPI](https://img.shields.io/pypi/v/connection-core.svg)](https://pypi.org/project/connection-core/)

## Features

- **<100KB footprint** - Minimal dependencies, SQLite-based
- **<50ms retrieval** - Fast semantic search
- **Works with any LLM** - Framework agnostic
- **MIT Licensed** - Use freely in any project

## Installation

```bash
pip install connection-core
```

## Quick Start

```python
from connection_core import MemoryEngine

# Initialize
memory = MemoryEngine()

# Add memories
memory.add("User's name is Alice")
memory.add("User prefers dark mode", importance=0.8)

# Recall relevant memories
results = memory.recall("What is the user's name?")
print(results[0].content)  # "User's name is Alice"

# Stats
print(memory.get_stats())
# {'total_memories': 2, 'database_size_kb': 12.5, ...}
```

## Why Connection-Core?

Most AI assistants forget everything between sessions. Connection-Core solves this:

| Feature | Without Memory | With Connection-Core |
|---------|----------------|---------------------|
| Remember user name | No | Yes |
| Track preferences | No | Yes |
| Learn from conversations | No | Yes |
| Improve over time | No | Yes |

## Use Cases

### Chatbots

```python
from connection_core import MemoryEngine
from connection_core.memory_engine import ConversationMemory

engine = MemoryEngine()
conversation = ConversationMemory(engine)

# Store conversation
conversation.add_turn("user", "My name is Alice")
conversation.add_turn("assistant", "Nice to meet you, Alice!")

# Later session
history = conversation.get_recent(10)
```

### Coding Assistants

```python
from connection_core.memory_engine import SemanticMemory

semantic = SemanticMemory(engine)

# Store project knowledge
semantic.add_concept("project.framework", "FastAPI")
semantic.add_concept("project.database", "PostgreSQL")

# Retrieve
framework = semantic.get_concept("project.framework")
```

### Research Tools

```python
# Store findings
engine.add("Finding: X improves Y by 50%",
           importance=0.9,
           tags=["research", "results"])

# Recall by topic
findings = engine.recall("research findings about X")
```

## API Reference

### MemoryEngine

```python
engine = MemoryEngine(config=None)

# Add memory
memory = engine.add(
    content="Important fact",
    importance=0.8,
    tags=["tag1", "tag2"],
    metadata={"source": "user"}
)

# Recall memories
memories = engine.recall(
    query="search term",
    limit=5,
    min_importance=0.5
)

# Get by ID
memory = engine.get(memory_id)

# Update
memory = engine.update(memory_id, content="Updated")

# Delete
engine.delete(memory_id)

# Stats
stats = engine.get_stats()
```

### Configuration

```python
from connection_core import MemoryConfig

config = MemoryConfig(
    storage_path="memory.db",
    max_memories=10000,
    default_importance=0.5,
    decay_rate=0.001,
)

engine = MemoryEngine(config)
```

## REST API

Start the server:

```bash
python -m connection_core.api --port 8000
```

Endpoints:

```
GET  /health          - Health check
GET  /stats           - Statistics
GET  /memories        - List memories
POST /memories        - Create memory
POST /recall          - Recall memories
PUT  /memories/:id    - Update memory
DELETE /memories/:id  - Delete memory
```

## Performance

| Operation | Latency |
|-----------|---------|
| Add | 2ms |
| Recall | 15ms |
| Get by ID | 1ms |

| Memory Count | DB Size |
|--------------|---------|
| 1,000 | 95KB |
| 10,000 | 850KB |
| 100,000 | 8.2MB |

## Contributing

Contributions welcome! Please read our contributing guidelines.

```bash
git clone https://github.com/quantum-floor-ai/connection-core
cd connection-core
pip install -e ".[dev]"
pytest
```

## License

MIT License - see [LICENSE_MIT.txt](LICENSE_MIT.txt)

**Free for personal and commercial use.**

## About

Connection-Core is developed by Quantum-Floor AI as an open-source gift to the AI community.

- Website: https://quantum-floor.ai
- GitHub: https://github.com/quantum-floor-ai/connection-core
- PyPI: https://pypi.org/project/connection-core/
