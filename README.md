# Alpha Todo CLI

A simple CLI todo app built by autonomous agents for Milestone Alpha validation.

## Calculator

`calc.py` is a CLI arithmetic calculator.

### Usage

```
python calc.py <command> [args]
```

### Commands

| Command | Arguments | Description |
|---|---|---|
| `add` | `a b` | Return `a + b` |
| `subtract` | `a b` | Return `a - b` |
| `multiply` | `a b` | Return `a * b` |
| `divide` | `a b` | Return `a / b` — raises error on zero divisor |
| `power` | `base exponent` | Return `base ** exponent` |
| `sqrt` | `number` | Return square root — raises error for negative input |
| `mod` | `a b` | Return remainder of `a / b` — raises error on zero divisor |
| `abs` | `number` | Return absolute value of `number` |
| `history` | `[--last N]` | Show last N calculations (default: 10) |

### Examples

```
python calc.py add 10 3        # 13.0
python calc.py mod 10 3        # 1.0
python calc.py divide 10 0     # Error: Division by zero is not allowed
python calc.py history --last 5
```
