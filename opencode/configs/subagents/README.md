# Subagents

This directory no longer holds the runtime subagent definitions.

## Active Source Of Truth

- Published prompt sources: `ai-prompts`
- Managed runtime files: `../../agents/*.md`
- Population workflow: `just build-agents` from `~/ai`
- External compiler: `~/opencode-plugins/clis/opencode-permission-policy-compiler`
- Policy definition: `../opencode-permission-policy-compiler/config.toml`

The repo-level build runs `just build-config` first so the compiled
`opencode.json` receives the global permission baseline before agent markdown
is regenerated.

## Update Flow

- update or publish the source prompt in `ai-prompts`
- update the external policy compiler if permission behavior must change
- edit `../opencode-permission-policy-compiler/config.toml` if the global baseline must change
- run `just build-agents`

Do not edit files in `../../agents/` directly. They are regenerated from the
published prompt slugs.
