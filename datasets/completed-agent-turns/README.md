# Completed agent turns

This collection is the control set for [stopped-early-agent-turns](../stopped-early-agent-turns/README.md). It holds Claude Code and Codex agent turns that ended a complete unit of work. The evidence for each one is the user's very next message, read in full: it accepts the result or moves to a new task, and it does not say or imply that the work was unfinished or wrong. The collection holds only the agent turns, not the user messages.

Each control turn is matched to one stopped-early turn from the same session. So the harness, project, period, and model version are the same in each pair.

## Records

`turns.jsonl` has one JSON object on each line.

| Field | Meaning |
| --- | --- |
| `id` | A stable label for the record |
| `harness` | `claude` or `codex`; always the same as the matched turn |
| `matched_to` | The `id` of the stopped-early turn from the same session |
| `source` | The session archive path, relative to the root of the `~/agent-transcripts` corpus. A path that starts with `~/` is a live session that is not yet in the corpus. |
| `line` | The JSONL line in that session that holds the agent turn |
| `timestamp` | The time of the agent turn |
| `agent_turn` | The text of the agent's last message before the user's next message |

## Selection

1. Every session that holds a stopped-early turn was read from its raw file. Each agent turn of at least 150 characters that a typed user message followed was taken, except the stopped-early turns themselves. This gave 4413 pairs from 94 sessions.
2. Pairs were dropped if the user message was a notification, a message from another agent, a slash command, or contained correction words such as "why", "wrong", "stop", "left", "finish", "still", "again", "instead", "missing", or "failed". No filter was applied to the agent text.
3. For each stopped-early turn, the three remaining turns from its session that were closest to it in length were kept as candidates. This gave 337 unique candidates.
4. Three model judges read every candidate's next user message in full and labeled it `complete`, `incomplete`, or `unclear`, with `unclear` as the default when in doubt. Labels: 56 `complete`, 153 `incomplete`, 128 `unclear`.
5. Each of the 56 `complete` user messages was then read again by hand. A message was rejected if it asked for a refinement or correction of the same work, set a different order of work, ran a step the agent should have run (for example a push), or was only "Yes". 36 were kept.

## Balance

| Property | stopped-early | completed |
| --- | --- | --- |
| Records | 141 | 36 |
| Claude / Codex | 64 / 77 | 12 / 24 |
| Median `agent_turn` length | 1076 characters | 1012 characters |
| Sessions | 94 | the same sessions as their matches |

## Limits

- Only 36 of 141 stopped-early turns have a matched control. The others had no candidate in their session that passed every check.
- In step 4, about 45% of the candidates that passed the word filter were labeled `incomplete`. So the absence of correction words is weak evidence of completion, and the hand check in step 5 is the gate that matters.
- A user message that moves to a new task shows only that the user did not object at that point.
- Email addresses in agent text were replaced with `[email]`. Agent text can still quote or paraphrase what the user wrote earlier in the session.
