# Task Plugin Gaps

Date: 2026-03-05
Scope: `/home/dzack/ai/opencode/plugins/task.ts` and async agent infrastructure

---

## Current Status

**Sync Agents:** Working well, feature parity achieved. Need improvements only.

**Async Agents:** Core functionality works well.

**TUI Visibility Status:** Session linking and tool-count/duration updates are working at upstream parity. Remaining visibility gap is MCP current-operation naming when title is empty in upstream MCP wrapper output.

---

## Contract Clarifications (Authoritative)

1. **Async launch lifecycle is tool-response-first, not callback-first**
   - The initial `task` tool call starts the child session and performs launch verification up to and including `running`.
   - The `running` status is returned as the tool call result.
   - Launch success must not emit a separate callback. A callback that says "tool started" is redundant and wrong.

2. **Callback channel is only for true async updates**
   - Callbacks are reserved for background updates after the tool already returned.
   - Required callback classes are:
     - tiny time-based heartbeat pings
     - terminal completion/error updates

3. **Heartbeats are liveness pings, not result forwarding**
   - Heartbeats fire on a fixed time cadence.
   - Heartbeats must stay minimal: current status plus a timestamp (or age) of last child activity/tool result.
   - Heartbeats must not forward child tool outputs/results to the parent.
   - Returning every child result defeats the context-savings goal of background delegation.

4. **Completion callback payload is transcript tail only**
   - There is no separate "agent response object" in this mode; callback content is constructed by plugin policy.
   - Completion callbacks should include only the last `N` lines from transcript tooling output.
   - Completion callbacks should include a transcript-followup hint for deeper inspection when needed.
   - Completion callbacks must not include full transcript dumps or reconstructed full-result payloads.

5. **Child-tool restriction note**
   - Child-tool restrictions are already handled globally by subagent permissions and are not a local gap in this plugin doc.

6. **Running verification timeout scope**
   - Running verification timeout tuning is a developer/ops reliability concern.
   - It is not an agent-facing concept and should not appear as agent policy.

---

## Required Feature: Groq Results Enhancement

The subagent transcript must be fed to a Groq model with a large context window.

### Groq Model Outputs (Required)

1. **Turn-by-turn summary** - Concise, readable language summary of the agent's actions per turn. Must include time taken per step (extracted from transcript timestamps).

2. **Summarized final result** - A condensed version of the typically verbose final message the subagent gives.

3. **Completion confidence score** - Groq model compares the original prompt with the transcript and assigns a confidence score.

4. **Performance report** - Concise report flagging potential issues:
   - Provider errors or delays
   - Bad tool calls
   - Failed operations
   - Models hallucinating information
   - Models reward hacking or carrying out trivial operations to fulfill the letter of the law

5. **Total time taken**

6. **Link to transcript** - Pre-exported to a temp directory for review.

7. **Session ID and continuation message** - Message stating this subagent's session can be continued by doing XYZ.

8. **Git diff summary** - Summary of changes made within the subagent session.

### Groq Rubric Requirements

- The Groq agent needs a version-controlled external rubric prompt.
- The rubric must be testable in isolation.

### Subagent Return Payload

The return of the subagent call must include:
- Condensed turn-by-turn summary
- Summarized final result
- Performance confidence score
- Total time taken
- Concise performance report
- Link to transcript (pre-exported to temp dir)
- Session ID
- Continuation instructions (how to resume this session)
- Git diff summary

---

## Required Feature: Git Working Tree Provisioning

The subagent task must have a feature to automatically provision a git working tree and organize the subagent's work there.

**Purpose:**
- Managed and merged in by the main agent if desired
- Avoid using manual git manipulations like checkout or restore which can be destructive during concurrent work

---

## Remaining Gaps

### 1. MCP Current-Operation Naming in Task Display
- **Issue:** In task live display, MCP child tools often show only aggregate count (`N toolcalls`) instead of named current operation.
- **Cause (source-backed):**
  - Task renderer shows named current op only when child `state.title` is non-empty.
  - Processor copies `state.title` from tool output `title`.
  - MCP wrapper returns `title: ""`.
- **Scope:** Upstream/core behavior; plugin currently matches this behavior.
- **Testing:** Human TUI verification still required for end-to-end confirmation per phase gates.

### 2. Completion Fan-Out Under Concurrency
- Current behavior can still emit one terminal callback per finished task.
- If many tasks complete near the same time, parent turn churn can spike.
- **Improvement:** Optional per-parent completion coalescing that preserves concise terminal signals without merging full results.

### 3. No Delegation Index for Discovery/Recovery
- No local index mapping delegation names/descriptions → session IDs.
- Recovery relies on reading opencode's session database directly.
- **Note:** "Task IDs" are anachronistic. Session IDs are the unique keys for specific tasks.
- **Improvement:** Simple project-level index (`delegation_list`) for compact discovery without full transcript reads.

### 4. No Compaction Context Injection for Delegation State
- Plugin does not currently append running/recent delegation context in compaction flow.
- **Improvement target:** `experimental.session.compacting` context injection with retrieval hints.

### 5. Groq Enhancement Layer (Not Yet Implemented)
- See "Required Feature: Groq Results Enhancement" above.

### 6. Git Working Tree Provisioning (Not Yet Implemented)
- See "Required Feature: Git Working Tree Provisioning" above.

---

## Non-Gaps / Rejected Directions

1. **Callback "running started" notifications**
   - Rejected by contract. Launch verification belongs in initial tool result.

2. **Child result streaming to parent callbacks**
   - Rejected by contract. Heartbeats are for liveness, not child result transport.

3. **Agent-facing running-timeout semantics**
   - Rejected by contract. Timeout/retry tuning is implementation-side only.

---

## External Repo Observations (Adoption Cautions)

1. **Registry/package mapping inconsistency**
   - `registry.json` references files not present on `main` (`src/plugin/kdco-background-agents.ts`, missing skill path).
   - Validate mapping before direct adoption.

2. **Inline result payload pattern**
   - External repo sends substantial result payloads in notifications (`<result>...</result>`).
   - This conflicts with the context-saving contract for this plugin design.

---

## Suggested Next Actions

1. Keep launch verification entirely inside initial tool response and remove any launch-state callbacks.
2. Enforce fixed-cadence, minimal heartbeat payload shape (status + last-activity timestamp only).
3. Enforce completion callbacks as transcript-tail-only plus transcript-followup hint.
4. Add delegation index and compaction injection for robust recovery after compaction/restart.
5. Track upstream MCP title handling change separately from plugin logic if named MCP current-operation display is required.
6. Implement Groq results enhancement (see spec above).
7. Implement git working tree provisioning (see spec above).
