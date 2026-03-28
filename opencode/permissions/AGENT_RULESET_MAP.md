# Agent → Ruleset Mapping Reference

Generated: 2026-03-19

## Primary Agents

| Agent Name             | Prompt Slug                               | Ruleset        | Overrides                                           |
| ---------------------- | ----------------------------------------- | -------------- | --------------------------------------------------- |
| Interactive            | `interactive-agents/interactive`          | `Interactive`  | none                                                |
| (Lattice) Orchestrator | `interactive-agents/lattice-orchestrator` | `Orchestrator` | none                                                |
| Minimal                | `interactive-agents/minimal`              | inline mixins  | `mixin_bash_unrestricted()`, `mixin_orchestrator()` |
| orchestrator           | `interactive-agents/orchestrator`         | `Orchestrator` | none                                                |
| Plan (Custom)          | `interactive-agents/plan-custom`          | `Planner`      | none                                                |
| plan                   | `interactive-agents/plan`                 | `Planner`      | none                                                |
| Repository Steward     | `interactive-agents/repository-steward`   | `Planner`      | none                                                |
| Unrestricted Test      | `interactive-agents/unrestricted-test`    | inline mixins  | `mixin_allow_all_permissions()`                     |
| Zotero Librarian       | `interactive-agents/zotero-librarian`     | `Coordinator`  | `edit: deny`, `apply_patch: deny`                   |

## Subagents

### Writer Group

| Agent Name            | Prompt Slug                         | Ruleset      |
| --------------------- | ----------------------------------- | ------------ |
| Writer: Documentation | `sub-agents/project-initializer`    | `DocsWriter` |
| Writer: General Code  | `sub-agents/general-code-writer`    | `CodeWriter` |
| Writer: Python        | `sub-agents/python-code-writer`     | `CodeWriter` |
| Writer: Refactorer    | `sub-agents/refactorer`             | `CodeWriter` |
| Writer: SageMath      | `sub-agents/sagemath-code-writer`   | `CodeWriter` |
| Writer: Tests         | `sub-agents/test-writer`            | `TestWriter` |
| Writer: TypeScript    | `sub-agents/typescript-code-writer` | `CodeWriter` |

### Reviewer Group

| Agent Name                | Prompt Slug                           | Ruleset    |
| ------------------------- | ------------------------------------- | ---------- |
| Reviewer: Code            | `sub-agents/code-reviewer`            | `Reviewer` |
| Reviewer: Plan Contract   | `sub-agents/plan-contract-validator`  | `Reviewer` |
| Reviewer: Plans           | `sub-agents/plan-reviewer`            | `Reviewer` |
| Reviewer: Semantic Audit  | `sub-agents/semantic-auditor`         | `Reviewer` |
| Reviewer: Test Compliance | `sub-agents/test-compliance-reviewer` | `Reviewer` |

### Researcher Group

| Agent Name                | Prompt Slug                           | Ruleset      |
| ------------------------- | ------------------------------------- | ------------ |
| general                   | `sub-agents/general`                  | `Researcher` |
| Researcher: Code Base     | `sub-agents/explore`                  | `Researcher` |
| Researcher: Documentation | `sub-agents/documentation-researcher` | `Researcher` |
| Researcher: Repo Explorer | `sub-agents/explore`                  | `Researcher` |

### Lattice Group

| Agent Name                                  | Prompt Slug                                                   | Ruleset      |
| ------------------------------------------- | ------------------------------------------------------------- | ------------ |
| (Lattice) Researcher: Documentation         | `lattice-sub-agents/lattice-researcher-documentation`         | `Researcher` |
| (Lattice) Reviewer: Checklist Completionist | `lattice-sub-agents/lattice-reviewer-checklist-completionist` | `Reviewer`   |
| (Lattice) Reviewer: Documentation Librarian | `lattice-sub-agents/lattice-reviewer-documentation-librarian` | `Reviewer`   |
| (Lattice) Reviewer: Test Coverage           | `lattice-sub-agents/lattice-reviewer-test-coverage`           | `Reviewer`   |
| (Lattice) Writer: Algorithm Porter          | `lattice-sub-agents/lattice-writer-algorithm-porter`          | `CodeWriter` |
| (Lattice) Writer: Interface Designer        | `lattice-sub-agents/lattice-writer-interface-designer`        | `CodeWriter` |
| (Lattice) Writer: Interface Implementer     | `lattice-sub-agents/lattice-writer-interface-implementer`     | `CodeWriter` |
| (Lattice) Writer: TDD                       | `lattice-sub-agents/lattice-writer-tdd`                       | `TestWriter` |
| (Lattice) Writer: Test Methods              | `lattice-sub-agents/lattice-writer-test-methods`              | `TestWriter` |

## Ruleset Definitions

### Interactive

```python
[mixin_orchestrator(), mixin_session_tools(), mixin_interactive(), mixin_bash_unrestricted()]
```

### Orchestrator

```python
[mixin_orchestrator(), mixin_interactive(), mixin_bash_unrestricted()]
```

### Planner

```python
[mixin_planner()]
```

### Coordinator

```python
[mixin_orchestrator(), mixin_session_tools()]
```

### CodeWriter

```python
[mixin_code_writer()]
```

### DocsWriter

```python
[mixin_docs_writer()]
```

### TestWriter

```python
[mixin_test_writer()]
```

### Researcher

```python
[mixin_researcher()]
```

### Reviewer

```python
[mixin_reviewer()]
```

## Mixin Reference

See `src/mixins.py` for full definitions:

- `mixin_interactive()` — Full read/write access
- `mixin_planner()` — Read all, write plans only
- `mixin_orchestrator()` — Task/todo management
- `mixin_code_writer()` — Read src+plans, write src
- `mixin_test_writer()` — Read tests+plans, write tests
- `mixin_docs_writer()` — Read docs+plans, write docs
- `mixin_reviewer()` — Read all, write nothing
- `mixin_researcher()` — Read all, write nothing
- `mixin_bash_unrestricted()` — Allow all bash
- `mixin_bash_standard()` — Allow safe bash subset
- `mixin_session_tools()` — Introspection tools
