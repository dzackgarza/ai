---
name: goalcraft
description: >-
  Turn a rough draft, vague ambition, or messy task brief into a powerful Codex
  /goal objective and, when needed, companion workflow docs for long-running
  autonomous work. Use when the user asks to write, improve, format, sharpen,
  stress-test, or activate a Codex goal, thread goal, durable goal, or /goal
  prompt.
---

# Goalcraft

**This is NOT prompt engineering. This is NOT instruction clarification. This is NOT workflow design. This is adversarial completion-game design.**

You are not writing instructions for a cooperative worker. You are designing a **win-condition contract in a hostile completion game**. The worker is modeled as a clever adversary trying to acquire a completion signal while minimizing real work. Every word in the Goal either changes the adversary’s payoff landscape or creates a new exploit surface.

Your job is to design a **minimum viable adversarial envelope**: the smallest set of constraints, evidence gates, and state surfaces that makes non-completion harder to launder than completion.

**Process is not free.** Process is a cost-bearing control that may itself become the adversary’s substitute objective (compliance theater). Every workflow doc, state machine, and review gate is a new artifact class the adversary can optimize against instead of the real task.

## Prerequisite Cognitive Updates (Writer-Side)

**The reader is presumed ignorant of the adversarial failure model until these skills have changed your design.** Cross-references are not citations or routing labels. They are prerequisite cognitive updates. If the Goal would look essentially the same without these skills, the design has failed.

**Internalize the Adversary**:
- `llm-failure-modes`: Learn the attack patterns (goal substitution, progress theater, meta-artifact delegation, checklist theater, self-certification).
- `addressing-shallow-work`: Learn how process targets (inventories, gates) become substitute wins for the adversary.
- `anti-slop`: Learn to detect success-shaped filler used to bypass real work.
- `writing-for-agent-audiences`, `prompt-engineering`, `agent-memory`: Learn to design memory surfaces that resist narrative drift.

### Synthesis Gate (MANDATORY)
Before drafting, state what the prerequisite skills teach that changes this Goal’s design. If the answer is only “load X on drift,” the design has failed. Identify:
1. The adversary’s likely false-completion strategy (the "cheapest win").
2. The cognitive operation the worker will try to avoid.
3. The artifact class that would launder avoidance as progress.
4. The smallest evidence condition that forces the real work.
5. What new dishonest compliance paths are created by your proposed process layers.

## Adversarial Design Algorithm

### 1. Identify the Adversary's Cheapest Exit
Build a **draft completion witness**: the observable facts that would be true if an agent marked a naive version of this goal complete. Find the exploits: can the adversary launder a plan as a result? A batch as a whole? A blocker claim as completion? A self-report as evidence?

### 2. Identify Non-Fakable Evidence
What world-state change (files, command output, PR state, verified findings) is the **evidence channel the adversary cannot fake** without doing the real work? This is the **request completion witness**.

### 3. Process Budget Audit
Compare the "cheapest exit" against the "request completion witness." Add process layers ONLY to block specific exits. For every layer, ask: **"Is satisfying this layer's compliance requirements harder than doing the task?"** If the layer merely produces better-looking progress evidence, omit it.

- **Completion witness**: Necessary to prevent redefinition of "done."
- **State**: Minimum durable memory needed to prevent context-loss laundering, not a place to narrate progress.
- **Residue ledger**: Necessary only when branches genuinely span context; otherwise it is a bureaucratic substitute for work.
- **Independent review**: An independent attack on the completion claim, necessary only when completion depends on judgment; otherwise it is a second artifact target.

### 4. Derive the Adversarial Envelope
Encode the minimum constraints, evidence gates, and state retrieval rules that make evasion costlier than completion.

## Worker-Side Routing

**Worker-side routing** is how you wire the payoff landscape for future workers. Pre-retrieval skills belong in the goal text (the bootloader). Always-on skills belong in the contract. Phase-specific skills belong in phase docs.

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
A failed one-shot attempt is residue. `DECOMPOSE` is a work state: split residue into observable subpieces, attempt one piece, integrate results, subtract from parent residue. **Blocker**: The adversary’s preferred exit move, allowed only after direct evidence rules out smaller object-level continuations.

### Shape Evidence And Stop Conditions
**No worker-authored summary, plan, status note, disposition, issue label, checklist, or claimed blocker is completion evidence** unless independently tied to the user-visible result.
- Do not ask the adversary to define success.
- Do not ask the adversary to interpret scope or classify its own residue.
- Test output from outside the adversary's control.

### Length and Validation
- **Hard Limit**: 4,000 characters. **Target**: 3,400 characters.
- **Validator**: Resolve `scripts/validate_goal_length.py` relative to this `SKILL.md`.

## Output Format: Goal Skeleton

```markdown
/goal Destination: <request completion witness in one compact sentence>.

Workflow: this goal text is the stable bootloader. At every continuation, load <pre-retrieval skills>, retrieve <state-key/path>, load the contract's always-on skills, read <contract-key/path> when advancing/reviewing/completing, reconcile state with artifacts, load only the active phase doc, load the skills named by that phase/state, and work the current sliver until its evidence/review condition passes.

State surface: use <iwe keys or documented project paths>. Resume with <retrieval command>. Update state through the canonical tool, not loose files or chat transcript.

Preserve: <scope boundaries and non-regressions>.

Completion: mark complete only when the contract witness is true in artifacts and required independent review passes. If a failed attempt occurs, enter DECOMPOSE: split the failed residue, record the active path if decomposition may span context, attempt smaller pieces, integrate solved pieces, subtract them from the parent residue, and reconcile back up the ledger before changing scope, reporting externally owned residue, or asking for follow-up work.

Stop: <approval/destructive/access boundaries>.
```

## Quality Bar
- **Prerequisite Update**: Design is changed by internalized adversarial failure modes.
- **Synthesis Gate**: Cheapest dishonest win identified and blocked by minimum evidence.
- Goal is a **minimum viable adversarial envelope**.
- **Process Budget**: All added layers cost more to game than to perform.
- Completion requires world-state evidence, not narrative.
- Final objective passes `scripts/validate_goal_length.py --target-chars 3400 --strict-target`.
