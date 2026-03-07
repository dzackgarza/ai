// =============================================================================
// Compaction Override Examples
// =============================================================================
//
// Hook: experimental.session.compacting
// Fires: Before the LLM generates a continuation summary during context compaction
//
// Compaction manages context window usage by summarizing old conversation history
// when the context fills up, allowing long sessions to continue without hitting
// token limits.
//
// Configuration (opencode.json):
// {
//   "compaction": {
//     "auto": true,        // Automatically compact when context is full (default)
//     "prune": true,       // Remove old tool outputs to save tokens
//     "reserved": 10000,   // Token buffer reserved for compaction process
//     "model": "github-copilot/gpt-4.1"  // Model for generating summary
//   }
// }
//
// =============================================================================
// Pattern 1: Inject Additional Context (augments default prompt)
// =============================================================================
//
// Use output.context.push() to add domain-specific context that should persist
// across compaction. The default compaction prompt is preserved.
//
// export const CompactionPlugin: Plugin = async (ctx) => {
//   return {
//     "experimental.session.compacting": async (input, output) => {
//       output.context.push(`
// ## Custom Context
// Include any state that should persist across compaction:
// - Current task status
// - Important decisions made
// - Files being actively worked on
// `)
//     }
//   }
// }
//
// =============================================================================
// Pattern 2: Replace Prompt Entirely (overrides default)
// =============================================================================
//
// Set output.prompt to completely replace the default compaction prompt.
// When output.prompt is set, the output.context array is IGNORED.
//
// export const CustomCompactionPlugin: Plugin = async (ctx) => {
//   return {
//     "experimental.session.compacting": async (input, output) => {
//       output.prompt = `
// You are generating a continuation prompt for a multi-agent swarm session.
//
// Summarize:
// 1. The current task and its status
// 2. Which files are being modified and by whom
// 3. Any blockers or dependencies between agents
// 4. The next steps to complete the work
//
// Format as a structured prompt that a new agent can use to resume work.
// `
//     }
//   }
// }
//
// =============================================================================
// TODOs for Enhanced Compaction
// =============================================================================
//
// TODO: Reconstruct session transcript and produce a summary of what the user
// specifically asked each turn, and the steps and tool call results the agent
// took. The exact sequence of actions already taken needs to be part of compaction.
//
// TODO: Store the compaction prompt as a template in ~/ai/prompts/compaction.md
// and load it dynamically rather than hardcoding in the plugin.
//
// TODO: Find the Claude Code or Cursor Codex compaction template and leverage
// it as a reference or base for our custom compaction prompt.
//
// TODO: Add specific instructions to include what the last N steps were attempting
// to accomplish and how to finish that immediate task (prevents losing context
// mid-task during compaction).
//
// TODO: Inject git diff status into the compaction prompt so the next agent
// knows what files have uncommitted changes and what was modified.
//
// TODO: Have the compaction agent list important reference files that should be
// kept in context (files frequently read/modified during the session).
//
// TODO: Have the compaction agent reconstruct a timeline of events, including:
// - Mistakes not to repeat (dead ends, wrong approaches identified)
// - Avenues already tried (prevents cycling through same failed solutions)
// - Key decisions made and why
// - Current blockers and hypotheses being tested
//
// TODO: Report in-flight async work (pending async_command calls, and any
// other background operations) so the next agent knows what operations are
// still running and can wait for results or handle completion.
//
// =============================================================================
// Key Behavior
// =============================================================================
// - output.context.push() → augments the default prompt
// - output.prompt = "..." → replaces default prompt entirely (context ignored)
//
// Source: https://github.com/anomalyco/opencode/blob/dev/packages/web/src/content/docs/plugins.mdx

// =============================================================================
// Default Compaction Prompt (upstream opencode)
// =============================================================================
// Source: packages/opencode/src/session/compaction.ts — SessionCompaction.process
//
// The default prompt that opencode uses when compacting a session:
//
// ```
// Provide a detailed prompt for continuing our conversation above.
// Focus on information that would be helpful for continuing the conversation,
// including what we did, what we're doing, which files we're working on, and
// what we're going to do next.
// The summary that you construct will be used so that another agent can read
// it and continue the work.
//
// When constructing the summary, try to stick to this template:
// ---
// ## Goal
//
// [What goal(s) is the user trying to accomplish?]
//
// ## Instructions
//
// - [What important instructions did the user give you that are relevant]
// - [If there is a plan or spec, include information about it so next agent
//   can continue using it]
//
// ## Discoveries
//
// [What notable things were learned during this conversation that would be
// useful for the next agent to know when continuing the work]
//
// ## Accomplished
//
// [What work has been completed, what work is still in progress, and what
// work is left?]
//
// ## Relevant files / directories
//
// [Construct a structured list of relevant files that have been read, edited,
// or created that pertain to the task at hand. If all the files in a directory
// are relevant, include the path to the directory.]
// ---
// ```

// =============================================================================
// Cursor Compaction Prompt (reference)
// =============================================================================
// Source: getcursor/cursor — cursor/src/vs/workbench/contrib/chat/common/chat.ts
//
// CONTEXT_COMPACTION_PROMPT_TEMPLATE:
//
// ```
// You are an AI assistant that is summarizing a conversation.
// Your goal is to extract the most important information from the conversation.
// Do not add any new information.
// Do not respond to the user.
// Do not say "Okay, I will summarize the conversation." or anything similar.
// Output the summary directly.
//
// ---
//
// Here is the conversation:
// {{ CONVERSATION }}
// ```

// =============================================================================
// Claude Code Compaction Prompt
// =============================================================================
// Not exposed in source code.
//
// Claude Code uses an external "Auto-compaction API" for summarization.
// The prompt text is not in the client-side codebase.
//
// Known: strips images/PDFs before compaction, /compact command, auto-triggers
// at ~80% context window, no preamble recap after compaction.
