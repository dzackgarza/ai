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
| **Canonical Smoke Test** | `canonical-smoke-test.ts` | Canonical | Minimal docs-style `mytool` probe; known-good visibility and execution control |
| **Canonical Shadowing Test** | `canonical-shadowing-test.ts` | Canonical | Minimal `webfetch` shadow probe; known-good built-in shadowing control |
| **Session Harness (CLI utility)** | `external` | Active | Primary entrypoint moved to `dzackgarza/opencode-manager`; local `utilities/harness/` is a compatibility layer during retirement. |

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
    ├── harness/                    # compatibility wrapper/docs for external opencode-manager
    └── scripts/
```

## Session Harness

The local harness is being retired. The primary entrypoint is the private repo
`dzackgarza/opencode-manager`.

Use the centralized wrappers:

```bash
just opencode-harness run --help
just opencode-session --help
just opencode-session list --limit 5
```

Direct GitHub-backed commands:

```bash
uvx --from git+https://github.com/dzackgarza/opencode-manager.git ocm --help
```

The local `utilities/harness/` directory remains only as a compatibility wrapper and
historical source snapshot during cutover.

## Canonical Control Probes

Two plugin files in this directory are reserved as known-good controls for proving tool
visibility and tool dispatch:

- `canonical-smoke-test.ts`
- `canonical-shadowing-test.ts`

Use them as the first rung in any shadowing or nondeterministic-behavior investigation.
They are intentionally minimal and stay as close as possible to the docs example.
When validating non-autoload load paths, the files in `plugins/` may be commented out
and distinct non-colliding active copies may instead be loaded via `file://` from
`/home/dzack/ai/opencode/tools/canonical-plugin-probes/`.

Known-good probes:

```bash
command opencode run \
  "Call the tool named mytool with foo=probe. Then reply with ONLY the exact tool output."

command opencode run \
  "Call the tool named webfetch with url=https://example.com. Then reply with ONLY the exact tool output."
```

Known-good interactive stdout:

- `⚙ mytool {"foo":"probe"}`
- `PASS_MYTOOL_SHADOW_PROBE_20260310`
- `% WebFetch https://example.com`
- `EXEC_WEBFETCH_SHADOW_GLOBAL_PASS_01 https://example.com`

Do not treat description-only prompts or final assistant text as proof. For machine-
readable proof of dispatch, capture raw `tool_use` events instead of only the final text.

## Prompt Router

Prompt Router now lives in the standalone plugin repo at `/home/dzack/opencode-plugins/prompt-router`.

Runtime behavior remains the same:
- classifies each incoming user message into one of six tiers
- uses the canonical prompt slug `micro-agents/prompt-difficulty-classifier` from `ai-prompts`
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
