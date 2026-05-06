# Permission Builder Specification

## Overview

The permission builder is a **two-stage compilation pipeline** that transforms agent templates into runtime-ready OpenCode agent configurations with fully inlined permission sets.

**Key Design Principle:** Permission logic remains in Python for programmatic composition. Agent templates declare _which_ rulesets to apply via tags. The builder resolves tags → rulesets → permissions.

---

## Stage 1: ai-prompts Template Compilation

**Location:** `~/opencode-plugins/clis/ai-prompts/`

**Input:** Prompt templates in `prompts/` directory with frontmatter metadata

**Output:** Compiled markdown files in `compiled-agents/` directory

### Template Frontmatter Schema

```yaml
---
description: <string>
mode: primary | subagent
name: <string>
permission_tags:
  - <tag1>
  - <tag2>
  - ...
permission_overrides: # optional
  <tool>: <permission>
---
```

**Fields:**

| Field                  | Type         | Required | Description                                        |
| ---------------------- | ------------ | -------- | -------------------------------------------------- |
| `description`          | string       | yes      | Agent description                                  |
| `mode`                 | string       | yes      | `primary` or `subagent` (affects base permissions) |
| `name`                 | string       | yes      | Display name                                       |
| `permission_tags`      | list[string] | **yes**  | Ordered list of ruleset tags to apply              |
| `permission_overrides` | dict         | no       | Final overrides applied after all rulesets         |

### Example Template

```yaml
---
description: Default collaborative agent
mode: primary
name: Interactive
permission_tags:
  - orchestrator
  - session_tools
  - interactive
  - bash_unrestricted
permission_overrides:
  edit:
    '*.secret': deny
---
```

---

## Stage 2: Permission Builder

**Location:** `~/ai/opencode/permissions/`

**Input:** Compiled markdown files from ai-prompts with `permission_tags` field

**Output:** OpenCode-compliant agent markdown in `~/.config/opencode/agents/`

### Compilation Pipeline

```
compiled-agents/interactive.md
    ↓ (parse frontmatter)
permission_tags: [orchestrator, session_tools, interactive, bash_unrestricted]
    ↓ (resolve each tag → Python ruleset class)
src/rulesets/orchestrator.py → Orchestrator.layers()
src/rulesets/session_tools.py → SessionTools.layers()  # or mixin
src/rulesets/interactive.py → Interactive.layers()
src/rulesets/bash_unrestricted.py → BashUnrestricted.layers()
    ↓ (collect all layers)
layers = [
    GLOBAL_DEFAULTS,
    BASE_TYPE_PERMS[mode],
    *orchestrator_layers,
    *session_tools_layers,
    *interactive_layers,
    *bash_unrestricted_layers,
    *overrides
]
    ↓ (deep_merge left-to-right)
final_permissions: dict
    ↓ (inject into frontmatter)
~/.config/opencode/agents/interactive.md
```

### Layer Precedence (lowest → highest)

1. **`GLOBAL_DEFAULTS`** — Baseline for every known tool (defined in `compiler.py`)
2. **Base-type adjustments** — `pure_agent` vs `subagent` (task/todowrite permissions)
3. **Ruleset layers** — Each tag resolves to one or more layers from Python ruleset classes
4. **Overrides** — Agent-specific final adjustments from `permission_overrides`

**Merge semantics:** `deep_merge` — later layers win for conflicting keys. Nested dicts are merged at key level (paths coexist).

### Tag Resolution

**Tag format:** Snake-case string matching Python module name

**Resolution algorithm:**

```python
tag = "code_writer"
module = import_module(f"src.rulesets.{tag}")
class_name = "CodeWriter"  # snake_case → PascalCase
ruleset_class = getattr(module, class_name)
layers = ruleset_class.layers()  # returns list[dict]
```

**Error handling:**

- Unknown tag → raise `ValueError` with available tags
- Missing class → raise `ValueError` with expected class name
- `.layers()` not callable → raise `ValueError`

---

## Python Ruleset Structure

**Location:** `src/rulesets/<tag>.py`

**Required interface:**

```python
class <PascalCaseTag>:
    @classmethod
    def layers(cls) -> list[dict]:
        """Return list of permission layer dicts."""
        return [mixin_one(), mixin_two(), ...]
```

**Example:**

```python
# src/rulesets/interactive.py
from src.mixins import mixin_orchestrator, mixin_session_tools, mixin_interactive, mixin_bash_unrestricted

class Interactive:
    @classmethod
    def layers(cls) -> list[dict]:
        return [
            mixin_orchestrator(),
            mixin_session_tools(),
            mixin_interactive(),
            mixin_bash_unrestricted(),
        ]
```

### Mixins

**Location:** `src/mixins.py`

Mixin functions return permission dicts for specific tool groups:

```python
def mixin_interactive() -> dict:
    """Full read/write access to all paths."""
    return deep_merge(
        read_only_in(["*"]),
        write_only_in(["*"])
    )

def mixin_planner() -> dict:
    """Read all, write plans only."""
    return deep_merge(
        read_only_in(["*"]),
        write_only_in(["*.serena/plans*"])
    )
```

---

## File Structure

```
~/ai/opencode/permissions/
├── main.py                  # CLI entry point, build orchestration
├── compiler.py              # GLOBAL_DEFAULTS, layer merging, tag resolution
├── mixins.py                # Permission building blocks (read_only_in, etc.)
├── models.py                # Tool lists, constants
├── validate_inventory.py    # Tool validation
├── display.py               # Rich output formatting
├── agent_markdown.py        # Markdown parsing/rendering utilities
└── src/rulesets/
    ├── __init__.py
    ├── interactive.py       # class Interactive with .layers()
    ├── orchestrator.py      # class Orchestrator with .layers()
    ├── planner.py           # class Planner with .layers()
    ├── code_writer.py       # class CodeWriter with .layers()
    ├── test_writer.py       # class TestWriter with .layers()
    ├── docs_writer.py       # class DocsWriter with .layers()
    ├── researcher.py        # class Researcher with .layers()
    ├── reviewer.py          # class Reviewer with .layers()
    └── coordinator.py       # class Coordinator with .layers()
```

---

## CLI Interface

```bash
# Build all agents from compiled ai-prompts output
just build-permissions

# Or directly:
cd ~/ai/opencode/permissions
uv run python main.py build \
    --compiled-agents-dir ~/opencode-plugins/clis/ai-prompts/compiled-agents

# Validate tool inventory
uv run python main.py validate-tools

# Show effective permissions for an agent
uv run python main.py show-effective Interactive --path "src/**/*.py"
```

---

## Justfile Recipe

```justfile
# Build all OpenCode permissions
build-permissions:
    @just -f ~/opencode-plugins/clis/ai-prompts/justfile compile-agents
    @cd ~/ai/opencode/permissions && uv run python main.py build
```

**Execution order:**

1. Compile ai-prompts templates → `compiled-agents/`
2. Run permission builder → `~/.config/opencode/agents/`
3. Rebuild `opencode.json` via `scripts/build_config.py`
4. Validate runtime visibility via `opencode agent list`

---

## Error Handling

### Build-Time Errors

| Error                             | Cause                                         | Resolution                                             |
| --------------------------------- | --------------------------------------------- | ------------------------------------------------------ |
| `Missing 'permission_tags' field` | Template lacks required field                 | Add `permission_tags` to frontmatter                   |
| `Unknown ruleset: <tag>`          | Tag doesn't match any `src/rulesets/<tag>.py` | Create ruleset module or fix tag name                  |
| `Expected class <Name> not found` | Module exists but class naming wrong          | Ensure PascalCase class name matches tag               |
| `Undeclared tool: <tool>`         | Tool in ruleset not in `GLOBAL_DEFAULTS`      | Add tool to `GLOBAL_DEFAULTS` with baseline permission |

### Runtime Validation

After build, validate:

```python
runtime_agents = subprocess.run(["opencode", "agent", "list"], capture_output=True)
missing = expected_agents - runtime_agents
if missing:
    raise RuntimeError(f"Agents not visible at runtime: {missing}")
```

---

## Adding a New Ruleset

1. **Create module:** `src/rulesets/<tag>.py`
2. **Define class:**

   ```python
   from src.mixins import mixin_one, mixin_two

   class <PascalCaseTag>:
       @classmethod
       def layers(cls) -> list[dict]:
           return [mixin_one(), mixin_two()]
   ```

3. **Update templates:** Add tag to `permission_tags` in agent frontmatter
4. **Test:** `just build-permissions` and verify agent has expected permissions

---

## Adding a New Agent

1. **Create template:** `prompts/<category>/<agent-name>.md` in ai-prompts
2. **Add frontmatter:**
   ```yaml
   ---
   description: ...
   mode: primary | subagent
   name: ...
   permission_tags:
     - <existing_tag1>
     - <existing_tag2>
   ---
   ```
3. **Compile:** `just build-permissions`

No Python changes required for new agents — tags compose existing rulesets.

---

## Design Rationale

### Why Tags Instead of Direct Ruleset Names?

- **Composability:** Agents can combine multiple rulesets (e.g., `interactive` + `bash_unrestricted`)
- **Ordering:** Tags are applied in order, enabling fine-grained precedence control
- **Abstraction:** Tags can be semantic (e.g., `full_access`) while mapping to multiple underlying rulesets

### Why Python Rulesets Instead of YAML?

- **Programmatic composition:** Rulesets can use conditionals, loops, and complex logic
- **Mixin reuse:** Python functions can be combined dynamically
- **Type safety:** `.layers()` return type is enforced by Python
- **Testing:** Rulesets can have unit tests

### Why Two-Stage Compilation?

- **Separation of concerns:** ai-prompts owns templates, permissions owns security policy
- **Independent iteration:** Can update rulesets without touching templates
- **Auditability:** Permission changes are tracked separately from prompt changes

---

## Migration Notes

**From old Python agent classes to tags:**

Old:

```python
# agents/primary/interactive.py
class InteractiveAgent(PureAgent):
    def permission_layers(self) -> list[dict]:
        return Interactive.layers()
```

New:

```yaml
# prompts/interactive-agents/interactive.md
---
permission_tags:
  - interactive
---
```

**Deleted:**

- `agents/` directory (all Python agent definitions)
- `src/base.py` (Agent base class)

**Retained:**

- `src/rulesets/*.py` (Python ruleset classes)
- `src/mixins.py` (permission building blocks)
- `compiler.py` (GLOBAL_DEFAULTS, merge logic)
