"""
Connection-Core: Persistent Memory Engine for AI
================================================

A lightweight, open-source memory system that gives any AI persistent memory.
MIT Licensed - Our gift to the AI community.

Features:
- <100KB footprint
- <50ms response time
- Works with any LLM
- Semantic memory retrieval
- Conversation history management

Usage:
    from connection_core import MemoryEngine

    memory = MemoryEngine()
    memory.add("User prefers dark mode")

    relevant = memory.recall("What are the user's preferences?")
"""

from .connection_core import MemoryEngine, Memory, MemoryConfig
from .memory_engine import SemanticMemory, ConversationMemory
from .api import MemoryAPI, create_app

__version__ = "1.0.0"
__author__ = "Quantum-Floor AI"
__license__ = "MIT"

__all__ = [
    "MemoryEngine",
    "Memory",
    "MemoryConfig",
    "SemanticMemory",
    "ConversationMemory",
    "MemoryAPI",
    "create_app",
]
