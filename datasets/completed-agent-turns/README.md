# Completed agent turns

Claude Code and Codex agent turns where the agent clearly finished the work: the user's next message accepts the result or moves to a new task. The user messages are not stored. The incomplete counterpart is [stopped-early-agent-turns](../stopped-early-agent-turns/README.md).

Each line of `turns.jsonl` is one turn: `harness`, the `source` session path in `~/agent-transcripts`, the `line` in that session, and the `agent_turn` text.
