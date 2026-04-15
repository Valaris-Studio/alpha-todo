"""Tests for the todo CLI app."""

import csv
import json
import os
import tempfile

import pytest

from todo import TaskStore, build_parser, cmd_add, cmd_list, cmd_done, cmd_export, validate_priority, DEFAULT_PRIORITY, VALID_PRIORITIES


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


# --- cmd_export ---

def test_export_writes_csv(tmp_store, tmp_path, capsys):
    tmp_store.add("Task A", priority="high")
    tmp_store.add("Task B", priority="low")
    output_path = str(tmp_path / "out.csv")
    cmd_export(tmp_store, output_path)
    captured = capsys.readouterr()
    assert "Exported 2 tasks to" in captured.out
    assert "out.csv" in captured.out

    with open(output_path, newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        rows = list(reader)
    assert rows[0] == ["id", "title", "done", "created_at"]
    assert len(rows) == 3  # header + 2 tasks
    assert rows[1][1] == "Task A"
    assert rows[2][1] == "Task B"


def test_export_csv_columns_match(tmp_store, tmp_path):
    task = tmp_store.add("Check columns")
    tmp_store.mark_done(task["id"])
    output_path = str(tmp_path / "out.csv")
    cmd_export(tmp_store, output_path)

    with open(output_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
    assert rows[0]["id"] == str(task["id"])
    assert rows[0]["title"] == "Check columns"
    assert rows[0]["done"] == "True"
    assert rows[0]["created_at"] == task["created"]


def test_export_no_tasks(tmp_store, capsys):
    cmd_export(tmp_store, "unused.csv")
    captured = capsys.readouterr()
    assert "No tasks to export" in captured.out
    assert not os.path.exists("unused.csv")


def test_export_file_write_error(tmp_store, capsys):
    tmp_store.add("Will fail")
    bad_path = "/nonexistent_dir/nope.csv"
    with pytest.raises(SystemExit) as exc_info:
        cmd_export(tmp_store, bad_path)
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert captured.err  # something printed to stderr


def test_export_default_filename(tmp_store, tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    tmp_store.add("Default file")
    cmd_export(tmp_store, "tasks.csv")
    captured = capsys.readouterr()
    assert "tasks.csv" in captured.out
    assert os.path.exists(tmp_path / "tasks.csv")


# --- parser: export subcommand ---

def test_parser_export_default_output():
    parser = build_parser()
    args = parser.parse_args(["export"])
    assert args.output == "tasks.csv"


def test_parser_export_custom_output():
    parser = build_parser()
    args = parser.parse_args(["export", "--output", "my_tasks.csv"])
    assert args.output == "my_tasks.csv"
