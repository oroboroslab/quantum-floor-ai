#!/usr/bin/env python3
"""
Connection-Core Performance Tests
=================================

Benchmarks for the memory engine.
"""

import os
import sys
import time
import tempfile
import statistics

sys.path.insert(0, '..')

from connection_core import MemoryEngine, MemoryConfig


def benchmark_add(engine: MemoryEngine, count: int = 1000) -> dict:
    """Benchmark memory addition."""
    times = []

    for i in range(count):
        start = time.perf_counter()
        engine.add(f"Benchmark memory content {i} with some additional text")
        elapsed = (time.perf_counter() - start) * 1000
        times.append(elapsed)

    return {
        "operation": "add",
        "count": count,
        "mean_ms": statistics.mean(times),
        "median_ms": statistics.median(times),
        "std_ms": statistics.stdev(times) if len(times) > 1 else 0,
        "min_ms": min(times),
        "max_ms": max(times),
        "total_ms": sum(times),
    }


def benchmark_recall(engine: MemoryEngine, queries: list, runs: int = 100) -> dict:
    """Benchmark memory recall."""
    times = []

    for _ in range(runs):
        for query in queries:
            start = time.perf_counter()
            engine.recall(query, limit=5)
            elapsed = (time.perf_counter() - start) * 1000
            times.append(elapsed)

    return {
        "operation": "recall",
        "count": len(times),
        "mean_ms": statistics.mean(times),
        "median_ms": statistics.median(times),
        "std_ms": statistics.stdev(times) if len(times) > 1 else 0,
        "min_ms": min(times),
        "max_ms": max(times),
    }


def benchmark_get(engine: MemoryEngine, memory_ids: list, runs: int = 100) -> dict:
    """Benchmark memory get by ID."""
    times = []

    for _ in range(runs):
        for mid in memory_ids:
            start = time.perf_counter()
            engine.get(mid)
            elapsed = (time.perf_counter() - start) * 1000
            times.append(elapsed)

    return {
        "operation": "get",
        "count": len(times),
        "mean_ms": statistics.mean(times),
        "median_ms": statistics.median(times),
        "std_ms": statistics.stdev(times) if len(times) > 1 else 0,
        "min_ms": min(times),
        "max_ms": max(times),
    }


def print_result(result: dict):
    """Print benchmark result."""
    print(f"\n{result['operation'].upper()} ({result['count']} operations)")
    print(f"  Mean:   {result['mean_ms']:.3f}ms")
    print(f"  Median: {result['median_ms']:.3f}ms")
    print(f"  Std:    {result['std_ms']:.3f}ms")
    print(f"  Min:    {result['min_ms']:.3f}ms")
    print(f"  Max:    {result['max_ms']:.3f}ms")


def main():
    print("=" * 60)
    print("CONNECTION-CORE PERFORMANCE BENCHMARK")
    print("=" * 60)
    print()
    print("Target: <50ms recall latency")
    print("Target: <100KB database footprint")
    print()

    # Create temp database
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "benchmark.db")

    config = MemoryConfig(
        storage_path=db_path,
        max_memories=50000,
    )
    engine = MemoryEngine(config)

    try:
        # Benchmark ADD
        print(">>> Benchmarking ADD operation...")
        add_result = benchmark_add(engine, count=1000)
        print_result(add_result)

        # Get some memory IDs for GET benchmark
        memories = engine.recall("Benchmark", limit=10)
        memory_ids = [m.id for m in memories]

        # Benchmark RECALL
        print("\n>>> Benchmarking RECALL operation...")
        queries = ["benchmark", "memory", "content", "text", "additional"]
        recall_result = benchmark_recall(engine, queries, runs=20)
        print_result(recall_result)

        # Benchmark GET
        print("\n>>> Benchmarking GET operation...")
        get_result = benchmark_get(engine, memory_ids, runs=50)
        print_result(get_result)

        # Check database size
        db_size = os.path.getsize(db_path)
        db_size_kb = db_size / 1024

        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)

        print(f"""
    Memory Count:      {engine.count()}
    Database Size:     {db_size_kb:.1f}KB

    Performance:
    - Add:    {add_result['mean_ms']:.3f}ms mean
    - Recall: {recall_result['mean_ms']:.3f}ms mean
    - Get:    {get_result['mean_ms']:.3f}ms mean

    Targets:
    - Recall <50ms:    {'PASS' if recall_result['mean_ms'] < 50 else 'FAIL'}
    - Size <100KB:     {'PASS' if db_size_kb < 100 else f'FAIL ({db_size_kb:.0f}KB)'}
    """)

        # Pass/Fail
        passed = recall_result['mean_ms'] < 50
        print(f"BENCHMARK STATUS: {'PASSED' if passed else 'NEEDS OPTIMIZATION'}")
        print("=" * 60)

    finally:
        engine.close()
        if os.path.exists(db_path):
            os.remove(db_path)
        os.rmdir(temp_dir)


if __name__ == "__main__":
    main()
