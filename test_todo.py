"""Tests for the todo CLI app."""

import json
import os
import tempfile
from unittest.mock import patch
from datetime import date

import pytest

from todo import (
    TaskStore, build_parser, cmd_add, cmd_list, cmd_done,
    validate_priority, validate_due_date, _format_due,
    DEFAULT_PRIORITY, VALID_PRIORITIES,
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


# --- validate_due_date ---

def test_validate_due_date_accepts_valid():
    assert validate_due_date("2026-05-01") == "2026-05-01"
    assert validate_due_date("2026-12-31") == "2026-12-31"


def test_validate_due_date_rejects_bad_format():
    with pytest.raises(Exception) as exc_info:
        validate_due_date("05-01-2026")
    assert "invalid date format" in str(exc_info.value)


def test_validate_due_date_rejects_non_date_string():
    with pytest.raises(Exception) as exc_info:
        validate_due_date("not-a-date")
    assert "invalid date format" in str(exc_info.value)


def test_validate_due_date_rejects_invalid_calendar_date():
    with pytest.raises(Exception) as exc_info:
        validate_due_date("2026-02-30")
    assert "invalid date" in str(exc_info.value)


# --- TaskStore.add with due_date ---

def test_add_default_no_due_date(tmp_store):
    task = tmp_store.add("No deadline")
    assert task["due_date"] is None


def test_add_with_due_date(tmp_store):
    task = tmp_store.add("Has deadline", due_date="2026-05-01")
    assert task["due_date"] == "2026-05-01"


# --- Backfill missing due_date on load ---

def test_load_backfills_missing_due_date(tmp_path):
    path = str(tmp_path / "tasks.json")
    legacy_tasks = [
        {"id": 1, "title": "Old task", "priority": "medium", "done": False, "created": "2026-01-01T00:00:00+00:00"}
    ]
    with open(path, "w") as fh:
        json.dump(legacy_tasks, fh)

    store = TaskStore(path=path)
    tasks = store.all()
    assert tasks[0]["due_date"] is None


# --- _format_due ---

def test_format_due_none():
    assert _format_due(None) == ""


def test_format_due_future_date():
    with patch("todo.date") as mock_date:
        mock_date.today.return_value = date(2026, 1, 1)
        mock_date.fromisoformat = date.fromisoformat
        assert _format_due("2026-12-31") == "2026-12-31"


def test_format_due_overdue():
    with patch("todo.date") as mock_date:
        mock_date.today.return_value = date(2026, 6, 1)
        mock_date.fromisoformat = date.fromisoformat
        assert _format_due("2026-05-01") == "2026-05-01 [OVERDUE]"


def test_format_due_today_not_overdue():
    with patch("todo.date") as mock_date:
        mock_date.today.return_value = date(2026, 5, 1)
        mock_date.fromisoformat = date.fromisoformat
        assert _format_due("2026-05-01") == "2026-05-01"


# --- CLI parser with --due ---

def test_parser_add_no_due_date():
    parser = build_parser()
    args = parser.parse_args(["add", "Test task"])
    assert args.due is None


def test_parser_add_with_due_date():
    parser = build_parser()
    args = parser.parse_args(["add", "--due", "2026-05-01", "Test task"])
    assert args.due == "2026-05-01"


def test_parser_add_invalid_due_date():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["add", "--due", "not-a-date", "Test task"])


# --- cmd_add output with due date ---

def test_cmd_add_prints_due_date(tmp_store, capsys):
    cmd_add(tmp_store, "Buy milk", "medium", due_date="2026-05-01")
    captured = capsys.readouterr()
    assert "due: 2026-05-01" in captured.out


def test_cmd_add_no_due_date_omits_due(tmp_store, capsys):
    cmd_add(tmp_store, "Buy milk", "medium")
    captured = capsys.readouterr()
    assert "due:" not in captured.out


# --- cmd_list output with due column ---

def test_cmd_list_shows_due_column(tmp_store, capsys):
    tmp_store.add("Task A", due_date="2026-05-01")
    tmp_store.add("Task B")
    with patch("todo.date") as mock_date:
        mock_date.today.return_value = date(2026, 1, 1)
        mock_date.fromisoformat = date.fromisoformat
        cmd_list(tmp_store)
    captured = capsys.readouterr()
    lines = captured.out.strip().split("\n")
    assert "Due" in lines[0]
    assert "2026-05-01" in lines[2]


def test_cmd_list_shows_overdue_marker(tmp_store, capsys):
    tmp_store.add("Overdue task", due_date="2025-01-01")
    with patch("todo.date") as mock_date:
        mock_date.today.return_value = date(2026, 4, 15)
        mock_date.fromisoformat = date.fromisoformat
        cmd_list(tmp_store)
    captured = capsys.readouterr()
    assert "[OVERDUE]" in captured.out


# --- Due date persists through save/load cycle ---

def test_due_date_persists(tmp_path):
    path = str(tmp_path / "tasks.json")
    store1 = TaskStore(path=path)
    store1.add("Deadline task", due_date="2026-05-01")

    store2 = TaskStore(path=path)
    assert store2.all()[0]["due_date"] == "2026-05-01"


def test_due_date_null_persists(tmp_path):
    path = str(tmp_path / "tasks.json")
    store1 = TaskStore(path=path)
    store1.add("No deadline")

    store2 = TaskStore(path=path)
    assert store2.all()[0]["due_date"] is None
