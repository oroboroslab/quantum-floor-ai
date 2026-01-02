#!/usr/bin/env python3
"""
Connection-Core Test Suite
==========================

Tests for the memory engine.
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, '..')

from connection_core import MemoryEngine, Memory, MemoryConfig


class TestMemoryEngine(unittest.TestCase):
    """Tests for MemoryEngine."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_memory.db")

        config = MemoryConfig(storage_path=self.db_path)
        self.engine = MemoryEngine(config)

    def tearDown(self):
        """Clean up."""
        self.engine.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        os.rmdir(self.temp_dir)

    def test_add_memory(self):
        """Test adding a memory."""
        memory = self.engine.add("Test memory content")

        self.assertIsInstance(memory, Memory)
        self.assertEqual(memory.content, "Test memory content")
        self.assertIsNotNone(memory.id)
        self.assertGreater(memory.created_at, 0)

    def test_add_with_options(self):
        """Test adding memory with options."""
        memory = self.engine.add(
            content="Important fact",
            importance=0.9,
            tags=["important", "fact"],
            metadata={"source": "test"}
        )

        self.assertEqual(memory.importance, 0.9)
        self.assertEqual(memory.tags, ["important", "fact"])
        self.assertEqual(memory.metadata["source"], "test")

    def test_recall(self):
        """Test recalling memories."""
        self.engine.add("Python is a programming language")
        self.engine.add("JavaScript runs in browsers")
        self.engine.add("Python is used for AI")

        results = self.engine.recall("Python", limit=5)

        self.assertGreater(len(results), 0)
        self.assertTrue(any("Python" in m.content for m in results))

    def test_get_memory(self):
        """Test getting a specific memory."""
        original = self.engine.add("Unique content")
        retrieved = self.engine.get(original.id)

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, original.id)
        self.assertEqual(retrieved.content, original.content)

    def test_update_memory(self):
        """Test updating a memory."""
        memory = self.engine.add("Original content")
        updated = self.engine.update(
            memory.id,
            content="Updated content",
            importance=0.8
        )

        self.assertEqual(updated.content, "Updated content")
        self.assertEqual(updated.importance, 0.8)

    def test_delete_memory(self):
        """Test deleting a memory."""
        memory = self.engine.add("To be deleted")
        success = self.engine.delete(memory.id)

        self.assertTrue(success)
        self.assertIsNone(self.engine.get(memory.id))

    def test_clear(self):
        """Test clearing all memories."""
        self.engine.add("Memory 1")
        self.engine.add("Memory 2")
        self.engine.add("Memory 3")

        count = self.engine.clear()

        self.assertEqual(count, 3)
        self.assertEqual(self.engine.count(), 0)

    def test_count(self):
        """Test counting memories."""
        self.assertEqual(self.engine.count(), 0)

        self.engine.add("Memory 1")
        self.engine.add("Memory 2")

        self.assertEqual(self.engine.count(), 2)

    def test_stats(self):
        """Test getting statistics."""
        self.engine.add("Memory 1", importance=0.5)
        self.engine.add("Memory 2", importance=0.7)

        stats = self.engine.get_stats()

        self.assertEqual(stats["total_memories"], 2)
        self.assertAlmostEqual(stats["average_importance"], 0.6, places=1)
        self.assertGreater(stats["database_size_bytes"], 0)

    def test_export_import(self):
        """Test exporting and importing memories."""
        self.engine.add("Export test 1")
        self.engine.add("Export test 2")

        export_path = os.path.join(self.temp_dir, "export.json")
        exported = self.engine.export(export_path)

        self.assertEqual(exported, 2)
        self.assertTrue(os.path.exists(export_path))

        # Clear and import
        self.engine.clear()
        imported = self.engine.import_memories(export_path)

        self.assertEqual(imported, 2)
        self.assertEqual(self.engine.count(), 2)

    def test_max_memories_limit(self):
        """Test that max memories limit is enforced."""
        config = MemoryConfig(
            storage_path=self.db_path,
            max_memories=5
        )
        engine = MemoryEngine(config)

        for i in range(10):
            engine.add(f"Memory {i}", importance=i/10)

        # Should only have 5 memories
        self.assertEqual(engine.count(), 5)

        engine.close()

    def test_importance_decay(self):
        """Test importance decay."""
        self.engine.add("Decay test", importance=1.0)

        updated = self.engine.decay_importance()

        memory = self.engine.recall("Decay test", limit=1)[0]
        self.assertLess(memory.importance, 1.0)


class TestMemoryOperations(unittest.TestCase):
    """Additional memory operation tests."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_memory.db")
        config = MemoryConfig(storage_path=self.db_path)
        self.engine = MemoryEngine(config)

    def tearDown(self):
        self.engine.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        os.rmdir(self.temp_dir)

    def test_search_relevance(self):
        """Test that search returns relevant results."""
        self.engine.add("The weather is sunny today")
        self.engine.add("I need to buy groceries")
        self.engine.add("The sunny weather is perfect for a walk")

        results = self.engine.recall("sunny weather", limit=5)

        # Both weather-related memories should be returned
        self.assertGreaterEqual(len(results), 2)

    def test_empty_search(self):
        """Test search with empty query."""
        self.engine.add("Memory 1", importance=0.5)
        self.engine.add("Memory 2", importance=0.9)

        results = self.engine.recall("", limit=5)

        # Should return highest importance memories
        self.assertGreater(len(results), 0)

    def test_nonexistent_memory(self):
        """Test operations on non-existent memory."""
        result = self.engine.get("nonexistent_id")
        self.assertIsNone(result)

        result = self.engine.update("nonexistent_id", content="new")
        self.assertIsNone(result)

        result = self.engine.delete("nonexistent_id")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
