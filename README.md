# Alpha Todo CLI

A simple CLI todo app built by autonomous agents for Milestone Alpha validation.

## Calculator (`calc.py`)

A CLI arithmetic calculator with history tracking.

### Usage

```
python calc.py <command> [args]
```

### Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `add` | `a b` | Add two numbers |
| `subtract` | `a b` | Subtract b from a |
| `multiply` | `a b` | Multiply two numbers |
| `divide` | `a b` | Divide a by b (raises error on division by zero) |
| `power` | `base exponent` | Raise base to exponent (0\*\*0 returns 1) |
| `sqrt` | `number` | Square root (exits with error for negative input) |
| `mod` | `a b` | Compute a modulo b |
| `abs` | `number` | Absolute value of a number |
| `percentage` | `value percent` | Compute `percent`% of `value` |
| `factorial` | `n` | Factorial of a non-negative integer (max n=170) |
| `history` | `[--last N]` | Show last N calculation history entries (default: 10) |

### Examples

```bash
python calc.py add 3 5          # 8.0
python calc.py divide 10 4      # 2.5
python calc.py power 2 8        # 256.0
python calc.py abs -- -42       # 42.0
python calc.py factorial 10     # 3628800
python calc.py percentage 200 15  # 30.0
python calc.py history --last 5
```

### Error Handling

- `divide`: raises `ValueError` on division by zero
- `power`: raises `ValueError` for non-numeric input
- `abs`: raises `ValueError` for non-numeric input
- `factorial`: raises `ValueError` for negative, non-integer, or input exceeding 170
- `percentage`: raises `ValueError` for non-numeric input

### History

Calculations are appended to `~/.calc_history` in `expr=result` format.
