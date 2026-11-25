# Completed agent turns

This collection is the control set for [stopped-early-agent-turns](../stopped-early-agent-turns/README.md). It holds Claude Code and Codex agent turns that end a unit of work that was actually complete. The collection holds only the agent turns, not the user messages.

Each turn has one of two kinds of evidence that the work was done:

- `accepted`: the user's next message accepted the result ("looks good", "that works", "great, now …") and either ended the topic or started a new task.
- `session-end`: the turn is the last agent message in its session. The last user message before it was not a correction, and the turn reports finished, verified work.

## Records

`turns.jsonl` has one JSON object on each line.

| Field | Meaning |
| --- | --- |
| `id` | A stable label for the record: the harness and its line number in the selection run |
| `harness` | `claude` or `codex` |
| `evidence` | `accepted` or `session-end` |
| `source` | The session archive path, relative to the root of the `~/agent-transcripts` corpus |
| `line` | The JSONL line in that session that holds the agent turn |
| `timestamp` | The time of the agent turn |
| `agent_turn` | The text of the agent's last message before the user's reply, or before the end of the session |

## Selection

The `~/agent-transcripts` index (built 2026-11-20) was searched on 2026-11-25. The search used the same raw-line checks as the stopped-early set, so it kept only messages that a person typed.

- `accepted`: The search found user messages of at most 600 characters that contain words of acceptance, such as "looks good", "perfect", "great", "thanks", or "that works". A message was dropped if it also contained correction words, such as "why", "wrong", "stop", "left", "finish", or "remaining".
- `session-end`: Two seeded random samples of Claude Code and Codex sessions were taken, each session 200 KB to 20 MB in size: 200 sessions with seed `20261125` and 500 sessions with seed `20261126`. Records from the second sample have `s2` in their `id`. A turn that both samples found is in the collection only once. From each session with at least three user messages, the last agent turn was taken. The session was dropped if the last user message was a correction.

In both groups, an agent turn was dropped if it was shorter than 150 characters or named open work: "remaining", "outstanding", "next step", "not yet", "still need", "TODO", "follow-up", "blocked", "pending", "gap", or an offer such as "would you like" or "should I". Each candidate was then read by hand. A candidate was dropped if the user's message showed a defect or only a question, or if the agent turn was a plan, a diagnosis, an admission of an error, or a report that work was still running.

Sessions written after the index was built were then scanned directly from their raw files, with the same filters: the newer corpus archives and the live `~/.claude/projects` and `~/.codex/sessions` trees. Records from that scan have `live` in their `id`. A record whose session is not yet in the corpus has a `source` path that starts with `~/`.

## Limits

- There are 104 records here, against 141 in the stopped-early set. Of the 104, 79 are `session-end` and 25 are `accepted`, and 73 are Codex turns.
- Acceptance shows only that the user did not object at that point. A defect found later in the session does not remove a record.
- The word filters remove some turns that were complete but say, for example, "no remaining work". So the control set leans toward turns that do not mention open work at all.
- Email addresses in agent text were replaced with `[email]`. Agent text can still quote or paraphrase what the user wrote earlier in the session.
