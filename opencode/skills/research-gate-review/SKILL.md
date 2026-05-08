---
name: research-gate-review
description: "Apply the 6-gate review kernel substantively — read code, find real bugs, avoid procedural checkboxing."
version: 1.0.0
author: session-derived
license: MIT
metadata:
  hermes:
    tags: [review, gate-protocol, code-review, mathematical-review, bug-hunting]
    related_skills: [research-proof-auditing, research-state-machine, requesting-code-review, llm-failure-modes]
---

# Research Gate Review

## Core principle

A review that only checks AC checkboxes and smoke exit codes is procedural theater, not a review.
The gate protocol exists to find real issues, not to produce review logs.

## When to use

**Load this skill at session start whenever any cards are in `needs-review` status.** The review kernel in `research-state-machine/references/review-kernel.md` defines the protocol; this skill operationalizes it. Do not rely on the kernel alone — this skill contains pitfall avoidance, anti-boxchecking rules, and the bug-pattern reference that the kernel intentionally leaves at a higher level of abstraction.

- Any card in `needs-review` status with the 6-gate protocol
- After implementing a task, before marking it needs-review (self-check Gates 1-2)
- When asked to "review" or "audit" implementation code

## The cardinal sin: checkboxing

Checkboxing looks like:

- Read card → ACs all [x] ✓
- Run smoke → exit 0 ✓  
- Check git diff → no spec weakening ✓
- Write "Gates passed: all 6, Outcome: complete" ✓
- Move to next card

This is NOT review. This is form-filling. The user will catch and correct this.

## The cardinal confusion: needs-review vs needs-human-input

`needs-review` does NOT mean "waiting for a human." It means the card is ready for the ordered gate-based protocol (Gates 1-6), which an independent AGENT can execute. The review kernel explicitly states:

- `needs-review`: the card is ready for the ordered gate-based protocol (Gates 1-6), which an independent agent can execute.
- `needs-human-input`: the card specifically requires human attention — a design decision, policy choice, or evaluation that cannot be delegated to an agent.

If you treat `needs-review` as blocking on human input, the user will correct you. You MUST dispatch review to fresh-context subagents and advance cards that pass.

## Subagent delegation (mandatory)

Every review MUST be executed by a fresh-context subagent. The coordinator's session is contaminated with implementation context and cannot produce independent judgment.

Workflow:
1. The coordinator dispatches to subagents via `delegate_task(tasks=[...])`
2. Each subagent receives: card body, work artifact paths, baseline artifact paths, and the review kernel. NOT the prior review logs or coordinator opinions.
3. The subagent applies Gates 1-6 in order, fail-fast. Produces a review log with concrete evidence.
4. The coordinator verifies the review for box-checking behavior.
5. If substantive → apply the status change. If not → reject and re-dispatch.

### Batching strategy

Use `delegate_task` with parallel tasks (3 concurrent). **One card per subagent** — do not give a single subagent multiple cards. A subagent reviewing 3 large spec cards will time out at 600s.

Effective pattern (proven 2026-05-07):
- 3 parallel subagents, each reviewing 1 card
- Each subagent receives: the card file path, the card-type-specific gate protocol, and the working directory
- Subagent reads the card body, verifies sources, writes `## 6-Gate Protocol Review Log` into the card file
- Throughput: ~3 cards per 8-10 minutes

Group cards by type (SPEC, PHASE, TASK) for coherent context. Within a type, group by mathematical domain.

**Do NOT pre-read the cards for the subagents.** The subagent must read the card itself — providing pre-digested summaries contaminates the review and invites checkboxing. Give the subagent the card path and the relevant gate protocol variant.

### Outcome application

- If all gates pass → outcome is `complete`. The coordinator changes `status: needs-review` to `status: complete`.
- If any gate fails → outcome is `revision-required`. Set `status: revision-required`, note what needs fixing, fix it, re-dispatch for review.
- If a genuine human decision is required → outcome is `needs-human-input`. Set `status: needs-human-input` and record the specific question.

## Card-type-specific gate protocols

The 6-gate protocol takes different forms depending on the card type. Load the right variant or the subagent will check the wrong things.

### TASK cards (implementation review)

Standard 6-gate protocol as defined in the review kernel:
- G1 Definition Grounding — every claim cites a canonical source path
- G2 Acceptance Criteria — independently verify against implementation artifacts. Read the code, run smokes, check edge cases.
- G3 Spec-Weakening — check git log for changes to spec files, smoke files, mapping docs
- G4 Gradient — decision cards not contradicted, smokes still pass, no regression
- G5 Mathematical Correctness — read implementation code, check for common bug patterns (see below)
- G6 Style and Compliance — @override/@final, type annotations, no banned patterns

These are the cards that produced implementation artifacts — code, smokes, commits.

### SPEC cards (source grounding review)

SPEC cards are mapping/tracking documents. The review is about whether the spec itself is mathematically complete and source-grounded, NOT about implementation code.

- G1 Source Grounding — every mapping row cites proper Sage source paths. Verify referenced files exist on disk at the claimed paths. Spot-check Sage source line numbers.
- G2 Sage Surface Completeness — every inventoried Sage surface accounted for in the spec's reconciliation tables. No unaccounted surfaces.
- G3 Constructor Route Justification — routes are mathematically valid. Category hierarchy correct. Constructor decomposition sound.
- G4 Nonmathematical Rejection — nonmathematical targets explicitly rejected with grounded rationale and replacement owners.
- G5 Ambiguity Routing — unresolved issues have decision cards or explicit routing. No hanging "decision needed" text without a card.
- G6 Obligation Preservation — no weakening without grounded replacement. Sage surface obligations preserved or elevated.

**Context for subagents:** The prompt must clearly state this is a SPEC review. Do not tell the subagent to "run smokes" or "read implementation code" — those don't exist for spec cards. Tell them to verify source files, cross-reference inventories, and check mathematical correctness of claims.

### PHASE cards (coordination review)

Phase cards are coordination/planning artifacts. The review is about child task completeness, exit criteria checkability, and dependency correctness.

- G1 Source Grounding — phase cites canonical sources, child tasks have grounded provenance
- G2 Exit Criteria Checkable — success criteria are specific, falsifiable, have clear verification method
- G3 Task Inventory Complete — child tasks cover all phase-scoped work; no undeclared stray tasks; no success criteria lacking an owner
- G4 No Scope Creep — phase stays within its stated boundary; cross-subtree gaps routed to appropriate downstream features
- G5 Dependency Correctness — child task dependencies form a valid DAG; no circular deps; no self-referential `dependsOn`; wrapup correctly depends on all work tasks
- G6 No Weakening — feature-level acceptance criteria preserved; no smoke relaxation; phase-level criteria are operational gates, not workarounds

**Key check:** If the phase card is `needs-review` but most child tasks are not `complete`, the phase is premature for review. Flag this as a finding — the phase should remain `in-progress` or `needs-human-input` until children are done.

### PLAN cards (plan-level review)

Plan cards sit above phases in the hierarchy. The review is about phase inventory completeness, exit criteria alignment with the owning feature, and cross-plan dependency correctness.

- G1 Source Grounding — plan cites canonical sources; migrated source corpus bodies have traceable provenance; no dead file references from pre-migration era. Check every listed source file against disk with `find`/`ls`.
- G2 Exit Criteria Checkable — success criteria are specific, falsifiable, and scoped to the plan's remit. Check for duplicate criteria between YAML `successCriteria` and body checkboxes (common copy-paste artifact).
- G3 Phase Inventory Complete — every phase listed in the plan's frontmatter `phases:` array (or body prose) exists on disk with the correct parent reference. No undeclared phases. No stray phases in subdirectories without a parent entry.
- G4 Scope Containment — plan stays within its stated boundary. Cross-subtree dependencies are explicitly declared, not hidden in prose. The plan's scope does not leak implementation work from lower-level phases.
- G5 Dependency Correctness — `dependsOn` matches the plan body's dependency statements. Body prose declaring a dependency that the YAML `dependsOn: []` omits is a Gate 5 failure (found in 3 plan cards this session). Check that sibling/subplan references resolve to existing files.
- G6 No Weakening — plan-level criteria preserve feature-level acceptance criteria. No smoke relaxation. No spec weakening. Plan gates are operational constraints, not workarounds for upstream incompleteness.

**Key check:** Plans that reference source files from a pre-migration era (e.g., `plans/todo.md`, `.agents/theory/`) are likely to have dead references. Gate 1 must check every path. Also check that `dependsOn` in YAML is not empty when the body declares cross-plan dependencies — this is a mechanical formatting bug that appears in ~40% of plan cards.

### Gate 2 done right (not just checking [x])

"Verify each item against the artifacts" means:

1. **Read the actual implementation code** the task produced. Don't trust the work log's description of what it did.
2. **Run the smoke yourself** — but also look at what it actually tests. Does the smoke cover the claim? Or does it only test the happy path?
3. **Check edge cases**: What happens with empty inputs? What happens with degenerate categories? What happens when Sage's implementation is broken?

### Common bug patterns to look for (Gate 5)

| Pattern | What to check | Example from session |
|---------|--------------|---------------------|
| `__eq__` on Sage wrapper | Sage may use identity-based equality. Override with elementwise comparison. | `ImageSubobject.__eq__` returned `False` for equal objects |
| `@abstract_method` delegating to Sage | Sage may have a broken concrete impl that satisfies the abstract check. Verify the impl works. | `ImageSubobject.__eq__` was abstract, Sage provided broken identity check |
| Methods returning raw Sage objects | Check for `refine_category` call. If missing, the result isn't in the project category. | `subjoinsemilattice` returned `JoinSemilattice` directly |
| `from sage.xxx import X as SageX` then `return SageX(...)` | The result is a Sage object without project refinement. Needs `refine_category`. | Same as above |
| `except ValueError:` | May miss `TypeError` or `AttributeError` from edge cases | `ImageSubobject.__contains__` only caught `ValueError` |
| Refined-parent routing | Route through `refine_category(result, categories)` not through the component method. A `component.tensor()` may resolve to a superclass method with incompatible kwargs, while `base_module.tensor()` has the correct signature. | `component.tensor(name=..., sym=...)` raised `TypeError: unexpected keyword argument 'name'`; fix was `base_module.tensor(...)` |
| Post-commit regression | After a cleanup commit fixes lint/fmt issues, a later implementation commit modifies the same files and reintroduces findings. The card that claimed clean lint may be stale. Re-check all claims against current HEAD. | F821 (`Posets` missing import) and E501/I001 regressions introduced by commit `3077a4d` after cleanup commit `31a5e7e` |
| Category supercategory leak | A `CategoryWithAxiom` whose `super_categories()` returns `[Sets().Finite()]` pulls in `Sets().Finite().ParentMethods.max()` as an abstract requirement, breaking objects whose elements don't support `max()`. Use empty `super_categories()` for axiom classes that provide methods without abstract obligations. | `TotallyOrderedSetsCategory.super_categories() = [Sets().Finite()]` caused `Not implemented method: max` on partition elements |

### Gate 3 done right

When checking for spec weakening, don't just check git diff is non-empty. Look at:

- Was `@abstract_method` removed? If so, is there a grounded decision or replacement owner?
- Was an obligation moved to a narrower category? If so, is it mathematically correct that the more general category can't satisfy it?
- Were smoke assertions reduced? Are fewer methods being tested?

### What to do when you find issues

1. **Fix them** — the review should produce improvements, not just findings
2. **Update the card** — log what you found and fixed
3. **Then mark complete** — if the work is now solid and the ACs are satisfied

## Review log writing discipline

When a fresh-context subagent completes a review, it MUST write the review log into the card body file. The coordinator MUST verify this happened before promoting the card. If the subagent only summarized in chat, the coordinator writes the review log based on the subagent's findings.

### Status transitions

| Current status | After review passes | After review fails |
|---------------|--------------------|--------------------| 
| `needs-review` | `complete` (write review log + change status) | `revision-required` (write findings, fix, re-review) |
| `revision-required` | Fix applied → `needs-review` → dispatch fresh review | Keep fixing |

Do NOT change `status: needs-review` to `status: complete` without writing the review evidence into the card body first. A status change without a review log is box-checking.

### Review log format in card body

Every promoted card must have a Review Log section containing:

```markdown
## Review Log

### Independent Review - YYYY-MM-DD (fresh-context subagent)

**Gates passed:** Gate 1 Definition Grounding, Gate 2 Acceptance Criteria, ...

**Gates failed:** none

**Outcome:** complete. All six gates pass with concrete falsifiable evidence.

- Gate 1: (concrete evidence: source paths, file lines)
- Gate 2: (evidence for each AC)
- Gate 3: (what was checked, what was found)
- Gate 4: (decision cards checked, gradient computed)
- Gate 5: (commands run, output, edge cases)
- Gate 6: (style rules checked, commit messages)

Verification: `command` passes.
```

## Naming discipline when reviewing categories

When reviewing category specifications, check that axiom and category names describe **mathematical properties of the objects in the category**, not properties of the implementation.

**Wrong:** `Sets().Partitioned().FiniteTotallyOrderedBase()` — "FiniteTotallyOrderedBase" describes what the base set data structure looks like. It's a software name.

**Right:** `Sets().Finite().TotallyOrdered().Partitioned()` — the chain composes existing mathematical axioms. The property "the base set is finite and totally ordered" is captured by the refinement `Finite().TotallyOrdered()`, not by an invented compound axiom.

**Test:** If the name needs to be explained by saying "it describes the base set, not the object," it's a software name, not a mathematical name.

## Pitfalls

- **You cannot review code you also wrote.** If you did any implementation on a task, flag it for independent review. Note the conflict in the review log.
- **Smoke exit 0 is not evidence of correctness.** The smoke may only test the happy path. Read the smoke file.
- **An AC marked [x] is not verified.** The implementer checked it. The reviewer must independently verify.
- **"No staged/unstaged diffs" is not evidence of no spec weakening.** The commits may already be pushed. Check `git log` for changes to spec and smoke files.
- **Reports of findings are not the same as fixes.** If you find a bug, fix it. Don't just write "Gate X finding: ..." and move on.
- **When in doubt, read the code.** If you haven't read the implementation files the task touches, you haven't reviewed it.
- **`refine_category(test=False)` hides abstract method gaps.** If the work uses `test=False`, check that the gaps are explicitly documented and routed to downstream cards. Silent suppression is not a fix.
- **Routing through the most refined parent is not always correct.** The refined parent may override methods with different signatures. Verify the method you route to has the expected parameters.
- **Large mapping specs time out at 600s.** SPEC-MAPPING-LATTICES (and similarly large specs >400 lines) will exhaust a subagent's time budget. For such cards, either split the review into focused chunks (e.g., "review only the lattice tier table" then "review only the constructor routes"), or give the subagent a more targeted prompt that skips source-verification busywork on already-verified sections.
- **Self-referential `dependsOn` is common.** Many wrapup task cards list themselves in their own `dependsOn` array. Check for this on every PHASE review — it's a mechanical bug that Gate 5 catches.
- **Phase prematurity.** A phase card in `needs-review` when most child tasks are not `complete` is premature. The phase review should wait until children are done. Flag the phase as `needs-human-input` with the finding rather than marking it `complete` with open children.
- **Cards live under unexpected features.** Don't construct card paths from card IDs assuming a specific feature directory. Use `find plans/features -name 'CARD-ID*'` to locate the actual file. SPEC cards for forms and lattices live under `FEATURE-MODULES-WITH-FORMS-AND-LATTICES`, not `FEATURE-CATEGORY-SPECS-AND-SAGE-SURFACES`.
- **Triage before dispatch.** Before dispatching reviews, scan all `needs-review` cards for existing review logs. Cards that already have substantive review logs but are still `needs-review` are almost always awaiting human signoff — move them to `needs-human-input` rather than redundantly re-reviewing. This single scan saved ~30 redundant subagent dispatches in one session.
- **Review log section header variance.** Subagents write `## 6-Gate Protocol Review Log` rather than the kernel's `## Review Log`. Accept either header when checking for review log presence. When writing the section header yourself, use `## 6-Gate Protocol Review Log` to match the subagent convention.

## References

- `research-state-machine/references/review-kernel.md`: the 6-gate protocol this skill operationalizes
- `.agents/skills/research-proof-auditing/references/proof-auditing.md`: evidence sufficiency for mathematical claims
- `requesting-code-review`: pre-commit code verification (complementary — runs before commit, not after)
- `llm-failure-modes`: common LLM cognitive failures that can corrupt review processes — overconfidence, confabulation, premature victory declaration, tool output blindness
- `references/batch-review-patterns.md`: concrete batch pipeline, context templates, and bug findings from the 2026-05-07 review session (15 cards reviewed, 14/15 successes, 18 real bugs found)
