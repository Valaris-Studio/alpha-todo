# Alpha Todo CLI

A simple CLI todo app built by autonomous agents for Milestone Alpha validation.

---

## Calculator CLI (`calc.py`)

A command-line calculator supporting arithmetic and mathematical operations.

### Usage

```
python calc.py <command> [args]
```

### Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `add` | `a b` | Sum of a and b |
| `subtract` | `a b` | Difference of a minus b |
| `multiply` | `a b` | Product of a and b |
| `divide` | `a b` | Quotient of a divided by b (raises error on zero divisor) |
| `power` | `base exponent` | base raised to exponent |
| `sqrt` | `number` | Square root (exits with code 1 for negative input) |
| `mod` | `a b` | Remainder of a divided by b (raises error on zero divisor) |
| `abs` | `number` | Absolute value |
| `floor` | `x` | Largest integer ≤ x |
| `ceil` | `x` | Smallest integer ≥ x |
| `log` | `x [--base N]` | Logarithm of x in given base (default: 10) |
| `history` | `[--last N]` | Show last N calculations from history (default: 10) |

### Input Validation

All core arithmetic operations (`add`, `subtract`, `multiply`, `divide`, `mod`, `floor`, `ceil`, `log`) raise `TypeError` if either input is not an `int` or `float`. Booleans are rejected.

```python
from calculator import add
add("2", 3)   # TypeError: a must be int or float, got str
add(None, 3)  # TypeError: a must be int or float, got NoneType
```

### History

Calculations are appended to `~/.calc_history` in `expr=result` format.

### Running Tests

```
pytest test_calc.py
```
