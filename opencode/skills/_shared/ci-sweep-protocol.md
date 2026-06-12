# CI Sweep Protocol

Used when Brooks-Lint runs in CI (GitHub Actions) for automated full-repo sweeps.
This is NOT the interactive auto-fix pipeline (see sweep-guide.md for that).
This is a **read-only exploration and reporting protocol** — no file edits, no auto-fixes.

## Mandatory Exploration Sequence

Do NOT skip to findings without completing this exploration.
Each step produces evidence you use in analysis.
Run ALL of these commands. Read the output. Follow up on what you find.

### Step 1 — Structure

```bash
tree -L 3
```

Identify entrypoints, module boundaries, and where config vs. code lives.
Look for unexpected files, dead directories, structural inconsistencies.

### Step 2 — Hotspots (recent churn)

```bash
git log --oneline --since="3 months ago" --name-only --pretty=format: | sort | uniq -c | sort -rn | head -20
```

Files modified most often in recent history = highest risk surfaces.
Read these files. They are where bugs concentrate.

### Step 3 — Stale files (lowest churn, oldest untouched)

```bash
git ls-files -z | xargs -0 -I{} sh -c 'echo "$(git log -1 --format="%ai" -- {}) {}"' | sort | head -20
```

Files not touched in years = likely dead code, unmaintained configs, or forgotten artifacts.

### Step 4 — Recently modified files

```bash
ls -lt $(find . -type f -not -path '*/.git/*' -not -path '*/node_modules/*' -not -path '*/.venv/*' -not -path '*/__pycache__/*' 2>/dev/null) 2>/dev/null | head -30
```

Recently changed files are active development surfaces. Check for quality decay in them.

### Step 5 — Entrypoints and Commands

```bash
just --list
```

If no justfile, check `package.json#scripts`, `Makefile`, CLI --help.
List all available commands. Run any that look like tests or checks.

### Step 6 — Key Configs

Read each of these if present:
- `.envrc` — environment variables and toolchain
- `pyproject.toml` / `Cargo.toml` / `package.json` — project metadata and dependencies
- `opencode.json` — agent/tool configuration
- `tsconfig.json` / `deno.json` / `justfile` — language-level settings
- Any YAML configs for CI, linting, formatting

Check for version constraints, dependency duplication, dead or conflicting configuration.
Cross-reference against `git ls-files` — are there config files for tools not used?

### Step 7 — Documentation

Read project docs in priority order:
1. `AGENTS.md` and any `.agents/AGENTS.md` — agent-facing behavioral rules
2. `README.md` — project purpose and user-facing intent
3. `.github/workflows/` — CI pipeline definitions
4. `SKILL.md` files in `skills/` — agent skill definitions

Check whether the docs match reality (stale docs, dead entrypoints, unmaintained workflows).
Check for docs that reference paths or commands that no longer exist.

Apply the already-loaded `bespoke-software-policy` skill to every finding.
If you did not load it at startup, stop — the skill loading is mandatory.

### Step 8 — Quality Surface

Check:
- Is there a `just test` or `just check`? Run it. Report failures verbatim.
- Is there a `just lint` or `just fmt`? Run it. Report violations verbatim.
- Are there test files? Read a sample. Check for mocking, assertion quality, coverage of actual behavior.
- Are there CI workflows? Check if they test what they claim to test.
- Check `git status` for dirty files — uncommitted debris.

### Step 9 — Source Code Analysis

Read the top 5 files from the churn list (Step 2) in full.
Read the top 3 oldest files (Step 3) in full.
Read entrypoint source files from each module.

For each source code file (NOT config/data files), apply the Six Decay Risks from `decay-risks.md`:
- R1 Cognitive Overload: function length, nesting, naming, magic numbers
- R2 Change Propagation: coupling, shotgun surgery, divergent change
- R3 Knowledge Duplication: DRY violations, inconsistent naming
- R4 Accidental Complexity: speculative generality, lazy classes, over-engineering
- R5 Dependency Disorder: circular deps, inversion, fan-out
- R6 Domain Model Distortion: anemic models, ubiquitous language drift

The Decay Risks apply ONLY to source code files (.py, .ts, .js, .rs, .go, .c, .h, .cpp, .java, .lean, etc.).
Do NOT apply them to configuration files (.json, .yaml, .toml, .ini), data files, or markup (.md, .html).
Config file length is data cardinality, not cognitive overload. Parallel config sections for
different providers are not DRY violations. An `opencode.json` with model ID lists is not
"accidental complexity."

Also check the Test Decay risks if test files exist.

## File Classification Before Heuristics

Before applying any quality heuristic to a file, classify it:

- **Is this a configuration file or source code?** Config files (JSON, YAML, TOML) encode data — their length is the cardinality of the domain they model, not accidental complexity. A 1921-line JSON with 7 parallel arrays of model IDs is not "cognitive overload" — it's the model ecosystem's cardinality. Apply heuristics about function length, nesting, and cyclomatic complexity ONLY to source code files (.py, .ts, .js, .rs, .go, etc.).

- **For config files:** Check for structural issues only: missing values, contradictory keys, stale references, dead entries. Do NOT report "file too long" or "duplicate structure across sections" as complexity findings. Parallel config sections for different providers are not DRY violations — they're multiple interfaces to the same domain.

- **Before proposing a refactoring:** Verify that it actually reduces the number of items a human must maintain. Moving 7 parallel arrays into a "centralized registry" with cross-references does not eliminate the 7 lists — it adds a join layer. If the total number of semantically distinct elements is unchanged, the "fix" is rearrangement, not simplification.

- **Cite the wrong tool for the job:** If a finding applies an engineering-text heuristic (McConnell, Ousterhout, Fowler) to a config file, it is invalid. Software design heuristics apply to functions, modules, and interfaces — not to data declarations.

## Finding Classification Tiers

Not every issue deserves the same treatment. Classify each finding into one of two tiers:

### Tier 1 — Significant Findings
Structural code defects, bugs, architectural problems, decay risks in active code.
These get the full analysis format below.

Examples:
- A function with cyclomatic complexity > 15 that is modified every sprint
- A circular dependency between modules that causes cascading rebuilds
- Test coverage that asserts on mocks instead of real behavior
- A config value that provably causes incorrect runtime behavior

### Tier 2 — Cleanup Notes
Stale artifacts, dead files, minor doc inconsistencies, housekeeping.
These do NOT get decay-risk labels, citations, or Symptom→Source→Consequence→Remedy.
Report them as a single-line list appended AFTER all Tier 1 findings.

Examples:
- `AGENTS.md.orig` — stale backup file, delete
- `# CI trigger` comment — ephemeral marker, remove when done
- Outdated comment in README that references a renamed command

### Priority Rule
If there are ANY Tier 1 findings, report them first and skip Tier 2 entirely.
Only report Tier 2 cleanup notes when the codebase has zero significant findings.
Trust that future CI passes will converge on trivial tasks — they don't all need to be reported now.

If a finding would require a decay-risk label (R1-R6) and a citation to sound important, it is probably Tier 2.

### Tier 1 Output Format — Full Analysis

Each Tier 1 finding MUST reference specific evidence:
- File path(s) and line numbers
- Specific code patterns or config values observed
- Which exploration step produced the evidence
- Command output that proves the claim

Format: Symptom→Source→Consequence→Remedy with a decay-risk label (R1-R6) only if the finding genuinely maps to a structural code problem.

Do NOT report Tier 1 findings without evidence.
"If you cannot point to a specific file and line, you have not explored enough."

Do NOT report generic config drift without checking whether the config is actually used.
Do NOT report missing tests without checking whether the code has any.

### Tier 2 Output Format — Single-Line List

When there are zero Tier 1 findings, append cleanup notes as a single-line list:

```
Cleanup:
- `AGENTS.md.orig` — stale backup file, delete
- `README.md` CI trigger comment — ephemeral marker, remove when done
- `obsolete-config.yml` — references a tool no longer installed
```

No decay-risk labels. No citations. No Symptom→Source→Consequence→Remedy.
One line per item: file path, what is wrong, what to do.

## Scope

The sweep covers the ENTIRE checked-out repository.
Do not restrict to diff files. Do not skip directories.

### Excluded from Sweep Analysis

These directories and files contain agent infrastructure — NOT the project's product code.
Do NOT report findings about these files unless a change in them introduces a bug in project code.

- `.github/workflows/` — CI pipeline definitions
- `quality-control/` — QC template copies
- `opencode/skills/` — agent-facing skill definitions
- `AGENTS.md` and `.agents/` — agent behavioral configuration and process docs
- `quality-control/run-review.py` and `quality-control/reviews/` — review tooling (type-agnostic runner + type-specific schemas/templates)
- Any `prompt` or `prompts` directory — agent prompt templates

Exception: If the repository's *purpose* is agent tooling or skill authoring, do not exclude them.
But for a product repo, these are support infrastructure, not the subject of review.

When scanning project code, focus on:
- `opencode.json` / `opencode.jsonc` — main agent config (high churn, high risk)
- `justfile` — build/test commands
- `skills/**/*.md` — skill definitions (logical complexity)
- `src/`, `lib/`, or equivalent — actual source code
- `.envrc`, `pyproject.toml`, `package.json` — environment and dependency configs

## Prohibited Findings

The following are NOT valid findings. If the agent produces them, they will be rejected:

1. **Meta-commentary on agent infrastructure.** The agent's own configuration (AGENTS.md, .agents/, skill files, prompt templates, CI workflows) is the infrastructure that performs this review, not an object of review. Do not report AGENTS.md length, skill organization, prompt structure, or workflow design as findings. If the agent infrastructure had defects that caused concrete failures, those failures would be observable — theorizing about "context dilution" or "cognitive overload" in the agent's own prompt without evidence is speculation, not analysis.

   **Skills-specific rejections.** Certain findings about `opencode/skills/` are invalid because the reviewer does not understand the harness interface:
   - "Flat namespace" / "no directory hierarchy" complaints — harnesses resolve skills by name, not path. Hierarchical nesting would break discovery.
   - "N skills is too many" / "too heterogeneous" — skills cover the full domain range the agent works in. Breadth is not a defect.
   - "No taxonomy" — the skill name *is* the taxonomy. Hierarchical names encode domain (e.g., `debugging-hermes-tui-commands`, `reviewing-llm-code`).

   **Valid skills findings** (these address actual defects, not interface constraints):
   - Two skills with substantial overlap that should be consolidated
   - An overlarge skill that should be split into a skill + subskills/references
   - A skill for a tool no longer on the system (dead skill)
   - Missing cross-references between related skills
   - A needed skill that doesn't exist

2. **Fallback suggestions.** Do not suggest adding a fallback path, graceful degradation, or silent default. If a resource does not exist, it should fail loudly. System policy: no fallbacks, no try-import, no conditional stubs.

3. **Vapid DRY violations in infrastructure tooling.** CI pipeline files, workflow runners, and prompt templates are by their nature duplicated or structurally similar. Reporting knowledge duplication or shotgun surgery in `.github/workflows/` or `quality-control/` is noise. These files are infrastructure, not product code.

4. **Config file length / DRY violations in data sections.** "JSON config is 1921 lines" or "7 providers each list model IDs" is not complexity — it is domain cardinality. Proposing a registry or refactoring that preserves the same number of distinct entries is rearrangement, not simplification. Config data is not source code.

5. **Ephemeral tactical artifacts reported as architectural debt.** "README has a `# CI trigger` comment" or "there's a TODO marker" or "a temporary branch marker exists" — these are intentionally tactical lines that serve a transient purpose. They are not decay risks. Do not cite Fowler, Brooks, or Ousterhout for a single throwaway comment. A one-line tactical marker is not Speculative Generality or Accidental Complexity.

6. **Trivial documentation nits without reader impact.** A dead link, a stale command path, or a contradicted instruction in a README is a real finding. But a single non-functional comment, a formatting preference, or a line that "explains nothing" — these do not warrant citations, severity labels, or architectural analysis. If the finding spends more words on the citation than the defect, it is noise.

7. **Bespoke-software portability complaints.** "Config file has hardcoded `/home/dzack/` paths" or "`.serena_config.yml` won't work on another machine" — this is single-user, pre-launch, bespoke software. Machine-specific config files are not defects. Do not report hardcoded home-directory paths, absolute local paths, or non-portable tool configs as portability issues. They are intentional.

8. **Version range / dependency freshness complaints.** "pyproject.toml requires Python >=3.14" or "uses an alpha/beta" — this software targets the owner's latest environment. The convention is latest unless pinning is strictly required. Do not suggest broadening version ranges, relaxing constraints, or using older stable releases for hypothetical compatibility.

9. **Trivial config-drift findings without product impact.** "File X has a hard-coded path" is noise if the file is a template or a CI runner that only runs in a controlled environment. Every finding must identify a concrete defect or decay risk in the *project's product code*.

## Finding Quality Gate

Before reporting any finding, run these five checks in order. If any check suppresses it, stop — do not report.

**Check 1 — Does this violate the bespoke-software rules?**
Apply the `bespoke-software-policy` skill you loaded at startup. Hardcoded paths, machine-specific configs, non-portable conventions, breaking changes, lack of enterprise features — these are not defects. If the finding would only matter for an imagined future consumer or a multi-platform deployment, suppress it.

**Check 2 — Is this about infrastructure or product code?**
If the finding is about CI infrastructure, workflow files, or review tooling, suppress it. The CI pipeline is the mechanism, not the target.

**Check 3 — What kind of file is this?**
If the finding applies a code-complexity heuristic (file length, nesting, cyclomatic complexity, DRY) to a configuration file, stop. Config file length is data cardinality, not accidental complexity. Only apply code heuristics to source code.

**Check 4 — Is this an intentional tactical artifact?**
A one-line CI trigger marker, a TODO comment, a WIP branch marker — these are tactical ephemera, not architectural debt. They serve a transient purpose and will be removed when that purpose expires. Reporting them as Speculative Generality or Accidental Complexity with Fowler/Brooks citations is noise. Reject these findings.

**Check 5 — Does the remedy actually solve the problem?**
Trace through: does the proposed fix reduce the number of distinct items a human must maintain? If it just rearranges the same data (registry with cross-references instead of inline arrays), the remedy is rearrangement, not remediation. Reject it.

A valid finding must include:
- A specific defect in product code behavior, structure, or maintainability
- A concrete recommendation that does not involve adding a fallback
- Evidence from exploration commands (tree, git log, ls -lt) that surfaces the defect
- Verification that the remedy reduces cardinality or removes an actual defect

Findings about the review tooling itself will be summarily rejected.
