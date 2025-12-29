#!/usr/bin/env python3
"""
AXIS-7B-C Selection-to-Speech Demo
==================================

Demonstrates instant text selection to speech workflow.
Ideal for accessibility and productivity applications.
"""

import time
import sys
from axis_api import AxisModel, AxisConfig


def simulate_text_selection(model: AxisModel, text: str) -> float:
    """
    Simulate selecting text and speaking it.
    Returns latency in milliseconds.
    """
    # Simulate: User selects text -> Instantly speak
    start = time.perf_counter()
    audio = model.selection_to_speech(text)
    latency = (time.perf_counter() - start) * 1000
    return latency


def main():
    print("=" * 60)
    print("AXIS-7B-C Selection-to-Speech Demo")
    print("=" * 60)
    print()
    print("Scenario: User selects text anywhere, instant speech output")
    print("Target: <20ms from selection to audio")
    print()

    # Initialize model
    config = AxisConfig(
        preload=True,
        hardware_acceleration=True,
        voice_quality="balanced"
    )
    model = AxisModel(config=config)

    # Demo 1: Quick selections (typical usage)
    print(">>> Demo 1: Quick Text Selections")
    print("-" * 60)

    quick_selections = [
        "Hello",
        "Submit form",
        "View details",
        "Delete item",
        "Save changes",
        "Close window",
        "Open settings",
        "Log out",
    ]

    latencies = []
    for text in quick_selections:
        latency = simulate_text_selection(model, text)
        latencies.append(latency)
        status = "OK" if latency < 20 else ("WARN" if latency < 50 else "SLOW")
        print(f"  [{status:4}] {latency:6.2f}ms - '{text}'")

    avg_latency = sum(latencies) / len(latencies)
    print()
    print(f"  Average latency: {avg_latency:.2f}ms")
    print(f"  Under 20ms: {sum(1 for l in latencies if l < 20)}/{len(latencies)}")
    print()

    # Demo 2: Longer selections
    print(">>> Demo 2: Longer Text Selections")
    print("-" * 60)

    long_selections = [
        "Please confirm your order before proceeding.",
        "Your session will expire in 5 minutes.",
        "Click here to learn more about our services.",
        "Error: Please check your input and try again.",
    ]

    for text in long_selections:
        latency = simulate_text_selection(model, text)
        status = "OK" if latency < 50 else "SLOW"
        print(f"  [{status:4}] {latency:6.2f}ms")
        print(f"         '{text[:40]}...'")

    print()

    # Demo 3: Continuous reading
    print(">>> Demo 3: Continuous Reading Simulation")
    print("-" * 60)

    paragraphs = [
        "The quick brown fox jumps over the lazy dog.",
        "Pack my box with five dozen liquor jugs.",
        "How vexingly quick daft zebras jump!",
        "The five boxing wizards jump quickly.",
    ]

    print("  Simulating reading a document paragraph by paragraph...")
    total_time = 0
    for i, para in enumerate(paragraphs, 1):
        latency = simulate_text_selection(model, para)
        total_time += latency
        print(f"  Paragraph {i}: {latency:.2f}ms")

    print()
    print(f"  Total processing: {total_time:.0f}ms for {len(paragraphs)} paragraphs")
    print()

    # Usage examples
    print(">>> Integration Examples")
    print("-" * 60)
    print("""
    # System tray integration (Windows/Mac/Linux)
    import keyboard

    model = AxisModel()

    def on_hotkey():
        selected = get_selected_text()  # Platform-specific
        audio = model.selection_to_speech(selected)
        play_audio(audio)

    keyboard.add_hotkey('ctrl+shift+s', on_hotkey)

    # Browser extension integration
    // content.js
    document.addEventListener('mouseup', async () => {
        const selection = window.getSelection().toString();
        if (selection) {
            await fetch('/api/axis/speak', {
                method: 'POST',
                body: JSON.stringify({ text: selection })
            });
        }
    });

    # VS Code extension
    vscode.commands.registerCommand('axis.speakSelection', () => {
        const editor = vscode.window.activeTextEditor;
        const selection = editor.document.getText(editor.selection);
        axisModel.selectionToSpeech(selection);
    });
    """)

    print("=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
