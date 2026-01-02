"""
Memory Engine Extensions
========================

Extended memory functionality for Connection-Core.
"""

import json
import time
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, field
from collections import deque

from .connection_core import MemoryEngine, Memory, MemoryConfig


@dataclass
class ConversationTurn:
    """A single turn in a conversation."""
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ConversationMemory:
    """
    Conversation History Memory

    Manages conversation turns with automatic summarization
    and important fact extraction.

    Example:
        >>> conv = ConversationMemory(engine)
        >>> conv.add_turn("user", "My name is Alice")
        >>> conv.add_turn("assistant", "Nice to meet you, Alice!")
        >>> history = conv.get_recent(5)
    """

    def __init__(
        self,
        engine: MemoryEngine,
        max_turns: int = 100,
        auto_extract: bool = True
    ):
        """
        Initialize conversation memory.

        Args:
            engine: The memory engine to use for persistence
            max_turns: Maximum turns to keep in memory
            auto_extract: Automatically extract important facts
        """
        self.engine = engine
        self.max_turns = max_turns
        self.auto_extract = auto_extract
        self._turns: deque = deque(maxlen=max_turns)
        self._load_history()

    def _load_history(self) -> None:
        """Load conversation history from storage."""
        memories = self.engine.recall("conversation:history", limit=self.max_turns)
        for memory in reversed(memories):  # Oldest first
            if memory.metadata.get("type") == "conversation_turn":
                turn = ConversationTurn(
                    role=memory.metadata.get("role", "unknown"),
                    content=memory.content,
                    timestamp=memory.created_at,
                    metadata=memory.metadata,
                )
                self._turns.append(turn)

    def add_turn(
        self,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ConversationTurn:
        """
        Add a conversation turn.

        Args:
            role: The speaker role ("user", "assistant", "system")
            content: The message content
            metadata: Optional additional data

        Returns:
            The created ConversationTurn
        """
        turn = ConversationTurn(
            role=role,
            content=content,
            metadata=metadata or {},
        )
        self._turns.append(turn)

        # Store in memory engine
        turn_metadata = {
            "type": "conversation_turn",
            "role": role,
            **turn.metadata,
        }

        self.engine.add(
            content=content,
            importance=0.3,  # Conversation turns have lower base importance
            tags=["conversation", f"role:{role}"],
            metadata=turn_metadata,
        )

        # Auto-extract important facts
        if self.auto_extract:
            self._extract_facts(content, role)

        return turn

    def _extract_facts(self, content: str, role: str) -> None:
        """Extract and store important facts from content."""
        # Simple fact extraction patterns
        important_patterns = [
            "my name is",
            "i am",
            "i prefer",
            "i like",
            "i don't like",
            "i want",
            "remember that",
            "note that",
        ]

        content_lower = content.lower()
        for pattern in important_patterns:
            if pattern in content_lower:
                # Store as high-importance fact
                self.engine.add(
                    content=content,
                    importance=0.8,
                    tags=["fact", "extracted", f"source:{role}"],
                    metadata={"extracted_from": "conversation", "pattern": pattern},
                )
                break

    def get_recent(self, count: int = 10) -> List[ConversationTurn]:
        """Get most recent conversation turns."""
        turns = list(self._turns)
        return turns[-count:] if len(turns) > count else turns

    def get_formatted(
        self,
        count: int = 10,
        format_template: str = "{role}: {content}"
    ) -> str:
        """Get formatted conversation history."""
        turns = self.get_recent(count)
        lines = [
            format_template.format(role=t.role.capitalize(), content=t.content)
            for t in turns
        ]
        return "\n".join(lines)

    def clear(self) -> int:
        """Clear conversation history."""
        count = len(self._turns)
        self._turns.clear()
        return count

    def search(self, query: str, limit: int = 5) -> List[ConversationTurn]:
        """Search conversation history."""
        memories = self.engine.recall(
            query,
            limit=limit,
            tags=["conversation"]
        )

        turns = []
        for memory in memories:
            if memory.metadata.get("type") == "conversation_turn":
                turns.append(ConversationTurn(
                    role=memory.metadata.get("role", "unknown"),
                    content=memory.content,
                    timestamp=memory.created_at,
                    metadata=memory.metadata,
                ))

        return turns


class SemanticMemory:
    """
    Semantic Memory System

    Organizes memories by concepts and relationships.
    Supports hierarchical knowledge structures.

    Example:
        >>> semantic = SemanticMemory(engine)
        >>> semantic.add_concept("user.preferences.theme", "dark mode")
        >>> theme = semantic.get_concept("user.preferences.theme")
    """

    def __init__(self, engine: MemoryEngine):
        """
        Initialize semantic memory.

        Args:
            engine: The memory engine to use
        """
        self.engine = engine
        self._concept_cache: Dict[str, Memory] = {}

    def add_concept(
        self,
        path: str,
        value: Any,
        importance: float = 0.7
    ) -> Memory:
        """
        Add or update a concept.

        Args:
            path: Dot-notation path (e.g., "user.preferences.theme")
            value: The concept value
            importance: Importance score

        Returns:
            The created/updated Memory
        """
        # Store as JSON if not string
        content = value if isinstance(value, str) else json.dumps(value)

        # Parse path for tags
        parts = path.split(".")
        tags = ["concept"] + [f"level{i}:{p}" for i, p in enumerate(parts)]

        memory = self.engine.add(
            content=content,
            importance=importance,
            tags=tags,
            metadata={
                "type": "concept",
                "path": path,
                "value_type": type(value).__name__,
            },
        )

        self._concept_cache[path] = memory
        return memory

    def get_concept(self, path: str) -> Optional[Any]:
        """
        Get a concept by path.

        Args:
            path: Dot-notation path

        Returns:
            The concept value or None
        """
        # Check cache first
        if path in self._concept_cache:
            memory = self._concept_cache[path]
            return self._parse_value(memory)

        # Search in engine
        memories = self.engine.recall(
            path,
            limit=1,
            tags=["concept"]
        )

        for memory in memories:
            if memory.metadata.get("path") == path:
                self._concept_cache[path] = memory
                return self._parse_value(memory)

        return None

    def _parse_value(self, memory: Memory) -> Any:
        """Parse memory content to original value type."""
        value_type = memory.metadata.get("value_type", "str")

        if value_type == "str":
            return memory.content
        else:
            try:
                return json.loads(memory.content)
            except json.JSONDecodeError:
                return memory.content

    def list_concepts(self, prefix: str = "") -> List[str]:
        """List all concept paths with given prefix."""
        memories = self.engine.recall(
            prefix or "concept",
            limit=100,
            tags=["concept"]
        )

        paths = []
        for memory in memories:
            path = memory.metadata.get("path", "")
            if path.startswith(prefix):
                paths.append(path)

        return sorted(set(paths))

    def delete_concept(self, path: str) -> bool:
        """Delete a concept."""
        if path in self._concept_cache:
            memory = self._concept_cache.pop(path)
            return self.engine.delete(memory.id)
        return False

    def get_related(self, path: str, limit: int = 5) -> List[Tuple[str, Any]]:
        """Get concepts related to a path."""
        # Get parent path
        parts = path.split(".")
        if len(parts) > 1:
            parent = ".".join(parts[:-1])
        else:
            parent = path

        related = []
        for concept_path in self.list_concepts(parent):
            if concept_path != path:
                value = self.get_concept(concept_path)
                related.append((concept_path, value))

        return related[:limit]


class WorkingMemory:
    """
    Working Memory System

    Short-term memory for current task context.
    Automatically clears after task completion.

    Example:
        >>> working = WorkingMemory(engine)
        >>> working.set_context("current_task", "writing code")
        >>> working.add_note("Need to handle edge cases")
        >>> context = working.get_all()
    """

    def __init__(self, engine: MemoryEngine, ttl_seconds: int = 3600):
        """
        Initialize working memory.

        Args:
            engine: The memory engine
            ttl_seconds: Time-to-live for working memory items
        """
        self.engine = engine
        self.ttl = ttl_seconds
        self._context: Dict[str, Any] = {}
        self._notes: List[str] = []
        self._start_time = time.time()

    def set_context(self, key: str, value: Any) -> None:
        """Set a context variable."""
        self._context[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        """Get a context variable."""
        return self._context.get(key, default)

    def add_note(self, note: str) -> None:
        """Add a working note."""
        self._notes.append(note)

    def get_notes(self) -> List[str]:
        """Get all working notes."""
        return self._notes.copy()

    def get_all(self) -> Dict[str, Any]:
        """Get all working memory contents."""
        return {
            "context": self._context.copy(),
            "notes": self._notes.copy(),
            "elapsed_seconds": time.time() - self._start_time,
        }

    def persist(self, importance: float = 0.6) -> int:
        """Persist working memory to long-term storage."""
        count = 0

        # Save context items
        for key, value in self._context.items():
            self.engine.add(
                content=f"{key}: {value}",
                importance=importance,
                tags=["working_memory", "context"],
                metadata={"key": key, "value": value},
            )
            count += 1

        # Save notes
        for note in self._notes:
            self.engine.add(
                content=note,
                importance=importance,
                tags=["working_memory", "note"],
            )
            count += 1

        return count

    def clear(self) -> None:
        """Clear working memory."""
        self._context.clear()
        self._notes.clear()
        self._start_time = time.time()

    def is_expired(self) -> bool:
        """Check if working memory has expired."""
        return (time.time() - self._start_time) > self.ttl
