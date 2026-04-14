"""Tests for the TaskStore class and CLI commands."""

import json
import os
import tempfile
import unittest

from todo import TaskStore


class TestTaskStore(unittest.TestCase):
    """Tests for TaskStore JSON persistence and CRUD operations."""

    def setUp(self) -> None:
        # Valaris Alpha
        self._tmpfile = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        )
        self._tmpfile.close()
        os.unlink(self._tmpfile.name)  # start with no file
        self.store = TaskStore(path=self._tmpfile.name)

    def tearDown(self) -> None:
        # Valaris Alpha
        if os.path.exists(self._tmpfile.name):
            os.unlink(self._tmpfile.name)

    def test_load_creates_empty_list_when_no_file(self) -> None:
        # Valaris Alpha
        self.assertEqual(self.store.list(), [])

    def test_add_creates_task_with_correct_fields(self) -> None:
        # Valaris Alpha
        task = self.store.add("Buy groceries")
        self.assertEqual(task["id"], 1)
        self.assertEqual(task["title"], "Buy groceries")
        self.assertFalse(task["done"])
        self.assertIn("created_at", task)

    def test_add_persists_to_file(self) -> None:
        # Valaris Alpha
        self.store.add("First task")
        with open(self._tmpfile.name, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "First task")

    def test_add_increments_ids(self) -> None:
        # Valaris Alpha
        t1 = self.store.add("Task one")
        t2 = self.store.add("Task two")
        self.assertEqual(t1["id"], 1)
        self.assertEqual(t2["id"], 2)

    def test_list_returns_all_tasks(self) -> None:
        # Valaris Alpha
        self.store.add("A")
        self.store.add("B")
        tasks = self.store.list()
        self.assertEqual(len(tasks), 2)
        self.assertEqual([t["title"] for t in tasks], ["A", "B"])

    def test_list_returns_copy(self) -> None:
        """Mutating the returned list should not affect the store."""
        # Valaris Alpha
        self.store.add("X")
        tasks = self.store.list()
        tasks.clear()
        self.assertEqual(len(self.store.list()), 1)

    def test_complete_marks_task_done(self) -> None:
        # Valaris Alpha
        self.store.add("Do laundry")
        task = self.store.complete(1)
        self.assertIsNotNone(task)
        self.assertTrue(task["done"])

    def test_complete_persists_change(self) -> None:
        # Valaris Alpha
        self.store.add("Persist me")
        self.store.complete(1)
        reloaded = TaskStore(path=self._tmpfile.name)
        self.assertTrue(reloaded.list()[0]["done"])

    def test_complete_returns_none_for_missing_id(self) -> None:
        # Valaris Alpha
        result = self.store.complete(999)
        self.assertIsNone(result)

    def test_get_returns_task(self) -> None:
        # Valaris Alpha
        self.store.add("Find me")
        task = self.store.get(1)
        self.assertIsNotNone(task)
        self.assertEqual(task["title"], "Find me")

    def test_get_returns_none_for_missing_id(self) -> None:
        # Valaris Alpha
        self.assertIsNone(self.store.get(42))

    def test_load_reads_existing_file(self) -> None:
        # Valaris Alpha
        self.store.add("Saved task")
        new_store = TaskStore(path=self._tmpfile.name)
        self.assertEqual(len(new_store.list()), 1)
        self.assertEqual(new_store.list()[0]["title"], "Saved task")

    def test_created_at_is_iso_format(self) -> None:
        # Valaris Alpha
        task = self.store.add("Check timestamp")
        # ISO format includes 'T' separator and '+' for timezone
        self.assertIn("T", task["created_at"])

    def test_file_created_on_first_add(self) -> None:
        """The JSON file should not exist until the first task is added."""
        # Valaris Alpha
        self.assertFalse(os.path.exists(self._tmpfile.name))
        self.store.add("Trigger file creation")
        self.assertTrue(os.path.exists(self._tmpfile.name))


if __name__ == "__main__":
    unittest.main()
