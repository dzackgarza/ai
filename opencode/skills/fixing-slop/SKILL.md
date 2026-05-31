---
name: fixing-slop
description: Use when fixing slop identified by anti-slop or reviewing-llm-code — converting fraudulent artifacts back into correct implementations without laundering. Also use when an agent proposes "renaming to be honest," "deleting the dead code," or any label-only remediation of a slop finding.
---

# Fixing Slop

## Core Rule

**Deleting or renaming slop is laundering.** Both destroy forensic evidence of the original intention. The slop artifact records what an agent was *trying to do* — obliterating it without understanding that intention means the unmet need that produced the slop still exists, and the next agent will produce the same slop all over again.

You cannot fix slop by removing it. You fix slop by reconstructing the narrative that produced it, identifying the correct intention, and fulfilling that intention with the right implementation.

## The Fixing Process

### Step 1: Reconstruct the narrative

Before touching any code, answer: what was the agent trying to do? Not "what does this code do" — what user request, goal, or directive produced this artifact?

Signals to reconstruct:

- Commit messages and branch names at the artifact's creation
- Surrounding context in the same commit or PR
- Doc comments that describe intent before implementation
- The artifact's position: what boundary does it sit on? what does it connect?
- The git history: was this added as a leaf (new file) or a patch (edit to existing)?

### Step 2: Identify the correct intention

Separate the *intention* from the *execution*. The execution is slop; the intention is the unmet need.

| Pattern | Slop execution | Correct intention |
| --- | --- | --- |
| Mocked E2E test labeled `Tauri E2E` | Mock IPC, static assertion, no boundary crossing | Prove the Tauri desktop app boundary works end-to-end |
| Manual HTML scanner in `render.rs` | String scanning for `src="`, asset read failures logged | Renderer output should include embedded/inlined assets |
| `BTreeSet` round-trip comparison | Unordered set comparison discarding command semantics | Prove parser → reconstructor preserves user's exact command |
| App-owned backup subsystem | Hash-file backup alongside docs claiming git-native | Crashes should not cause data loss |
| Config `unwrap_or_default()` | Silent defaulting after TOML parse failure | Malformed user config must be a visible startup error |

The slop execution is the path of least resistance. The agent substituted a weaker, achievable task for the harder, correct one. You must identify what the harder, correct task *was*.

### Step 3: Fulfill the correct intention

Only after identifying the intention, implement it correctly:

- Use the correct dependency
- Cross the real boundary
- Preserve the invariant that was violated
- Make the test prove the behavior, not the artifact's existence

The resulting implementation may look nothing like the slop artifact. That is correct — the slop was an evasion of the real work. The fix IS the real work.

## Banned Remediation Patterns

These are NEVER valid fixes for a slop finding. Reject them on sight.

| Banned pattern | Why it's laundering | What it looks like |
| --- | --- | --- |
| **Honest relabeling** | Renames the artifact so the label matches its fraudulence. Consumes the critique while leaving the defect intact. Destroys the label/behavior mismatch detection signal. | `Tauri E2E` → `browser-smoke`; `validateInput()` → `inputPresent()`; `just test` → `just test-unit` |
| **Deletion without reconstruction** | Removes the artifact without determining what intention it served. The unmet need remains; the next agent will reinvent the slop. | `git rm` the file, mark finding resolved |
| **Documentation laundering** | Adds a comment, doc, or README note that explains the slop instead of fixing it. Converts the finding into a documentation omission. | Adding `# mirrors /var/www/html/` above a hardcoded path; adding a "known limitation" section |
| **Status-field laundering** | Changes a status label, TODO marker, or issue state instead of changing the artifact. | Moving a finding from "bug" to "wontfix"; marking a card "future work" |
| **Scope relabeling** | Reframes the slop as intentionally scoped: "this is a smoke test," "this is minimal," "this is basic." The slop is now presented as deliberate under-engineering. | Calling a no-op test "minimal verification"; calling dead code "placeholder scaffolding" |
| **Commit message laundering** | The commit message describes the relabel or deletion as the resolution. | "reclassify: label mocked tests as browser-smoke"; "docs: document known recovery architecture gap" |

## Detection: Is This Fix Laundering?

Before accepting any "fix" to a slop finding, apply these checks:

- Does the artifact still exist in any form? If it was deleted — was the correct intention identified and fulfilled?
- Does the fix change runtime behavior? If the diff is only labels, comments, or deletions — it's laundering.
- Does the finding's original critique still apply? If you could paste the same finding text onto the "fixed" code and it would still be true — the fix was cosmetic.
- Was the correct intention fulfilled? If you can't point to the boundary-crossing test, the real dependency, or the architectural migration — the fix was avoidance.

## The Golden Rule

**The slop artifact is forensic evidence of an unmet need.** If you destroy the evidence without fulfilling the need, you have made the system worse: the need is now invisible, and the next artifact produced to address it will be slop again, but without the context to understand why.

Every slop fix must produce a git history that clearly shows:

1. The slop artifact as it existed (committed red)
2. The correct intention as identified from the narrative (documented)
3. The correct implementation that fulfills that intention (committed green)

If the fix does not produce this trail, it is laundering — and the original slop pattern will recur.

## Cross-References

- **`anti-slop/references/code-patterns.md`** → **Honest-Label Laundering** — The specific detection heuristics for renaming/relabeling.
- **`anti-slop/SKILL.md`** — The analysis skill; use this FIRST to identify slop, then use fixing-slop to remediate.
- **`handling-corrections/SKILL.md`** — The anti-thrashing protocol; use when a fix attempt is rejected as laundering.
