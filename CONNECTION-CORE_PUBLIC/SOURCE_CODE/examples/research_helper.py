#!/usr/bin/env python3
"""
Research Helper with Memory Example
===================================

Demonstrates a research assistant that stores and retrieves findings.
"""

import sys
sys.path.insert(0, '..')

from connection_core import MemoryEngine, MemoryConfig


def create_research_memory():
    """Create a research-focused memory engine."""

    config = MemoryConfig(
        storage_path="research_memory.db",
        max_memories=50000,  # Research can generate lots of findings
        default_importance=0.5,
    )

    return MemoryEngine(config)


def store_finding(engine: MemoryEngine, finding: str, source: str, topic: str):
    """Store a research finding."""

    engine.add(
        content=finding,
        importance=0.7,
        tags=["finding", f"topic:{topic}", f"source:{source}"],
        metadata={
            "source": source,
            "topic": topic,
            "type": "finding",
        }
    )

    print(f"Stored: {finding[:50]}...")


def store_question(engine: MemoryEngine, question: str, topic: str):
    """Store a research question."""

    engine.add(
        content=question,
        importance=0.6,
        tags=["question", f"topic:{topic}"],
        metadata={
            "topic": topic,
            "type": "question",
            "answered": False,
        }
    )

    print(f"Question stored: {question}")


def store_hypothesis(engine: MemoryEngine, hypothesis: str, topic: str):
    """Store a hypothesis."""

    engine.add(
        content=hypothesis,
        importance=0.8,
        tags=["hypothesis", f"topic:{topic}"],
        metadata={
            "topic": topic,
            "type": "hypothesis",
            "tested": False,
        }
    )

    print(f"Hypothesis stored: {hypothesis}")


def search_research(engine: MemoryEngine, query: str, limit: int = 10):
    """Search research memory."""

    memories = engine.recall(query, limit=limit)

    print(f"\nSearch results for '{query}':")
    print("-" * 50)

    for m in memories:
        mem_type = m.metadata.get("type", "unknown")
        source = m.metadata.get("source", "")
        topic = m.metadata.get("topic", "")

        print(f"[{mem_type.upper()}] (topic: {topic})")
        print(f"  {m.content}")
        if source:
            print(f"  Source: {source}")
        print(f"  Importance: {m.importance:.2f}")
        print()


def get_topic_summary(engine: MemoryEngine, topic: str):
    """Get summary of findings for a topic."""

    memories = engine.recall(
        topic,
        limit=20,
        tags=[f"topic:{topic}"]
    )

    findings = [m for m in memories if m.metadata.get("type") == "finding"]
    questions = [m for m in memories if m.metadata.get("type") == "question"]
    hypotheses = [m for m in memories if m.metadata.get("type") == "hypothesis"]

    print(f"\n=== Topic Summary: {topic} ===")

    if hypotheses:
        print(f"\nHypotheses ({len(hypotheses)}):")
        for h in hypotheses:
            print(f"  - {h.content}")

    if findings:
        print(f"\nFindings ({len(findings)}):")
        for f in findings:
            print(f"  - {f.content}")
            if f.metadata.get("source"):
                print(f"    (Source: {f.metadata['source']})")

    if questions:
        print(f"\nOpen Questions ({len(questions)}):")
        for q in questions:
            print(f"  - {q.content}")

    print()


def main():
    print("=" * 50)
    print("Research Helper with Memory Demo")
    print("=" * 50)
    print()

    engine = create_research_memory()

    # Simulate a research session on "AI Efficiency"

    topic = "AI efficiency"

    # Store hypothesis
    print(">>> Storing hypothesis...")
    store_hypothesis(
        engine,
        "Smaller models can match larger model performance through better architecture",
        topic
    )
    print()

    # Store findings
    print(">>> Storing findings...")
    findings = [
        ("Knowledge distillation can reduce model size by 90%",
         "Hinton et al. 2015"),
        ("Pruning removes up to 95% of weights with minimal accuracy loss",
         "Han et al. 2016"),
        ("Quantization reduces memory by 4x with 1% accuracy drop",
         "Jacob et al. 2018"),
        ("MoE architectures achieve better efficiency at scale",
         "Fedus et al. 2021"),
    ]

    for finding, source in findings:
        store_finding(engine, finding, source, topic)
    print()

    # Store questions
    print(">>> Storing questions...")
    questions = [
        "What is the minimum model size for emergent capabilities?",
        "Can architecture innovations replace parameter scaling?",
        "How does inference speed correlate with model quality?",
    ]

    for q in questions:
        store_question(engine, q, topic)
    print()

    # Search research
    print(">>> Searching for 'model size'...")
    search_research(engine, "model size", limit=5)

    # Get topic summary
    print(">>> Getting topic summary...")
    get_topic_summary(engine, topic)

    # Show stats
    stats = engine.get_stats()
    print(">>> Memory stats:")
    print(f"  Total memories: {stats['total_memories']}")
    print(f"  Database size: {stats['database_size_kb']}KB")
    print(f"  Total accesses: {stats['total_accesses']}")

    engine.close()


if __name__ == "__main__":
    main()
