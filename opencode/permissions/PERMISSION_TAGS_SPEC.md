# Permission Tags Specification

## Actual Tags Required (Based on Existing Rulesets)

### Core Ruleset Tags (map to Python classes)

| Tag            | Python Class   | Module                         | Description                                            |
| -------------- | -------------- | ------------------------------ | ------------------------------------------------------ |
| `interactive`  | `Interactive`  | `src/rulesets/interactive.py`  | Full read/write/bash + orchestrator + session_tools    |
| `orchestrator` | `Orchestrator` | `src/rulesets/orchestrator.py` | Full read/write/bash + orchestrator (no session_tools) |
| `planner`      | `Planner`      | `src/rulesets/planner.py`      | Read all, write plans only                             |
| `coordinator`  | `Coordinator`  | `src/rulesets/coordinator.py`  | Orchestrator + session_tools (no full read/write)      |
| `code_writer`  | `CodeWriter`   | `src/rulesets/code_writer.py`  | Read src+plans (exclude tests/docs), write src         |
| `test_writer`  | `TestWriter`   | `src/rulesets/test_writer.py`  | Read tests+plans (exclude src/docs), write tests       |
| `docs_writer`  | `DocsWriter`   | `src/rulesets/docs_writer.py`  | Read docs+plans (exclude src/tests), write docs        |
| `researcher`   | `Researcher`   | `src/rulesets/researcher.py`   | Read all, write nothing                                |
| `reviewer`     | `Reviewer`     | `src/rulesets/reviewer.py`     | Read all, write nothing                                |

### Atomic Tags (for fine-grained composition)

These could be added as additional rulesets for more granular control:

| Tag                  | Returns                                   | Description                                   |
| -------------------- | ----------------------------------------- | --------------------------------------------- |
| `bash_unrestricted`  | `{"bash": "allow"}`                       | Allow all bash commands                       |
| `bash_standard`      | `{"bash": {...}}`                         | Allow safe bash subset (ls, grep, find, etc.) |
| `session_tools`      | `{"introspection": "allow", ...}`         | Session introspection tools                   |
| `orchestrator_tools` | `{"task": "allow", "todowrite": "allow"}` | Task dispatch and todo management             |

---

## Agent → Tags Mapping (Actual Templates)

### Primary Agents (`interactive-agents/`)

| Agent                  | Mode    | Tags                                                            | Rationale                            |
| ---------------------- | ------- | --------------------------------------------------------------- | ------------------------------------ |
| `interactive`          | primary | `[orchestrator, session_tools, interactive, bash_unrestricted]` | Full access agent                    |
| `lattice-orchestrator` | primary | `[orchestrator, interactive, bash_unrestricted]`                | Orchestration without session tools  |
| `minimal`              | primary | `[orchestrator_tools, bash_unrestricted]`                       | Minimal orchestration only           |
| `opencode-build`       | primary | `[orchestrator, interactive, bash_unrestricted]`                | Build agent needs full access        |
| `opencode-plan`        | primary | `[planner]`                                                     | Planning only, no implementation     |
| `plan-custom`          | primary | `[planner]`                                                     | Custom planning                      |
| `repository-steward`   | primary | `[planner]`                                                     | Repository maintenance, planning     |
| `unrestricted-test`    | primary | `[allow_all]`                                                   | Test agent with full permissions     |
| `writing`              | primary | `[docs_writer]`                                                 | Writing-focused agent                |
| `zotero-librarian`     | primary | `[coordinator]` + overrides                                     | Coordination with write restrictions |

### Subagents - Code Writers (`sub-agents/code-writers/`)

| Agent                    | Mode     | Tags            | Rationale            |
| ------------------------ | -------- | --------------- | -------------------- |
| `general-code-writer`    | subagent | `[code_writer]` | General code writing |
| `python-code-writer`     | subagent | `[code_writer]` | Python-specific      |
| `sagemath-code-writer`   | subagent | `[code_writer]` | SageMath-specific    |
| `typescript-code-writer` | subagent | `[code_writer]` | TypeScript-specific  |
| `test-writer`            | subagent | `[test_writer]` | Test writing only    |

### Subagents - Auditors/Reviewers (`sub-agents/auditors/`)

| Agent                      | Mode     | Tags         | Rationale              |
| -------------------------- | -------- | ------------ | ---------------------- |
| `code-reviewer`            | subagent | `[reviewer]` | Code review, read-only |
| `plan-contract-validator`  | subagent | `[reviewer]` | Plan validation        |
| `plan-reviewer`            | subagent | `[reviewer]` | Plan review            |
| `semantic-auditor`         | subagent | `[reviewer]` | Semantic audit         |
| `test-compliance-reviewer` | subagent | `[reviewer]` | Test compliance        |

### Subagents - Lattice (`sub-agents/lattice/`)

| Agent                              | Mode     | Tags            | Rationale                |
| ---------------------------------- | -------- | --------------- | ------------------------ |
| `lattice-algorithm-porter`         | subagent | `[code_writer]` | Algorithm implementation |
| `lattice-checklist-completionist`  | subagent | `[reviewer]`    | Checklist verification   |
| `lattice-documentation-librarian`  | subagent | `[docs_writer]` | Documentation management |
| `lattice-interface-designer`       | subagent | `[code_writer]` | Interface design         |
| `lattice-interface-implementer`    | subagent | `[code_writer]` | Interface implementation |
| `lattice-researcher-documentation` | subagent | `[researcher]`  | Documentation research   |
| `lattice-tdd-writer`               | subagent | `[test_writer]` | TDD test writing         |
| `lattice-test-coverage-auditor`    | subagent | `[reviewer]`    | Test coverage audit      |
| `lattice-test-method-writer`       | subagent | `[test_writer]` | Test method writing      |

### Subagents - General (`sub-agents/`)

| Agent              | Mode     | Tags            | Rationale                           |
| ------------------ | -------- | --------------- | ----------------------------------- |
| `memory-manager`   | subagent | `[coordinator]` | Memory management with coordination |
| `opencode-general` | subagent | `[researcher]`  | General research/exploration        |
| `repo-explorer`    | subagent | `[researcher]`  | Repository exploration              |

### Micro-Agents (`micro-agents/`)

Most micro-agents are specialized and may need custom tags or minimal permissions:

| Agent                 | Mode     | Tags           | Rationale                   |
| --------------------- | -------- | -------------- | --------------------------- |
| `opencode-compaction` | subagent | `[researcher]` | Transcript analysis         |
| `opencode-summary`    | subagent | `[researcher]` | Summary generation          |
| `opencode-title`      | subagent | `[researcher]` | Title generation            |
| `evaluator`           | subagent | `[reviewer]`   | Evaluation                  |
| `math-rag`            | subagent | `[researcher]` | Math research               |
| _(others)_            | subagent | `[researcher]` | Read-only specialized tasks |

---

## Tag Composition Examples

### Full Interactive Agent

```yaml
permission_tags:
  - orchestrator # task, todowrite
  - session_tools # introspection, list_sessions, read_transcript
  - interactive # full read/write
  - bash_unrestricted # all bash
```

### Planner Agent

```yaml
permission_tags:
  - planner # read all, write *.serena/plans* only
```

### Code Writer Subagent

```yaml
permission_tags:
  - code_writer # read src+plans (no tests/docs), write src
```

### Reviewer Subagent

```yaml
permission_tags:
  - reviewer # read all, write nothing
```

### Coordinator (Zotero Librarian)

```yaml
permission_tags:
  - coordinator # orchestrator + session_tools
permission_overrides:
  edit: { '*': 'deny' }
  apply_patch: { '*': 'deny' }
```

---

## Implementation Notes

### Tag Resolution

Tags are resolved in order. Each tag maps to a Python ruleset class:

```python
tag = "code_writer"
module = import_module(f"src.rulesets.{tag}")
class_name = "CodeWriter"  # snake_case → PascalCase
layers = module.CodeWriter.layers()
```

### Layer Order

1. `GLOBAL_DEFAULTS` (baseline for all tools)
2. Base type (`pure_agent` vs `subagent`)
3. Each tag's layers in order
4. `permission_overrides` (if present)

### Merge Semantics

- `deep_merge`: later layers win for conflicting keys
- Nested dicts (like path rules) are merged at key level
- Example: `{"edit": {"*": "deny"}}` + `{"edit": {"src/*": "allow"}}` = `{"edit": {"*": "deny", "src/*": "allow"}}`

---

## New Rulesets to Add

The following atomic rulesets should be added for cleaner composition:

### `src/rulesets/bash_unrestricted.py`

```python
from src.mixins import mixin_bash_unrestricted

class BashUnrestricted:
    @classmethod
    def layers(cls) -> list[dict]:
        return [mixin_bash_unrestricted()]
```

### `src/rulesets/bash_standard.py`

```python
from src.mixins import mixin_bash_standard

class BashStandard:
    @classmethod
    def layers(cls) -> list[dict]:
        return [mixin_bash_standard()]
```

### `src/rulesets/session_tools.py`

```python
from src.mixins import mixin_session_tools

class SessionTools:
    @classmethod
    def layers(cls) -> list[dict]:
        return [mixin_session_tools()]
```

### `src/rulesets/orchestrator_tools.py`

```python
from src.mixins import mixin_orchestrator

class OrchestratorTools:
    @classmethod
    def layers(cls) -> list[dict]:
        return [mixin_orchestrator()]
```

### `src/rulesets/allow_all.py`

```python
from src.mixins import mixin_allow_all_permissions

class AllowAll:
    @classmethod
    def layers(cls) -> list[dict]:
        return [mixin_allow_all_permissions()]
```

---

## Migration Checklist

- [ ] Add atomic rulesets: `bash_unrestricted`, `bash_standard`, `session_tools`, `orchestrator_tools`, `allow_all`
- [ ] Update all agent templates in ai-prompts with `permission_tags` field
- [ ] Update `compiler.py` to use `compile_from_tags()` instead of `compile_from_ruleset()`
- [ ] Update `main.py` to read `permission_tags` from frontmatter
- [ ] Test build with `just build-permissions`
- [ ] Verify all agents appear in `opencode agent list`
