"""Tests for the priority field feature in the todo CLI app."""

import json
import os
import tempfile

import pytest

from todo import (
    TaskStore, build_parser, cmd_add, cmd_list, cmd_done, cmd_delete,
    cmd_list_done, validate_priority, DEFAULT_PRIORITY, VALID_PRIORITIES,
)


@pytest.fixture
def tmp_store(tmp_path):
    """Return a TaskStore backed by a temporary JSON file."""
    path = str(tmp_path / "tasks.json")
    return TaskStore(path=path)


# --- validate_priority ---

def test_validate_priority_accepts_valid_values():
    for p in VALID_PRIORITIES:
        assert validate_priority(p) == p


def test_validate_priority_case_insensitive():
    assert validate_priority("HIGH") == "high"
    assert validate_priority("Low") == "low"


def test_validate_priority_rejects_invalid():
    with pytest.raises(Exception) as exc_info:
        validate_priority("urgent")
    assert "invalid priority" in str(exc_info.value)


# --- TaskStore.add with priority ---

def test_add_default_priority(tmp_store):
    task = tmp_store.add("Buy groceries")
    assert task["priority"] == "medium"


def test_add_explicit_priority(tmp_store):
    task = tmp_store.add("Fix bug", priority="high")
    assert task["priority"] == "high"


def test_add_low_priority(tmp_store):
    task = tmp_store.add("Nice to have", priority="low")
    assert task["priority"] == "low"


# --- Backfill missing priority on load ---

def test_load_backfills_missing_priority(tmp_path):
    path = str(tmp_path / "tasks.json")
    legacy_tasks = [
        {"id": 1, "title": "Old task", "done": False, "created": "2026-01-01T00:00:00+00:00"}
    ]
    with open(path, "w") as fh:
        json.dump(legacy_tasks, fh)

    store = TaskStore(path=path)
    tasks = store.all()
    assert tasks[0]["priority"] == "medium"


# --- CLI parser ---

def test_parser_add_default_priority():
    parser = build_parser()
    args = parser.parse_args(["add", "Test task"])
    assert args.priority == "medium"


def test_parser_add_explicit_priority():
    parser = build_parser()
    args = parser.parse_args(["add", "--priority", "high", "Test task"])
    assert args.priority == "high"


def test_parser_add_invalid_priority():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["add", "--priority", "urgent", "Test task"])


# --- cmd_add output ---

def test_cmd_add_prints_priority(tmp_store, capsys):
    cmd_add(tmp_store, "Buy milk", "high")
    captured = capsys.readouterr()
    assert "priority: high" in captured.out


# --- cmd_list output ---

def test_cmd_list_shows_priority_column(tmp_store, capsys):
    tmp_store.add("Task A", priority="high")
    tmp_store.add("Task B", priority="low")
    cmd_list(tmp_store)
    captured = capsys.readouterr()
    lines = captured.out.strip().split("\n")
    assert "Priority" in lines[0]
    assert "high" in lines[2]
    assert "low" in lines[3]


def test_cmd_list_empty(tmp_store, capsys):
    cmd_list(tmp_store)
    captured = capsys.readouterr()
    assert "No tasks yet." in captured.out


# --- Priority persists through save/load cycle ---

def test_priority_persists(tmp_path):
    path = str(tmp_path / "tasks.json")
    store1 = TaskStore(path=path)
    store1.add("Persist me", priority="high")

    store2 = TaskStore(path=path)
    assert store2.all()[0]["priority"] == "high"


# --- TaskStore.delete ---

def test_delete_returns_deleted_task(tmp_store):
    task = tmp_store.add("Delete me")
    result = tmp_store.delete(task["id"])
    assert result["title"] == "Delete me"
    assert tmp_store.all() == []


def test_delete_not_found_returns_none(tmp_store):
    assert tmp_store.delete(999) is None


def test_delete_persists(tmp_path):
    path = str(tmp_path / "tasks.json")
    store = TaskStore(path=path)
    task = store.add("Will be deleted")
    store.delete(task["id"])

    reloaded = TaskStore(path=path)
    assert reloaded.all() == []


# --- TaskStore.done_tasks ---

def test_done_tasks_returns_only_completed(tmp_store):
    tmp_store.add("Pending task")
    tmp_store.add("Done task")
    tmp_store.mark_done(2)
    done = tmp_store.done_tasks()
    assert len(done) == 1
    assert done[0]["title"] == "Done task"


def test_done_tasks_empty_when_none_done(tmp_store):
    tmp_store.add("Not done")
    assert tmp_store.done_tasks() == []


# --- cmd_delete ---

def test_cmd_delete_prints_confirmation(tmp_store, capsys):
    tmp_store.add("To delete")
    cmd_delete(tmp_store, 1)
    captured = capsys.readouterr()
    assert "Deleted task #1" in captured.out
    assert "To delete" in captured.out


def test_cmd_delete_not_found_exits(tmp_store, capsys):
    with pytest.raises(SystemExit) as exc_info:
        cmd_delete(tmp_store, 999)
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "not found" in captured.err


# --- cmd_list_done ---

def test_cmd_list_done_shows_completed(tmp_store, capsys):
    tmp_store.add("Done one")
    tmp_store.add("Pending one")
    tmp_store.mark_done(1)
    cmd_list_done(tmp_store)
    captured = capsys.readouterr()
    assert "Done one" in captured.out
    assert "Pending one" not in captured.out
    assert "Status" in captured.out


def test_cmd_list_done_empty(tmp_store, capsys):
    tmp_store.add("Not done yet")
    cmd_list_done(tmp_store)
    captured = capsys.readouterr()
    assert "No completed tasks." in captured.out


# --- Parser: delete and list-done ---

def test_parser_delete_subcommand():
    parser = build_parser()
    args = parser.parse_args(["delete", "42"])
    assert args.command == "delete"
    assert args.id == 42


def test_parser_list_done_subcommand():
    parser = build_parser()
    args = parser.parse_args(["list-done"])
    assert args.command == "list-done"
