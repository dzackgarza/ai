# Managed Agent Policy Metadata

This repository no longer builds OpenCode agents from repo-local
`permission_tags` metadata.

## Current Contract

- prompt content is published from `ai-prompts`
- agent policy compilation is handled by `opencode-permission-policy-compiler`
- managed runtime agents are populated only through `just build-agents`

## Implication

If a managed agent needs different permissions:

- change the relevant policy behavior in `opencode-permission-policy-compiler`
- republish or fetch the prompt source from `ai-prompts`
- rerun `just build-agents`

Do not add new repo-local `permission_tags` workflows here. That path is
historical and has been removed from the active build flow.
