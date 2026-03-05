# Async TUI Observability Plan (Phase 0 + Two Phases, Gated)

## 1. Purpose

Define a strict gated plan for async `task` behavior, with human-in-the-loop TUI verification at the end of each phase.

This plan explicitly separates:

1. Phase 0: exact upstream `task` tool shadowing (same core lifecycle contract, no reinvention)
2. Session-management correctness (child session registration + navigability + live child session visibility)
3. Parent task-tool display refinement (incremental summary updates such as tool-call counts)

No Phase 1 work is allowed before Phase 0 is human-verified. No Phase 2 work is allowed before Phase 1 is human-verified.

---

## 2. Problem Statement

Current async behavior has mixed concerns:

- Session lifecycle wiring
- Parent tool-part lifecycle emulation
- UI-display mutation attempts

These concerns must be decoupled. The first objective is reliable native session-tree integration. Display embellishments are secondary.

---

## 3. Non-Negotiable Constraints

0. **Hard requirement**: Do not reinvent anything the upstream native `task` tool already does. Shadow upstream behavior and hook into existing core lifecycle functionality.

1. Sync and async must share the same child-session registration pathway.
2. Async must differ from sync only by dispatch semantics:
   - sync: await child prompt completion
   - async: fire-and-forget child prompt (do not await)
3. Phase 0 must establish upstream-equivalent `task` contract usage (metadata + return shape + lifecycle handoff to core).
4. Phase 1 must not include parent tool-part lifecycle emulation.
5. Phase 2 must not alter session-tree management behavior established in Phase 1.
6. Human verification in actual TUI is the gate for each phase.
7. Service restart is mandatory after each phase implementation cycle: restart `opencode-serve` before phase-gate verification.
8. No fallback logic in green-field phase-contract code paths. Contract violations must fail fast and be fixed at the source.

---

## 4. Phase 0 (Upstream Shadowing) - Required First Gate

### 4.1 Scope

Match upstream native `task` behavior exactly where core lifecycle ownership is concerned:

- Child-session creation/reuse semantics
- `context.metadata(...)` contract usage expected by core
- Tool return contract compatible with existing core `task` lifecycle expectations
- No custom parent tool-part state machine

### 4.2 Explicitly Out of Scope

- Any custom parent tool-part patching/mutation logic
- Any custom lifecycle reopening/restarting logic
- Any UI-specific hacks that bypass native task lifecycle handling

### 4.3 Implementation Directives

1. Read upstream `task` tool source and document the exact lifecycle contract.
2. Align plugin `task` integration to that contract exactly.
3. Confirm child-session linkage and metadata fields are emitted in the same shape expected by core/TUI.
4. Preserve metadata/title flow through core hooks only (for plugin tools: `context.metadata(...)` + `tool.execute.after` output metadata/title hydration if needed by plugin bridge behavior).
5. Remove/forbid any custom parent-part lifecycle manager logic.

### 4.3.2 Current Sync Shadow + Hook Contract (MUST NOT BREAK)

This is the baseline sync contract. It is immutable for Phase 0/1, except additive improvements to final returned text payload.

1. `tool.definition` hook:
   - refreshes task description from subagent cache/fetch path
   - must not block startup indefinitely
2. `task.execute` sync path:
   - validate subagent type
   - ask `task` permission via `context.ask(...)`
   - create/reuse child session with correct `parentID`
   - resolve model (subagent model preferred; parent-message model fallback)
   - register context through `context.metadata({ title, metadata: { sessionId, model } })`
   - run child with blocking `client.session.prompt(...)`
3. `tool.execute.after` hook (core hook surface only):
   - must hydrate completed task output `title` and `metadata.sessionId` (and `model` when available)
   - must not patch message parts directly
4. Core ownership boundary:
   - core/session processor owns tool-part lifecycle state transitions and TUI rendering behavior
   - plugin only supplies metadata/output through supported hook surfaces
5. Sync-path hard invariants:
   - no custom parent-part mutation loop
   - no lifecycle emulation
   - no alternate state machine for tool-part status
   - no fallback paths that mask contract mismatches (fail fast instead)

### 4.3.3 Sync Output Contract (Current)

Yes, there is a current output contract for sync path, but it is agent/transcript-facing only.
Programmatic sync/TUI linkage must use metadata contract via core hooks, not output parsing.

Required elements:

1. Parseable `task_id` line in output text (`task_id: <session_id> ...`).
2. `<task_result>` opening tag.
3. `</task_result>` closing tag.

Allowed improvements:

1. Add sections after `</task_result>` (for example summary blocks).
2. Extend output content without changing required keys/tags above.

Forbidden changes:

1. Removing/renaming `task_id`.
2. Removing or renaming `<task_result>` tags.
3. Making `task_id` non-parseable by existing hook logic.
4. Adding output-parsing fallbacks to recover missing programmatic metadata.

### 4.3.4 Recorded Regression Context (Root-Cause Guardrail)

- Symptom: parent task card can show `0 toolcalls · 0ms` even when child session did work.
- Root-cause class: plugin task output metadata/title not preserved in completed tool part as expected by TUI task renderer.
- Guardrail: solve via upstream-compatible contract and existing core hook surfaces only; do **not** patch parent tool parts directly.

### 4.4 Phase 0 Success Criteria

All must be true:

1. Plugin uses native core lifecycle path for task tool parts (no custom manager).
2. Parent tool part has the metadata fields required by TUI child-session resolution.
3. No manual parent-part patch loop is required for normal sync task observability.

### 4.5 Human Verification Gate (Required)

Human tester validates in TUI:

1. Run a sync `task`.
2. Confirm task card shows real child-session-derived metrics (not `0 toolcalls · 0ms` when child did work).
3. Confirm child session opens via native navigation and reflects the same work.

Gate decision:

- **PASS**: proceed to Phase 1
- **FAIL**: Phase 1 blocked; Phase 0 parity defects must be fixed first

### 4.6 Verification Record (2026-03-05)

Human TUI verification result: **PASS**.

Recorded outcome:

1. Sync task metrics are live and non-zero when child work occurs.
2. Tool-call activity is populated in the parent task display when child tools provide titles.
3. Child session navigation/observability behavior is correct for Phase 0 parity.

---

## 5. Phase 1 (Session Management Parity) - 90%

### 5.1 Scope

Implement only native session-management behavior for async tasks:

- Child session creation and parent linkage
- Child-session discoverability in session tree
- Live child session visibility via native navigation (`Ctrl+X` flows)
- Async callback messages to parent agent (heartbeat + terminal summary) for subscription context

### 5.2 Explicitly Out of Scope

- Parent tool-part status rewriting
- Parent tool-part running/completed state emulation
- Incremental parent tool metadata display tweaks (`N -> N+1` tool-call rendering)

### 5.3 Implementation Directives

1. Unify sync+async session initialization code path:
   - same `session.create` semantics
   - same parent linkage semantics
   - same `sessionId` metadata contract
2. Keep async dispatch non-blocking:
   - launch child prompt
   - return control immediately
3. Keep callback channel simple:
   - periodic heartbeat to parent agent
   - final completion/failure callback with static summary envelope
4. Define one final session-summary schema used by both sync and async terminal outputs.
5. Preserve verbose permanent logs for:
   - child session creation
   - parent-child linkage
   - prompt dispatch start/finish
   - child event receipt
   - heartbeat/final callback emission

### 5.4 Phase 1 Success Criteria

All must be true:

1. Child session consistently appears in native session tree.
2. Child session is navigable from parent via TUI shortcuts.
3. Child session displays live activity while running.
4. Async parent agent remains unblocked.
5. Final callback includes static terminal summary schema.

### 5.5 Human Verification Gate (Required)

Human tester validates in TUI:

1. Launch async task from parent.
2. Confirm immediate parent responsiveness.
3. Navigate to child session with native shortcuts.
4. Observe live child progression.
5. Return to parent and confirm heartbeat/final callback receipt.

Gate decision:

- **PASS**: proceed to Phase 2
- **FAIL**: Phase 2 blocked; Phase 1 defects must be fixed first

---

## 6. Phase 2 (Parent Tool Display Updates) - 10%

## 6.1 Precondition

Phase 0 and Phase 1 must both be marked PASS by human TUI verification.

### 6.2 Scope

Display-only enhancements to parent task tool representation, driven by child-session events:

- incremental summary updates (e.g., tool-call count)
- current child activity hints
- terminal summary alignment with shared schema

### 6.3 Implementation Directives

1. Do not change session-management logic from Phase 1.
2. Treat parent tool display as a rendering surface only.
3. Prefer minimal, robust update mechanism.
4. Avoid any attempt to reopen or semantically resurrect tool lifecycle.
5. Keep logs for every display update attempt and accepted/rejected UI effect.

### 6.4 Phase 2 Success Criteria

All must be true:

1. Parent tool display updates incrementally during async child execution.
2. Updates remain stable across navigation and refresh events.
3. Terminal displayed summary matches actual child session outcome.
4. Parent agent remains non-blocking throughout.

### 6.5 Human Verification Gate (Required)

Human tester validates in TUI:

1. Parent tool display starts with initial async state.
2. During child execution, parent display updates at least one incremental metric.
3. Terminal parent display matches child transcript/session summary.

Gate decision:

- **PASS**: finalize
- **FAIL**: iterate Phase 2 only; do not regress Phase 1 behavior

---

## 7. Deliverables

Phase 0 deliverables:

1. Source-level parity notes: upstream `task` contract vs plugin contract
2. Plugin aligned to native lifecycle ownership (no custom parent-part manager)
3. `opencode-serve` restart record (timestamp/status)
4. Human verification record (PASS/FAIL + notes)

Phase 1 deliverables:

1. Refactored async/sync lifecycle code with shared registration path
2. Permanent verbose logs for session-management observability
3. `opencode-serve` restart record (timestamp/status)
4. Human verification record (PASS/FAIL + notes)

Phase 2 deliverables:

1. Parent display update implementation
2. Permanent verbose logs for display-update observability
3. `opencode-serve` restart record (timestamp/status)
4. Human verification record (PASS/FAIL + notes)

---

## 8. Stop Conditions

Stop and escalate if any of the following occur:

1. Phase 1 cannot maintain native child-session navigability
2. Async callbacks interfere with parent turn stability
3. Phase 2 display updates require changing Phase 1 session-management behavior
4. Human verification contradicts logged behavior

---

## 9. Decision Rule

The implementation is accepted only if:

1. Phase 0 PASS (human verified in TUI)
2. Phase 1 PASS (human verified in TUI)
3. Phase 2 PASS (human verified in TUI)

No code-level argument substitutes for TUI verification at either gate.

---

## 10. Task ID vs Session Continuation Findings

This section records concrete findings from source inspection and local plugin implementation decisions.

### 10.1 Upstream `task` Tool Semantics (Source-Verified)

Upstream OpenCode native task tool:

1. Defines optional resume argument as `task_id` (not `session_id`) in task tool schema.
2. On execute:
   - if `task_id` exists and `Session.get(task_id)` succeeds, resume that session
   - otherwise create a new child session with `parentID = ctx.sessionID`
3. Sets task tool metadata via `ctx.metadata({ metadata: { sessionId, model } })`.

Primary upstream references:

1. `packages/opencode/src/tool/task.ts`
2. `packages/opencode/src/tool/task.txt`

### 10.2 What TUI Uses for Child Session Linking

TUI linkage for task/subagent navigation is driven by task-part metadata `sessionId`, not output text parsing of `task_id`.

Observed behavior in upstream TUI source:

1. Task component reads `props.metadata.sessionId`.
2. It calls `sync.session.sync(props.metadata.sessionId)` to hydrate child messages.
3. Tool-call counts and duration are computed from synced child-session messages.

Primary upstream reference:

1. `packages/opencode/src/cli/cmd/tui/routes/session/index.tsx` (Task tool renderer)

### 10.3 Output String Contract vs Core Lifecycle Contract

1. Upstream task output text includes `task_id: <session-id>` as agent-facing continuation guidance.
2. Core lifecycle integration (session tree registration + TUI child linking) is governed by:
   - child session creation/resume path
   - `context.metadata(... sessionId ...)`
   - core tool lifecycle machinery
3. Therefore, `task_id` in output is an agent-facing convention, not the session-linking mechanism.

### 10.4 Current Plugin Continuation Semantics

Current plugin decisions (implemented):

1. Resume input exposed to agents as `session_id` only.
2. Continuation logic is permissive:
   - if `session_id` resolves to an existing session, reuse it
   - else create a new child session with `parentID = context.sessionID`
3. Follow-up instructions now reference `session_id` continuation.

### 10.5 Compatibility Assessment

Assessment based on source inspection:

1. Replacing plugin-facing `task_id` argument with `session_id` does not inherently break TUI linking, provided metadata `sessionId` remains correct.
2. Upstream naming (`task_id`) remains the native convention in core docs/tool schema, but plugin shadowing can choose a different arg name.

### 10.6 Explicit Gaps / Inferences

For negative findings and limits of verification:

- Searched: `gh search code "task_id repo:anomalyco/opencode" --limit 100`; direct reads of:
  - `packages/opencode/src/tool/task.ts`
  - `packages/opencode/src/tool/task.txt`
  - `packages/opencode/src/cli/cmd/tui/routes/session/index.tsx`
- Found: No additional core path was identified that depends on parsing `task_id` from task output for TUI session linking.
- Conclusion: Based on limited evidence, it is likely safe to use `session_id` in plugin-facing schema/output while preserving native lifecycle hooks.
- Confidence: Medium-High.
- Gaps: No full upstream integration test suite run was performed here; human TUI verification remains required per phase gates.

### 10.7 MCP Tool Visibility Finding (Upstream Limitation, Not Plugin Regression)

Observed behavior:

1. In task live status, some child tools show as `↳ ToolName Title`, but MCP tools often fall back to `↳ N toolcalls`.
2. This is consistent with upstream core behavior.

Source-backed cause:

1. Task TUI renderer shows current operation only when a child tool part has non-empty `state.title`.
   - Reference: `packages/opencode/src/cli/cmd/tui/routes/session/index.tsx` (Task renderer logic).
2. Processor copies `state.title` from tool output `title`.
   - Reference: `packages/opencode/src/session/processor.ts` (`tool-result` handling).
3. MCP tool wrapper in prompt pipeline returns `title: ""` (empty string), while still returning output/metadata.
   - Reference: `packages/opencode/src/session/prompt.ts` (MCP tool wrapper return object).

Implication:

1. MCP tool calls are still counted/synced in child session data.
2. They commonly do not appear as named "current operation" lines because title is empty.
3. Built-in tools that return non-empty titles (for example many core tools) do show in current-operation display.

Conclusion:

1. Current plugin behavior is at upstream parity for this display characteristic.
2. Fixing MCP named-current-operation display requires upstream/core change (or explicit title synthesis policy), not a session-linking fix in this plugin.

### 10.8 Resumed Session Display Behavior (Observed)

Observed in TUI:

1. When a child session is resumed via another `task` invocation, each corresponding parent task component can reflect cumulative progress from the same child session.
2. This means parent-task feed history may show repeated/cumulative child-session progress snapshots rather than isolated per-invocation deltas.

Implication:

1. Parent task cards should be treated as session-progress views, not strict per-invocation execution ledgers, when multiple task entries target one resumed child session.

Mitigation adopted:

1. Transcript export now includes an explicit **Invocation Result Snapshot** section for the current task call.
2. This preserves top-level narrative reconstruction for delegation chains even when resumed-session UI cards are cumulative.

## 11. Current Phase Status (Working Baseline)

Status snapshot for current implementation:

1. **Phase 0 (Upstream Shadowing): PASS (human verified previously)**
   - Native task lifecycle contract preserved via core hooks:
     - `context.metadata(... sessionId ...)`
     - `tool.execute.after` metadata/title hydration
   - Child session registration and TUI navigation behavior preserved.

2. **Phase 1 (Async Session Management): IMPLEMENTED, pending human gate**
   - Async pathway is non-blocking and reuses sync terminal summary construction.
   - Sync pathway remains default and uses the same shared terminal summary builder.
   - Timeout handling is unified for sync/async and returns explicit `status: timeout` summaries (not generic execution errors), with transcript+resume guidance.

3. **Phase 2 (Parent Tool Part Display Refinements): NOT STARTED / BLOCKED BY GATE**
   - No Phase 2-specific parent tool-part emulation logic should be added before Phase 1 gate pass.

Operational guardrail now required:

1. Only one active `task` plugin implementation may be loaded at runtime.
2. Backup/reference files must not export a live `TaskPlugin` in `.ts` form.
