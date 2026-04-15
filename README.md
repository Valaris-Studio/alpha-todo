# Alpha Todo CLI

A simple CLI todo app built by autonomous agents for Milestone Alpha validation.

---

## Calculator (`calc.py`)

A command-line arithmetic calculator with history support.

### Usage

```
python calc.py <command> [args]
```

### Commands

| Command | Args | Description |
|---|---|---|
| `add` | `a b` | Add two numbers |
| `subtract` | `a b` | Subtract b from a |
| `multiply` | `a b` | Multiply two numbers |
| `divide` | `a b` | Divide a by b (raises error on zero divisor) |
| `power` | `base exponent` | Raise base to the given exponent |
| `sqrt` | `number` | Square root (exits with code 1 for negative input) |
| `mod` | `a b` | Compute a modulo b (exits with code 1 on zero divisor) |
| `abs` | `number` | Absolute value |
| `history` | `[--last N]` | Show last N calculations (default: 10) |

### Error Handling

- **Division by zero**: `divide` raises a `ValueError` with the message `"Division by zero is not allowed"`. The CLI catches this and exits with code 1.
- **Square root of negative number**: prints an error to stderr and exits with code 1.
- **Modulo by zero**: prints an error to stderr and exits with code 1.

### Examples

```bash
python calc.py add 3 5        # 8.0
python calc.py divide 10 2    # 5.0
python calc.py divide 10 0    # Error: Division by zero is not allowed (exit 1)
python calc.py power 2 8      # 256.0
python calc.py sqrt 16        # 4.0
python calc.py abs -- -7      # 7.0
python calc.py history --last 5
```

### History

Each successful calculation is appended to `~/.calc_history` in `expr=result` format.

### Running Tests

```bash
pytest test_calc.py
```
