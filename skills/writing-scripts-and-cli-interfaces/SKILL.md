---
name: writing-scripts-and-cli-interfaces
description: Use when creating shell scripts, Python CLI tools, or command-line interfaces.
---

# Writing Scripts and CLI Interfaces

## Default Stack

**Cyclopts + Pydantic v2 + basedpyright + Ruff + pytest golden tests**

Use Cyclopts for CLI presentation. Use Pydantic as the actual spec. This converges help text, validation, config loading, schemas, docs, and tests on one source of truth.

## Mandatory Requirements

Every CLI must have:

1. **Well-typed interfaces** — all arguments typed, no implicit Any
2. **Detailed help** — docstrings generate help text automatically
3. **Progressive disclosure** — flat CLIs banned after trivial size; use subcommands
4. **Documented defaults** — every default value explained
5. **Centralized config** — knobs/levers in YAML config files, not ad-hoc env vars
6. **Override flags** — CLI flags only for config overrides and one-off changes

## Division of Responsibility

### 1. Cyclopts for CLI Shape

Use Cyclopts for:

- Subcommands and argument parsing
- Help generation from docstrings
- Shell completion
- Parameter grouping for progressive disclosure

Keep business logic out of CLI callbacks. Delegate to typed functions immediately.

### 2. Pydantic for All Input Contracts

Use Pydantic models for:

- Command payloads
- Config files (via `Settings`)
- Environment variables / secrets
- Structured output models
- Cross-field invariant validation

Enable strict mode so the model rejects coercion instead of silently accepting bad data:

```python
from pydantic import BaseModel, ConfigDict

class Config(BaseModel):
    model_config = ConfigDict(strict=True)
```

### 3. `validate_call` on Orchestration Boundaries

Decorate internal functions that Cyclopts calls. This ensures validation even if the CLI layer is bypassed:

```python
from pydantic import validate_call

@validate_call
def process_data(input_path: Path, output_path: Path, threshold: float = 0.5) -> Result:
    ...
```

### 4. JSON Schema as Contract

Generate JSON Schema from Pydantic models for:

- Documentation generation
- Test fixtures
- Config file validation
- LLM prompting contracts
- Structured output validation

### 5. basedpyright Strict Mode

Enable strict mode to turn "typed-looking code" into actually checked code. Configure in `pyproject.toml`:

```toml
[tool.basedpyright]
strict = ["src"]
```

Rejects untyped public functions and unknown types.

### 6. Ruff as Hygiene Gate

Run immediately on generated code:

```bash
ruff check . && ruff format .
```

## Why Not Typer

Typer is suitable for small tools, but avoid it as the default for LLM-generated code. Typer encourages flat scripts where business logic entangles with CLI decorators. This produces:

- Functions only usable via CLI
- Validation buried in framework-specific syntax
- Help text scattered in decorators instead of docstrings
- No clear contract for reuse

Cyclopts keeps CLI and logic separate. Functions remain callable Python with `@validate_call` contracts.

## Project Structure

```
my-cli/
├── pyproject.toml
├── config.yaml              # Centralized knobs and levers
├── src/
│   └── my_cli/
│       ├── __main__.py      # entry point
│       ├── cli.py           # Cyclopts app, subcommands only
│       ├── models.py        # Pydantic models (the spec)
│       ├── logic.py         # Pure functions with @validate_call
│       └── config_loader.py # YAML → Pydantic Settings
└── tests/
    ├── test_cli.py          # --help golden tests
    ├── test_models.py       # validation edge cases
    └── test_logic.py        # business logic
```

## Example

### config.yaml

```yaml
processing:
  threshold: 0.5
  max_records: 10000
output:
  format: json
  compress: true
```

### models.py

```python
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, validate_call

class Config(BaseModel):
    model_config = ConfigDict(strict=True)

    threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    max_records: int = Field(default=10000, gt=0)
    output_format: str = "json"
    compress: bool = True

class ProcessingInput(BaseModel):
    model_config = ConfigDict(strict=True)

    input_path: Path
    output_path: Path = Path("output.json")
    threshold: float | None = None  # None = use config

@validate_call
def process_data(inp: ProcessingInput, config: Config) -> dict:
    """Core logic with guaranteed types."""
    effective_threshold = inp.threshold or config.threshold
    # ... implementation
    return {"records": 42, "threshold": effective_threshold}
```

### cli.py

```python
from pathlib import Path
from cyclopts import App
import yaml
from my_cli.models import Config, ProcessingInput, process_data

app = App()

def load_config() -> Config:
    with open("config.yaml") as f:
        return Config(**yaml.safe_load(f))

@app.command
def process(
    input_path: Path,
    output_path: Path | None = None,
    threshold: float | None = None,
):
    """Process data file with configurable threshold.

    Args:
        input_path: Path to input data
        output_path: Where to write output (default: output.json)
        threshold: Override config threshold (0.0-1.0)
    """
    config = load_config()
    inp = ProcessingInput(
        input_path=input_path,
        output_path=output_path or Path("output.json"),
        threshold=threshold,
    )
    result = process_data(inp, config)
    # ... output handling

# Subcommand for config management
@app.command
def config(
    show: bool = False,
    set_key: str | None = None,
    set_value: str | None = None,
):
    """View or modify configuration.

    Args:
        show: Display current config
        set_key: Key to update (dot notation: processing.threshold)
        set_value: New value for key
    """
    # Implementation
```

### Golden Test Pattern

```python
from cyclopts import App
from my_cli.cli import app

def test_process_help():
    """Golden test: --help output should contain expected sections."""
    # Capture help output
    help_text = app.help_text("process")
    assert "input_path" in help_text
    assert "threshold" in help_text
    assert "0.0-1.0" in help_text  # Default range documented
```

## Single Source of Truth

**The Pydantic model is the canonical spec.** All surfaces derive from it.

Maintain by:

1. **Generate JSON Schema** from models for external contracts
2. **Load config** through Pydantic Settings (not raw dict access)
3. **Validate at boundaries** with `@validate_call`
4. **Generate help** from docstrings (not hand-written)
5. **Test the spec** — model validation tests, not just CLI tests

When requirements change:

- Update the Pydantic model first
- CLI adapts automatically from types
- Config schema updates with the model
- Help text updates from docstrings

All surfaces converge on one source: the Pydantic model.

## Enforcement Rules

Apply these rules to force quality:

1. Every subcommand maps to typed input/output models
2. No business logic in CLI callback bodies — delegate to functions
3. No raw `dict[str, Any]` crossing module boundaries — use models
4. No ad-hoc `if` validation — use Pydantic validators
5. Every command has a one-line summary and longer docstring — help generated from this
6. Flat CLIs banned after trivial size — use subcommands
7. Every command has at least one golden `--help` test and one validation-failure test
8. Run Ruff immediately — reject untyped public functions, unknown types, and lint failures

## Anti-Patterns

- **Everything in one file** — separate CLI, models, logic
- **Click/argparse directly in business functions** — use decorators/validators
- **Manual type checking with isinstance** — use Pydantic strict mode
- **Hand-written help text** — generate from docstrings
- **Ad-hoc config parsing** — use Pydantic Settings
- **Multiple config formats** — YAML only

## Key Principle

**Use the CLI library for presentation. Use Pydantic as the real spec.**
