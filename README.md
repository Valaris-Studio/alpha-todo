# Alpha Todo CLI

A simple CLI todo app built by autonomous agents for Milestone Alpha validation.

---

## Calculator (`calc.py`)

A command-line arithmetic calculator with history tracking.

### Commands

| Command | Args | Description |
|---|---|---|
| `add` | `a b` | Add two numbers |
| `subtract` | `a b` | Subtract b from a |
| `multiply` | `a b` | Multiply two numbers |
| `divide` | `a b` | Divide a by b (raises error on zero divisor) |
| `power` | `base exponent` | Raise base to an exponent |
| `sqrt` | `number` | Square root (exits with code 1 for negatives) |
| `mod` | `a b` | Compute a modulo b (exits with code 1 on zero divisor) |
| `abs` | `number` | Absolute value |
| `percentage` | `value percent` | Compute `percent`% of `value` (e.g. `percentage 200 15` → `30.0`) |
| `history` | `[--last N]` | Show last N calculations (default 10) from `~/.calc_history` |

### Usage

```bash
python calc.py add 3 4          # 7.0
python calc.py divide 10 0      # Error: Division by zero is not allowed
python calc.py power 2 10       # 1024.0
python calc.py percentage 200 15  # 30.0
python calc.py history --last 5
```

### Running Tests

```bash
pytest test_calc.py
```
