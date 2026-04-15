# Alpha Todo CLI

A simple CLI calculator app built by autonomous agents for Milestone Alpha validation.

## Usage

```
python calc.py <command> [args]
```

## Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `add` | `a b` | Add two numbers |
| `subtract` | `a b` | Subtract b from a |
| `multiply` | `a b` | Multiply two numbers |
| `divide` | `a b` | Divide a by b (exits with code 1 on division by zero) |
| `power` | `base exponent` | Raise base to the power of exponent |
| `sqrt` | `number` | Compute the square root (exits with code 1 for negative input) |
| `mod` | `a b` | Compute a modulo b (exits with code 1 on division by zero) |
| `abs` | `number` | Compute the absolute value |
| `history` | `[--last N]` | Show last N calculation history entries (default: 10) |

## Examples

```bash
python calc.py add 3 5        # 8.0
python calc.py subtract 10 4  # 6.0
python calc.py multiply 3 4   # 12.0
python calc.py divide 10 2    # 5.0
python calc.py power 2 10     # 1024.0
python calc.py sqrt 16        # 4.0
python calc.py mod 10 3       # 1.0
python calc.py abs -7         # 7.0
python calc.py history --last 5
```

## History

Calculations are persisted to `~/.calc_history` in `expr=result` format.
