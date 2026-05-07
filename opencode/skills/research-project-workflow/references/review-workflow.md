# Condensed Review Protocol (6-Gate Order)

Use when a card is in `needs-review` status. Apply gates in order; stop at first failure.

## Gate 1: Definition Grounding
Every definition, type, predicate, constructor, method-owner claim traces to a source.
- Check: card body records source path, exact definition, owner category, hypotheses, codomain/return object.
- Fail: ungrounded, missing, or ambiguous definition → revision-required.

## Gate 2: Acceptance Criteria
Work satisfies its own criteria and every applicable parent criterion.
- Check: each `[ ]` vs evidence; card discharge claims are backed.
- Fail: unmet criteria, parent criteria violated, unbacked claim → revision-required.

## Gate 3: Spec-Weakening (category-spec cards)
No spec obligation deleted/weakened without a source-grounded replacement owner.
- Check: `git diff --cached`, `git diff`, commit diff. Flag deleted abstract methods, removed constructors, narrowed smokes, moved obligations without replacement owner.
- Fail: any of the above → revision-required.

## Gate 4: Gradient (Backsliding Detection)
Work must not reverse or contradict previously established truths.
- Check: decided decision cards, previously approved specs, previously passing smokes, resolved TODOs, git history.
- Fail: decision reversal, new smoke failures, resurrected TODO, removed approved spec surface → revision-required or blocked.

## Gate 5: Mathematical Correctness
Mathematical content must be correct for the claimed generality.
- Check: spec coherence, tests pass, algorithm correct, evidence matches escalation tier.
- Use `research-proof-auditing` for evidence sufficiency.
- Fail: tests fail, mathematical error, proxy evidence, tier mismatch → revision-required.

## Gate 6: Style and Compliance
Work follows repo style and compliance rules.
- Check: no raw ConditionSet, no variadic option bags, import hygiene, type annotations, no AI-slop, conventional commits.
- Fail: style violations, anti-slop patterns → revision-required.

## Outcomes
- **complete/done**: All gates passed
- **revision-required**: Fixable within card scope; rework → needs-review
- **blocked**: External prerequisite needed; set blocked_reason + create prerequisite card

## Review Log format

```markdown
### Review YYYY-MM-DD (Reviewer)

**Gates passed:** Gate 1 Definition Grounding, Gate 2 Acceptance Criteria, ...
**Gates failed:** Gate 3 Spec-Weakening, ...
**Outcome:** complete/done (or revision-required, or blocked)

#### Evidence

**Gate 1 — Definition Grounding:**
- [source provenance: cite the card's source-provenance section, mapping docs, decision cards]
- [for implementation: cite Sage docs/source, approved decisions, spec files]

**Gate 2 — Acceptance Criteria:**
- [x] [criterion] → [evidence that criterion is met]
- [x] [next criterion] → [evidence]

**Gate 3 — Spec-Weakening:**
- [state of git diff --cached and git diff]
- [any abstract-method removals and their grounding, or note that none exist]
- [no constructor obligations / smoke assertions / spec obligations deleted]

**Gate 4 — Gradient:**
- [no decision cards contradicted]
- [previously passing smokes not regressed: smoke command + exit code]
- [cross-subtree gaps routed, not locally patched]

**Gate 5 — Mathematical Correctness:**
- [for spec cards: well-typed method owners, explicit hypotheses]
- [for implementation: source-backed algorithms, correct mathematical owner placement]

**Gate 6 — Style and Compliance:**
- [no raw ConditionSet, variadic option bags, AI-slop]
- [conventional commits where present]
- [`just plan-validate` passes]

#### Residual Risks
- [what is explicitly not covered and why that is outside scope]
- [tracked follow-up: card IDs or gap table references]

---
```

### Example: All-gates-passed (spec/planning task)

```markdown
### Review 2026-05-07 (Independent Reviewer)

**Gates passed:** Gate 1 Definition Grounding, Gate 2 Acceptance Criteria, Gate 3 Spec-Weakening, Gate 4 Gradient, Gate 5 Mathematical Correctness, Gate 6 Style and Compliance
**Gates failed:** None
**Outcome:** complete/done

#### Evidence

**Gate 1 — Definition Grounding:**
- Source provenance cites SPEC-CATEGORY-LITERAL-METHOD-OWNERSHIP-INVENTORY and 11 SPEC-MAPPING-* files, each source-grounded in SAGE_INVENTORY.md and MAPPING.md.
- No new definitions introduced; task reconciles existing specs against Sage source.

**Gate 2 — Acceptance Criteria:**
- [x] Every mapping spec records which Sage docs/source files were checked → reconciliation commits updated coverage ledgers.
- [x] Missing Sage surfaces added or routed → gaps tracked as follow-up.
- [x] Inherited Sage category methods checked, not only concrete implementation classes.

**Gate 3 — Spec-Weakening:**
- No staged or unstaged diffs; reconciliation adds coverage entries, does not remove obligations.

**Gate 4 — Gradient:**
- Reconciliation commits only add coverage-verification entries; no mapping decisions reversed.
- No decision cards contradicted.

**Gate 5 — Mathematical Correctness:**
- Completeness-research task, not mathematical claim verification. Coverage ledgers verify that mapping rows correspond to actual Sage methods.

**Gate 6 — Style and Compliance:**
- Conventional commit messages. No code changes.
- `just plan-validate` passes (225 cards).

#### Residual Risks
- Coverage completeness depends on Sage version; version skew acknowledged but not resolved.
```

### Example: Gate-2 failure (spec/implementation task, scope shift)

```markdown
### Review 2026-05-07 (Independent Reviewer)

**Gates passed:** Gate 1 Definition Grounding
**Gates failed:** Gate 2 Acceptance Criteria
**Outcome:** revision-required

#### Gate 1 — Definition Grounding: PASS

- Source provenance well-established: cites triggering task, runtime smoke frontier, MAPPING.md, SAGE_INVENTORY.md.
- Mathematical review finding correctly identified pattern-matching error and redirected.

#### Gate 2 — Acceptance Criteria: FAIL

All 10 acceptance criteria remain unchecked `[ ]`:

1. `[ ] Before any method is moved...` (no evidence)
2. `[ ] Before any method is moved off Modules(R)...` (no evidence)
...

The work log shows the task shifted from implementation to spec-audit (updating SPEC-MODULE-ROOT-METHOD-OWNERSHIP-MAPPING and creating DECISION-MODULE-SIDEDNESS-STRUCTURE-AND-OVERLOAD-SURFACES). However, the ACs were not updated to reflect this scope shift.

**Required fixes:**
1. Either update acceptance criteria to match what was accomplished, or create a follow-up implementation card.
2. Mark completed criteria as [x] with evidence; route deferred work to a new child card.
3. Rerun scoped smoke and record current frontier.

**Re-review criteria:**
- Acceptance criteria are checked with evidence or replaced by updated criteria reflecting actual scope.
- Smoke frontier recorded.
```

## Pitfalls
- Do not review your own implementation; use an independent agent session
- A smoke improvement paired with interface shrinkage = Gate 3 failure regardless
- `dependsOn` cards with incomplete deps = `unstarted`, not `blocked`
- Revision-required is distinct from unstarted (no work done) and blocked (external blocker)
- Repetitive revision cycles = escalate to plan review or decision card
