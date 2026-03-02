---
name: reading-transcripts
description: Use when asked about previous conversations, previous sessions, transcript logs, past interactions, or when needing to parse session histories across any supported CLI agent.
---

# reading-transcripts

## Overview

Provides paths and parsing scripts for reading historical transcript logs from various CLI agent harnesses.

Intelligent agents can use this information to locate past conversations, list historical sessions, and extract plain-text transcripts from otherwise dense JSONL/database formats in order to answer user questions about past work.

## Quick Reference

| Action                      | Command                                                                                                    |
| --------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **1. List ALL sessions**    | `python ~/.agents/skills/reading-transcripts/scripts/list_all_sessions.py`                                 |
| **2. Parse any transcript** | `python ~/.agents/skills/reading-transcripts/scripts/parse_transcript.py --harness <harness> <identifier>` |

**Example Workflow:**

```bash
# 1. Find the most recent session
python ~/.agents/skills/reading-transcripts/scripts/list_all_sessions.py

# 2. Parse the transcript from the top result (pipe to tail to see the end!)
python ~/.agents/skills/reading-transcripts/scripts/parse_transcript.py --harness claude ~/.claude/projects/my-project/session.jsonl | tail -n 200
```

## Abstracted Parsing

All CLI platforms use entirely different underlying data stores, complex custom JSON schemas, and varying architectures (e.g. databases vs flat files vs hierarchical directories).

**NEVER attempt to read raw `.jsonl`, `.json`, or `.db` transcript logs manually.** Attempting to parse them with `grep`, `cat`, or `jq` is a waste of time, burns context, and will fail due to nested metadata, telemetry spam, and dense array structures.

You MUST bypass manual processing by feeding the identifier into the unified parser script:

```bash
python ~/.agents/skills/reading-transcripts/scripts/parse_transcript.py --harness <type> <identifier>
```

Supported harnesses: `claude`, `opencode`, `codex`, `kilocode`, `gemini`, `qwen`, `amp`

The parser script automatically extracts user prompts, assistant text, thinking blocks, tool calls, and truncated tool results, outputting them in a clean, chronological format.

## Verifying Subagents

When an agent (especially in OpenCode or Claude Code) launches a subagent, the subagent runs in its own entirely separate session. The main agent **only sees the final summary** returned by the subagent.

Because the main agent doesn't see the subagent's actual transcript, it will often confidently hallucinate that the subagent completed all its work perfectly, even if the subagent failed or skipped steps.

To verify what a subagent actually did:

1. Look at the tool result for the subagent in the main transcript.
2. Find its distinct session ID (e.g. `ses_<uuid>`) or file path (`rollout-*.jsonl`, `tasks/<uuid>.output`).
3. Run the parser script specifically on that subagent's identifier to read its isolated workflow.

## Common Mistakes

- **Trusting subagent summaries blindly:** Main agents only receive the final summary message of a delegated task and will often confidently assume incomplete work was done perfectly. Always track down the subagent's actual session ID or output file if you need to verify its work.
- **Reading from the top (head):** Sessions are long and often continued over days. The tasks at the beginning of the file may be completely unrelated to the current work. **Always start by piping the output to `tail -n 300`** to understand the most recent, relevant context before searching upward.

---

## 🛠️ Developer / Debugging Reference

The wrapper scripts abstract away the locations of the underlying data. If the scripts break, you should attempt to read these directories to debug the schemas and fix the python parser scripts before reverting to manual scanning. These directories serve as the 100% provable source of truth.

| Harness         | Storage Architecture        | Raw Path                                                                                                                                        |
| --------------- | --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **Claude Code** | Flat JSONL per project      | `~/.claude/projects/<slugified-project-name>/*.jsonl`                                                                                           |
| **Qwen Code**   | Flat JSONL per project      | `~/.qwen/projects/<slugified-project-name>/chats/*.jsonl`                                                                                       |
| **Codex CLI**   | Hierarchical Date JSONL     | `~/.codex/sessions/<YYYY>/<MM>/<DD>/rollout-*.jsonl`                                                                                            |
| **Gemini CLI**  | Flat JSON Array per project | `~/.gemini/tmp/<project-name>/chats/*.json`                                                                                                     |
| **Kilocode**    | Flat JSON Array per task    | `~/.kilocode/cli/global/tasks/<taskId>/api_conversation_history.json`                                                                           |
| **OpenCode**    | Langfuse API                | Fetched via `parse_langfuse_opencode.py` using session ID. Requires `LANGFUSE_BASE_URL`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` env vars. |
| **Amp CLI**     | Abstracted Cloud/Local      | Hidden _(Exported via CLI `amp threads markdown`)_                                                                                              |
