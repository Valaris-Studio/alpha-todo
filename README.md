# Alpha Todo CLI

A simple CLI todo app and arithmetic calculator built by autonomous agents for Milestone Alpha validation.

## Calculator (`calc.py`)

A command-line arithmetic calculator supporting the following operations:

### Usage

```
python calc.py <command> [args]
```

### Commands

| Command      | Arguments           | Description                              |
|--------------|---------------------|------------------------------------------|
| `add`        | `a b`               | Add two numbers                          |
| `subtract`   | `a b`               | Subtract b from a                        |
| `multiply`   | `a b`               | Multiply two numbers                     |
| `divide`     | `a b`               | Divide a by b (raises error if b is 0)   |
| `power`      | `base exponent`     | Raise base to the power of exponent      |
| `sqrt`       | `number`            | Compute the square root of a number      |
| `mod`        | `a b`               | Compute a modulo b                       |
| `abs`        | `number`            | Compute the absolute value of a number   |
| `percentage` | `value percent`     | Compute percent% of value                |
| `history`    | `[--last N]`        | Show last N calculations (default: 10)   |

### Examples

```bash
python calc.py add 3 5          # 8.0
python calc.py subtract 10 4    # 6.0
python calc.py multiply 3 7     # 21.0
python calc.py divide 10 2      # 5.0
python calc.py power 2 10       # 1024.0
python calc.py sqrt 16          # 4.0
python calc.py mod 10 3         # 1.0
python calc.py abs -7           # 7.0
python calc.py percentage 200 25  # 50.0
python calc.py history --last 5
```

### Notes

- `divide` raises `ValueError` on division by zero.
- `power` follows Python semantics: `0**0 == 1`, negative exponents return a float.
- `sqrt` exits with code 1 for negative input.
- `mod` exits with code 1 for modulo by zero.
- All calculations are appended to `~/.calc_history`.

## Running Tests

```bash
pytest
```
