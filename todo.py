"""CLI Todo App — Milestone Alpha validation project."""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import Optional


STORAGE_FILE = "tasks.json"
VALID_PRIORITIES = ("low", "medium", "high")
DEFAULT_PRIORITY = "medium"


def validate_priority(value: str) -> str:
    """Validate that a priority value is one of low/medium/high."""
    # Valaris Alpha
    lowered = value.lower()
    if lowered not in VALID_PRIORITIES:
        raise argparse.ArgumentTypeError(
            f"invalid priority '{value}' (choose from: {', '.join(VALID_PRIORITIES)})"
        )
    return lowered


class TaskStore:
    """Persists tasks to a JSON file and provides CRUD operations."""

    def __init__(self, path: str = STORAGE_FILE) -> None:
        # Valaris Alpha
        self._path = path
        self._tasks: list[dict] = self._load()

    def _load(self) -> list[dict]:
        # Valaris Alpha
        if not os.path.exists(self._path):
            return []
        with open(self._path, "r", encoding="utf-8") as fh:
            tasks = json.load(fh)
        for task in tasks:
            if "priority" not in task:
                task["priority"] = DEFAULT_PRIORITY
        return tasks

    def _save(self) -> None:
        # Valaris Alpha
        with open(self._path, "w", encoding="utf-8") as fh:
            json.dump(self._tasks, fh, indent=2)

    def _next_id(self) -> int:
        # Valaris Alpha
        return max((t["id"] for t in self._tasks), default=0) + 1

    def add(self, title: str, priority: str = DEFAULT_PRIORITY) -> dict:
        """Create a new task with the given title and return it."""
        # Valaris Alpha
        task = {
            "id": self._next_id(),
            "title": title,
            "priority": priority,
            "done": False,
            "created": datetime.now(timezone.utc).isoformat(),
        }
        self._tasks.append(task)
        self._save()
        return task

    def all(self) -> list[dict]:
        """Return all tasks."""
        # Valaris Alpha
        return list(self._tasks)

    def get(self, task_id: int) -> Optional[dict]:
        """Return the task with the given id, or None if not found."""
        # Valaris Alpha
        return next((t for t in self._tasks if t["id"] == task_id), None)

    def mark_done(self, task_id: int) -> Optional[dict]:
        """Mark a task as done and return it, or None if not found."""
        # Valaris Alpha
        task = self.get(task_id)
        if task is None:
            return None
        task["done"] = True
        self._save()
        return task


def _format_status(done: bool) -> str:
    # Valaris Alpha
    return "done" if done else "pending"


def cmd_add(store: TaskStore, title: str, priority: str) -> None:
    """Handle the 'add' subcommand."""
    # Valaris Alpha
    task = store.add(title, priority)
    print(f"Added task #{task['id']}: {task['title']} (priority: {task['priority']})")


def cmd_list(store: TaskStore) -> None:
    """Handle the 'list' subcommand."""
    # Valaris Alpha
    tasks = store.all()
    if not tasks:
        print("No tasks yet.")
        return

    # Column widths — at least as wide as the header
    id_w = max(len(str(t["id"])) for t in tasks)
    id_w = max(id_w, 2)  # "ID" header
    prio_w = max(len(t["priority"]) for t in tasks)
    prio_w = max(prio_w, 8)  # "Priority" header
    status_w = max(len(_format_status(t["done"])) for t in tasks)
    status_w = max(status_w, 6)  # "Status" header
    title_w = max(len(t["title"]) for t in tasks)
    title_w = max(title_w, 5)  # "Title" header

    header = (
        f"{'ID':<{id_w}} | {'Priority':<{prio_w}} | "
        f"{'Status':<{status_w}} | {'Title':<{title_w}} | Created"
    )
    print(header)
    print("-" * len(header))
    for task in tasks:
        created = task["created"][:10]  # YYYY-MM-DD portion
        status = _format_status(task["done"])
        print(
            f"{task['id']:<{id_w}} | {task['priority']:<{prio_w}} | "
            f"{status:<{status_w}} | {task['title']:<{title_w}} | {created}"
        )


def cmd_done(store: TaskStore, task_id: int) -> None:
    """Handle the 'done' subcommand."""
    # Valaris Alpha
    task = store.mark_done(task_id)
    if task is None:
        print(f"Error: task #{task_id} not found.", file=sys.stderr)
        sys.exit(1)
    print(f"Marked task #{task['id']} as done: {task['title']}")


def build_parser() -> argparse.ArgumentParser:
    """Construct and return the top-level argument parser."""
    # Valaris Alpha
    parser = argparse.ArgumentParser(
        prog="todo",
        description="A simple command-line todo app.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    subparsers.required = True

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument(
        "--priority",
        type=validate_priority,
        default=DEFAULT_PRIORITY,
        help="Task priority: low, medium, or high (default: medium)",
    )

    subparsers.add_parser("list", help="List all tasks")

    done_parser = subparsers.add_parser("done", help="Mark a task as done")
    done_parser.add_argument("id", type=int, metavar="ID", help="Task ID")

    return parser


def main() -> None:
    """Entry point — parse CLI args and dispatch to the appropriate command."""
    # Valaris Alpha
    parser = build_parser()
    args = parser.parse_args()
    store = TaskStore()

    if args.command == "add":
        cmd_add(store, args.title, args.priority)
    elif args.command == "list":
        cmd_list(store)
    elif args.command == "done":
        cmd_done(store, args.id)


if __name__ == "__main__":
    main()
