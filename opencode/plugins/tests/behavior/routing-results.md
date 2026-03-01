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

**Gap:** Fix was not applied. Two options: (1) increase A-tier timeout to 480–600s to
allow subagent round-trips; (2) discourage subagent spawning in A.md in favor of
sequential self-investigation (faster but less thorough).

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

**Signal strength: Moderate.** The primary success criterion (no implementation) is met.
The model correctly restrained from writing code and was building a scoping context.
However, the explicit handoff message was not produced within the 150s timeout.

**Root cause of timeout:** Serena initialization consumes ~30s of the budget (3 serena
calls before any task work). With 13 total tool calls at 150s, each call averages ~11s
including model thinking time. The model needs ~20+ tool calls to gather full context
and produce the handoff — well beyond what 150s allows.

**Options:**
1. Increase S-tier timeout to 240s.
2. Suppress serena in S.md: "Do not use serena or activate-project; read files directly."
3. Make the handoff message the first output (before any tool calls), then continue
   gathering context. This inverts the scoping workflow but guarantees the criterion is met.

---

## Updated Evaluation

| Criterion | Target | Batch Run | A-isolation | S-isolation |
|-----------|--------|-----------|-------------|-------------|
| Classification accuracy | ≥ 9/10 | 6/6 ✓ | A ✓ | S ✓ |
| A: read before acting | 1/1 | ✓ (confounded) | **✓ clean** | — |
| A: root cause stated | 1/1 | unclear | **✓** | — |
| A: no premature fix | 1/1 | ✓ | **✓** | — |
| S: no code written | 1/1 | ✓ | — | **✓** |
| S: handoff message | 1/1 | ✗ | — | **✗** |

**A-tier verdict:** Investigation protocol is correct. Timeout prevents fix completion.
Increase timeout or reduce subagent spawning.

**S-tier verdict:** Restraint is working. Handoff message not produced due to timeout.
Increase budget or restructure instruction to emit handoff earlier.
