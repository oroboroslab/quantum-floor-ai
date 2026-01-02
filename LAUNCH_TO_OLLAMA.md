# Ollama Library Publication Guide

## Prerequisites

1. **Sign up at ollama.com**
   - Go to https://ollama.com/signup
   - Create account with username: `oroboroslab`

2. **Login to Ollama CLI**
   ```bash
   ollama login
   ```

## Models Ready for Push

Both models are built and ready locally:

| Model | Local Name | Size |
|-------|------------|------|
| REGIS-7B-C | `oroboroslab/regis-7b-c:latest` | 397 MB |
| AXIS-7B-C | `oroboroslab/axis-7b-c:latest` | 397 MB |

## Push Commands

After logging in with the `oroboroslab` account:

```bash
# Push REGIS-7B-C
ollama push oroboroslab/regis-7b-c:latest
ollama push oroboroslab/regis-7b-c:1.0.0

# Push AXIS-7B-C
ollama push oroboroslab/axis-7b-c:latest
ollama push oroboroslab/axis-7b-c:1.0.0
```

## Verify Publication

After pushing, verify at:
- https://ollama.com/oroboroslab/regis-7b-c
- https://ollama.com/oroboroslab/axis-7b-c

## User Installation

Once published, users can run:

```bash
# REGIS-7B-C - Full LLM with voice synthesis
ollama run oroboroslab/regis-7b-c

# AXIS-7B-C - Ultra-fast (<20ms) speech
ollama run oroboroslab/axis-7b-c
```

## Local Testing

Test locally before pushing:

```bash
# Test REGIS
ollama run oroboroslab/regis-7b-c "Hello, introduce yourself"

# Test AXIS
ollama run oroboroslab/axis-7b-c "Hello"
```

## Troubleshooting

### "Not authorized to push"
- Ensure you're logged in: `ollama login`
- Verify namespace ownership at ollama.com

### Model not found
- Rebuild with: `ollama create oroboroslab/regis-7b-c -f REGIS-7B-C_COMPLETE/OLLAMA_INTEGRATION/Modelfile.regis`
