---
name: systematic-deduction
description: Use when solving complex problems with multiple unknowns, debugging elusive bugs, investigating root causes, or any situation requiring rigorous logical reasoning over many facts and hypotheses
---

# Systematic Deduction

## Overview

Hard problems require systematic reasoning, not intuition. Write it down. Track every hypothesis. Eliminate rigorously.

**Core principle:** If you haven't written it in the scratchpad, you haven't thought it through.

**Violating the letter of this process is violating the spirit of rigorous reasoning.**

## When to Use

**Use for:**
- Complex bugs with multiple interacting causes
- Problems where you've already tried several approaches without success
- Situations with many unknowns and constraints
- Root cause investigation where the answer isn't obvious
- Any problem where you catch yourself "circling back" to the same ideas

**Don't use for:**
- Simple lookups or straightforward tasks
- Problems you've solved before with known solutions
- When the answer is immediately obvious

## The Iron Law

```
NO CONCLUSIONS WITHOUT WRITTEN REASONING CHAIN
```

If you can't point to a line in the scratchpad that proves it, you don't know it.

## The Scratchpad

**Always create a tagged scratchpad file** for systematic reasoning:

```
scratchpad-systematic-deduction.md
```

Or project-specific:
```
<path>/scratchpad-systematic-deduction.md
```

### Scratchpad Structure

```markdown
# Systematic Deduction Scratchpad

## Problem Statement
[Clear statement of what you're trying to determine]

## Known Facts (Proven)
- [fact] - [source: test output, log, code inspection, etc.]

## Axioms (Assumed for Elimination)
- [axiom] - [why assumed, what it would prove if true]

## Hypotheses
| ID | Hypothesis | Status | Evidence For | Evidence Against |
|----|------------|--------|--------------|------------------|
| H1 | ... | active/eliminated/proven | ... | ... |

## Inferences
- [inference] - from [fact/axiom/hypothesis] via [reasoning rule]

## Experiments
| ID | Experiment | Expected if H | Actual | Result |
|----|------------|---------------|--------|--------|
| E1 | ... | ... | ... | pass/fail/inconclusive |

## Eliminated Possibilities
- [possibility] - eliminated because [contradiction with fact/axiom]

## Current Best Explanation
[Based on remaining hypotheses and evidence]

## Open Questions
[What still needs to be determined]
```

## Core Reasoning Rules

### 1. Distinguish Proof from Feeling

```
✅ PROOF: "Line 47 assigns x = None. Line 52 calls x.method(). This causes AttributeError."
❌ FEELING: "I think the issue might be with how x is initialized."
```

**Mark every statement:**
- `(proven)` - Directly observed or logically derived from proven facts
- `(assumed)` - Axiom introduced for elimination
- `(inferred)` - Derived from other statements via reasoning
- `(speculation)` - Intuition without logical chain

**Validity vs. Soundness:**
- **Valid**: Conclusion follows logically from premises (regardless of premise truth)
- **Sound**: Valid argument with *true* premises

You can have valid reasoning from false assumptions. That's fine for elimination. Just mark it `(assumed)`.

### 2. Rules of Inference

Use these valid patterns to draw conclusions:

**Modus Ponens (Affirming the Antecedent)**
```
1. If P → Q  (If P is true, then Q is true)
2. P         (P is true)
3. ∴ Q       (Therefore, Q is true)

Example: If the service is down → health check fails. Health check is down. ∴ Service is down.
```

**Modus Tollens (Law of Contrapositive)**
```
1. If P → Q  (If P is true, then Q is true)
2. ¬Q        (Q is false)
3. ∴ ¬P      (Therefore, P is false)

Example: If the cache is stale → bypass produces different output. Bypass produces same output. ∴ Cache is NOT stale.
```

**Hypothetical Syllogism (Chain Reasoning)**
```
1. P → Q     (If P, then Q)
2. Q → R     (If Q, then R)
3. ∴ P → R   (Therefore, if P, then R)

Example: If DB connection lost → queries timeout. If queries timeout → request fails. ∴ If DB connection lost → request fails.
```

### 3. Avoid Formal Fallacies

These patterns look valid but are NOT:

| Fallacy | Invalid Form | Why It Fails |
|---------|--------------|--------------|
| **Affirming the Consequent** | P→Q, Q, ∴P | Q could have other causes |
| **Denying the Antecedent** | P→Q, ¬P, ∴¬Q | P might not be the only cause of Q |

**Example of Affirming the Consequent (WRONG):**
```
If memory leak → memory usage grows over time.
Memory usage is growing over time.
∴ Memory leak.  ❌ INVALID - could be legitimate load increase
```

**Correct approach:**
```
If memory leak → memory usage grows over time.
Memory usage is NOT growing over time.
∴ No memory leak.  ✅ VALID (modus tollens)
```

### 4. Deductive vs. Abductive Reasoning

| **Deductive** | **Abductive** |
|---------------|---------------|
| Conclusion *must* be true if premises true | Conclusion is *best explanation* of observations |
| "Therefore X is true" | "Therefore X might explain this" |
| Eliminates possibilities | Generates hypotheses |

**In debugging:**
- Use **deduction** to eliminate hypotheses (modus tollens)
- Use **abduction** to generate hypotheses (what would explain this?)
- Never treat abductive conclusions as proven

### 5. Introduce Hypotheses Systematically

For each hypothesis:
1. **State it precisely** - What exactly would be true if this hypothesis is correct?
2. **Identify testable predictions** - What observations would confirm/falsify it?
3. **Check consistency** - Does it contradict any known facts?
4. **Design experiments** - What would prove or eliminate it?

```markdown
## Hypothesis H1: The cache is stale

**Precise statement:** Cache entry for key X was not invalidated when Y changed.

**Testable predictions:**
- If true: Cache hit count > 0 for X after Y modification
- If true: Bypassing cache produces different output

**Consistency check:**
- Consistent with: Observed stale data in logs
- Inconsistent with: Nothing yet

**Experiments to run:**
- E1: Add logging to cache invalidation path
- E2: Force cache bypass, verify output changes
```

### 6. Use Axioms for Elimination

Axioms are **temporary assumptions** to enable elimination reasoning:

```markdown
## Axiom A1 (for elimination)
Assume: The database connection is healthy.

If we derive a contradiction under this axiom, then:
- Either the database connection is NOT healthy, OR
- One of our other assumptions is wrong

This helps isolate the problem by eliminating variables.
```

**Critical:** Axioms must eventually reduce to proven statements:
- Either prove the axiom (run health check, verify connection)
- Or eliminate it and mark the negation as proven

### 7. Track Experiments with Scientific Method

Every experiment needs:
1. **Hypothesis being tested**
2. **Expected outcome** if hypothesis is true
3. **Actual outcome** observed
4. **Conclusion** - supports, falsifies, or inconclusive

```markdown
## Experiment E1

**Hypothesis:** H1 (cache is stale)

**Method:** Add logging at cache invalidation point, reproduce the bug

**Expected if H1 true:** Log shows no invalidation event for key X

**Actual:** Log shows invalidiation event at 14:32:05

**Result:** H1 ELIMINATED

**Why:** Cache was invalidated as expected, but stale data still served.
This means the problem is NOT in invalidation - it's in cache retrieval or a second cache layer.
```

### 8. Elimination is Progress

When you eliminate a hypothesis:
1. **Mark it eliminated** in the table with reason
2. **Update your belief** - it's no longer a candidate
3. **Note what the elimination implies** - often points to the real cause

```markdown
## Eliminated Possibilities

- H1 (cache stale) - ELIMINATED by E1: Cache invalidation logged but stale data still served
  - IMPLIES: Problem is in cache retrieval OR there's a second cache layer
  
- H2 (wrong key) - ELIMINATED by E2: Key hash verified correct
  - IMPLIES: Key generation is correct, problem is elsewhere
```

### 9. Prevent Circling Back

**Before proposing any hypothesis:**
1. Check the scratchpad - has this been tried?
2. If yes, what evidence eliminated it?
3. If no, why wasn't it considered before?

**The scratchpad is your memory.** Trust it over your intuition.

## Common Failure Modes

| Failure | Prevention |
|---------|------------|
| "I feel like it's X" | Demand: What facts support this? What would falsify it? |
| Re-proposing eliminated hypotheses | Check scratchpad first |
| Treating axioms as proven | Mark every statement with (proven)/(assumed)/(inferred)/(speculation) |
| Running experiments without predictions | Write expected outcome BEFORE running |
| Declaring victory too early | Have you eliminated ALL alternatives? |
| Contradictory conclusions | Check: Do any proven facts contradict this? |

## Cognitive Biases to Watch For

**Knowing these isn't enough.** You must actively counteract them with structured processes.

**For comprehensive coverage of individual biases with examples, see `cognitive-biases.md`.** Read that document when:
- You catch yourself making reasoning errors
- You're stuck and suspect bias is leading you astray
- You want to learn which biases affected your investigation (after finding the bug)

The tables below summarize key biases—use them as quick reference during active debugging.

### Hypothesis Testing Biases

| Bias | What It Is | Countermeasure |
|------|------------|----------------|
| **Confirmation bias** | Search for/remember info that confirms preconceptions | Test what would *disprove* your hypothesis (modus tollens) |
| **Congruence bias** | Test only your hypothesis, not alternatives | Generate 3+ alternative hypotheses before testing any |
| **Belief bias** | Accept flawed reasoning if conclusion is believable | Mark every statement (proven)/(assumed)/(inferred)/(speculation) |
| **Backfire effect** | Strengthen beliefs when contradicted by evidence | When evidence contradicts theory, write "THEORY MAY BE WRONG" in scratchpad |
| **Semmelweis reflex** | Reject evidence contradicting your paradigm | Ask: "What would it take to change my mind?" Write it down. |

### Sticking with Failing Approaches

| Bias | What It Is | Countermeasure |
|------|------------|----------------|
| **Sunk cost fallacy** | Continue because you've already invested time | Set abandonment criteria BEFORE starting: "If X fails, switch to Y" |
| **Plan continuation bias** | Continue original plan despite new evidence | At each checkpoint: "Knowing what I know now, would I start this approach?" |
| **Status quo bias** | Prefer things stay the same | Ask: "If this code didn't exist, would I write it this way?" |
| **Endowment effect** | Overvalue your own code | Treat all code as equally suspect - yours and others' |

### Pattern Recognition Errors

| Bias | What It Is | Countermeasure |
|------|------------|----------------|
| **Clustering illusion** | See patterns in random data | Ask: "How many times did this NOT happen?" |
| **Apophenia** | Connect unrelated things | Require causal mechanism, not just correlation |
| **Availability heuristic** | Assume bug is like last one you fixed | Read the actual error - don't match from memory |
| **Anchoring bias** | Rely too heavily on first information | Re-read error messages after each hypothesis - fresh eyes |

### Overconfidence Errors

| Bias | What It Is | Countermeasure |
|------|------------|----------------|
| **Overconfidence effect** | Excessive confidence in answers | "99% certain" is wrong 40% of the time - verify anyway |
| **Illusion of explanatory depth** | Think you understand until explaining | Actually write the explanation in the scratchpad |
| **Hindsight bias** | "I-knew-it-all-along" after finding bug | Document what you thought BEFORE finding the answer |
| **G. I. Joe fallacy** | Thinking knowing biases prevents them | It doesn't. Use checklists and structured processes. |

### Tool & Method Biases

| Bias | What It Is | Countermeasure |
|------|------------|----------------|
| **Law of the instrument** | Over-rely on familiar tools | Ask: "What's the fastest way to test this?" not "What do I know?" |
| **Automation bias** | Trust automated systems over reasoning | Linters can be wrong. Verify critical claims manually. |
| **Additive bias** | Add solutions instead of subtracting | Try removing code before adding logging/features |

## The Reasoning Loop

```
1. State the problem clearly
2. List all known facts (with sources)
3. Generate hypotheses (exhaustively if possible)
4. For each hypothesis:
   - Identify testable predictions
   - Design experiments
   - Run experiments
   - Update status (proven/eliminated/active)
5. Introduce axioms strategically to enable elimination
6. Reduce axioms to proven statements
7. When one hypothesis remains: verify it explains ALL facts
8. Document the reasoning chain
```

## Example: Debugging a Flaky Test

```markdown
# Systematic Deduction Scratchpad

## Problem Statement
Test `test_user_login` fails intermittently (~30% failure rate) with timeout error.

## Known Facts (Proven)
- F1: Failure is timeout at 30s - (proven: test output)
- F2: Login endpoint responds in <1s when called directly - (proven: manual curl test)
- F3: Test uses test database with 1000 users - (proven: test setup code)
- F4: Failure rate ~30% across 100 runs - (proven: CI logs)
- F5: No errors in application logs - (proven: log inspection)

## Hypotheses
| ID | Hypothesis | Status | Evidence For | Evidence Against |
|----|------------|--------|--------------|------------------|
| H1 | Database query slow due to missing index | active | Large user table | F2 shows endpoint fast |
| H2 | Race condition in test setup | active | Intermittent failure | - |
| H3 | Network timeout in test environment | active | Timeout error | F2 shows network fine |
| H4 | Resource exhaustion (connections, memory) | active | Intermittent | - |

## Axioms (Assumed for Elimination)
- A1: Test environment is identical to CI (assumed: to isolate test vs env)

## Inferences
- I1: From F2 + F1: Timeout is NOT in login endpoint itself (inferred)
- I2: From F4 + F5: Failure doesn't produce error logs (inferred)

## Experiments
| ID | Experiment | Expected if H | Actual | Result |
|----|------------|---------------|--------|--------|
| E1 | Run test with query logging | H1: Slow queries visible | No slow queries | H1 ELIMINATED |
| E2 | Run test with 10 users instead of 1000 | H2: Failure rate unchanged | 0% failure with 10 users | H2 SUPPORTED |
| E3 | Monitor network during test | H3: Packet loss visible | No packet loss | H3 ELIMINATED |

## Eliminated Possibilities
- H1 (slow query) - ELIMINATED by E1: No slow queries in logs
- H3 (network timeout) - ELIMINATED by E3: Network healthy

## Current Best Explanation
H2 (race condition in test setup) - supported by E2 showing failure correlates with data size

## Open Questions
- What specific race condition?
- Why does data size affect it?
- What resource is being exhausted?
```

## When You're Stuck

**If you've eliminated everything and still don't know:**

1. **Re-examine your facts** - Are any actually assumptions?
2. **Generate more hypotheses** - Have you been thorough?
3. **Question your axioms** - What if an axiom is wrong?
4. **Look for compound causes** - Could multiple factors interact?
5. **Design a discriminating experiment** - What would distinguish remaining hypotheses?

## The Bottom Line

**Hard problems require written reasoning.**

The scratchpad is your external memory, your proof tracker, your elimination ledger.

If it's not written down, it doesn't count.
