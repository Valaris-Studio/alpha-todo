"""CLI Todo App — Milestone Alpha validation project."""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import Optional


STORAGE_FILE = "tasks.json"


class TaskStore:
    """Persists tasks to a JSON file and provides CRUD operations."""

    def __init__(self, path: str = STORAGE_FILE) -> None:
        self._path = path
        self._tasks: list[dict] = self._load()

    def _load(self) -> list[dict]:
        if not os.path.exists(self._path):
            return []
        with open(self._path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def _save(self) -> None:
        with open(self._path, "w", encoding="utf-8") as fh:
            json.dump(self._tasks, fh, indent=2)

    def _next_id(self) -> int:
        return max((t["id"] for t in self._tasks), default=0) + 1

    def add(self, title: str) -> dict:
        """Create a new task with the given title and return it."""
        task = {
            "id": self._next_id(),
            "title": title,
            "done": False,
            "created": datetime.now(timezone.utc).isoformat(),
        }
        self._tasks.append(task)
        self._save()
        return task

    def all(self) -> list[dict]:
        """Return all tasks."""
        return list(self._tasks)

    def get(self, task_id: int) -> Optional[dict]:
        """Return the task with the given id, or None if not found."""
        return next((t for t in self._tasks if t["id"] == task_id), None)

    def mark_done(self, task_id: int) -> Optional[dict]:
        """Mark a task as done and return it, or None if not found."""
        task = self.get(task_id)
        if task is None:
            return None
        task["done"] = True
        self._save()
        return task

    def delete(self, task_id: int) -> Optional[dict]:
        """Remove a task by id and return it, or None if not found."""
        task = self.get(task_id)
        if task is None:
            return None
        self._tasks = [t for t in self._tasks if t["id"] != task_id]
        self._save()
        return task

    def done_tasks(self) -> list[dict]:
        """Return all completed tasks."""
        return [t for t in self._tasks if t["done"]]


def _format_status(done: bool) -> str:
    return "done" if done else "pending"


def cmd_add(store: TaskStore, title: str) -> None:
    """Handle the 'add' subcommand."""
    task = store.add(title)
    print(f"Added task #{task['id']}: {task['title']}")


def cmd_list(store: TaskStore) -> None:
    """Handle the 'list' subcommand."""
    tasks = store.all()
    if not tasks:
        print("No tasks yet.")
        return
    _print_task_table(tasks)


def cmd_done(store: TaskStore, task_id: int) -> None:
    """Handle the 'done' subcommand."""
    task = store.mark_done(task_id)
    if task is None:
        print(f"Error: task #{task_id} not found.", file=sys.stderr)
        sys.exit(1)
    print(f"Marked task #{task['id']} as done: {task['title']}")


def cmd_delete(store: TaskStore, task_id: int) -> None:
    """Handle the 'delete' subcommand."""
    task = store.delete(task_id)
    if task is None:
        print("Task not found")
        return
    print(f"Deleted task #{task['id']}: {task['title']}")


def _print_task_table(tasks: list[dict]) -> None:
    """Print a table of tasks; prints 'No tasks.' if the list is empty."""
    if not tasks:
        print("No tasks.")
        return

    id_w = max(max(len(str(t["id"])) for t in tasks), 2)
    status_w = max(max(len(_format_status(t["done"])) for t in tasks), 6)
    title_w = max(max(len(t["title"]) for t in tasks), 5)

    header = f"{'ID':<{id_w}} | {'Status':<{status_w}} | {'Title':<{title_w}} | Created"
    print(header)
    print("-" * len(header))
    for task in tasks:
        created = task["created"][:10]
        status = _format_status(task["done"])
        print(f"{task['id']:<{id_w}} | {status:<{status_w}} | {task['title']:<{title_w}} | {created}")


def cmd_list_done(store: TaskStore) -> None:
    """Handle the 'list-done' subcommand."""
    _print_task_table(store.done_tasks())


def build_parser() -> argparse.ArgumentParser:
    """Construct and return the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="todo",
        description="A simple command-line todo app.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    subparsers.required = True

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")

    subparsers.add_parser("list", help="List all tasks")

    done_parser = subparsers.add_parser("done", help="Mark a task as done")
    done_parser.add_argument("id", type=int, metavar="ID", help="Task ID")

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, metavar="ID", help="Task ID")

    subparsers.add_parser("list-done", help="List completed tasks")

    return parser


def main() -> None:
    """Entry point — parse CLI args and dispatch to the appropriate command."""
    parser = build_parser()
    args = parser.parse_args()
    store = TaskStore()

    if args.command == "add":
        cmd_add(store, args.title)
    elif args.command == "list":
        cmd_list(store)
    elif args.command == "done":
        cmd_done(store, args.id)
    elif args.command == "delete":
        cmd_delete(store, args.id)
    elif args.command == "list-done":
        cmd_list_done(store)


if __name__ == "__main__":
    main()
