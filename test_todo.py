"""Tests for the TaskStore class and CLI commands."""

import json
import os
import tempfile

import pytest

from todo import TaskStore, build_parser, cmd_add, cmd_done, cmd_list


@pytest.fixture()
def store(tmp_path):
    """Return a TaskStore backed by a temporary JSON file."""
    # Valaris Alpha
    path = str(tmp_path / "tasks.json")
    return TaskStore(path=path)


class TestTaskStoreAdd:

    def test_add_returns_task_with_expected_fields(self, store):
        # Valaris Alpha
        task = store.add("Buy milk")
        assert task["id"] == 1
        assert task["title"] == "Buy milk"
        assert task["done"] is False
        assert "created_at" in task

    def test_add_increments_id(self, store):
        # Valaris Alpha
        t1 = store.add("First")
        t2 = store.add("Second")
        assert t2["id"] == t1["id"] + 1

    def test_add_persists_to_disk(self, store):
        # Valaris Alpha
        store.add("Persisted task")
        with open(store._path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        assert len(data) == 1
        assert data[0]["title"] == "Persisted task"


class TestTaskStoreList:

    def test_list_empty(self, store):
        # Valaris Alpha
        assert store.list() == []

    def test_list_returns_all_tasks(self, store):
        # Valaris Alpha
        store.add("A")
        store.add("B")
        assert len(store.list()) == 2

    def test_list_returns_copy(self, store):
        # Valaris Alpha
        store.add("Original")
        tasks = store.list()
        tasks.clear()
        assert len(store.list()) == 1


class TestTaskStoreComplete:

    def test_complete_marks_done(self, store):
        # Valaris Alpha
        store.add("Finish report")
        task = store.complete(1)
        assert task is not None
        assert task["done"] is True

    def test_complete_persists(self, store):
        # Valaris Alpha
        store.add("Persist done")
        store.complete(1)
        reloaded = TaskStore(path=store._path)
        assert reloaded.get(1)["done"] is True

    def test_complete_nonexistent_returns_none(self, store):
        # Valaris Alpha
        assert store.complete(999) is None


class TestTaskStoreLoad:

    def test_load_creates_empty_list_when_no_file(self, tmp_path):
        # Valaris Alpha
        path = str(tmp_path / "nonexistent.json")
        store = TaskStore(path=path)
        assert store.list() == []

    def test_load_reads_existing_file(self, tmp_path):
        # Valaris Alpha
        path = str(tmp_path / "existing.json")
        seed = [{"id": 1, "title": "Seeded", "done": False, "created_at": "2026-01-01T00:00:00+00:00"}]
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(seed, fh)
        store = TaskStore(path=path)
        assert len(store.list()) == 1
        assert store.list()[0]["title"] == "Seeded"


class TestTaskStoreSave:

    def test_save_creates_file(self, tmp_path):
        # Valaris Alpha
        path = str(tmp_path / "new.json")
        store = TaskStore(path=path)
        store.add("Create file")
        assert os.path.exists(path)


class TestCLICommands:

    def test_cmd_add_prints_confirmation(self, store, capsys):
        # Valaris Alpha
        cmd_add(store, "Test task")
        output = capsys.readouterr().out
        assert "Added task #1" in output
        assert "Test task" in output

    def test_cmd_list_empty(self, store, capsys):
        # Valaris Alpha
        cmd_list(store)
        output = capsys.readouterr().out
        assert "No tasks yet." in output

    def test_cmd_list_shows_tasks(self, store, capsys):
        # Valaris Alpha
        store.add("Listed task")
        cmd_list(store)
        output = capsys.readouterr().out
        assert "Listed task" in output
        assert "pending" in output

    def test_cmd_done_marks_complete(self, store, capsys):
        # Valaris Alpha
        store.add("To complete")
        cmd_done(store, 1)
        output = capsys.readouterr().out
        assert "Marked task #1 as done" in output

    def test_cmd_done_nonexistent_exits(self, store):
        # Valaris Alpha
        with pytest.raises(SystemExit) as exc_info:
            cmd_done(store, 999)
        assert exc_info.value.code == 1


class TestBuildParser:

    def test_parse_add(self):
        # Valaris Alpha
        parser = build_parser()
        args = parser.parse_args(["add", "New task"])
        assert args.command == "add"
        assert args.title == "New task"

    def test_parse_list(self):
        # Valaris Alpha
        parser = build_parser()
        args = parser.parse_args(["list"])
        assert args.command == "list"

    def test_parse_done(self):
        # Valaris Alpha
        parser = build_parser()
        args = parser.parse_args(["done", "42"])
        assert args.command == "done"
        assert args.id == 42
