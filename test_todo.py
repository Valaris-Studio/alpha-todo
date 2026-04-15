"""Tests for the todo CLI app."""

import json
import os
import tempfile

import pytest

from todo import TaskStore, build_parser, cmd_add, cmd_list, cmd_done, cmd_search, validate_priority, DEFAULT_PRIORITY, VALID_PRIORITIES


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


# --- TaskStore.search ---

def test_search_returns_matching_tasks(tmp_store):
    tmp_store.add("Buy groceries")
    tmp_store.add("Clean house")
    tmp_store.add("Buy milk")
    results = tmp_store.search("buy")
    assert len(results) == 2
    assert all("buy" in t["title"].lower() for t in results)


def test_search_case_insensitive(tmp_store):
    tmp_store.add("Write REPORT")
    results = tmp_store.search("report")
    assert len(results) == 1
    assert results[0]["title"] == "Write REPORT"


def test_search_no_matches(tmp_store):
    tmp_store.add("Buy groceries")
    results = tmp_store.search("xyz")
    assert results == []


def test_search_empty_store(tmp_store):
    results = tmp_store.search("anything")
    assert results == []


# --- cmd_search ---

def test_cmd_search_displays_matches(tmp_store, capsys):
    tmp_store.add("Buy groceries", priority="high")
    tmp_store.add("Clean house", priority="low")
    tmp_store.add("Buy milk", priority="medium")
    cmd_search(tmp_store, "buy")
    captured = capsys.readouterr()
    lines = captured.out.strip().split("\n")
    assert "Priority" in lines[0]
    assert "Buy groceries" in lines[2]
    assert "Buy milk" in lines[3]
    assert "Clean house" not in captured.out


def test_cmd_search_no_matches_message(tmp_store, capsys):
    tmp_store.add("Buy groceries")
    cmd_search(tmp_store, "xyz")
    captured = capsys.readouterr()
    assert 'No tasks matching "xyz"' in captured.out


def test_cmd_search_no_matches_empty_store(tmp_store, capsys):
    cmd_search(tmp_store, "anything")
    captured = capsys.readouterr()
    assert 'No tasks matching "anything"' in captured.out


# --- search parser ---

def test_parser_search_requires_query():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["search"])


def test_parser_search_accepts_query():
    parser = build_parser()
    args = parser.parse_args(["search", "groceries"])
    assert args.command == "search"
    assert args.query == "groceries"
