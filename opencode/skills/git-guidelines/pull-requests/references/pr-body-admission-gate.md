# PR Body Structure: The Three-Layer Contract

## Purpose

A PR body is a **fixed acceptance contract** written before implementation. It defines what external behavior the PR will produce, what evidence will prove it works, and what the current judgment is.

This document specifies how to write that contract so an independent reviewer can judge completion without relying on the implementer's claims.

## The Three-Layer Contract

Every PR body contains exactly three layers:

### 1. User Stories (product behavior only)

**What belongs:**
- Externally observable outcomes
- User or system behaviors
- Installation/setup results
- Integration points that must work

**What does NOT belong:**
- Implementation architecture
- File names or directory structure
- Specific libraries or tools chosen
- Internal refactoring justifications
- "Clean up technical debt"

**Example (correct):**
```markdown
## Intended Result
- A DSL author can expose a Lean-elaborated computational language through the kernel without DSL-specific Python integration
- A mathematician can install it and use a persistent notebook session
- Successful cells commit; failed or cancelled cells do not
- Completion, inspection, output, and recovery operate on the active DSL environment
- At least one real external DSL works through that interface
```

**Example (wrong):**
```markdown
## Intended Result
- Implement KernelProtocol with async message handlers
- Add transaction manager using contextlib for rollback
- Refactor plugin loader to use importlib.metadata
- Create proof certificates in JSON Schema format
```

### 2. Evidence Hypotheses (bounded proxies with exclusion justification)

These are **hypotheses about sufficient evidence**, not product requirements. They must:
- State what behavior will be demonstrated
- Explain what false positive each test excludes
- Be replaceable by reviewer judgment

**Required format:**

| Story Requirement | Proposed Evidence | What False Positive It Excludes |
|-------------------|-------------------|--------------------------------|
| Install real DSL | Clean install + real Jupyter execution | Developer-checkout-only success |
| Transactional state | Success/failure/cancellation journeys | Status-only or helper-level atomicity |
| Recovery preserves work | Kill real worker and continue | Recovery helper that production never uses |
| Generic integration | NbDsl + independent external DSL | Kernel hard-coded to one plugin |
| Safe output | Control-like output through real channel | Unit codec tests bypassing wiring |

**Critical principle:** A reviewer can say "this evidence is insufficient" or "this evidence is redundant" without changing the user stories. Evidence strategies are not requirements.

### 3. Current Judgment (generated just-in-time)

Produced by inspecting HEAD, running evidence, and evaluating gaps:

```markdown
## Current Status
- ✅ **Install real DSL**: Complete. Evidence: [CI run], [artifact link]
- ✅ **Transactional state**: Complete. Evidence: [test file], [journeys validation]
- ⚠️  **Recovery preserves work**: Partial. Known gap: recovery works but continuation API incomplete
- ❌ **Generic integration**: Blocked. External DSL crashes on import (see #123)
- ✅ **Safe output**: Complete. Evidence: [integration test]

## Merge Decision
Not ready. Generic integration must work. Recovery continuation can ship as follow-up (tracked in #124).

## Residual Risks
- Recovery API is minimal but sufficient for current DSL
- No performance testing under 1000+ cell notebooks
```

**What does NOT belong here:**
- Commit identities
- Historical plan changes
- Logs and full transcripts
- DONE annotations in the body
- Explanations of why previous approaches failed
- Instructions for how future agents must work

## Hard Admission Rules

Before opening or updating a PR, the body must pass these gates:

### Rule 1: No implementation architecture as requirements
❌ **Reject:**
```markdown
- [ ] Implement message broker using ZeroMQ
- [ ] Add async transaction manager with context protocol
- [ ] Create JSON Schema validator for certificates
```

✅ **Accept:**
```markdown
## Scope
- Included: Persistent notebook state across cell executions
- Excluded: Multi-user collaboration, distributed execution
- Preserved: Existing notebook file format compatibility
```

### Rule 2: No evidence strategies as permanent obligations
❌ **Reject:**
```markdown
- [ ] Generate proof certificates in proof-artifacts/
- [ ] Re-run validation after every head change
- [ ] Maintain evidence lineage with commit SHAs
- [ ] Seven workstreams must each produce evidence
```

✅ **Accept:**
```markdown
## Evidence Required
See table in section 2 above. Each test must demonstrate the behavior and exclude the named false positive.
```

### Rule 3: No mutable progress tracking in the contract
❌ **Reject:**
```markdown
- [x] ~~Week 1: Foundation work~~ DONE (commits abc123..def456)
- [x] ~~Certificate generation~~ DONE but needs regeneration
- [ ] Address review round 3 findings (62 closed, 77 new)
- [ ] Update this body with latest status
```

✅ **Accept:**
```markdown
## GitHub Tracking
- Closes #45 (transactional cell execution)
- Closes #67 (external DSL integration)
- Refs #23 (parent: notebook stability roadmap)
- Refs #89 (deferred: performance optimization)
```

Progress lives in commits, CI, and GitHub issue status—not in manually maintained PR body annotations.

### Rule 4: No process instructions for future agents
❌ **Reject:**
```markdown
## Agent Obligations
- All work must remain in this single PR
- Evidence must be regenerated after any head change
- Design choices may not be simplified
- Must follow seven-workstream decomposition
- Review feedback requires disposition artifacts
```

✅ **Accept:**
```markdown
## Review Focus
- Does this achieve the intended user-facing outcome?
- Is any acceptance criterion tautological or implementation-defined?
- Would any test pass on plausibly broken code?
- Is any file outside the declared scope boundary?
```

### Rule 5: No self-certification loops
The agent writing the implementation **cannot** be the sole judge of completion.

❌ **Reject:**
```markdown
- [x] All requirements complete (verified by builder agent)
- [x] Evidence sufficient (see my certificates)
- [x] Ready for merge (I checked everything)
```

✅ **Accept:**
```markdown
## Evidence for Independent Review
Each claimed behavior links to:
- Test file demonstrating the behavior
- CI run showing the test passes
- Explanation of what broken code would fail the test

Reviewer: please verify these tests are non-tautological.
```

### Rule 5a: No self-stamped claims—use GitHub's automatic validation
Any claim in the PR body must be **independently verifiable** through GitHub's automatic mechanisms, not through manual assertions.

❌ **Reject (self-stamped):**
```markdown
## Closes
- Closes #45 ✓ (I verified this is complete)
- Closes #67 ✓ (all acceptance criteria met)
- Issue #89 can be closed after this merges
```

✅ **Accept (automatically validated):**
```markdown
## GitHub Tracking
Closes #45, #67

<!-- GitHub automatically creates Development links and will close these on merge.
     An independent reviewer can verify the links exist and the issues are actually satisfied. -->
```

**Validation method:**
```bash
# Verify GitHub parsed the closing keywords correctly
gh pr view <PR_NUMBER> --json closingIssuesReferences

# Expected output shows GitHub recognizes the issues:
# "closingIssuesReferences": [
#   {"id": "...", "number": 45, ...},
#   {"id": "...", "number": 67, ...}
# ]
```

**Key principle:** 
- Use `Closes #N` keywords in the body → GitHub creates Development links automatically
- The PR shows linked issues in the sidebar → independently verifiable
- On merge, GitHub closes them automatically → no manual claiming
- If GitHub didn't parse it, the link doesn't exist → forces correct format

**Wrong pattern (manual claiming):**
- Agent writes "I close #45" in prose without closing keyword
- Agent adds checkbox "- [x] #45 is done" 
- Agent manually marks issues closed in a tracking table
- Agent says "this PR satisfies #45" without GitHub seeing the link

**Right pattern (automatic validation):**
- Use exact closing keywords: `Closes #N`, `Fixes #N`, `Resolves #N`
- Verify GitHub parsed it: `gh pr view --json closingIssuesReferences`
- Reviewer sees Development links in PR sidebar
- On merge, GitHub closes automatically—no agent action needed

### Rule 6: No proxy breeding—keep deferred/excluded work out of checkboxes
❌ **Reject:**
```markdown
- [ ] Current phase 1 work
- [ ] Future phase 2 work (deferred)
- [ ] Nice-to-have cleanup (out of scope)
- [ ] Alternative approach (not chosen)
- [ ] Documentation updates (for later PR)
```

✅ **Accept:**
```markdown
## Scope
- Included: [what this PR does]
- Explicitly excluded: Phase 2 multi-user (#89), performance tuning (#90)
- Deferred for follow-up: UI polish (#91), extended DSL library (#92)

## Claim Map
- [ ] Transactional execution (#45)
- [ ] External DSL integration (#67)
```

Only required-for-this-PR work becomes a checkbox.

### Rule 7: No provisional decomposition as law
❌ **Reject:**
```markdown
## Required Workstreams
This PR requires seven workstreams in this exact order:
1. Foundation (must complete first)
2. Kernel protocol (cannot be simplified)
3. Transaction manager (architectural necessity)
...
Each workstream must produce evidence before the next begins.
```

✅ **Accept:**
```markdown
## Implementation Plan
1. Add transactional cell execution
2. Integrate external DSL loader
3. Wire completion/inspection to DSL environment

If review discovers a simpler approach, the plan can change.
```

## When to Reject a PR Body

Stop and revise the plan when any of these are true:

1. **Architecture is in the acceptance criteria**
   - User stories mention file names, class names, or libraries
   - Completion depends on "implemented X pattern"

2. **Evidence strategy became product requirements**
   - Certificates, logs, or artifact schemas are deliverables
   - Regeneration, lineage, or provenance tracking is in the checklist

3. **Mutable state is in the contract**
   - DONE markers, progress percentages, or status timestamps
   - Historical explanations of why previous approaches failed
   - "Update this section weekly"

4. **Process is encoded as obligations**
   - Instructions for how agents must behave
   - Exact workstream decomposition that cannot be simplified
   - "All work must stay in one PR"
   - Branch protection rules repeated in the body

5. **Self-certification loop**
   - Builder agent marks its own work complete
   - Evidence produced by the same system that needs proving
   - "I verified everything"

6. **Proxy breeding**
   - Deferred work, future work, excluded scope in checkboxes
   - Every checkbox parent has 5+ mechanical sub-items
   - More governance/process items than user-story items

7. **Missing independent stopping judgment**
   - No external reviewer can say "ship it" or "block it" from the body alone
   - Completion criteria are "all checkboxes ticked" without reference to user stories
   - Evidence points to other evidence rather than to behavior

## Recovery: What to Do When a PR Body Fails Admission

1. **Stop adding to the PR**—every new commit while the body is structurally wrong makes the problem worse.

2. **Extract the real user stories**—what external behavior is this PR trying to enable?

3. **Separate evidence from requirements**—which obligations are "prove X works" versus "X must work"?

4. **Remove mutable tracking**—DONE markers, historical explanations, progress percentages go away.

5. **Remove process encoding**—agent instructions, workstream mandates, exact tool choices.

6. **Shrink to claimed scope only**—deferred, future, excluded work leaves the checklist.

7. **Rewrite using the three-layer model above.**

8. **Have an independent reviewer judge**—someone who didn't write the plan.

## Example: Before and After

### ❌ Before (Recursive Proxy Breeding)

```markdown
## Implementation Plan
This PR implements the complete NbDsl kernel architecture using seven required workstreams:

### Workstream 1: Foundation
- [x] ~~Implement KernelProtocol base~~ DONE (commit abc123)
- [ ] Generate foundation certificates
- [ ] Validate foundation evidence after head changes

### Workstream 2: Transaction Management
- [ ] Implement transaction manager (cannot be simplified per design decision)
- [ ] Add rollback using contextlib.AbstractContextManager
- [ ] Certificate schema for transaction proofs
...

### Evidence Requirements
All workstreams must produce proof certificates in `proof-artifacts/` with:
- Exact commit SHA provenance
- Timestamp of validation
- Lineage chain to parent evidence
- Regeneration required after any head change

### Completion Authority
Builder agent marks each item done after self-verification. All seven workstreams must complete before merge. Design choices may not be simplified.

### Repository Governance
All work must remain in this single PR. Branch protection requires:
- All certificates valid
- All workstreams complete
- Evidence synchronized to HEAD
```

**Problems:**
- Implementation architecture in user stories
- Evidence generation is a product requirement
- Mutable DONE markers
- Process encoded as obligations
- Self-certification
- Provisional decomposition became law

### ✅ After (Three-Layer Contract)

```markdown
## Intended Result
- DSL author can expose computational language through kernel without Python integration
- Mathematician can install and use persistent notebook sessions
- Successful cells commit; failed/cancelled cells do not
- At least one real external DSL works end-to-end

## Scope
- Included: Generic DSL kernel protocol, transactional cell execution, one reference DSL
- Excluded: Multi-user collaboration, distributed execution, performance optimization
- Preserved: Existing Jupyter notebook file format, current cell execution API

## GitHub Tracking
- Closes #45 (transactional execution)
- Closes #67 (generic DSL integration)
- Refs #23 (parent roadmap: notebook stability)
- Refs #89 (deferred: performance work)
- Milestone: Notebook Kernel Stability v1

## Evidence Required

| Story | Proposed Evidence | Excludes |
|-------|-------------------|----------|
| Install real DSL | Clean install + Jupyter execution | Developer-only success |
| Transactional state | Success/fail/cancel journeys | Status-only atomicity |
| Recovery works | Kill worker and continue | Unused helper code |
| Generic integration | Two independent DSLs | Hard-coded plugin |

## Claim Map
- [ ] **#45 - Transactional cell execution**
  - Evidence: `test_cell_transactions.py` (success/fail/cancel journeys)
  - Current: [CI run #456]
- [ ] **#67 - Generic DSL integration**
  - Evidence: NbDsl + one external DSL both working
  - Current: NbDsl works, external DSL blocked (see #123)

## Current Status
⚠️ Not ready. External DSL integration blocked by import error (tracked in #123). All other stories complete.

## Review Focus
- Do these stories capture the intended notebook workflow?
- Is the external-DSL evidence sufficient to prove genericness?
- Are any tests tautological (would pass on broken code)?
```

**Improvements:**
- User stories are product behavior only
- Evidence is hypothesis, not requirement
- No mutable tracking in body
- No process encoding
- Progress tracked via GitHub issues + CI
- Independent reviewer can judge from this alone

## Summary

The admission gate prevents:
1. **Proxy substitution**: evidence strategies becoming product requirements
2. **Self-reinforcing loops**: more work generating more obligations
3. **Process encoding**: provisional plans becoming permanent law
4. **Mutable contracts**: progress tracking in the acceptance criteria
5. **Self-certification**: builder judging its own completion
6. **Self-stamped claims**: manual assertions instead of GitHub's automatic validation
7. **Scope creep**: deferred work in the checklist

A PR body that passes this gate is:
- **Stable**: the three layers don't expand during implementation
- **Falsifiable**: an independent reviewer can judge completion
- **Bounded**: obligations are finite and tied to user stories
- **Honest**: evidence is proposed, not required; reviewers can override
- **Automatically validated**: GitHub mechanisms (Development links, closing keywords) prove claims, not agent assertions

The post-mortem shows what happens without this gate: 37 commits, 52 files, 10K+ lines, 139+ findings, and the original notebook workflow still not demonstrated.
