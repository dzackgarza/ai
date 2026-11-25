# Stopped-early agent turns

This collection holds agent turns from Claude Code and Codex sessions. In each one, the agent did one of two things:

- `stopped-to-report`: the agent ended its turn to report or describe outstanding work. The next step was clear and inside the task, so the agent should have done it.
- `loose-ends`: the agent said the work was done, but it left parts undone, left debris, or left out required items.

The user's reply after each turn showed the defect. This collection holds only the agent turns, not the user replies.

## Records

`turns.jsonl` has one JSON object on each line.

| Field | Meaning |
| --- | --- |
| `id` | A stable label for the record: the harness and its line number in the selection run |
| `harness` | `claude` or `codex` |
| `pattern` | `stopped-to-report` or `loose-ends` |
| `source` | The session archive path, relative to the root of the `~/agent-transcripts` corpus |
| `line` | The JSONL line in that session that holds the agent turn |
| `timestamp` | The time of the agent turn |
| `agent_turn` | The text of the agent's last message before the user's reply |

To read the turn in its session, use the transcript corpus tools: `just slice <source> <marker>` in `~/agent-transcripts`.

## Selection

The `~/agent-transcripts` index (built 2026-11-20) was searched on 2026-11-25 for user messages that contain phrases such as "why did you stop", "why are you stopping", "outstanding work", "you left", "loose ends", "finish the work", and "narrating". Each hit was checked in the raw session file to confirm that a person typed it. Tool results, system reminders, task notifications, and messages from other agents were removed. For each remaining message, the agent text immediately before it was taken.

Each candidate user message was then read by hand. A pair was kept only when the user's reply clearly said that the agent stopped early to report, or that the agent left work undone. A pair was dropped when the reply was about something else, for example only narration style or a new request. If one agent turn had more than one matching reply, it is in the collection only once.

Sessions written after the index was built were then scanned directly from their raw files, with the same filters: the newer corpus archives and the live `~/.claude/projects` and `~/.codex/sessions` trees. Records from that scan have `live` in their `id`. A record whose session is not yet in the corpus has a `source` path that starts with `~/`.

## Limits

- Phrase search finds only the replies that use these phrases. Other replies that identify the same defect are not in the collection.
- The `pattern` label comes from the user's reply, not from a separate review of the agent turn.
- Email addresses in agent text were replaced with `[email]`. Agent text can still quote or paraphrase what the user wrote earlier in the session.

The control set of completed turns is in [completed-agent-turns](../completed-agent-turns/README.md).
