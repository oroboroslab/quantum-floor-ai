#!/usr/bin/env python3
"""
AXIS-7B-C Latency Test Suite
============================

Comprehensive latency testing to verify <20ms guarantee.
"""

import time
import statistics
import sys
from typing import List, Tuple
from axis_api import AxisModel, AxisConfig


def run_latency_test(model: AxisModel, text: str, runs: int = 100) -> dict:
    """Run latency test for a given text."""
    latencies = []

    for _ in range(runs):
        start = time.perf_counter()
        model.instant_speech(text)
        latency = (time.perf_counter() - start) * 1000
        latencies.append(latency)

    return {
        "text": text[:30] + "..." if len(text) > 30 else text,
        "runs": runs,
        "mean": statistics.mean(latencies),
        "median": statistics.median(latencies),
        "std": statistics.stdev(latencies),
        "min": min(latencies),
        "max": max(latencies),
        "p50": sorted(latencies)[int(runs * 0.50)],
        "p95": sorted(latencies)[int(runs * 0.95)],
        "p99": sorted(latencies)[int(runs * 0.99)],
        "under_20ms": sum(1 for l in latencies if l < 20) / runs * 100,
        "under_50ms": sum(1 for l in latencies if l < 50) / runs * 100,
    }


def print_result(result: dict) -> None:
    """Print formatted test result."""
    print(f"\n  Text: '{result['text']}'")
    print(f"  Runs: {result['runs']}")
    print(f"  Mean: {result['mean']:.2f}ms | Median: {result['median']:.2f}ms | Std: {result['std']:.2f}ms")
    print(f"  Min: {result['min']:.2f}ms | Max: {result['max']:.2f}ms")
    print(f"  P50: {result['p50']:.2f}ms | P95: {result['p95']:.2f}ms | P99: {result['p99']:.2f}ms")
    print(f"  Under 20ms: {result['under_20ms']:.1f}% | Under 50ms: {result['under_50ms']:.1f}%")


def main():
    print("=" * 70)
    print("AXIS-7B-C LATENCY VERIFICATION TEST")
    print("=" * 70)
    print()
    print("Model Size: 48MB (300x smaller than Llama-7B)")
    print("Target: <20ms for 95% of requests")
    print()

    # Initialize model
    config = AxisConfig(
        preload=True,
        hardware_acceleration=True,
        cache_size=0,  # Disable cache for accurate testing
        voice_quality="fast"
    )

    print("Loading AXIS-7B-C...")
    model = AxisModel(config=config)
    print("Model ready!")
    print()

    # Test categories
    tests = {
        "Short phrases (1-3 words)": [
            "Hello",
            "Yes",
            "Click here",
            "Submit",
            "OK",
        ],
        "Medium phrases (4-8 words)": [
            "Please confirm your selection",
            "Loading your data now",
            "Operation completed successfully",
            "Error detected in input",
        ],
        "Long phrases (9+ words)": [
            "The quick brown fox jumps over the lazy dog",
            "Please wait while we process your request",
            "Your changes have been saved successfully to the database",
        ],
    }

    all_results = []

    for category, phrases in tests.items():
        print(f"\n>>> {category}")
        print("-" * 70)

        for phrase in phrases:
            result = run_latency_test(model, phrase, runs=50)
            print_result(result)
            all_results.append(result)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    all_means = [r["mean"] for r in all_results]
    all_p95 = [r["p95"] for r in all_results]
    all_under_20 = [r["under_20ms"] for r in all_results]

    print(f"""
    Overall Statistics:
    -------------------
    Average Mean Latency:    {statistics.mean(all_means):.2f}ms
    Average P95 Latency:     {statistics.mean(all_p95):.2f}ms
    Average Under 20ms:      {statistics.mean(all_under_20):.1f}%

    Target Compliance:
    ------------------
    Target: <20ms for 95% of requests
    Result: {statistics.mean(all_under_20):.1f}% under 20ms

    Model Specifications:
    ---------------------
    Size: 48MB
    Architecture: 7-level proprietary
    Hardware: {'GPU/NPU' if config.hardware_acceleration else 'CPU'}
    Cache: {'Enabled' if config.cache_size > 0 else 'Disabled for test'}

    COMPARISON TO COMPETITION:
    --------------------------
    | Model          | Size    | Latency |
    |----------------|---------|---------|
    | Llama-7B       | 14GB    | ~500ms  |
    | Whisper        | 1.5GB   | ~200ms  |
    | AXIS-7B-C      | 48MB    | <20ms   |
    """)

    # Pass/Fail
    passed = statistics.mean(all_under_20) >= 95
    status = "PASSED" if passed else "FAILED"
    print(f"\n    TEST STATUS: {status}")
    print("=" * 70)

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
