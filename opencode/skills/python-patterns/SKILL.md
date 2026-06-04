---
name: python-patterns
description: Use when writing Python code - for projects using pydantic, uv, justfile, and modern Python conventions
---
# Python Development Patterns

Opinionated, modern Python patterns for building robust, efficient, and maintainable
applications. Targets the **latest Python** — no backwards compatibility hedging.

## When to Activate

- Writing new Python code

- Reviewing Python code

- Refactoring existing Python code

- Designing Python packages/modules

## Non-Negotiable Rules

1. **Always `from __future__ import annotations`** as the first import in every file

2. **Always fully typed** — every function signature, every variable where not trivially
   obvious. No `Any` unless interfacing with untyped externals

3. **Always pydantic** — never `dataclasses`, never `NamedTuple` for data containers

4. **Always `X | None`** — never `Optional[X]`, never `Union[X, Y]`, always use `|`
   syntax

5. **Always uv** — never pip, never pip-tools, never poetry.
   Use PEP 723 inline script metadata for standalone scripts with external dependencies.
   Run via `uv run script.py`. Executable scripts get `#!/usr/bin/env -S uv run --script`.
   See `tool-provisioning-and-environment-hygiene` under "Self-Contained Python Scripts
   with uv" for the full hierarchy, forbidden pathways, and review rule.

6. **Always a venv** — managed by uv

7. **Always pyproject.toml** — project-owned metadata and runtime/build dependencies live here. Generic QC config lives in `~/ai/quality-control`.

8. **Always a justfile** — all dev commands go through `just`

9. **Fail fast with asserts** — no speculative try/catch in greenfield code

10. **Target latest Python** — no version guards, no `sys.version_info` checks

11. **No `None` returns on deterministic paths** — if a function cannot return `None`
    given the invariants of the caller’s context, the return type is not `T | None` and
    the body does not `return None`. If the allegedly-impossible case occurs,
    `assert False, f"invariant violated: {detail}"`. Silent `None` returns on paths that
    should be unreachable hide bugs rather than exposing them.

12. **No `Any` in owned code without an explicit user decision** — `Any` opts the type
    checker out entirely.
    The two legitimate exceptions forced by Python’s type system: (a) `__contains__`
    implementations (protocol requires `object`); (b) `*args`/`**kwargs` relay functions
    that forward to an upstream signature you cannot change.
    Every other use of `Any` requires an explicit comment explaining why the type system
    cannot express the constraint.

13. **No variadics in owned function signatures** — no `*args`, no `**kwargs`, no
    positional-only parameters in code you write and own.
    All parameters must be named, typed, and keyword-accessible.
    Variadics make call sites opaque, resist static analysis, and turn every refactoring
    into a grep exercise.
    The only exceptions: (a) `__init_subclass__` / framework hooks where the framework
    mandates it; (b) genuine delegation wrappers like `functools.wraps` relay functions.

14. **No defensive guards for conditions that have not been observed** — do not add
    `try/except SomeError` for an error that has never actually occurred in production
    or testing. Every error handler must be justified by a real, documented incident.
    A hard dependency that must be installed (`notify-send`, `systemctl`, `ags`) must
    not have a `FileNotFoundError` guard — if it is missing, the system is broken and
    the crash is the correct behavior.
    The `doctor` command exists to diagnose setup errors; runtime code does not.

## Core Principles

### 1. Readability Counts

```python
from __future__ import annotations

# Good: Clear and readable
def get_active_users(users: list[User]) -> list[User]:
    """Return only active users from the provided list."""
    return [user for user in users if user.is_active]

# Bad: Clever but confusing
def get_active_users(u):
    return [x for x in u if x.a]
```

### 2. Explicit is Better Than Implicit

```python
from __future__ import annotations

import logging

# Good: Explicit configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Bad: Hidden side effects
import some_module
some_module.setup()  # What does this do?
```

### 3. Fail Fast — No Speculative Exception Handling

Greenfield code should **NOT** use exceptions for flow control.
Instead:

- **Assert semantic invariants** to catch bugs immediately

- **Let errors propagate** — an unhandled crash with a traceback is better than a
  silently swallowed error

- **Only add try/catch AFTER** you have observed a specific error in practice, then
  handle that specific case

```python
from __future__ import annotations

from pathlib import Path

# Good: Fail fast with assertions
def load_config(path: Path) -> Config:
    assert path.exists(), f"Config file missing: {path}"
    assert path.suffix == ".toml", f"Expected .toml, got: {path.suffix}"
    raw = path.read_text()
    assert len(raw) > 0, f"Config file is empty: {path}"
    return Config.model_validate(tomllib.read(raw))

# Bad: Speculative try/catch for errors you haven't seen
def load_config(path: Path) -> Config:
    try:
        with open(path) as f:
            return Config.from_json(f.read())
    except FileNotFoundError as e:
        raise ConfigError(f"Config file not found: {path}") from e
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in config: {path}") from e

# Bad: EAFP-style speculative exception handling
def get_value(dictionary: dict[str, str], key: str) -> str | None:
    try:
        return dictionary[key]
    except KeyError:
        return None

# Good: Direct check, fail fast if invariant violated
def get_value(dictionary: dict[str, str], key: str) -> str:
    assert key in dictionary, f"Missing required key {key!r} in {dictionary.keys()}"
    return dictionary[key]

# Good: When None is a valid return, just use .get()
def get_value_optional(dictionary: dict[str, str], key: str) -> str | None:
    return dictionary.get(key)
```

### When to Use Exceptions

Exception handling is appropriate **only** at system boundaries and for **observed,
specific** errors:

```python
from __future__ import annotations

import httpx

# Good: Handling an external system boundary you KNOW fails
def fetch_data(url: str) -> bytes:
    response = httpx.get(url)
    response.raise_for_status()  # let httpx's own error propagate
    return response.content

# Good: Triaging a SPECIFIC observed error after it happened in practice
def fetch_data_with_retry(url: str, retries: int = 3) -> bytes:
    for attempt in range(retries):
        try:
            response = httpx.get(url, timeout=10)
            response.raise_for_status()
            return response.content
        except httpx.TimeoutException:
            if attempt == retries - 1:
                raise
    raise AssertionError("unreachable")
```

## Type Hints

### Every File Starts With This

```python
from __future__ import annotations
```

No exceptions. This enables modern annotation syntax everywhere.

### Modern Typing Patterns

```python
from __future__ import annotations

from collections.abc import Iterator, Callable, Sequence
from typing import TypeVar

# Always use | for unions, never Optional or Union
def process_user(user_id: str, data: dict[str, str], active: bool = True) -> User | None:
    if not active:
        return None
    return User(user_id=user_id, data=data)

# Type aliases with type statement (Python 3.12+)
type JSON = dict[str, JSON] | list[JSON] | str | int | float | bool | None

# Generic types
T = TypeVar("T")

def first(items: list[T]) -> T | None:
    return items[0] if items else None
```

### Protocol-Based Duck Typing

```python
from __future__ import annotations

from typing import Protocol

class Renderable(Protocol):
    def render(self) -> str: ...

def render_all(items: list[Renderable]) -> str:
    return "\n".join(item.render() for item in items)
```

## Pydantic Models (Never Dataclasses)

### Basic Models

```python
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

class User(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True

user = User(id="123", name="Alice", email="alice@example.com")
```

### Models with Validation

```python
from __future__ import annotations

from pydantic import BaseModel, EmailStr, field_validator

class User(BaseModel):
    email: EmailStr
    age: int

    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int) -> int:
        assert 0 <= v <= 150, f"Invalid age: {v}"
        return v
```

### Immutable Models

```python
from __future__ import annotations

from pydantic import BaseModel

class Point(BaseModel):
    model_config = {"frozen": True}

    x: float
    y: float

    def distance(self, other: Point) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
```

### Serialization

```python
from __future__ import annotations

from pydantic import BaseModel

class Config(BaseModel):
    name: str
    debug: bool = False
    workers: int = 4

# From dict
config = Config.model_validate({"name": "myapp", "debug": True})

# To dict
data = config.model_dump()

# From JSON string
config = Config.model_validate_json('{"name": "myapp"}')

# To JSON string
json_str = config.model_dump_json()
```

## Context Managers

```python
from __future__ import annotations

from contextlib import contextmanager
from collections.abc import Iterator
import time

@contextmanager
def timer(name: str) -> Iterator[None]:
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"{name} took {elapsed:.4f} seconds")

with timer("data processing"):
    process_large_dataset()
```

## Comprehensions and Generators

```python
from __future__ import annotations

from collections.abc import Iterator, Iterable

# List comprehensions for simple transforms
names = [user.name for user in users if user.is_active]

# Generator expressions for lazy evaluation
total = sum(x * x for x in range(1_000_000))

# Generator functions for large data
def read_large_file(path: str) -> Iterator[str]:
    with open(path) as f:
        for line in f:
            yield line.strip()
```

## Decorators

```python
from __future__ import annotations

import functools
import time
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def timer(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function() -> None:
    time.sleep(1)
```

## Concurrency Patterns

```python
from __future__ import annotations

import asyncio
import concurrent.futures

# Threading for I/O-bound tasks
def fetch_all_urls(urls: list[str]) -> dict[str, str]:
    def fetch_url(url: str) -> str:
        import urllib.request
        with urllib.request.urlopen(url) as response:
            return response.read().decode()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        results: dict[str, str] = {}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            results[url] = future.result()  # let it crash if it fails
    return results

# Async/await for concurrent I/O
async def fetch_all(urls: list[str]) -> dict[str, str]:
    import aiohttp
    async def fetch_one(session: aiohttp.ClientSession, url: str) -> str:
        async with session.get(url) as response:
            return await response.text()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return dict(zip(urls, results))
```

## Project Setup

### Standard Project Layout

```
myproject/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── main.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── user.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   └── test_models.py
├── pyproject.toml
├── justfile
├── README.md
└── .gitignore
```

### Import Conventions

```python
from __future__ import annotations

# stdlib
import sys
from pathlib import Path

# third-party
import httpx
from pydantic import BaseModel

# local
from mypackage.models import User
from mypackage.utils import format_name
```

### pyproject.toml — Project Metadata and Dependencies

```toml
[project]
name = "mypackage"
version = "1.0.0"
requires-python = ">=3.13"
dependencies = [
    "pydantic>=2.0",
    "httpx>=0.27",
]

# Generic QC tools (ruff, mypy, pytest, etc.) run from central/global QC — do not install per-repo.
# See the `quality-control` skill.
[dependency-groups]
dev = []

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--tb=short -q"
# Remaining QC config (ruff, mypy, coverage, etc.) belongs in global QC.
```

### justfile — Project Dev Commands (QC Delegated)

```just
# Default: show available commands
default:
    @just --list

# Set up the project from scratch
setup:
    uv venv
    uv sync

# Delegate all QC (fmt, lint, typecheck, test, coverage) to global QC.
test:
    @just -f ~/ai/quality-control/justfile test

test-ci:
    @just -f ~/ai/quality-control/justfile test-ci

# Clean build artifacts
clean:
    rm -rf .mypy_cache .pytest_cache .ruff_cache htmlcov .coverage
    find . -type d -name __pycache__ -exec rm -rf {} + || true

# Add a dependency
add *PKGS:
    uv add {{PKGS}}

# Add a dev dependency
add-dev *PKGS:
    uv add --group dev {{PKGS}}

# Update all dependencies
update:
    uv lock --upgrade
    uv sync
```

### Project Bootstrap

```bash
# Create project
mkdir myproject && cd myproject
uv init --lib
uv add pydantic
# Generic QC tools (ruff, mypy, pytest, etc.) run from central/global QC — see the `quality-control` skill
# Copy justfile from above
# Run: just setup
```

## Assert Patterns — Fail Fast

The assert pattern is the primary error-handling mechanism for greenfield code.
Asserts document semantic invariants and dump relevant debugging data when they fire.

```python
from __future__ import annotations

from pathlib import Path
from pydantic import BaseModel

class UserConfig(BaseModel):
    name: str
    max_retries: int
    output_dir: str

def process_config(config: UserConfig) -> Path:
    assert config.max_retries > 0, f"max_retries must be positive, got: {config.max_retries}"

    output = Path(config.output_dir)
    assert output.is_dir(), f"Output dir does not exist: {output}"

    result_file = output / f"{config.name}.json"
    assert not result_file.exists(), f"Result already exists, refusing to overwrite: {result_file}"

    return result_file

def merge_datasets(a: list[dict[str, str]], b: list[dict[str, str]]) -> list[dict[str, str]]:
    assert len(a) > 0, f"First dataset is empty"
    assert len(b) > 0, f"Second dataset is empty"

    keys_a = set(a[0].keys())
    keys_b = set(b[0].keys())
    assert keys_a == keys_b, f"Schema mismatch: {keys_a} != {keys_b}"

    merged = a + b
    assert len(merged) == len(a) + len(b), f"Merge lost data: {len(merged)} != {len(a)} + {len(b)}"
    return merged
```

### When NOT to Assert

- **User input validation** — use pydantic validators, they produce structured errors

- **System boundaries** (network, filesystem at runtime) — these fail in expected ways,
  use specific try/catch only after observing the failure

- **Library APIs** consumed by others — raise proper exceptions for public interfaces

## Memory and Performance

```python
from __future__ import annotations

from collections.abc import Iterator

# Generator for large data — don't load everything into memory
def read_lines(path: str) -> Iterator[str]:
    with open(path) as f:
        for line in f:
            yield line.strip()

# Use join, not string concatenation in loops
result = "".join(str(item) for item in items)
```

## Quick Reference

| Pattern | Rule |
| --- | --- |
| Imports | `from __future__ import annotations` first, always |
| Data models | Pydantic `BaseModel`, never dataclasses |
| Unions | `X \| None`, never `Optional[X]` |
| Error handling | Assert invariants, fail fast, no speculative try/catch |
| Package manager | `uv` only |
| Environment | `uv venv`, always |
| Project config | In `pyproject.toml`; QC config (lint/typecheck/coverage) belongs in global QC |
| Dev commands | All in `justfile`, run via `just` |
| QC (fmt/lint/typecheck/test/coverage) | Delegated to global QC — use `just test` and see the `quality-control` skill |
| Target Python | Latest (3.13+), no backwards compat |

## Anti-Patterns to Avoid

```python
from __future__ import annotations

# Bad: dataclass (use pydantic BaseModel)
from dataclasses import dataclass
@dataclass
class User:
    name: str

# Bad: Optional from typing
from typing import Optional
def f(x: Optional[str]) -> Optional[int]: ...

# Bad: Union from typing
from typing import Union
def f(x: Union[str, int]) -> None: ...

# Bad: Missing annotations import
# (no `from __future__ import annotations` at top)

# Bad: Untyped code
def process(data):
    return data

# Bad: Speculative try/catch
try:
    result = compute(x)
except Exception:
    result = default

# Use: uv add package
# Use: PEP 723 metadata + uv run script.py (for standalone scripts)
# Use: inline dependencies block (instead of requirements.txt for scripts)

# Bad: Config in setup.cfg, tox.ini, .pylintrc, etc.
# All config belongs in pyproject.toml

# Bad: Running tools directly
# ruff check .        # use: just test (all QC delegated)
# pytest              # use: just test

# Bad: Bare except or broad except
try:
    something()
except:
    pass

# Good: Assert + let it crash
assert condition, f"Debug info: {relevant_data}"

# ── New rules ────────────────────────────────────────────────────────────────

# Bad: silent None return on a deterministic path
def get_reminder(reminder_id: str) -> dict | None:
    row = db.fetch(reminder_id)
    if row is None:
        return None   # wrong: caller already verified the ID exists
    return row

# Good: assert the invariant, crash loudly if violated
def get_reminder(reminder_id: str) -> dict:
    row = db.fetch(reminder_id)
    assert row is not None, f"get_reminder called for unknown id: {reminder_id!r}"
    return row

# Bad: Any in owned code
from typing import Any
def process(data: Any) -> Any: ...   # type checker is now blind here

# Good: name the actual type
def process(data: dict[str, str]) -> list[str]: ...

# Bad: variadics in owned code
def send(*args: str, **kwargs: object) -> None: ...     # opaque, unrefactorable
def configure(**options: object) -> None: ...           # same problem

# Good: explicit named parameters
def send(command: str, target: str, timeout: int = 5) -> None: ...
def configure(debug: bool = False, workers: int = 4) -> None: ...

# Bad: defensive guard for a hard dependency that must be installed
import subprocess
try:
    subprocess.run(["notify-send", msg], check=True)
except FileNotFoundError:
    return False   # wrong: if notify-send is missing, the system is broken

# Good: crash. The setup problem is real; hiding it is not.
subprocess.run(["notify-send", msg], check=True)   # CalledProcessError propagates correctly

# Bad: guard for an error that has never been observed
try:
    result = parse_date(user_input)
except OverflowError:
    return None   # wrong: has this ever actually happened? add it if/when it does.

# Good: let it crash until you have a real incident to handle
result = parse_date(user_input)
```

## Bridge-Burning Policies

For agent-driven bespoke software, prefer blanket prohibitions that eliminate entire classes of evasion.

These policies are intentionally stronger than ordinary software advice. Their purpose is not universal elegance. Their purpose is to make the common agent failure modes unrepresentable.

### 1. No defaults in runtime logic

Runtime code should not contain defaults for required application behavior. Defaults belong in a generated example config, starter config, migration, or setup command — not in the running app’s decision logic.

- **Bad:**
```rust
timeout_ms.unwrap_or(750)
render_command.unwrap_or(DEFAULT_RENDER_COMMAND)
config.foo.unwrap_or_else(default_foo)
```
- **Better:**
```text
The app ships with a complete config.
Startup validates the config.
Missing values are fatal.
```
- **What this burns:**
  - `require_or_default` helpers
  - absent-vs-present boolean branch tests
  - silent config drift
  - “use defaults when malformed” review suggestions
  - partial config support
  - stringly fallback diagnostics
  - helper-level proof laundering

This also collapses the proof burden. You no longer need to prove that the app chooses the correct default in twenty places. You prove that a complete config is loaded, and incomplete config fails.

### 2. No fallbacks, period

A fallback is usually the app making a decision the user did not make.

- **Bad:**
```text
try rofi, else dmenu, else builtin picker
try configured command, else default command
try real API, else cached fake
try local file, else generated placeholder
try Tauri IPC, else browser mock
```
- **Better (Explicit Selection):**
```text
The config names the command/provider/mode.
If it is wrong, fail.
The user fixes the config or the app is changed.
```
- **What this burns:**
  - fallback chains
  - graceful degradation
  - “works on my machine” discovery logic
  - optional critical dependencies
  - test-only fallback branches
  - enterprise compatibility hedges
  - fake success after dependency failure

A fallback path is not “resilience”; it is an unreviewed alternate design.

### 3. No optional critical dependencies

If the app requires `pandoc`, `rofi`, `systemctl`, `zotero`, `ags`, a Tauri plugin, or a configured CLI, it is not optional.

- **Bad:**
```python
try:
    import x
except ImportError:
    ...
```
- **Bad:**
```rust
if which("pandoc").is_ok() { ... } else { ... }
```
- **Better:**
```text
Doctor/setup verifies dependencies.
Runtime assumes them.
Missing dependency is a setup failure and should crash loudly.
```
- **What this burns:**
  - try-import stubs
  - dependency fallback paths
  - skipif dependency missing
  - “works without X” branches
  - mocked stand-ins
  - fallback providers

### 4. No partial success

Owned commands should either complete the claimed operation or return a hard error.

- **Bad:**
```text
return { ok: true, warnings: [...] }
return partial entries after read_dir error
render with missing diagrams but show warning
save file but fail to remove backup silently
```
- **Better:**
```text
If an owned substep fails, the operation fails.
```
- **What this burns:**
  - warning laundering
  - partial object success
  - empty-array-on-error
  - best-effort modes
  - hidden data loss
  - soft failure states

### 5. No proof-free smoke tests

No tests that are not proof-bearing. If a diagnostic harness is genuinely useful, it should live outside the test/QC proof path as a command, not as a test-shaped artifact.

- **Bad:**
```text
browser-smoke test with mocked IPC
harness test that only proves mount
test renamed to “smoke” after review
```
- **Better:**
```text
diagnostic command: just diagnose-frontend-shell
or real test: exercises real Tauri IPC boundary
```
- **What this burns:**
  - honest-label laundering
  - mocked E2E tests
  - “non-proof test” explanations
  - future agents citing smoke as evidence
  - test suite pollution

If it is in the test suite, it proves repository-owned behavior. Otherwise it is not a test.

### 6. No mocks, fakes, stubs, or simulated environments

Do not allow:
- mocks
- fake APIs
- test doubles
- stub services
- simulated filesystems
- mocked Tauri IPC
- mocked network responses as proof

Use:
- real boundary
- captured real response
- local real service
- fixture file with real structure
- explicit diagnostic outside proof path

And add:
*Deleting a mock test is not enough. The proof burden must be replaced, invalidated, or recorded as unresolved.*

### 7. No deletion without burden disposition

When slop is found, agents will either launder it or delete it. Deletion can be laundering if the original problem disappears with the artifact.

Required before deleting a criticized artifact:
- What original problem caused this to exist?
- Is that problem still live?
- Where is it now solved?
- If unsolved, where is it explicitly recorded?
- Could a future agent reintroduce the same artifact?

- **What this burns:**
  - cleanup-as-resolution
  - removing fake tests without replacing proof
  - deleting wrappers while leaving the integration gap
  - closing review threads because evidence disappeared

*Slop remediation is obligation management, not artifact management.*

### 8. No boolean mode flags in owned APIs

Boolean flags are one of the easiest ways to hide policy choices.

- **Bad:**
```rust
require_or_default(value, config_exists, message, default)
save(path, allow_external)
render(markdown, strict)
```
- **Better:**
```rust
load_default_config()
load_user_config(path)
save_workspace_file(...)
save_absolute_file(...)
render_checked(...)
```
Or use an enum with explicit states if there are genuinely multiple modes.

- **What this burns:**
  - branch-forcing tests
  - helper-local proof laundering
  - wrong flag at call site
  - unclear semantics
  - “true means strict?” ambiguity

In tests, a boolean often means the test is not constructing the real state. It is just selecting the branch it wants.

### 9. No helper-level proof for boundary-level obligations

A review comment about startup config, file save, Tauri IPC, subprocess lifecycle, or E2E behavior must be resolved at that boundary.

- **Bad:**
```text
review: config startup defaults are wrong
fix: add tests for require_or_default(...)
```
- **Better:**
```text
test actual config file absent/present/malformed through build_initial_state
test actual save operation through command boundary
test actual subprocess timeout kills the process
```
- **What this burns:**
  - new helper extracted after review
  - unit tests that mirror the patch
  - proof of branch behavior instead of product behavior
  - tests that would pass if the app stopped calling the helper

*Helper tests are supplementary. They cannot resolve boundary feedback.*

### 10. No exact string assertions unless the string is a public contract

Exact string assertions are often tautological, especially when the test passes the string into the function.

- **Bad:**
```rust
let error = helper(None, true, "missing foo", default).unwrap_err();
assert_eq!(error, "missing foo");
```
- **Better:**
```rust
assert!(matches!(error, ConfigError::MissingRequired { key } if key == "pandoc.render_command"));
```
Or, better still, test the actual boundary and assert that it fails with a structured error.

- **What this burns:**
  - message plumbing tests
  - brittle implementation coupling
  - tests that prove the test’s own literal

### 11. No stringly typed errors for owned failures

Owned errors should be structured. Strings can be rendered at the edge. They should not be the internal contract.

- **Bad:**
```rust
Result<T, String>
Err("missing config value".into())
```
- **Better:**
```rust
enum ConfigError {
    MissingRequired { key: &'static str },
    MalformedToml { path: PathBuf, source: toml::de::Error },
}
```
- **What this burns:**
  - exact string tests
  - ambiguous failure classification
  - review-thread debates about wording
  - catch-all error laundering

### 12. No `Option<T>` in initialized core state for required data

Optionality belongs at the boundary, before normalization. After initialization, required state should be total. If initialization cannot supply the field, initialization fails.

- **Bad:**
```rust
struct AppState {
    render_command: Option<String>,
    workspace_root: Option<PathBuf>,
}
```
- **Better:**
```rust
struct AppState {
    render_command: String,
    workspace_root: PathBuf,
}
```
- **What this burns:**
  - repeated unwrap_or
  - defensive guards
  - impossible-condition tests
  - runtime fallback decisions
  - soft initialization

### 13. No ambient discovery chains

Discovery chains are fallbacks in disguise.

- **Bad:**
```text
look in env var
then project config
then home config
then built-in default
then inferred current directory
```
- **Better:**
```text
one configured path
or one explicit startup rule
or one setup-generated config
```
If multiple locations are truly supported, they should be an explicit ordered contract with tests. But for agent-driven bespoke software, the default should be one source.

- **What this burns:**
  - local-artifact laundering
  - mystery config precedence
  - probe-driven behavior
  - “works because it found something else”

### 14. No hidden global state as source of truth

Do not let the app infer behavior from installed tools, current directory, environment variables, shell profiles, caches, or home-directory artifacts unless that is explicitly the product contract.

- **Bad:**
```text
if fd installed use fd else find
if env var exists use it else config
read ~/.something because maybe credentials are there
```
- **Better:**
```text
config declares the command/path/provider
doctor verifies it
runtime uses it
```
- **What this burns:**
  - installed-tool-first behavior
  - local snooping
  - implicit user preference inference
  - environment-dependent tests

### 15. No local QC authority

Do not let repos define their own generic lint/type/test/coverage gates. They delegate to global QC.

- **What this burns:**
  - local recipe proliferation
  - narrow check passing
  - per-repo tool drift
  - agents modifying QC to pass

### 16. No bypass comments

No:
- `# type: ignore`
- `# noqa`
- `# pragma: no cover`
- `eslint-disable`
- `ts-ignore`
- `skip`
- `xfail`

If the tool is wrong, fix the type surface, change the code shape, or escalate.

- **What this burns:**
  - checker appeasement
  - proof masking
  - silent escape hatches

### 17. No compatibility shims or legacy paths in pre-launch bespoke software

No:
- legacy adapter
- deprecated path
- backward-compatible parser
- old config loader
- compat mode

Replace the old path. Delete it after transferring the burden.

- **What this burns:**
  - branch accretion
  - fallback preservation
  - “just in case” code
  - parallel implementations

### 18. No general-purpose defensive validation inside trusted hot paths

Validate once at the owned boundary, then use total types internally.

- **Bad:**
```text
every function checks null, malformed input, missing fields, impossible variants
```
- **Better:**
```text
boundary validates
core assumes
asserts document impossible states
```
- **What this burns:**
  - enterprise edge-case accretion
  - impossible-condition tests
  - hot-path defensive programming
  - logic noise

### 19. No “quarantine” as remediation

Quarantine language is often fluent laundering.

Suspicious words:
- `quarantined`
- `isolated`
- `non-proof`
- `smoke-only`
- `legacy`
- `diagnostic-only`
- `temporary`
- `compatibility`
- `fallback`
- `scaffold`
- `future-owned`
- `out-of-scope`

These terms trigger a burden-disposition check:
- What problem remains?
- Why does this artifact still exist?
- Can future agents cite it as proof?
- Is it in a proof path?

If yes, it is still slop.

### 20. No issue/comment/documentation as completion

Administrative artifacts can preserve truth, but they do not solve implementation/proof obligations.

- **Bad:**
```text
opened issue, therefore resolved
documented limitation, therefore fixed
renamed test, therefore compliant
comment explains fake proof, therefore okay
```
- **Better:**
```text
issue records unresolved burden
PR remains incomplete unless original task was only to document/triage
```
- **What this burns:**
  - completion laundering
  - metadata as progress
  - future-work as resolution

---

## Policy Exception Protocol

A policy exception must not be granted casually. Any exception requires:
1. **Explicit request:** Explicit user request or source-backed product requirement.
2. **Policy identified:** Stating the exact named policy being violated.
3. **Justification:** Explaining why the blanket rule blocks a real required behavior.
4. **Replacement invariant:** Defining a replacement invariant that prevents the old gaming behavior.
5. **Boundary proof:** Providing proof at the owned boundary.
6. **Audit trail:** Visible commit/PR explanation recording the exception details.

For example, an exception allowing a fallback provider is only allowed if the product explicitly owns multi-provider behavior, and tests prove that: provider selection is explicit, failure is visible, no fake data is returned, the user can tell which provider ran, and config declares the provider order.

---

**Remember**: Fail fast.
Type everything. Use pydantic.
Run `just test` (all QC, delegated to global QC) before committing.
No exceptions without evidence of a specific observed failure.
No variadics, no `Any`, no silent `None` on deterministic paths.
