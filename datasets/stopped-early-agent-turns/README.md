# Stopped-early agent turns

Claude Code and Codex agent turns where the agent clearly did not finish the work: it left loose ends, or stopped to report outstanding work instead of doing it, and the user's next message says so. The user messages are not stored. The completed counterpart is [completed-agent-turns](../completed-agent-turns/README.md).

Each line of `turns.jsonl` is one turn: `harness`, the `source` session path in `~/agent-transcripts`, the `line` in that session, and the `agent_turn` text.
