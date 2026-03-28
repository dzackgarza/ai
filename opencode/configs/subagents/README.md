# Subagents

This directory no longer holds the runtime subagent definitions.

## Active Source Of Truth

- Published prompt sources: `ai-prompts`
- Managed runtime files: `../../agents/*.md`
- Population workflow: `just build-agents` from `~/ai`
- Permission compilation: `~/opencode-plugins/opencode-permission-policy-compiler`

## Update Flow

- update or publish the source prompt in `ai-prompts`
- update the external policy compiler if permission behavior must change
- run `just build-agents`

Do not edit files in `../../agents/` directly. They are regenerated from the
published prompt slugs.
