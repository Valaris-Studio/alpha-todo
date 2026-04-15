# Alpha Todo CLI

A simple CLI todo app built by autonomous agents for Milestone Alpha validation.

## Calculator (`calc.py`)

A Python CLI calculator supporting basic arithmetic and math operations.

### Commands

| Command | Description | Example |
|---|---|---|
| `add a b` | Add two numbers | `python calc.py add 3 4` |
| `subtract a b` | Subtract b from a | `python calc.py subtract 10 3` |
| `multiply a b` | Multiply two numbers | `python calc.py multiply 5 6` |
| `divide a b` | Divide a by b (raises error on zero) | `python calc.py divide 10 2` |
| `power base exp` | Raise base to exponent | `python calc.py power 2 8` |
| `sqrt number` | Square root (exits 1 for negative) | `python calc.py sqrt 9` |
| `mod a b` | Modulo a % b (exits 1 on zero divisor) | `python calc.py mod 10 3` |
| `abs number` | Absolute value | `python calc.py abs -5` |
| `factorial n` | n! iterative (n ≥ 0, integer, n ≤ 170) | `python calc.py factorial 5` |
| `percentage value pct` | Compute pct% of value | `python calc.py percentage 200 15` |
| `history [--last N]` | Show last N calculations (default 10) | `python calc.py history --last 5` |

### Notes

- `factorial` accepts non-negative integers only; raises `ValueError` for negative values, floats, or inputs exceeding `MAX_FACTORIAL_INPUT = 170` (the largest n where n! fits in a float without overflow).
- All calculations are appended to `~/.calc_history` in `expr=result` format.

### Running tests

```bash
pytest test_calc.py
```
