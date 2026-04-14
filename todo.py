"""CLI Todo App — Milestone Alpha validation project."""

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional


TASKS_FILE = "tasks.json"


@dataclass
class Task:
    id: int
    title: str
    done: bool
    created_at: str


class TaskStore:
    """Reads and writes tasks to a JSON file."""

    def __init__(self, filepath: str = TASKS_FILE):
        self._filepath = filepath

    def load(self) -> list[Task]:
        """Load all tasks from disk; returns empty list if file absent."""
        if not os.path.exists(self._filepath):
            return []
        with open(self._filepath, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
        return [Task(**item) for item in raw]

    def save(self, tasks: list[Task]) -> None:
        """Persist tasks list to disk."""
        with open(self._filepath, "w", encoding="utf-8") as fh:
            json.dump([asdict(t) for t in tasks], fh, indent=2)

    def add(self, title: str) -> Task:
        """Create a new task, persist it, and return it."""
        tasks = self.load()
        next_id = (max(t.id for t in tasks) + 1) if tasks else 1
        task = Task(
            id=next_id,
            title=title,
            done=False,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        tasks.append(task)
        self.save(tasks)
        return task

    def list(self) -> list[Task]:
        """Return all tasks."""
        return self.load()

    def complete(self, task_id: int) -> Optional[Task]:
        """Mark a task as done by id; returns the updated task or None if not found."""
        tasks = self.load()
        for task in tasks:
            if task.id == task_id:
                task.done = True
                self.save(tasks)
                return task
        return None
