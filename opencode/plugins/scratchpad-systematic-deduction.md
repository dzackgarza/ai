# Systematic Deduction Scratchpad

## Problem Statement
Why do some plugins load and appear as tools in OpenCode while others don't, even though all compile successfully?

## Known Facts (Proven)
- F1: All 11 plugins compile successfully with `bun build` - (proven: build output)
- F2: All 11 plugins pass TypeScript type checking - (proven: tsc --noEmit)
- F3: Working tools (tested via `opencode run --agent Minimal`): mytool, sleep, introspection, list_sessions, read_transcript - (proven: test output)
- F4: Non-working tools: async_command, git_add, git_commit, write_plan, plan_exit - (proven: test output)
- F5: local-tools.ts uses re-export pattern: `export { PluginName } from "./dev/.../index.ts"` - (proven: file inspection)
- F6: Working plugins: SleepPlugin, IntrospectionPlugin, ListSessionsPlugin, ReadTranscriptPlugin all use `({ client })` context - (proven: code inspection)
- F7: Non-working plugins: GitAddPlugin, GitCommitPlugin use `({ $ })` context - (proven: code inspection)
- F8: WritePlanPlugin uses `async () => {}` with no context params - (proven: code inspection)
- F9: AsyncCommandPlugin uses `({ client })` but doesn't work - (proven: code inspection + test)
- F10: PlanExitPlugin uses `({ client })` but doesn't work - (proven: code inspection + test)
- F11: Minimal agent has restrictive permissions (bash, task, todoread, todowrite, external_directory, question) - (proven: opencode.json)
- F12: Interactive agent ALSO doesn't see git_add, async_command, write_plan - (proven: test output just now)
- F13: Interactive agent HAS git_add, git_commit in its permission config - (proven: opencode.json inspection)

## Hypotheses
| ID | Hypothesis | Status | Evidence For | Evidence Against |
|----|------------|--------|--------------|------------------|
| H1 | Plugins using `$` (shell) context don't load | eliminated | F7 shows git_add, git_commit use `$` | F9, F10: async_command, plan_exit use `client` not `$` but also don't work |
| H2 | Plugins with no context params don't load | active | F8: WritePlanPlugin has no params and doesn't work | Need to test other no-param plugins |
| H3 | Plugin re-export pattern is broken | active | All plugins compile but some don't appear | Some plugins DO work with same pattern |
| H4 | Minimal agent permissions filter tool visibility | active | F11 shows Minimal has very limited permissions | But sleep, introspection work despite not being in permission list |
| H5 | Plugins are loaded but agent can't see them due to permission gating | active | Agent says "I don't have X tool" for some | But agent DOES report having sleep, introspection |
| H6 | There's a runtime load order issue | speculation | - | No evidence either way |
| H7 | Plugin file location matters (dev/ subdirectory vs root) | speculation | - | All plugins are in dev/ subdirectory |

## Inferences
- I1: From F3 + F4 + F6 + F7 + F8: Context params alone don't determine loading (inferred: async_command uses client but fails)
- I2: From F3 + F5: Re-export pattern works for SOME plugins (inferred: sleep, introspection work)
- I3: From F9 + F10: Something distinguishes async_command/plan_exit/write_plan from sleep/introspection (inferred)

## Experiments
| ID | Experiment | Expected if H | Actual | Result |
|----|------------|---------------|--------|--------|
| E1 | Test each plugin individually by uncommenting one at a time | H3: Some load, some don't | Confirmed: 5 work, 5 don't | H3 SUPPORTED - pattern works selectively |
| E2 | Check if non-working plugins have different export signature | H2: Different signatures | Confirmed: write_plan has no params, git_* have `$` | H2 PARTIALLY SUPPORTED |
| E3 | Ask agent about tool availability with full permission agent | H4/H5: Different results with different agents | NOT RUN YET | INCONCLUSIVE |

## Eliminated Possibilities
- H1 (plugins using `$` don't load) - ELIMINATED: async_command and plan_exit use `client` not `$` but also don't work

## Current Best Explanation
Combination of H2 + H4 + H5: 
- WritePlanPlugin has no context params - may fail to initialize
- GitAddPlugin, GitCommitPlugin use `$` which may not be available at plugin load time
- Minimal agent permissions may filter which tools are visible to the agent

## Open Questions
- What context params are REQUIRED for a plugin to load?
- Does the Minimal agent's permission config affect tool VISIBILITY or tool EXECUTION?
- What distinguishes sleep/introspection (work) from async_command/plan_exit (don't work) when both use `({ client })`?
