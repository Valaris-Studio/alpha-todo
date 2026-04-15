# Alpha Todo CLI

A simple CLI todo app built by autonomous agents for Milestone Alpha validation.

## Usage

```
python todo.py <command> [options]
```

### Commands

| Command | Description |
|---|---|
| `add <title>` | Add a new task |
| `list` | List all tasks |
| `done <id>` | Mark a task as done |

### `add`

```
python todo.py add "Buy groceries"
python todo.py add "Fix critical bug" --priority high
```

Options:
- `--priority {low,medium,high}` — Task priority (default: `medium`)

### `list`

Prints all tasks in a table: `ID | Priority | Status | Title | Created`

```
python todo.py list
```

### `done`

```
python todo.py done 3
```

Exits with code 1 if the task ID does not exist.

## Storage

Tasks are persisted in `tasks.json` in the working directory.

## Requirements

Python 3.10+ (stdlib only, no dependencies).
