#!/usr/bin/env python3
"""
REGIS-7B-C Basic Chat Example
=============================

Demonstrates basic chat functionality with REGIS-7B-C.
"""

from regis_api import RegisModel, RegisConfig


def main():
    print("=" * 50)
    print("REGIS-7B-C Basic Chat Demo")
    print("=" * 50)
    print()

    # Initialize with custom config
    config = RegisConfig(
        max_tokens=512,
        temperature=0.8,
        voice_enabled=False  # Text only for this demo
    )

    # Create model instance
    model = RegisModel(config=config)

    print("Loading REGIS-7B-C (220MB)...")
    model.load()
    print("Model loaded successfully!")
    print()

    # Simple generation
    print(">>> Generating response to: 'What is quantum computing?'")
    print("-" * 50)
    response = model.generate("What is quantum computing? Explain in simple terms.")
    print(response)
    print()

    # Multi-turn chat
    print(">>> Multi-turn conversation:")
    print("-" * 50)

    messages = [
        {"role": "user", "content": "Hello! I'm learning about AI."},
    ]

    response = model.chat(messages)
    print(f"User: {messages[0]['content']}")
    print(f"REGIS: {response}")
    print()

    messages.append({"role": "assistant", "content": response})
    messages.append({"role": "user", "content": "What makes your architecture special?"})

    response = model.chat(messages)
    print(f"User: {messages[-1]['content']}")
    print(f"REGIS: {response}")
    print()

    # Streaming example
    print(">>> Streaming generation:")
    print("-" * 50)
    print("REGIS: ", end="", flush=True)
    for chunk in model.generate_stream("Tell me a short story about AI."):
        print(chunk, end="", flush=True)
    print("\n")

    # Cleanup
    model.unload()
    print("Model unloaded. Demo complete!")


if __name__ == "__main__":
    main()
