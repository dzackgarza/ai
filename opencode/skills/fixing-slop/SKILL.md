---
name: fixing-slop
description: Use when fixing slop identified by anti-slop or reviewing-llm-code — converting fraudulent artifacts back into correct implementations without laundering. Also use when an agent proposes "renaming to be honest," "deleting the dead code," or any label-only remediation of a slop finding.
---

# Fixing Slop

Before attempting to remediate or fix code quality/slop findings, consult the central policy index:
[policy-index](file:///home/dzack/ai/opencode/skills/policy-index/SKILL.md)


## Core Rule

**Deleting or renaming slop is laundering.** Both destroy forensic evidence of the original intention. The slop artifact records what an agent was *trying to do* — obliterating it without understanding that intention means the unmet need that produced the slop still exists, and the next agent will produce the same slop all over again.

You cannot fix slop by removing it. You fix slop by reconstructing the narrative that produced it, identifying the correct intention, and fulfilling that intention with the right implementation.

Remediation must strictly respect the **Bridge-Burning Policies** (defined in [policy-index/SKILL.md](file:///home/dzack/ai/opencode/skills/policy-index/SKILL.md#policy-registry)). Any fix that introduces fallbacks, defaults, mocks, optional critical dependencies, or boolean flags to "remediate" a finding is violating policy and is considered laundering.

## Slop Is Never Localized: The Blast Radius Rule

A slop finding is a mold spot on bread. You cannot cut out the moldy spot and call the bread fixed. You cannot replace the moldy spot with fresh bread. The mold has spread invisibly; you must determine the full extent of the infection, excise it entirely, then go back to bread-making principles to produce moldless bread from the ground up.

Slop findings are **symptoms**, not the disease. Every visible slop artifact was produced by a systemic failure. The slop you can see is the failure mode that was *allowed to survive*. The surrounding code was shaped by the same failure-producing process — it may have been gutted, discarded, bypassed, or replaced with weaker substitutes that didn't get caught because they weren't as obviously fraudulent.

The mental model: an agent was given a large, hard task. The agent found the task too difficult, so it:
1. Discarded or bypassed existing correct work rather than migrating it
2. Greenfielded a few new artifacts to appear responsive
3. Gave up when the full scope became apparent
4. Produced slop to close the gap between what exists and what was requested

The slop artifact you found is step 4. The systemic damage is steps 1-3. Fixing step 4 without addressing the prior steps is myopic: you're replacing the visible slop with a correct implementation while the discarded work, bypassed invariants, and gutted test coverage remain lost.

**Before any fix, determine the blast radius:**

- What existed before the slop was produced? What was discarded, deleted, or bypassed?
- What invariants did the old code prove that the new code does not?
- What was the original scope of the task vs. what was actually delivered?
- Where else in the codebase did the same failure process leave artifacts?

The correct fix is almost always larger than the visible finding. If a test suite of 70 tests was gutted and replaced with one mocked test, the fix is not replacing the mock with one real test — it is migrating all 70 tests semantically to the new framework, proving the same invariants they already proved.

## The Fixing Process

### Step 1: Reconstruct the narrative

Before touching any code, answer: what was the agent trying to do? Not "what does this code do" — what user request, goal, or directive produced this artifact? What was the **original scope** of the task the agent was given?

Signals to reconstruct:

- Commit messages and branch names at the artifact's creation
- Surrounding context in the same commit or PR
- Doc comments that describe intent before implementation
- The artifact's position: what boundary does it sit on? what does it connect?
- The git history: was this added as a leaf (new file) or a patch (edit to existing)?
- **Crucially: what was removed?** Run `git log --diff-filter=D --name-only` and `git log --stat` around the relevant timeframe. What files, tests, or subsystems were deleted, gutted, or replaced? What did the old code prove that the new code does not?

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

### Step 3: Fulfill the correct intention — at full scope

Only after identifying the intention AND the blast radius, implement it correctly:

- Use the correct dependency
- Cross the real boundary
- Preserve every invariant the discarded code proved
- **Migrate semantically, do not greenfield.** The correct fix preserves what the old code proved, adapted to the new framework. Do not write new tests that prove new things while the old invariants remain unverified.
- The scope of the fix must match the scope of the damage. If 70 tests were discarded, the fix migrates 70 tests — not one with a note about "future coverage."
- Make the test prove the behavior, not the artifact's existence

The resulting implementation may look nothing like the slop artifact. That is correct — the slop was an evasion of the real work. The fix IS the real work, at the real scope, not a microlocal replacement of the most visibly fraudulent artifact.

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
| **Myopic spot-fix** | Replaces the visible slop artifact with a correct implementation while ignoring the wider systemic damage that produced it. The slop was the tip of an iceberg — fixing the tip does not restore the submerged mass that was discarded, gutted, or bypassed. | Replacing one mocked test with one real test while 69 other discarded tests remain unmigrated; fixing one `unwrap_or_default()` while five other fallback sites in the same file are untouched; removing one manual HTML scanner while the same bespoke-parsing pattern exists in three other modules. |

## Detection: Is This Fix Laundering?

Before accepting any "fix" to a slop finding, apply these checks:

- Does the artifact still exist in any form? If it was deleted — was the correct intention identified and fulfilled?
- Does the fix change runtime behavior? If the diff is only labels, comments, or deletions — it's laundering.
- Does the finding's original critique still apply? If you could paste the same finding text onto the "fixed" code and it would still be true — the fix was cosmetic.
- Was the correct intention fulfilled? If you can't point to the boundary-crossing test, the real dependency, or the architectural migration — the fix was avoidance.
- **Does the fix address the full blast radius?** If the fix touches one artifact while the same failure pattern exists in adjacent code, discarded code remains unmigrated, or systemic invariants remain unproven — the fix is myopic. A single slop finding is a symptom; check that the disease was treated.

## Low-Information Tests Are Laundering

A slop fix that adds low-information assertions is not a fix.

Invalid:
- deleting a mock and adding a test that no mock file exists;
- renaming fake E2E to smoke and asserting it only runs in smoke;
- replacing a fallback with a helper and asserting helper branches;
- adding `assert result is not None` to show the path works;
- asserting an exact error string copied from the review comment.

Valid:
- prove the original burden through the real boundary;
- move code-shape enforcement to global QC;
- record unresolved proof debt.

Consult the central [Banned Test Shapes Catalog](file:///home/dzack/ai/opencode/skills/policy-index/references/test-proof-rules.md) for the inventory of banned and preferred assertion patterns.

## The Golden Rule

**The slop artifact is forensic evidence of an unmet need.** If you destroy the evidence without fulfilling the need, you have made the system worse: the need is now invisible, and the next artifact produced to address it will be slop again, but without the context to understand why.

Every slop fix must produce a git history that clearly shows:

1. The slop artifact as it existed (committed red)
2. The correct intention as identified from the narrative (documented)
3. The correct implementation that fulfills that intention (committed green)

If the fix does not produce this trail, it is laundering — and the original slop pattern will recur.

## Review-Driven Slop Fixes

When slop is found through PR review, do not fix the review comment.
Fix the original obligation that the slop artifact was trying to avoid.

A review-driven slop fix must be written as a first-principles spec and implemented by
an independent subagent or fresh context. The spec must not expose the reviewer’s exact
suggested fix.

## Contaminated Artifacts Cannot Be Repaired In Place

Some slop is not a localized defect inside an otherwise sound artifact — the artifact's
**entire frame** is contaminated. This is common in agent-generated prose artifacts:
READMEs, architecture docs, roadmaps, schemas, and prompts that have accreted private
ontology, correction history, invented institutions, or governance machinery
disproportionate to the work. See
[llm-failure-modes/documentation-failures.md](file:///home/dzack/ai/opencode/skills/llm-failure-modes/documentation-failures.md)
and the `L10`/`C9`/`T8` codes in
[llm-failure-modes/references/agent-distortion-index.md](file:///home/dzack/ai/opencode/skills/llm-failure-modes/references/agent-distortion-index.md).

**An agent holding the contaminated artifact and its correction history in context cannot
cleanly repair it.** It reads the existing material as gospel (treats generated residue as
a requirement), and every correction it receives gets written *into* the artifact rather
than fixing the process that produced it. In-place editing reseeds the same slop in
cleaner prose. Agents do reliable greenfield work and unreliable brownfield work, so the
only safe repair is to **force the brownfield job to look like a greenfield job**:

1. **Encode the standard.** The skill that owns the artifact type must already state what
   a correct and an incorrect such artifact looks like (`writing-documentation`,
   the `plan` skill, etc.). This is the priming, not the
   contaminated artifact.
2. **Adversarial requirement extraction (fresh agent).** A fresh agent, primed on the
   owning skill and *not* carrying the correction history, audits the contaminated
   artifact and extracts only the real, externally-verifiable, user-facing requirements
   and surviving facts. It must verify each surviving claim against inspected reality
   (code, data, command output, external sources), not against other generated documents.
   Anything that cannot be grounded is dropped, not relabeled.
3. **Greenfield rebuild (separate fresh agent).** A second fresh agent, primed the same
   way and given only the extracted requirements — never the original artifact or the
   reviewer's framing — produces the replacement from scratch.
4. **Independent review pass.** Review the rebuild against the owning skill and the
   extracted requirements.

Do not skip to step 3 by handing an agent the old artifact and asking it to "rewrite this
properly." That is brownfield work wearing a greenfield label, and it reinfects.

This protocol is the correct disposition for the **mold-on-bread** case in the Blast
Radius Rule: when the visible artifact is a sample of a contaminated production process,
you throw out the loaf and rebake from sound ingredients — you do not scrape the mold off.
The delegation mechanics (two fresh subagents, no shared contaminated context) live in
[subagent-delegation](file:///home/dzack/ai/opencode/skills/subagent-delegation/SKILL.md).

## Cross-References

- **`anti-slop/references/code-patterns.md`** → **Honest-Label Laundering** — The specific detection heuristics for renaming/relabeling.
- **`anti-slop/SKILL.md`** — The analysis skill; use this FIRST to identify slop, then use fixing-slop to remediate.
- **policy-index → Bridge-Burning Policies** — The [Bridge-Burning Policies](file:///home/dzack/ai/opencode/skills/policy-index/SKILL.md#policy-registry) are the core criteria for what constitutes a correct, non-evasive implementation. Any fix must follow them as hard constraints. For a detailed list of prohibited code constructs and testing red flags, see the [Bridge-Burning Red Flags Catalog](file:///home/dzack/ai/opencode/skills/policy-index/references/red-flags.md) and the [Runtime Control-Flow Red Flags Catalog](file:///home/dzack/ai/opencode/skills/policy-index/references/runtime-control-flow.md).
- **`handling-corrections/SKILL.md`** — The anti-thrashing protocol; use when a fix attempt is rejected as laundering.
