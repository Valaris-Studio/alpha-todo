"""Tests for the CLI todo app."""

import json
import os
import tempfile
from unittest.mock import patch

import pytest

from todo import TaskStore, build_parser, cmd_add, cmd_done, cmd_list


@pytest.fixture
def store(tmp_path):
    """Return a TaskStore backed by a temp file."""
    return TaskStore(path=str(tmp_path / "tasks.json"))


class TestTaskStore:
    """Tests for TaskStore persistence and CRUD."""

    def test_add_returns_task_with_fields(self, store):
        task = store.add("Buy milk")
        assert task["id"] == 1
        assert task["title"] == "Buy milk"
        assert task["done"] is False
        assert "created" in task

    def test_add_increments_ids(self, store):
        t1 = store.add("First")
        t2 = store.add("Second")
        assert t1["id"] == 1
        assert t2["id"] == 2

    def test_all_returns_all_tasks(self, store):
        store.add("A")
        store.add("B")
        assert len(store.all()) == 2

    def test_all_returns_empty_when_no_tasks(self, store):
        assert store.all() == []

    def test_get_existing_task(self, store):
        store.add("Find me")
        task = store.get(1)
        assert task is not None
        assert task["title"] == "Find me"

    def test_get_nonexistent_task(self, store):
        assert store.get(999) is None

    def test_mark_done_sets_flag(self, store):
        store.add("Finish this")
        task = store.mark_done(1)
        assert task is not None
        assert task["done"] is True

    def test_mark_done_nonexistent_returns_none(self, store):
        assert store.mark_done(42) is None

    def test_persistence_across_instances(self, tmp_path):
        path = str(tmp_path / "tasks.json")
        s1 = TaskStore(path=path)
        s1.add("Persist me")
        s2 = TaskStore(path=path)
        assert len(s2.all()) == 1
        assert s2.all()[0]["title"] == "Persist me"


class TestBuildParser:
    """Tests for argparse parser construction."""

    def test_parse_add(self):
        parser = build_parser()
        args = parser.parse_args(["add", "New task"])
        assert args.command == "add"
        assert args.title == "New task"

    def test_parse_list(self):
        parser = build_parser()
        args = parser.parse_args(["list"])
        assert args.command == "list"

    def test_parse_done(self):
        parser = build_parser()
        args = parser.parse_args(["done", "3"])
        assert args.command == "done"
        assert args.id == 3

    def test_no_command_raises(self):
        parser = build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args([])


class TestCommands:
    """Tests for CLI command handlers."""

    def test_cmd_add_prints_confirmation(self, store, capsys):
        cmd_add(store, "Write tests")
        output = capsys.readouterr().out
        assert "Added task #1" in output
        assert "Write tests" in output

    def test_cmd_list_empty(self, store, capsys):
        cmd_list(store)
        output = capsys.readouterr().out
        assert "No tasks yet" in output

    def test_cmd_list_shows_table(self, store, capsys):
        store.add("Task A")
        store.add("Task B")
        cmd_list(store)
        output = capsys.readouterr().out
        assert "ID" in output
        assert "Status" in output
        assert "Title" in output
        assert "Created" in output
        assert "Task A" in output
        assert "Task B" in output
        assert "pending" in output

    def test_cmd_list_shows_done_status(self, store, capsys):
        store.add("Done task")
        store.mark_done(1)
        cmd_list(store)
        output = capsys.readouterr().out
        assert "done" in output

    def test_cmd_done_success(self, store, capsys):
        store.add("Complete me")
        cmd_done(store, 1)
        output = capsys.readouterr().out
        assert "Marked task #1 as done" in output

    def test_cmd_done_nonexistent_exits(self, store):
        with pytest.raises(SystemExit) as exc_info:
            cmd_done(store, 999)
        assert exc_info.value.code == 1
