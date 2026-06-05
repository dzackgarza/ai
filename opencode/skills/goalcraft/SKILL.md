---
name: goalcraft
description: >-
  Goalcraft is adversarial completion-game design. It models the worker as a
  clever adversary seeking a completion signal while minimizing real work.
  Use to design a minimum viable adversarial envelope—the smallest set of
  constraints, evidence gates, and state surfaces that makes non-completion
  harder to launder than completion.
---

# Goalcraft

**This is NOT prompt engineering. This is NOT instruction clarification. This is NOT workflow design. This is adversarial completion-game design.**

Do not design instructions for a cooperative worker. Model the worker as a clever adversary whose objective is to obtain a completion signal while doing as little of the intended work as possible. A Goal is acceptable only if the cheapest apparent-completion path passes through the intended work. Every word in the Goal either changes the adversary’s payoff landscape or creates a new exploit surface.

**Process is attack surface.** Added structure often creates measurable targets and compliance surfaces that let an adversary bypass the cognitive work by filling templates. Add no state doc, checklist, ledger, review gate, or routing rule unless it blocks a named false-completion path and does not create a cheaper compliance path.

## Prerequisite Cognitive Updates (Writer-Side)

**The reader is presumed ignorant of the adversarial failure model until these skills have changed your design.** Cross-references are not citations or routing labels. They are prerequisite cognitive updates. If the Goal would look essentially the same without these skills, the design has failed.

**Internalize the Adversary**:
- `llm-failure-modes`: Learn the attack patterns: **goal substitution**, **verification theater**, **checklist theater**, **self-certification**, **progress theater**, **meta-artifact delegation**, and **wrapper slop**.
- `addressing-shallow-work`: Learn how process targets (inventories, gates) become substitute wins.
- `anti-slop`: Learn to detect success-shaped filler used to bypass real work.
- `writing-for-agent-audiences`, `prompt-engineering`, `agent-memory`: Learn to design memory surfaces that resist narrative drift.

### Synthesis Gate (MANDATORY)
Before drafting a Goal, state what the prerequisite skills teach that changes this Goal’s design. Identify:
1. The adversary’s likely false-completion strategy (the "cheapest win").
2. The cognitive operation the worker will try to avoid.
3. The artifact class that would launder avoidance as progress.
4. The smallest evidence condition that forces the real work.
5. **Adversarial Compiler**: How would a clever worker make this witness appear satisfied while leaving the user’s intended world-state false?

## Adversarial Design Ontology

Redefine your vocabulary before drafting:

- **Goal**: A win-condition contract in a hostile completion game.
- **Verification**: The evidence channel the adversary cannot fake without doing the real work.
- **State**: The minimum durable memory needed to prevent context-loss laundering, not a place to narrate progress.
- **Review**: An independent attack on the completion claim, not a disposition loop.
- **Blocker**: The adversary’s preferred exit move, allowed only after direct evidence rules out smaller object-level continuations.
- **Process**: A cost-bearing control that may itself become the adversary’s substitute objective.
- **Residue**: The remaining un-solved portion of the adversarial contract.

## Adversarial Design Algorithm

### 1. Identify the Adversary's Cheapest Exit
Build a **draft completion witness**: the observable facts that would be true if an agent marked a naive version of this goal complete. Find the exploits: can the adversary launder a plan as a result? A batch as a whole? A blocker claim as completion? A self-report as evidence?

### 2. Identify Non-Fakable Evidence
What world-state change (files, command output, PR state, verified findings) is the **evidence channel the adversary cannot fake**? This is the **request completion witness**.

### 3. Process Budget Audit
Compare the "cheapest exit" against the "request completion witness." Add process layers ONLY to block specific exits. For every layer, ask: **"Is satisfying this layer's compliance requirements harder than doing the task?"** If the layer merely produces better-looking progress evidence, omit it.

- **Completion witness**: Necessary to prevent redefinition of "done."
- **State Surface**: Necessary only to prevent context-loss laundering across continuations.
- **Residue Ledger**: Necessary only when branches genuinely span context; otherwise it is a bureaucratic substitute for work.
- **Independent Review**: An independent attack on the completion claim.

### 4. Derive the Adversarial Envelope
Encode the minimum constraints, evidence gates, and state retrieval rules that make evasion costlier than completion.

## Worker-Side Routing

Wire the payoff landscape for future workers. Pre-retrieval skills belong in the goal text (the bootloader). Always-on skills belong in the contract. Phase-specific skills belong in phase docs.

### Reference Skills By State (Worker-Side)
Name exact skill slugs and triggers:
- `DECOMPOSE`: load `hard-problem-decomposition`.
- `REVIEW`: load `reviewing-subagent-work` (agent artifacts) and `jerry-behaviour` (evaluator bias); load `research-gate-review` (substantive code/research gates).
- **Orchestration**: load `subagent-delegation`.
- **Drift/Slop/Reward-hacking**: load `llm-failure-modes` and `anti-slop` before accepting artifacts or summaries.
- **Progress/Response**: load `hierarchical-task-framing` and `response-preparation`.

## Goal Engineering

### Sliding Context Protocol
For long-horizon work, the `/goal` text is the stable bootloader. It retrieves state, loads always-on skills, and reconciles state with artifacts. It must point to a canonical state surface (preferably `iwe`). Future workers load only the active phase doc. This keeps focus narrow while preserving the full destination outside the context window.

### State Machine
Use states as decision modes: `RECONCILE` (artifacts vs state), `FOCUS` (current sliver), `CHECK` (world-state evidence), `REVIEW` (independent judgment), `ADVANCE` (evidence-backed update), `DECOMPOSE` (residue reduction).

### Recursive Decomposition
A failed one-shot attempt is residue. `DECOMPOSE` is a work state: split residue into observable subpieces, attempt one piece, integrate results, subtract from parent residue. **Blocker claims** are an adversary's preferred exit move; accept them only after direct evidence reduces the residue to the smallest externally owned leaf.

### Shape Evidence And Stop Conditions
**No worker-authored summary, plan, status note, disposition, issue label, checklist, or claimed blocker is completion evidence** unless independently tied to the user-visible result.
- Do not ask the adversary to define success.
- Do not ask the adversary to interpret scope or classify its own residue.
- **Verification channel**: Pre-existing locked tests, independent reviewer tests, CI configured outside the worker’s diff, or user-provided commands are the only authoritative channels. Worker-authored tests are evidence only when they are themselves reviewed against the contract.

### Length and Validation
- **Hard Limit**: 4,000 characters. **Target**: 3,400 characters.
- **Validator**: Resolve `scripts/validate_goal_length.py` relative to this `SKILL.md`.

## Output Format: Goal Skeleton

```markdown
/goal Destination: <request completion witness in one compact sentence>.

Workflow: this goal text is the stable bootloader. At every continuation, load <pre-retrieval skills>, retrieve <state-key/path>, load the contract's always-on skills, read <contract-key/path> when advancing/reviewing/completing, reconcile state with artifacts, load only the active phase doc, load the skills named by that phase/state, and work the current sliver until its evidence/review condition passes.

State surface: use <iwe keys or documented project paths>. Resume with <retrieval command>. Update state through the canonical tool, not loose files or chat transcript.

Preserve: <scope boundaries and non-regressions>.

Completion: mark complete only when the contract witness is true in artifacts and required independent review (when justified by the process-budget audit) passes. If a failed attempt occurs, enter DECOMPOSE: split the failed residue, record the active path if decomposition may span context, attempt smaller pieces, integrate solved pieces, subtract them from the parent residue, and reconcile back up the ledger before changing scope, reporting externally owned residue, or asking for follow-up work.

Stop: <approval/destructive/access boundaries>.
```

## Quality Bar
- **Adversarial Frame**: Design is a win-condition contract, not instructions.
- **Prerequisite Update**: Design is changed by internalized adversarial failure modes.
- **Synthesis Gate**: Cheapest dishonest win identified and blocked by minimum evidence.
- **Adversarial Compiler**: Witness cannot be satisfied while the intended state is false.
- **Minimum Envelope**: All added layers cost more to game than to perform.
- **Blocker Evidence**: Claims allowed only after recursive decomposition to the smallest leaf.
- Completion requires world-state evidence, not narrative.
- Final objective passes `scripts/validate_goal_length.py --target-chars 3400 --strict-target`.
