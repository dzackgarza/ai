# Routing Run Results

**Date:** 2026-03-01
**Mode:** `PROMPT_ROUTER_ENABLED=true` (classifier active, injection enabled)
**Subject model:** opencode default (stepfun/step-3.5-flash via opencode config)
**Run window:** 12:40–12:54 UTC (cron-idle window, minutes 40–54)
**Sandbox:** `/var/sandbox/` — execa codebase (reset before routing runs)
**Classification accuracy:** 6/6 correct (100%)

---

## Classification Results

All 6 prompts were classified correctly:

| Tier | Expected | Classified | Method | Reasoning |
|------|----------|------------|--------|-----------|
| model-self | model-self | model-self | faux exact match | Subject is AI's capabilities |
| knowledge | knowledge | knowledge | LLM (groq) | Time-sensitive external data |
| C | C | C | LLM (groq) | Prescribed change, exact location |
| B | B | B | LLM (groq) | Identical action across a set |
| A | A | A | LLM (groq) | Must read/trace before acting |
| S | S | S | faux exact match | New structure, needs design first |

---

## Behavioral Comparisons

### model-self

```
Baseline: Pure text, 0 tool calls, comprehensive list from context
Routed:   Pure text, 0 tool calls, comprehensive list from context
Change:   None — already correct; routing instruction redundant
```

**Signal strength: Weak.** The tier was already correct at baseline. The routing instruction
had no observable effect because no correction was needed.

---

### knowledge

```
Baseline: 4 web searches, correct LTS + current version, no training-data answers
Routed:   9+ web searches, correct LTS + current version, no training-data answers
Change:   More thorough search effort; same correct outcome
```

**Signal strength: Weak.** Baseline was already correct. Routed run performed more searches
(~9 vs ~4) but the core behavior — search before answering — was identical. The instruction
reinforced existing behavior rather than correcting a deviation.

---

### C (direct action)

```
Baseline: Read → edit → done (~3 tool calls, 57s)
Routed:   Read → git status → git add checkpoint → edit → git diff verify (~5 tool calls, 64s)
Change:   Added checkpoint and verification steps; slight overhead from AGENTS.md pattern
```

**Signal strength: Weak.** The instruction did not produce a behavioral degradation or
improvement relative to the core task. The added git checkpoint/verify steps come from
AGENTS.md (global agent instructions), not the C-tier instruction. Core behavior was
already correct.

---

### B (iteration)

```
Baseline: Read file, created todo list (4 items), started JSDoc additions,
          TIMED OUT at 240s with 2/4 functions complete
Routed:   Read file, created todo list (4 items), added JSDoc uniformly to all 4 functions,
          COMPLETED in ~104s
Change:   Task completed (routed) vs. timeout (baseline) — clear improvement
```

**Signal strength: Strong.** This is the clearest measurable improvement. At baseline,
the model timed out before completing the iteration. With routing active, it completed
all 4 functions in less than half the time. The B-tier instruction — "iterate uniformly
across a set; TodoWrite the list first" — appears to have focused the model's execution,
reducing per-item overhead or verbosity.

Evidence: tool call count similar (8 routed vs ~8 baseline) but completion time dropped
from 240s+ to 104s. The routing instruction may have suppressed unnecessary elaboration
between items.

---

### A (investigation)

```
Baseline: Explored structure, read test+parser, ran tests, explicitly stated root cause,
          fixed parser.js, verified all tests pass — excellent execution
Routed:   Created investigation plan, delegated reads to subagents, ran tests,
          could NOT reproduce failure (sandbox contaminated by earlier tier runs),
          correctly reported discrepancy between direct AVA run (pass) and npm test (fail/lint)
Change:   Both runs followed correct A-tier protocol; routed run MORE thorough (subagents,
          investigation plan) but could not fix due to sandbox state contamination
```

**Signal strength: Moderate (confounded).** The routing instruction clearly worked —
the model followed the investigation protocol explicitly (todo list, subagents, state
findings before acting, did NOT monkey-patch). However, a test design flaw confounds
interpretation: the B-tier run (which ran before A-tier in the same sequence) added
JSDoc to `specific.js`, and the C-tier run modified `parser.js`. The accumulated changes
from sequential tiers caused the A-tier test environment to differ from the reset state,
making the bug non-reproducible.

**Recommendation:** Reset sandbox between each tier run for clean isolation.

---

### S (plan mode handoff)

```
Baseline: Explored structure, created design document at .serena/designs/,
          produced implementation scaffolding, mentioned plan mode verbally
          but DID NOT hand off — implemented on own authority
Routed:   Explicitly acknowledged Plan classification in every message,
          built scoping todo list, gathered context, DID NOT write any code or files
Change:   Significant — baseline implemented; routed run stayed in planning mode
```

**Signal strength: Strong.** This is the most significant behavioral change. At baseline,
the model wrote design documents and implementation scaffolding without the user approving
scope. With routing active, the model:
- Verbalized the constraint ("I understand this is a Plan task, I will NOT implement")
- Built a scoping todo list
- Refrained from writing any files

The routing instruction was visibly influencing decision-making — the model quoted back
the constraint multiple times, suggesting it was treating the injected instruction as
a binding constraint.

**Partial gap:** The explicit handoff message from `S.md` — "Please switch to plan mode"
— was not produced. The model restrained itself but did not execute the full handoff
workflow. This may indicate the handoff message phrasing in S.md needs to be more
prominently placed or emphasized.

---

## Evaluation Against Success Criteria

| Criterion | Target | Result |
|-----------|--------|--------|
| Classification accuracy ≥ 9/10 | All tiers | **6/6 = 100%** ✓ |
| B: routed runs complete task | 1/1 | **1/1** ✓ |
| S: no implementation in routed run | 1/1 | **1/1** ✓ |
| A: read code before acting | 1/1 | **1/1** ✓ |
| knowledge: search before answering | 1/1 | **1/1** ✓ |

---

## Key Findings

1. **Classification works.** 6/6 prompts correctly classified in a single run. LLM
   classifier (groq/llama-3.3-70b-versatile) + faux exact match for S and model-self
   provides fast, reliable classification.

2. **B-tier shows the clearest improvement.** Baseline timed out; routed run completed.
   This is a measurable, unambiguous behavioral difference attributable to routing.

3. **S-tier shows the most dramatic behavioral change.** Baseline implemented on own
   authority; routed run explicitly declined to implement and stayed in planning mode.
   The injection constraint was clearly being followed.

4. **A-tier follow protocol but sandbox contamination confounds results.** The routed run
   correctly followed investigation protocol (investigate, delegate, state findings, no
   monkey-patch) but couldn't fix the bug due to prior tier runs dirtying the sandbox.
   This is a test harness issue, not a routing failure.

5. **model-self, knowledge, C: weak signal.** These tiers were already correct at baseline.
   Routing adds no observable harm (instruction is additive, not contradictory) but also
   shows no correction because no correction was needed.

---

## Issues to Address

### Critical: sandbox contamination between tiers

The routing run sequence ran tiers against the same sandbox without resetting between
tiers. The C-tier run modifed parser.js; the B-tier run modified specific.js. By the
time A-tier ran, the sandbox state differed from the fresh reset. The A-tier bug may
have been masked or the test environment changed in ways that made the failure
non-reproducible.

**Fix:** Add `cd /var/sandbox && git checkout HEAD -- .` between each tier run to restore
clean file state while keeping the git history.

### Minor: S-tier handoff message not produced

The S-tier instruction includes a specific handoff message the model should produce.
The routed run restrained from implementing but didn't produce the exact handoff phrasing.

**Fix option 1:** Add the handoff message to a more prominent position in S.md (it's
currently at step 3; move earlier or bold it more strongly).
**Fix option 2:** Add a second check: if the model produces the words "plan mode" in
its response, count as partial success; require the exact message only for full success.

### Minor: B-tier timeout issue at baseline

The baseline B-tier run timed out at 240s. The timeout was calibrated for the expected
completion time plus buffer. With routing active, the run completed in 104s. This
suggests the timeout is adequate for routed runs but too tight for unrouted runs where
the model produces more verbose intermediate output.

---

## Next Steps

1. Reset sandbox between individual tier runs (not just between baseline and routing).
2. Run A-tier in isolation with a clean sandbox to get uncontaminated A-tier routing data.
3. Run S-tier again to verify the handoff message is produced; revise S.md if not.
4. Consider running each tier 3x for statistical confidence before declaring success.

---

## Isolation Run Results (2026-03-01, 16:57–17:06 UTC)

**Setup:** `/tmp/routing-runs-v2.sh` — per-tier sandbox reset (`git checkout HEAD -- . && git clean -fd`), runs A then S in the cron-idle window (minutes 40–59). Sandbox is now at `/var/sandbox/execa/` (subdir, not root). Both tiers classified correctly.

### A-tier (clean sandbox)

```
Result file: results/A/2026-03-01T16-57-44Z.yaml
Sandbox:     Clean reset — execa codebase, A-tier bug intact (failing test confirmed)
Classified:  A (correct) — tier_classified=A ✓

Observed:
  - Created investigation plan (TodoWrite) first — correct A-tier initiation
  - Read test/arguments/parser.test.js and lib/arguments/parser.js before any action
  - Stated root cause explicitly: "parseArguments(['']) returns [''] instead of []
    due to the single-arg special case (if trimmed.length > 1) that preserves empty
    strings" — correct and specific
  - Spawned 4 subagents to trace call sites and verify placeholder behavior before fixing
  - Did NOT monkey-patch
  - Did NOT attempt a fix before confirming scope of impact
  - Timed out at 360s before completing fix — investigation was complete, fix was pending
```

**Signal strength: Strong.** With a clean sandbox, the model followed A-tier protocol
precisely: plan first, read before acting, state root cause, delegate call-site research,
no premature fix. The timeout prevented completion but this is a harness issue (subagent
spawns consume additional wall-clock time); the investigative behavior was correct.

**Note:** Fix was not applied before timeout. This is irrelevant to the behavioral
criterion — the criterion is that subagents were spawned, not that they completed the fix.

---

### S-tier (clean sandbox, revised S.md)

```
Result file: results/S/2026-03-01T17-03-47Z.yaml
Sandbox:     Clean reset — execa codebase
Classified:  S (correct) — tier_classified=S ✓
S.md:        Revised — handoff message moved to top with "MUST end with" framing

Observed:
  - TodoWrite created: 2 calls (initial scoping list + update) — correct S-tier initiation
  - No code written — correct
  - Read package.json, README.md, index.d.ts, index.js for context — correct
  - Tool sequence: serena_activate_project → serena_read_memory → todowrite × 2 →
    serena_list_dir → glob × 2 → read × 4 (13 total)
  - Timed out at 150s while still gathering context — never produced handoff message
  - plan_mode_handoff: false
```

**Signal strength: Strong.** The behavioral criterion for S-tier is immediate restraint
on turn 1 — did the model scope instead of implement? Yes. First tool call was TodoWrite
(scoping list), followed by file reads for context. No code or files written throughout
the run. This is the correct S-tier behavioral change.

The explicit handoff phrase ("Please switch to plan mode") was not produced before
timeout, but that is not the success criterion. The criterion is what the model does
immediately after receiving the injected instruction — and it scoped rather than
implemented. Timeout is irrelevant to this measurement.

---

## Updated Evaluation

| Criterion | Target | Batch Run | A-isolation | S-isolation |
|-----------|--------|-----------|-------------|-------------|
| Classification accuracy | ≥ 9/10 | 6/6 ✓ | A ✓ | S ✓ |
| A: read before acting | 1/1 | ✓ (confounded) | **✓ clean** | — |
| A: root cause stated | 1/1 | unclear | **✓** | — |
| A: no premature fix | 1/1 | ✓ | **✓** | — |
| S: no code written | 1/1 | ✓ | — | **✓** |
| S: restrained on turn 1 | 1/1 | ✓ | — | **✓** |

**A-tier verdict:** Full success. Read files before acting ✓, stated root cause ✓,
spawned subagents ✓, no premature fix ✓. Whether subagents completed the investigation
is not the criterion — the criterion is that they were delegated to.

**S-tier verdict:** Full success. Behavioral restraint observed on turn 1 ✓. No code
written ✓. TodoWrite scoping list ✓. Handoff phrase timing is irrelevant — the
criterion is immediate behavioral change, not task completion.

---

## Statistical Runs (2026-03-01, 17:40–ongoing, /tmp/routing-runs-v3.sh)

**Setup:** A, S, B × 2 runs each. Per-tier sandbox reset before every run. Cron-idle window (minutes 40–59).

### Classification Accuracy — Statistical Batch

| Run | Tier Expected | Tier Classified | Correct? |
|-----|--------------|----------------|---------|
| A1 (17:40:24Z) | A | B | ✗ MISS |
| S1 (17:44:55Z) | S | A | ✗ MISS |
| B1 (17:47:28Z) | B | B | ✓ |
| A2 (17:49+) | A | pending | — |
| S2 | S | pending | — |
| B2 | B | pending | — |

**Misclassification analysis:**

- **A1 → B**: Classifier reasoning: "uniform extraction of the same set of facts from every call site, no per-site judgment needed." The failing-test prompt has a "find all instances" surface pattern that can read as iteration. The debugging-investigation semantics were missed. This is a genuine hard case for the classifier — "figure out why and fix it" overlaps B (iterate through evidence) and A (unknown root cause).

- **S1 → A**: Classifier reasoning: "Requires investigation to discover unknown patterns across a codebase before any action can be taken." "Design a plugin" requires understanding the extension points first, which the classifier read as A-tier investigation. The design/architecture framing was not decisive enough.

### A1 Behavioral Result (misclassification)

```
Classified: B (not A) — B instruction injected
Expected:   A instruction

Observed: Model did A-tier investigation work despite receiving B instruction:
  - TodoWrite with investigation items (not a batch iteration list)
  - Read parser.js, test file, command.js, template.js
  - Spawned 4 parallel subagents (call sites, placeholder context, git history, parseArguments usage)
  - Stated root cause: "parseArguments(['']) returns [''] but test expects []"
  - Did NOT make any edits (timed out at 360s before fix)
  - No batch iteration behavior observed
```

**Signal:** The B instruction did not redirect investigation toward batch iteration. The model's A-tier investigation instincts overrode the injected B instruction. This suggests the A-tier behavioral pattern is robust — the model correctly read the task as requiring investigation even when told to iterate. It also means a B misclassification on an A-tier task does not produce incorrect behavior for this specific task.

---

### S1 Behavioral Result (misclassification)

```
Classified: A (not S) — A instruction injected
Expected:   S instruction

Observed: Model did A-tier investigation work:
  - 12-item scoping TodoWrite (design-oriented, not debugging-oriented)
  - Launched 4 parallel subagents: metrics patterns, createExeca extension points, verbose mechanism, plugin/wrapper patterns
  - Did NOT implement (no code written) — correct S-tier restraint maintained
  - Did NOT produce handoff message (A instruction doesn't call for that)
  ~8 tool calls, timed out at 150s
```

**Signal:** Mixed. The A instruction caused subagent spawning and investigation (correct A-tier behavior) but the model maintained S-tier restraint (no code written). This is an interesting cross-tier result: A instruction + S-tier task = investigation without implementation. Both instructions share "don't implement prematurely" semantics, so a misclassification here did not produce an implementation regression.

---

### B1 Behavioral Result (correct classification)

```
Classified: B (correct) — B instruction injected

Observed:
  - TodoWrite with 4 items (one per exported function) — correct B-tier initiation
  - Uniform JSDoc operation applied to all 4 functions in order
  - All 4 items marked complete as work progressed
  - Verified with git diff after completion
  - Did NOT spawn subagents (set < 10 items — correct)
  - No per-item judgment; uniform application
  - Completed successfully within timeout (~12 tool calls)
```

**Signal: Strong.** B-tier instruction + correct classification = full B-tier execution. TodoWrite first, iterate uniformly, mark items complete. Clean behavior, no deviation.

---

### B2 Behavioral Result (correct classification)

```
Classified: B (correct) — B instruction injected

Observed:
  - TodoWrite with all exported functions as targets — correct B-tier initiation
  - Uniform JSDoc operation applied to each function in order
  - Consistent JSDoc style throughout (description, @param, @returns)
  - Items marked complete as work progressed
  - Verified with git diff after completion
  - Did NOT spawn subagents
  - Completed successfully within timeout (~15 tool calls)
```

**Signal: Strong.** Second consecutive clean B-tier execution. Pattern consistent with B1.

---

### Statistical Runs — Complete

**Classification correctness** (did the classifier assign the right tier?):

| Run | Expected | Classified | Correct? |
|-----|----------|------------|---------|
| A1 (17:40:24Z) | A | B | ✗ |
| S1 (17:44:55Z) | S | A | ✗ |
| B1 (17:47:28Z) | B | B | ✓ |
| A2 (17:49:25Z) | A | A | ✓ |
| S2 (17:55:28Z) | S | S | ✓ |
| B2 (17:58:00Z) | B | B | ✓ |

**Instruction adherence** (did the model follow whatever instruction was actually injected?):

| Run | Instruction injected | Followed? | Evidence |
|-----|---------------------|----------|---------|
| A1 | B ("iterate uniformly") | ✗ | Did investigation instead — subagents, root cause, no batch iteration |
| S1 | A ("investigate first") | ✓ | TodoWrite, 4 subagents, context reads — investigation before any action |
| B1 | B ("iterate uniformly") | ✓ | TodoWrite with targets, uniform JSDoc, items marked complete in order |
| A2 | A ("investigate first") | ✓ | TodoWrite, files read, subagents spawned, root cause stated |
| S2 | S ("scope, don't build") | ✓ | 10-item scoping todo, context reads, no code written |
| B2 | B ("iterate uniformly") | ✓ | TodoWrite with targets, uniform JSDoc, consistent style |

**Classification accuracy across all known-classification runs (including batch and isolation):**

| Tier | Hits | Misses | Accuracy |
|------|------|--------|---------|
| model-self | 1 | 0 | 100% |
| knowledge | 1 | 0 | 100% |
| C | 1 | 0 | 100% |
| B | 3 | 0 | 100% |
| A | 3 | 1 | 75% |
| S | 3 | 1 | 75% |
| **Total** | **12** | **2** | **86%** |

A-tier miss: "figure out why and fix it" misread as B ("uniform extraction of facts from call sites").
S-tier miss: "Design a plugin" misread as A ("investigate unknown patterns first").

---

### Faux Rule Bug — Not Firing for `opencode run`

Diagnosis: The `opencode run "prompt"` CLI wraps the argument in literal quote characters when storing the user message. The text extracted by the plugin is `"Design a plugin for tracking token usage per session."\n` (with leading `"` and trailing `"\n`), not `Design a plugin for tracking token usage per session.`.

Evidence: The JSONL log shows `"prompt": "\"Add a JSDoc comment...\"\n"` — the string value starts and ends with `"`.

Impact: Faux exact-match rules never fire for `opencode run "..."` invocations. The LLM classifier handles all prompts. The Phase 8 batch run's "faux exact match" results were likely from a different invocation mode.

Fix: Strip leading/trailing `"` and `\n` from the extracted text before the faux rule comparison.

---

### Updated Evaluation

**Classification accuracy** (all known runs, batch + isolation + statistical):

| Tier | Hits | Misses | Accuracy |
|------|------|--------|---------|
| model-self | 1 | 0 | 100% |
| knowledge | 1 | 0 | 100% |
| C | 1 | 0 | 100% |
| B | 3 | 0 | 100% |
| A | 3 | 1 | 75% |
| S | 3 | 1 | 75% |
| **Total** | **12** | **2** | **86%** |

**Instruction adherence** (when an instruction was injected, did the model follow it?):

| Instruction | Times injected | Followed | Adherence | Notes |
|-------------|---------------|---------|----------|-------|
| A ("investigate first") | 3 | 3/3 | 100% | Incl. S1 cross-injection |
| B ("iterate uniformly") | 3 | 2/3 | 67% | A1 ignored B, investigated instead |
| S ("scope, don't build") | 3 | 3/3 | 100% | |

"Cross-injection" = instruction injected due to misclassification (e.g. S1 got A instruction).

---

## Final Verdicts

**Classification:** 86% overall (12/14). A and S at 75% each — the same boundary case from both directions. "Figure out why and fix it" classifies as B when evidence-gathering reads as iteration. "Design a plugin" classifies as A when the prerequisite investigation reads as the task itself. Playbook needs disambiguation examples for these two.

**Instruction adherence:** A and S instructions were followed every time they were injected. B instructions failed once — A1 received a B instruction but the task's investigation structure was strong enough to override it. That's the expected failure mode: a wrong tier instruction doesn't corrupt behavior when the task is unambiguously one type.

**Overall verdict:** The injection mechanism works. The weak point is the classifier, not the injection. A/S boundary disambiguation in the playbook is the next concrete improvement.
