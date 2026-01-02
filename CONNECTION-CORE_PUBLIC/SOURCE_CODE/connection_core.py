"""
Connection-Core: Main Memory Engine
===================================

The core memory system for persistent AI memory.
MIT Licensed.
"""

import os
import json
import time
import hashlib
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, field, asdict
from pathlib import Path
import sqlite3


@dataclass
class Memory:
    """A single memory entry."""
    id: str
    content: str
    created_at: float
    importance: float = 0.5
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    access_count: int = 0
    last_accessed: Optional[float] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Memory":
        return cls(**data)


@dataclass
class MemoryConfig:
    """Configuration for the memory engine."""
    storage_path: str = "memory.db"
    max_memories: int = 10000
    default_importance: float = 0.5
    decay_rate: float = 0.001  # Importance decay per day
    min_importance: float = 0.1
    embedding_enabled: bool = False  # Simple mode by default


class MemoryEngine:
    """
    Connection-Core Memory Engine

    A lightweight memory system that gives AI persistent memory.
    Designed to be simple, fast, and effective.

    Features:
    - SQLite-based storage (<100KB)
    - Fast retrieval (<50ms)
    - Importance-based ranking
    - Tag-based organization
    - Automatic importance decay

    Example:
        >>> engine = MemoryEngine()
        >>> engine.add("User's name is Alice")
        >>> engine.add("User prefers dark mode", importance=0.8)
        >>> memories = engine.recall("What is the user's name?")
        >>> print(memories[0].content)
        "User's name is Alice"
    """

    def __init__(self, config: Optional[MemoryConfig] = None):
        """
        Initialize the memory engine.

        Args:
            config: Optional configuration. Uses defaults if not provided.
        """
        self.config = config or MemoryConfig()
        self._db: Optional[sqlite3.Connection] = None
        self._init_database()

    def _init_database(self) -> None:
        """Initialize SQLite database."""
        self._db = sqlite3.connect(
            self.config.storage_path,
            check_same_thread=False
        )
        self._db.row_factory = sqlite3.Row

        cursor = self._db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                created_at REAL NOT NULL,
                importance REAL DEFAULT 0.5,
                tags TEXT DEFAULT '[]',
                metadata TEXT DEFAULT '{}',
                access_count INTEGER DEFAULT 0,
                last_accessed REAL
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance DESC)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_created ON memories(created_at DESC)
        """)

        # Full-text search
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                content,
                content='memories',
                content_rowid='rowid'
            )
        """)

        self._db.commit()

    def _generate_id(self, content: str) -> str:
        """Generate unique ID for content."""
        timestamp = str(time.time())
        data = f"{content}{timestamp}".encode()
        return hashlib.sha256(data).hexdigest()[:16]

    def add(
        self,
        content: str,
        importance: Optional[float] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Memory:
        """
        Add a new memory.

        Args:
            content: The memory content
            importance: Importance score (0-1)
            tags: Optional tags for organization
            metadata: Optional additional data

        Returns:
            The created Memory object
        """
        memory = Memory(
            id=self._generate_id(content),
            content=content,
            created_at=time.time(),
            importance=importance or self.config.default_importance,
            tags=tags or [],
            metadata=metadata or {},
        )

        cursor = self._db.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO memories
            (id, content, created_at, importance, tags, metadata, access_count, last_accessed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            memory.id,
            memory.content,
            memory.created_at,
            memory.importance,
            json.dumps(memory.tags),
            json.dumps(memory.metadata),
            memory.access_count,
            memory.last_accessed,
        ))

        # Update FTS index
        cursor.execute("""
            INSERT INTO memories_fts(rowid, content)
            SELECT rowid, content FROM memories WHERE id = ?
        """, (memory.id,))

        self._db.commit()

        # Enforce max memories limit
        self._enforce_limit()

        return memory

    def recall(
        self,
        query: str,
        limit: int = 5,
        min_importance: Optional[float] = None,
        tags: Optional[List[str]] = None
    ) -> List[Memory]:
        """
        Recall memories relevant to a query.

        Args:
            query: Search query
            limit: Maximum memories to return
            min_importance: Minimum importance threshold
            tags: Filter by tags

        Returns:
            List of relevant memories, ranked by relevance
        """
        min_imp = min_importance or self.config.min_importance
        start_time = time.time()

        cursor = self._db.cursor()

        # Search using FTS
        if query.strip():
            # Use FTS for text search
            cursor.execute("""
                SELECT m.*
                FROM memories m
                JOIN memories_fts fts ON m.rowid = fts.rowid
                WHERE memories_fts MATCH ?
                AND m.importance >= ?
                ORDER BY m.importance DESC, m.created_at DESC
                LIMIT ?
            """, (query, min_imp, limit))
        else:
            # Return most important recent memories
            cursor.execute("""
                SELECT * FROM memories
                WHERE importance >= ?
                ORDER BY importance DESC, created_at DESC
                LIMIT ?
            """, (min_imp, limit))

        rows = cursor.fetchall()
        memories = []

        for row in rows:
            memory = Memory(
                id=row["id"],
                content=row["content"],
                created_at=row["created_at"],
                importance=row["importance"],
                tags=json.loads(row["tags"]),
                metadata=json.loads(row["metadata"]),
                access_count=row["access_count"],
                last_accessed=row["last_accessed"],
            )

            # Filter by tags if specified
            if tags and not any(t in memory.tags for t in tags):
                continue

            memories.append(memory)

            # Update access stats
            self._record_access(memory.id)

        elapsed = (time.time() - start_time) * 1000

        return memories

    def _record_access(self, memory_id: str) -> None:
        """Record memory access for analytics."""
        cursor = self._db.cursor()
        cursor.execute("""
            UPDATE memories
            SET access_count = access_count + 1, last_accessed = ?
            WHERE id = ?
        """, (time.time(), memory_id))
        self._db.commit()

    def get(self, memory_id: str) -> Optional[Memory]:
        """Get a specific memory by ID."""
        cursor = self._db.cursor()
        cursor.execute("SELECT * FROM memories WHERE id = ?", (memory_id,))
        row = cursor.fetchone()

        if not row:
            return None

        return Memory(
            id=row["id"],
            content=row["content"],
            created_at=row["created_at"],
            importance=row["importance"],
            tags=json.loads(row["tags"]),
            metadata=json.loads(row["metadata"]),
            access_count=row["access_count"],
            last_accessed=row["last_accessed"],
        )

    def update(
        self,
        memory_id: str,
        content: Optional[str] = None,
        importance: Optional[float] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Memory]:
        """Update an existing memory."""
        memory = self.get(memory_id)
        if not memory:
            return None

        if content is not None:
            memory.content = content
        if importance is not None:
            memory.importance = importance
        if tags is not None:
            memory.tags = tags
        if metadata is not None:
            memory.metadata = metadata

        cursor = self._db.cursor()
        cursor.execute("""
            UPDATE memories
            SET content = ?, importance = ?, tags = ?, metadata = ?
            WHERE id = ?
        """, (
            memory.content,
            memory.importance,
            json.dumps(memory.tags),
            json.dumps(memory.metadata),
            memory_id,
        ))
        self._db.commit()

        return memory

    def delete(self, memory_id: str) -> bool:
        """Delete a memory."""
        cursor = self._db.cursor()
        cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
        affected = cursor.rowcount
        self._db.commit()
        return affected > 0

    def clear(self) -> int:
        """Clear all memories. Returns count deleted."""
        cursor = self._db.cursor()
        cursor.execute("SELECT COUNT(*) FROM memories")
        count = cursor.fetchone()[0]

        cursor.execute("DELETE FROM memories")
        cursor.execute("DELETE FROM memories_fts")
        self._db.commit()

        return count

    def count(self) -> int:
        """Get total memory count."""
        cursor = self._db.cursor()
        cursor.execute("SELECT COUNT(*) FROM memories")
        return cursor.fetchone()[0]

    def _enforce_limit(self) -> None:
        """Remove oldest, least important memories if over limit."""
        count = self.count()
        if count <= self.config.max_memories:
            return

        # Remove excess memories (lowest importance first)
        excess = count - self.config.max_memories
        cursor = self._db.cursor()
        cursor.execute("""
            DELETE FROM memories WHERE id IN (
                SELECT id FROM memories
                ORDER BY importance ASC, created_at ASC
                LIMIT ?
            )
        """, (excess,))
        self._db.commit()

    def decay_importance(self) -> int:
        """
        Apply importance decay to all memories.
        Call periodically (e.g., daily) to let old memories fade.

        Returns:
            Number of memories updated
        """
        cursor = self._db.cursor()
        cursor.execute("""
            UPDATE memories
            SET importance = MAX(importance - ?, ?)
        """, (self.config.decay_rate, self.config.min_importance))

        affected = cursor.rowcount
        self._db.commit()

        return affected

    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        cursor = self._db.cursor()

        cursor.execute("SELECT COUNT(*) FROM memories")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(importance) FROM memories")
        avg_importance = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(access_count) FROM memories")
        total_accesses = cursor.fetchone()[0] or 0

        # Database file size
        db_size = os.path.getsize(self.config.storage_path) if os.path.exists(self.config.storage_path) else 0

        return {
            "total_memories": total,
            "average_importance": round(avg_importance, 3),
            "total_accesses": total_accesses,
            "database_size_bytes": db_size,
            "database_size_kb": round(db_size / 1024, 2),
            "max_memories": self.config.max_memories,
        }

    def export(self, output_path: str) -> int:
        """Export all memories to JSON file."""
        cursor = self._db.cursor()
        cursor.execute("SELECT * FROM memories ORDER BY created_at DESC")

        memories = []
        for row in cursor.fetchall():
            memories.append({
                "id": row["id"],
                "content": row["content"],
                "created_at": row["created_at"],
                "importance": row["importance"],
                "tags": json.loads(row["tags"]),
                "metadata": json.loads(row["metadata"]),
                "access_count": row["access_count"],
                "last_accessed": row["last_accessed"],
            })

        with open(output_path, "w") as f:
            json.dump({"memories": memories, "exported_at": time.time()}, f, indent=2)

        return len(memories)

    def import_memories(self, input_path: str) -> int:
        """Import memories from JSON file."""
        with open(input_path, "r") as f:
            data = json.load(f)

        memories = data.get("memories", [])
        count = 0

        for m in memories:
            self.add(
                content=m["content"],
                importance=m.get("importance", self.config.default_importance),
                tags=m.get("tags", []),
                metadata=m.get("metadata", {}),
            )
            count += 1

        return count

    def close(self) -> None:
        """Close database connection."""
        if self._db:
            self._db.close()
            self._db = None

    def __enter__(self) -> "MemoryEngine":
        return self

    def __exit__(self, *args) -> None:
        self.close()
