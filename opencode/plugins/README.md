# OpenCode Plugins

Custom plugins for OpenCode, loaded globally from `~/.config/opencode/plugins/`.

## Quick start

```bash
just check-plugins                     # typecheck + compile + import smoke tests
just opencode-session                  # session management CLI (list, delete, stats, etc.)
```

`just check-plugins` is the canonical plugin gate. It catches errant plugins before an OpenCode session by typechecking, bundling `local-tools.ts`, and smoke-importing every active local plugin entrypoint so import-time failures from top-level code are surfaced immediately.

## Plugin inventory

| Plugin | File | Status | Purpose |
|--------|------|--------|---------|
| **Prompt Router** | `external` | Production | Moved to standalone plugin repo: `/home/dzack/opencode-plugins/prompt-router/src/index.ts` |
| **Stop Hooks** | `external` | Production | Moved to standalone plugin repo: `/home/dzack/opencode-plugins/improved-stop-hooks` |
| ↳ OTP Checker | `external` | Demo | Detects a verification code in the assistant response and reveals a secret phrase |
| ↳ Reflexive Agreement | `external` | Active | Intercepts "you're right" / "they are right" responses and prompts for independent reasoning |
| ↳ Obvious Question | `external` | Active | Intercepts "should I..." questions and prompts the agent to resolve them autonomously |
| **Command Interceptor** | `examples/command-interceptor/index.ts` | Demo | Proof-of-concept: detects keyphrases ("intercept test", "plugin check") and injects a hidden passphrase the model must echo |
| **Context Injector** | `context-injector.ts` | Demo | Proof-of-concept: injects additional context when a specific keyphrase appears in the user message |
| **CoT Trivial Interceptor** | `cot-trivial-test.ts` | Dev (gated) | Mid-stream CoT interceptor: detects "trivial" in reasoning and re-prompts. Requires manual gate removal to activate. |
| **Write Plan** | `write_plan.ts` | Active | Custom tool `write_plan`: writes a plan document to `.serena/plans/` |
| **Plan Exit** | `plan_exit.ts` | Active | Custom tool `plan_exit`: presents a verification checklist before exiting plan mode |
| **Sleep** | `sleep.ts` | Active | Custom tools `sleep` / `sleep_until`: real wall-clock waiting with a 60-minute safety cap |
| **Async Command** | `async-command.ts` | Active | Custom tool `async_command`: fires a background sleep and injects the result via `promptAsync` when done |
| **Introspection** | `introspection.ts` | Active | Custom tool `introspection`: returns the agent's own session ID, message ID, and agent name |
| **List Sessions** | `list-sessions.ts` | Active | Custom tool `list_sessions`: lists sessions with token counts, models, and duration |
| **Read Transcript** | `read-transcript.ts` | Active | Custom tool `read_transcript`: exports and parses a session transcript to a temp file with head/tail preview |
| **Session Harness (CLI utility)** | `utilities/harness/session-harness.ts` | Active | Session management CLI (list, delete, get, messages, create, stats). Not loaded as a plugin module. |

## File map

```
plugins/
├── justfile                        # Dev recipes (just check, just test, etc.)
├── tsconfig.json                   # TypeScript config for Bun ESM
├── package.json                    # Dependencies (instructor, openai, opencode-ai/plugin, zod)
│
├── (moved) stop-hooks plugin       # Now in /home/dzack/opencode-plugins/improved-stop-hooks
│
├── context-injector.ts             # Demo: keyphrase → context injection
├── cot-trivial-test.ts             # Dev: mid-stream CoT interceptor (gated)
│
├── write_plan.ts                   # Tool: write plan to .serena/plans/
├── plan_exit.ts                    # Tool: plan exit verification checklist
├── sleep.ts                        # Tool: sleep / sleep_until
├── async-command.ts                # Tool: fire-and-forget background command
├── introspection.ts                # Tool: session metadata self-report
├── list-sessions.ts                # Tool: session list with token stats
├── read-transcript.ts              # Tool: export + preview session transcript
│
├── examples/
│   ├── command-interceptor/        # Demo: keyphrase → passphrase injection
│   │   ├── index.ts
│   │   └── command-interceptor.test.ts
│   └── retired/
│
├── (external) prompt-router        # Standalone package:
│   └── /home/dzack/opencode-plugins/prompt-router
│
├── tests/
│   └── unit/                       # bun test — active plugin unit tests
│
└── utilities/
    ├── harness/                    # session-harness.ts CLI (not auto-loaded as plugin)
    └── scripts/
```

## Session Harness

Centralized CLI for managing OpenCode sessions. Exposes the complete session API.

**Usage:**
```bash
just session <command> [options]
# or directly:
bun run utilities/harness/session-harness.ts <command> [options]
```

**Session Management:**
| Command | Description | Example |
|---------|-------------|---------|
| `list` | List all sessions | `just session list --limit 10` |
| `get` | Get session details | `just session get ses_abc123` |
| `children` | List child sessions | `just session children ses_abc123` |
| `create` | Create new session | `just session create --title "test"` |
| `update` | Update session | `just session update ses_abc123 --title "new"` |
| `delete` | Delete a session | `just session delete ses_abc123` |
| `abort` | Abort running session | `just session abort ses_abc123` |
| `share` | Share a session | `just session share ses_abc123` |
| `unshare` | Unshare a session | `just session unshare ses_abc123` |
| `summarize` | Start summarization | `just session summarize ses_abc123` |
| `init` | Initialize (analyze & AGENTS.md) | `just session init ses_abc123` |

**Messages:**
| Command | Description | Example |
|---------|-------------|---------|
| `messages` | List messages | `just session messages ses_abc123` |
| `message` | Get single message | `just session message ses_abc123 msg_xyz` |

**Interaction:**
| Command | Description | Example |
|---------|-------------|---------|
| `prompt` | Send prompt | `just session prompt ses_abc123 "hello"` |
| `command` | Send command | `just session command ses_abc123 todo_write` |
| `shell` | Run shell command | `just session shell ses_abc123 "ls -la"` |

**History:**
| Command | Description | Example |
|---------|-------------|---------|
| `revert` | Revert a message | `just session revert ses_abc123 msg_xyz` |
| `unrevert` | Restore reverted | `just session unrevert ses_abc123` |

**Permissions:**
| Command | Description | Example |
|---------|-------------|---------|
| `permission` | Respond to permission | `just session permission ses_abc123 perm_xyz allow` |

**Statistics:**
| Command | Description | Example |
|---------|-------------|---------|
| `stats` | Show statistics | `just session stats` |

**Options:**
- `--json` - Output as JSON (all commands)
- `--limit N` - Limit results (list, messages)
- `--no-reply` - Don't wait for AI response (prompt)
- `--output-format` - Request structured output (prompt)
- `--title "text"` - Set title (create, update)
- `--parent <id>` - Set parent session (create)
- `--analyze` - Analyze app (init)

**Examples:**
```bash
# List recent sessions
just session list --limit 5

# Create a child session
just session create --title "subagent-test" --parent ses_abc123

# Send a prompt without waiting for response
just session prompt ses_abc123 "background task" --no-reply

# Export messages as JSON
just session messages ses_abc123 --json > messages.json

# Get statistics
just session stats

# Respond to a permission request
just session permission ses_abc123 perm_xyz allow-session
```

**Safety:**
- Delete requires explicit session ID (no bulk operations)
- No `--all` or `--older-than` flags (prevents accidental mass deletion)
- Single-session deletion only

**Programmatic API:**
```typescript
import { 
  listSessions, deleteSession, getStats,
  sendPrompt, getMessages, createSession 
} from "./utilities/harness/session-harness";

const sessions = await listSessions();
const stats = await getStats();
await deleteSession("ses_abc123");
await sendPrompt("ses_abc123", "hello");
```

## Prompt Router

Prompt Router now lives in the standalone plugin repo at `/home/dzack/opencode-plugins/prompt-router`.

Runtime behavior remains the same:
- classifies each incoming user message into one of six tiers
- uses the canonical prompt files in `~/ai/prompts/micro_agents/prompt_difficulty_classifier/`
- appends JSONL classifications to `/var/sandbox/.prompt-router.log`

## Stop Hooks

Runs on every `session.idle` event. Collects results from all registered hook functions and, if any return `force_stop: true`, injects a report back into the session as a new user message.

The stop-hooks plugin was extracted to:

- `/home/dzack/opencode-plugins/improved-stop-hooks/src/stop-hooks.ts`
- `/home/dzack/opencode-plugins/improved-stop-hooks/src/stop_hooks/`

To add a hook: create `src/stop_hooks/my-hook.ts`, export one `async (ctx: StopHookContext) => Promise<StopHookResult>` function, import it in `src/stop-hooks.ts` and add to `STOP_HOOKS`.

## Environment Variables

See `.envrc` for all environment variables.

## YouTube Processing Pipeline Dependencies

The YouTube transcript pipeline has hard dependencies. These are not optional fallbacks.

### Required runtime dependencies

- `yt-dlp` with impersonation support (`curl-cffi`): use `yt-dlp[default,curl-cffi]`
- JavaScript runtime for YouTube challenge solving: `bun`, `node`, or `deno`
- yt-dlp remote challenge components: `--remote-components ejs:github`
- Media tooling: `ffmpeg` and `ffprobe`
- Speech transcription stage: `openai-whisper` (CLI `whisper`)

### English-first processing path

1. Enumerate available subtitles (`--list-subs`)
2. Extract English subtitles (`--sub-langs "en,en-orig"`)
3. If no usable English subtitles are available, run speech transcription with Whisper

### Tested command shape

```bash
uvx --from 'yt-dlp[default,curl-cffi]' yt-dlp \
  --remote-components ejs:github \
  --js-runtimes bun --js-runtimes node \
  --list-subs "<url>"

uvx --from 'yt-dlp[default,curl-cffi]' yt-dlp \
  --remote-components ejs:github \
  --js-runtimes bun --js-runtimes node \
  --skip-download --write-subs --write-auto-subs \
  --sub-langs "en,en-orig" --sub-format vtt \
  -o "<out>/%(id)s.%(ext)s" "<url>"

uvx --from openai-whisper whisper \
  --model tiny --language en --task transcribe \
  --output_format txt --output_dir "<out>" "<audio-file>"
```
