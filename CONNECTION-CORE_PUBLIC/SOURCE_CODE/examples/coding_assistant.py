#!/usr/bin/env python3
"""
Coding Assistant with Memory Example
====================================

Demonstrates a coding assistant that remembers project context.
"""

import sys
sys.path.insert(0, '..')

from connection_core import MemoryEngine, MemoryConfig
from memory_engine import SemanticMemory, WorkingMemory


def create_coding_assistant():
    """Create a coding assistant with project memory."""

    config = MemoryConfig(
        storage_path="coding_assistant_memory.db",
        max_memories=10000,
    )
    engine = MemoryEngine(config)

    semantic = SemanticMemory(engine)
    working = WorkingMemory(engine, ttl_seconds=7200)  # 2 hour session

    return engine, semantic, working


def learn_project_context(semantic: SemanticMemory):
    """Store project context in semantic memory."""

    # Store project information
    semantic.add_concept("project.name", "MyApp")
    semantic.add_concept("project.language", "Python")
    semantic.add_concept("project.framework", "FastAPI")

    # Store coding conventions
    semantic.add_concept("conventions.style", "PEP 8")
    semantic.add_concept("conventions.testing", "pytest")
    semantic.add_concept("conventions.docstrings", "Google style")

    # Store architecture decisions
    semantic.add_concept("architecture.pattern", "Clean Architecture")
    semantic.add_concept("architecture.database", "PostgreSQL")
    semantic.add_concept("architecture.cache", "Redis")

    print("Project context stored!")


def start_task(working: WorkingMemory, task_description: str):
    """Start a new coding task."""

    working.clear()
    working.set_context("task", task_description)
    working.set_context("status", "in_progress")
    working.add_note(f"Started task: {task_description}")

    print(f"Task started: {task_description}")


def add_finding(working: WorkingMemory, finding: str):
    """Add a finding during the task."""

    working.add_note(finding)
    print(f"Noted: {finding}")


def complete_task(engine: MemoryEngine, working: WorkingMemory):
    """Complete current task and persist important findings."""

    working.set_context("status", "completed")

    # Persist working memory to long-term storage
    count = working.persist(importance=0.7)
    print(f"Task completed. Persisted {count} items to memory.")

    working.clear()


def get_project_context(semantic: SemanticMemory) -> str:
    """Get formatted project context."""

    context = []

    project_name = semantic.get_concept("project.name")
    if project_name:
        context.append(f"Project: {project_name}")

    language = semantic.get_concept("project.language")
    if language:
        context.append(f"Language: {language}")

    framework = semantic.get_concept("project.framework")
    if framework:
        context.append(f"Framework: {framework}")

    pattern = semantic.get_concept("architecture.pattern")
    if pattern:
        context.append(f"Architecture: {pattern}")

    return "\n".join(context)


def main():
    print("=" * 50)
    print("Coding Assistant with Memory Demo")
    print("=" * 50)
    print()

    engine, semantic, working = create_coding_assistant()

    # Simulate a coding session

    # 1. Learn project context
    print(">>> Learning project context...")
    learn_project_context(semantic)
    print()

    # 2. Show what we know about the project
    print(">>> Project context:")
    print(get_project_context(semantic))
    print()

    # 3. Start a coding task
    print(">>> Starting a task...")
    start_task(working, "Implement user authentication endpoint")
    print()

    # 4. Add findings during development
    print(">>> Adding findings...")
    add_finding(working, "Need to add JWT token validation")
    add_finding(working, "Found existing auth middleware in /middleware/auth.py")
    add_finding(working, "User model needs 'last_login' field")
    print()

    # 5. Check working memory
    print(">>> Current working memory:")
    wm = working.get_all()
    print(f"Task: {wm['context'].get('task')}")
    print(f"Status: {wm['context'].get('status')}")
    print(f"Notes:")
    for note in wm['notes']:
        print(f"  - {note}")
    print()

    # 6. Complete task
    print(">>> Completing task...")
    complete_task(engine, working)
    print()

    # 7. Later: Recall what we learned
    print(">>> Recalling relevant memories for 'authentication'...")
    memories = engine.recall("authentication", limit=5)
    for m in memories:
        print(f"  [{m.importance:.2f}] {m.content}")
    print()

    # Show final stats
    stats = engine.get_stats()
    print(">>> Memory stats:")
    print(f"  Total memories: {stats['total_memories']}")
    print(f"  Database size: {stats['database_size_kb']}KB")

    engine.close()


if __name__ == "__main__":
    main()
