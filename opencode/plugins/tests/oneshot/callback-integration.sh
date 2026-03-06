#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/dzack/ai/opencode/plugins"
IMPROVED_TASK_PLUGIN="file:///home/dzack/opencode-plugins/improved-task/src/index.ts"
SLEEP_PLUGIN="file:///home/dzack/ai/opencode/plugins/sleep.ts"
ASYNC_COMMAND_PLUGIN="file:///home/dzack/ai/opencode/plugins/async-command.ts"
MODEL="openrouter/stepfun/step-3.5-flash:free"

workdir="$(mktemp -d /tmp/opencode-callback-integration.XXXXXX)"
home_dir="$workdir/home"
xdg_config_dir="$workdir/xdg-config"
xdg_data_dir="$workdir/xdg-data"
cleanup() {
  rm -rf "$workdir"
}
trap cleanup EXIT
mkdir -p "$home_dir" "$xdg_config_dir" "$xdg_data_dir"

jq -n \
  --arg schema "https://opencode.ai/config.json" \
  --arg model "$MODEL" \
  --arg improvedTask "$IMPROVED_TASK_PLUGIN" \
  --arg sleepPlugin "$SLEEP_PLUGIN" \
  --arg asyncPlugin "$ASYNC_COMMAND_PLUGIN" \
  '{
    "$schema": $schema,
    model: $model,
    default_agent: "LocalMainCallback",
    plugin: [$improvedTask, $sleepPlugin, $asyncPlugin],
    mcp: {},
    agent: {
      "LocalMainCallback": {
        description: "Local callback integration test agent",
        mode: "primary",
        model: $model,
        prompt: "Follow instructions exactly. Call requested tools in order. Keep answers terse.",
        permission: {
          task: "allow",
          sleep: "allow",
          async_command: "allow",
          bash: "deny",
          todoread: "deny",
          todowrite: "deny"
        }
      },
      "LocalWorkerCallback": {
        description: "Local worker subagent for callback integration checks",
        mode: "subagent",
        model: $model,
        prompt: "Return exactly one line: WORKER_DONE.",
        permission: {
          bash: "deny",
          todoread: "deny",
          todowrite: "deny"
        }
      }
    },
    permission: {
      task: "allow",
      sleep: "allow",
      async_command: "allow"
    }
  }' > "$workdir/opencode.json"

prompt_file="$workdir/prompt.txt"
cat > "$prompt_file" <<'PROMPT'
Use tools in this exact order:
1) Call sleep with seconds=1.
2) Call async_command with seconds=1 and message="callback-smoke".
3) Call task with description="callback check", prompt="Reply exactly WORKER_DONE.", subagent_type="LocalWorkerCallback", and mode="async".
After all tool calls, reply exactly: CALLBACK_SEQUENCE_STARTED
PROMPT

run_log="$workdir/run.log"
run_status=0
(
  cd "$workdir"
  HOME="$home_dir" \
  XDG_CONFIG_HOME="$xdg_config_dir" \
  XDG_DATA_HOME="$xdg_data_dir" \
  OPENCODE_CONFIG="$workdir/opencode.json" \
  OPENCODE_CONFIG_DIR="$workdir" \
  OPENCODE_DISABLE_PROJECT_CONFIG=1 \
  timeout 120 sh -lc "cat '$prompt_file' | opencode"
) >"$run_log" 2>&1 || run_status=$?

if [[ "$run_status" -ne 0 && "$run_status" -ne 124 ]]; then
  echo "callback integration run failed with exit code: $run_status"
  sed -n '1,260p' "$run_log"
  exit 1
fi

events_file=""
for candidate in \
  "$workdir/.opencode/events.jsonl" \
  "$home_dir/.opencode/events.jsonl" \
  "$xdg_data_dir/opencode/events.jsonl"; do
  if [[ -f "$candidate" ]]; then
    events_file="$candidate"
    break
  fi
done

if [[ -z "$events_file" ]]; then
  echo "missing events file: $events_file"
  sed -n '1,260p' "$run_log"
  exit 1
fi

session_id="$(grep -o 'ses_[a-zA-Z0-9]*' "$events_file" | head -1 || true)"
if [[ -z "$session_id" ]]; then
  echo "failed to detect session id from events"
  sed -n '1,260p' "$run_log"
  exit 1
fi

export_json="$workdir/export.json"
OPENCODE_CONFIG="$workdir/opencode.json" \
OPENCODE_CONFIG_DIR="$workdir" \
OPENCODE_DISABLE_PROJECT_CONFIG=1 \
HOME="$home_dir" \
XDG_CONFIG_HOME="$xdg_config_dir" \
XDG_DATA_HOME="$xdg_data_dir" \
opencode export "$session_id" > "$export_json"

texts_file="$workdir/texts.txt"
jq -r '.messages[]?.parts[]? | select(.type=="text") | (.text // empty)' "$export_json" > "$texts_file"

if ! rg -q '\[sleep_poll_callback\]' "$texts_file"; then
  echo "missing sleep callback marker"
  sed -n '1,260p' "$texts_file"
  exit 1
fi

if ! rg -q '\[async-command completed\]' "$texts_file"; then
  echo "missing async_command callback marker"
  sed -n '1,260p' "$texts_file"
  exit 1
fi

if ! rg -q '^status: (completed|timeout|failed)$' "$texts_file"; then
  echo "missing terminal task callback summary"
  sed -n '1,260p' "$texts_file"
  exit 1
fi

if ! rg -q '^## 1\. Summarized Final Result$' "$texts_file"; then
  echo "missing task summary section"
  sed -n '1,260p' "$texts_file"
  exit 1
fi

echo "Callback integration check passed for session: $session_id"
