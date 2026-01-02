#!/usr/bin/env python3
"""
REGIS-7B-C Voice Synthesis Demo
===============================

Demonstrates the integrated voice synthesis capabilities.
Converts text and web pages to natural speech.
"""

import os
from pathlib import Path
from regis_api import RegisModel, RegisConfig


def main():
    print("=" * 50)
    print("REGIS-7B-C Voice Synthesis Demo")
    print("=" * 50)
    print()

    # Enable voice in config
    config = RegisConfig(
        voice_enabled=True,
        voice_speed=1.0,
        voice_pitch=1.0
    )

    model = RegisModel(config=config)

    print("Loading REGIS-7B-C with voice engine...")
    model.load()
    print("Model and voice engine ready!")
    print()

    # Create output directory
    output_dir = Path("./voice_output")
    output_dir.mkdir(exist_ok=True)

    # Demo 1: Simple text-to-speech
    print(">>> Demo 1: Text-to-Speech")
    print("-" * 50)

    text = "Hello! I am REGIS, a 220 megabyte language model with integrated voice synthesis."
    print(f"Text: {text}")

    audio = model.text_to_speech(
        text,
        output_path=str(output_dir / "demo1_hello.wav")
    )
    print(f"Audio saved: {output_dir / 'demo1_hello.wav'}")
    print(f"Audio size: {len(audio)} bytes")
    print()

    # Demo 2: Generate and speak
    print(">>> Demo 2: Generate + Speak")
    print("-" * 50)

    prompt = "Explain AI in one sentence."
    response = model.generate(prompt, max_tokens=100)
    print(f"Prompt: {prompt}")
    print(f"Response: {response}")

    audio = model.text_to_speech(
        response,
        output_path=str(output_dir / "demo2_explanation.wav"),
        speed=1.1  # Slightly faster
    )
    print(f"Audio saved: {output_dir / 'demo2_explanation.wav'}")
    print()

    # Demo 3: Different voice settings
    print(">>> Demo 3: Voice Variations")
    print("-" * 50)

    sample_text = "The quick brown fox jumps over the lazy dog."

    # Normal
    model.text_to_speech(
        sample_text,
        output_path=str(output_dir / "demo3_normal.wav"),
        speed=1.0,
        pitch=1.0
    )
    print("Normal voice saved: demo3_normal.wav")

    # Slow
    model.text_to_speech(
        sample_text,
        output_path=str(output_dir / "demo3_slow.wav"),
        speed=0.7,
        pitch=1.0
    )
    print("Slow voice saved: demo3_slow.wav")

    # Fast
    model.text_to_speech(
        sample_text,
        output_path=str(output_dir / "demo3_fast.wav"),
        speed=1.5,
        pitch=1.0
    )
    print("Fast voice saved: demo3_fast.wav")

    # High pitch
    model.text_to_speech(
        sample_text,
        output_path=str(output_dir / "demo3_high.wav"),
        speed=1.0,
        pitch=1.3
    )
    print("High pitch saved: demo3_high.wav")

    # Low pitch
    model.text_to_speech(
        sample_text,
        output_path=str(output_dir / "demo3_low.wav"),
        speed=1.0,
        pitch=0.7
    )
    print("Low pitch saved: demo3_low.wav")
    print()

    # Demo 4: Page-to-speech (if URL provided)
    print(">>> Demo 4: Page-to-Speech")
    print("-" * 50)
    print("Usage: model.page_to_speech('https://example.com')")
    print("This will fetch, summarize, and speak web content.")
    print("Latency: <100ms for most pages")
    print()

    # Cleanup
    model.unload()
    print("=" * 50)
    print(f"Demo complete! Audio files saved to: {output_dir.absolute()}")
    print("=" * 50)


if __name__ == "__main__":
    main()
