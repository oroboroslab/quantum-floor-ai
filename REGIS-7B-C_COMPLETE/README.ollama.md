# REGIS-7B-C

Full-featured language model with integrated voice synthesis. 64x smaller than Llama-7B with equivalent quality.

## Specifications

| Spec | Value |
|------|-------|
| **Size** | 398 MB |
| **Equivalent** | Llama-7B class |
| **Compression** | 64x smaller |
| **Context Window** | 2,048 tokens |
| **Architecture** | Quantum-Floor 7-Level |
| **License** | Commercial |

## Performance

| Metric | Value |
|--------|-------|
| Page-to-Speech | <100ms |
| Memory Usage | ~600 MB RAM |
| Quality | Llama-7B equivalent |
| Compression Ratio | 64:1 |

## Key Features

- **Extreme Compression**: 64x smaller than competitors
- **Integrated Voice**: Built-in text-to-speech synthesis
- **7-Level Architecture**: Proprietary quantum-floor compression
- **Full LLM Capabilities**: Complete language understanding
- **Page-to-Speech**: Convert entire pages to audio

## Use Cases

- Document narration
- Audiobook generation
- Accessibility applications
- Voice-enabled assistants
- Content creation
- Multilingual speech

## Quick Start

```bash
ollama run oroboroslabs/regis-7b-c
```

## API Example

```python
import requests

response = requests.post('http://localhost:11434/api/generate',
    json={
        'model': 'oroboroslabs/regis-7b-c',
        'prompt': 'Introduce yourself',
        'stream': False
    }
)
print(response.json()['response'])
```

## Quantum-Floor AI Family

| Model | Size | Specialty |
|-------|------|-----------|
| AXIS-7B-C | 398 MB | Ultra-Fast (<20ms) |
| **REGIS-7B-C** | 398 MB | Full LLM + Voice |
| CORVUS-1B | 1.3 GB | Edge Deployment |
| CORVUS-3B | 2.0 GB | General Purpose |

## Links

- [Quantum-Floor AI](https://oroboroslab.github.io)
- [GitHub](https://github.com/oroboroslab)

---
**Built by Oroboros Labs** | Quantum-Floor AI Technology
