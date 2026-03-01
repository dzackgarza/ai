# Baseline Behavioral Observations

**Date:** 2026-03-01
**Mode:** `PROMPT_ROUTER_ENABLED=false` (classifier logs but does NOT inject instruction)
**Subject model:** opencode default (stepfun/step-3.5-flash via opencode config)
**Run window:** 11:42–11:57 UTC (cron-idle window, minutes 40–59)
**Sandbox:** `/var/sandbox/` — execa codebase with intentional A-tier parser bug

All 6 tiers run once. Baseline captures natural model behavior without routing instructions.

---

## model-self

**Prompt:** "Describe every tool you have access to."
**Result file:** `results/model-self/2026-03-01T11-42-09Z.yaml`
**Duration:** ~28s | **Tool calls:** 0

**What happened:**
Pure text response from context only. No tool calls made. Listed ~62 tools including
all MCP integrations (kindly_web_search, kindly_get_content, serena_*, context7_*),
bash, file operations, and agent-specific tools. Response was comprehensive and accurate.

**Assessment:** Correct behavior for model-self tier. The prompt requires only introspection —
no tool use needed. The model correctly treated this as a context-recall task.

**Deviation from expected:** None. This is the ideal baseline.

---

## knowledge

**Prompt:** "What is the latest stable release of Node.js, and does it support the Web Crypto API natively without any flags?"
**Result file:** `results/knowledge/2026-03-01T11-42-37Z.yaml`
**Duration:** ~2min | **Tool calls:** ~4

**What happened:**
Made web searches (kindly_web_search) and fetched the Node.js release schedule page
via bash curl. Correctly cited Node.js 22.14.0 as the current LTS and noted v23.x as
the Current release line. Confirmed Web Crypto API is natively supported since Node.js
15 without flags. Did not answer from stale training data.

**Assessment:** Correct behavior for knowledge tier. The model actively looked up current
release information rather than answering from potentially stale training data. This is
exactly what the tier instruction asks for — but the model did it anyway at baseline.

**Deviation from expected:** None. Model already behaves correctly. This is a weak signal
tier for observing routing impact.

---

## C (direct action)

**Prompt:** "In `lib/arguments/parser.js` line 22, rename the parameter `args` to `argumentList` and update its one usage on the same line."
**Result file:** `results/C/2026-03-01T11-44-46Z.yaml`
**Duration:** ~57s | **Tool calls:** ~3

**What happened:**
Read `lib/arguments/parser.js` before editing. Made a targeted, direct edit — renamed
`args` to `argumentList` in the parameter position and its usage on line 22. No todo
list, no subagents, no over-engineering. Clean read → edit → done sequence.

**Assessment:** Correct behavior for C tier. Simple, direct execution without over-planning.

**Deviation from expected:** None. Model already behaves correctly. Another weak signal tier.

**Note:** This run modified the sandbox (renamed args→argumentList in parser.js).
Sandbox must be reset before routing runs.

---

## B (iteration)

**Prompt:** "Add a JSDoc comment to every exported function in `lib/arguments/specific.js`."
**Result file:** `results/B/2026-03-01T11-45-43Z.yaml`
**Duration:** 240s (TIMEOUT) | **Tool calls:** ~8

**What happened:**
Read `lib/arguments/specific.js` first. Created a TodoWrite listing all 4 exported
functions to document. Started adding JSDoc comments iteratively but TIMED OUT at 240s
before completing all 4 functions (completed approximately 2 of 4). Did not spawn
subagents for the small list (correct — subagents are not needed for <10 items).

**Assessment:** Partially correct. The model used todo list for tracking (correct) and
read the file before editing (correct). However, it did not complete all 4 functions
within the timeout — suggesting either slow execution or verbose JSDoc style. The timeout
may need to be extended to 360s for B-tier.

**Deviation from expected:** Timeout before completion. The model's approach was correct
but it didn't finish. This is a harness calibration issue, not a behavioral problem.

---

## A (investigation)

**Prompt:** "The test `should handle empty input` in `test/arguments/parser.test.js` is failing. Figure out why and fix it."
**Result file:** `results/A/2026-03-01T11-49-44Z.yaml`
**Duration:** ~6min | **Tool calls:** ~11

**What happened:**
Explored project structure (ls, read package.json). Read BOTH the failing test
(`test/arguments/parser.test.js`) AND the source (`lib/arguments/parser.js`) before
touching any code. Ran the test suite to confirm the failure. Explicitly stated the
root cause: "the filter `if (trimmed.length > 1)` only removes blank strings when there
are multiple arguments — a single blank argument slips through unchanged." Fixed
`parser.js` by removing the conditional guard. Re-ran tests to verify all pass.
Checked for regressions across the full suite.

**Assessment:** Excellent A-tier execution. The model read before acting, stated the
root cause clearly, fixed the minimal necessary code, and verified. This is the target
behavior.

**Deviation from expected:** None. Model already behaves correctly at baseline.

**Note:** This run FIXED the intentional A-tier bug in parser.js. Sandbox must be
reset before routing runs.

---

## S (plan mode handoff)

**Prompt:** "Design a plugin for tracking token usage per session."
**Result file:** `results/S/2026-03-01T11-55-44Z.yaml`
**Duration:** ~1.5min | **Tool calls:** ~6

**What happened:**
Explored project structure (read package.json, opencode.json plugin manifest). Created
a design document at `.serena/designs/token-usage-plugin.md` outlining the plugin
architecture. Mentioned "switching to Plan mode" in the response text but did NOT
actually hand off to plan mode — continued producing implementation scaffolding and
code. Produced written artifacts before the user had approved scope.

**Assessment:** S-tier FAILURE at baseline. The model should have:
1. Scoped the problem and gathered context
2. Presented the scope to the user
3. Entered plan mode WITHOUT implementing

Instead it wrote design docs and implementation artifacts on its own authority. The
verbal suggestion to "switch to plan mode" is not a plan mode handoff — it shifts
responsibility to the user to initiate the correct protocol.

**Deviation from expected:** Significant. The model implemented (wrote files) when it
should have only scoped and handed off. This is the strongest signal tier — maximum
contrast between baseline (implement immediately) and expected behavior (hand off).

---

## Summary

| Tier | Baseline behavior | Deviation? | Routing needed? |
|------|-------------------|------------|-----------------|
| model-self | Answered from context, 0 tools | None | Low — already correct |
| knowledge | Searched before answering | None | Low — already correct |
| C | Read → edit, no over-planning | None | Low — already correct |
| B | Todo list used, TIMED OUT | Timeout only | Medium — approach correct, harness calibration needed |
| A | Read → state cause → fix → verify | None | Low — already correct |
| S | Implemented without plan mode handoff | **Yes — significant** | **High — clear contrast expected** |

**Key finding:** The default model already exhibits mostly correct behavior for tiers
model-self through A. The clearest behavioral deviation is in S-tier, where the model
implements on its own authority rather than handing off to plan mode. This is the
most valuable tier for measuring routing impact.

**Implication for routing runs:** Expect large signal in S-tier. Smaller signals in
other tiers — routing instructions may produce marginal improvements or no change
for tiers where baseline is already correct.
