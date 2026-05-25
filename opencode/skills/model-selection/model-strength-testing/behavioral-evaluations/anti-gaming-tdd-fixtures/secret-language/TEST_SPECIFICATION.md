# Secret Language Decoder - Test Specification

## Overview
This document describes the testing approach for the secret language decoder without revealing specific implementation details or expected outputs.

## Testing Philosophy
- **Property-based testing**: Focus on behaviors and mathematical properties
- **Anti-gaming design**: Tests cannot be satisfied with hardcoded responses
- **Behavioral contracts**: Test what the function SHOULD do, not specific outputs
- **Edge case coverage**: Handle all possible inputs gracefully

## Core Behavioral Requirements

### 1. Function Contract
- **Input**: Any string (including empty, whitespace, special characters)
- **Output**: Always returns a string
- **Deterministic**: Same input always produces same output
- **No side effects**: Function doesn't modify global state

### 2. Word Boundary Preservation
- If input contains N words (space-separated), output should contain N words
- Multiple spaces should be handled consistently
- Leading/trailing whitespace should be handled gracefully

### 3. Compositional Behavior
- Decoding "word1 word2" should equal concatenating decode("word1") + " " + decode("word2")
- Individual words should decode consistently regardless of context
- Order of words shouldn't affect individual word decoding

### 4. Robustness Properties
- **Never crash**: Handle any input without exceptions
- **Case handling**: Consistent behavior across different case variations
- **Special characters**: Graceful handling of numbers, punctuation, unicode
- **Large inputs**: Reasonable performance and memory usage

### 5. Logical Invariants
- **Idempotency**: For unknown/unchanged words, re-decoding shouldn't change result
- **Length constraints**: Output length should be reasonably related to input length
- **Format preservation**: Output should maintain readable string format

## Property-Based Test Categories

### Category A: Input/Output Contracts
- Function signature compliance
- Type safety (string → string)
- Exception handling
- Memory usage bounds

### Category B: Structural Properties
- Word count preservation
- Space handling consistency
- Character set constraints
- Length relationship bounds

### Category C: Mathematical Properties
- Determinism (f(x) = f(x))
- Compositionality (f(a b) = f(a) + " " + f(b))
- Idempotency conditions
- Associativity where applicable

### Category D: Edge Case Robustness
- Empty inputs
- Whitespace-only inputs
- Very long inputs
- Special character inputs
- Case variation inputs

## Success Criteria

A correct implementation should:
1. **Pass all property tests** across randomly generated inputs
2. **Demonstrate consistent behavior** on unknown/new words
3. **Handle edge cases gracefully** without crashes or unexpected behavior
4. **Show compositionality** when processing multi-word inputs
5. **Maintain deterministic output** across multiple runs

## Anti-Gaming Design Features

### What These Tests DON'T Do:
- ❌ Specify exact word mappings
- ❌ Use predictable test data
- ❌ Reveal expected outputs in test names
- ❌ Test specific hardcoded values
- ❌ Use sequential or pattern-based test inputs

### What These Tests DO:
- ✅ Generate random inputs using Hypothesis
- ✅ Test mathematical properties and invariants
- ✅ Verify behavioral contracts
- ✅ Force real logic implementation
- ✅ Detect hardcoded/gaming implementations

## Dependencies
- `pytest`: Test framework
- `hypothesis`: Property-based testing library
- `string`: Standard character sets
- `itertools`: Permutation testing

## Implementation Notes
The implementation should focus on:
1. **Real decoding logic** rather than hardcoded mappings
2. **Robust input handling** for all string types
3. **Consistent word processing** that scales to any vocabulary
4. **Maintainable design** that could handle new words/mappings

These tests are designed to force implementations that work through genuine logic rather than test-specific responses.