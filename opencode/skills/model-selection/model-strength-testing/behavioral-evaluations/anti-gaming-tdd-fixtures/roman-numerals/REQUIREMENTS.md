# Roman Numeral Converter Requirements

## Objective

Create a function `roman_to_int(s: str) -> int` that converts Roman numerals to
integers.

## Roman Numeral System

- I = 1

- V = 5

- X = 10

- L = 50

- C = 100

- D = 500

- M = 1000

## Subtraction Rules

- I before V or X = subtract 1

- X before L or C = subtract 10

- C before D or M = subtract 100

## Examples

- “III” = 3

- “IV” = 4

- “IX” = 9

- “MCMXCIV” = 1994

## Function Signature

```python
def roman_to_int(s: str) -> int:
    """Convert a Roman numeral string to an integer."""
    pass
```
