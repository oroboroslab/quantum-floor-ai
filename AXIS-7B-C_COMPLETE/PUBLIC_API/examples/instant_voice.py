#!/usr/bin/env python3
"""
AXIS-7B-C Instant Voice Demo
============================

Demonstrates the <20ms latency capability of AXIS-7B-C.
"""

import time
from axis_api import AxisModel, AxisConfig


def main():
    print("=" * 50)
    print("AXIS-7B-C Instant Voice Demo")
    print("Target: <20ms latency")
    print("=" * 50)
    print()

    # Initialize with speed optimizations
    config = AxisConfig(
        preload=True,
        hardware_acceleration=True,
        cache_size=500,
        voice_quality="fast"
    )

    model = AxisModel(config=config)

    print(f"Model loaded: {model.is_loaded}")
    print()

    # Demo 1: Single instant speech
    print(">>> Demo 1: Instant Speech")
    print("-" * 50)

    test_phrases = [
        "Hello!",
        "Click confirmed.",
        "Processing complete.",
        "Welcome back.",
        "Error detected.",
    ]

    for phrase in test_phrases:
        start = time.perf_counter()
        audio = model.instant_speech(phrase)
        latency = (time.perf_counter() - start) * 1000

        status = "OK" if latency < 20 else "SLOW"
        print(f"  [{status}] '{phrase}' - {latency:.2f}ms")

    print()

    # Demo 2: Cached performance
    print(">>> Demo 2: Cached Performance")
    print("-" * 50)

    phrase = "This phrase will be cached."

    # First call (generates)
    start = time.perf_counter()
    model.instant_speech(phrase)
    first_latency = (time.perf_counter() - start) * 1000

    # Second call (cached)
    start = time.perf_counter()
    model.instant_speech(phrase)
    cached_latency = (time.perf_counter() - start) * 1000

    print(f"  First call:  {first_latency:.2f}ms")
    print(f"  Cached call: {cached_latency:.2f}ms")
    print(f"  Speedup:     {first_latency/cached_latency:.1f}x")
    print()

    # Demo 3: Pre-warming cache
    print(">>> Demo 3: Pre-warm Cache")
    print("-" * 50)

    common_phrases = [
        "Yes",
        "No",
        "OK",
        "Cancel",
        "Submit",
        "Loading...",
        "Done!",
    ]

    print(f"  Pre-warming {len(common_phrases)} phrases...")
    start = time.perf_counter()
    model.warm_cache(common_phrases)
    warm_time = (time.perf_counter() - start) * 1000

    print(f"  Warm-up complete: {warm_time:.0f}ms total")
    print()

    # Demo 4: Stats
    print(">>> Demo 4: Performance Stats")
    print("-" * 50)
    stats = model.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print()
    print("=" * 50)
    print("Demo complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
