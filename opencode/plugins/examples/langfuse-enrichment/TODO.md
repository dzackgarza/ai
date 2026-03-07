# TODO: Enrich Langfuse with OpenCode Session Data

## Problem

The `opencode-plugin-langfuse` captures LLM traces but does **not** include:

- `directory` — the project's absolute path
- `agent` — the agent name (e.g., "Interactive")

These are present in OpenCode's session/message models but not sent to Langfuse.

## Solution

Create a companion plugin that attaches `opencode.directory` and `opencode.agent` as span attributes.

## Approach

1. Leverage OpenTelemetry's `getCurrentSpan()` to access the active span
2. Subscribe to `message.created` / `message.updated` events
3. Read `client.session.directory` (from Session type)
4. Read agent from `event.properties.info.user.agent` or `assistant.agent`
5. Call `span.setAttribute(key, value)` before the span ends

## Why This Works

- The langfuse plugin already initializes `NodeSDK` with `LangfuseSpanProcessor`
- OpenCode's internal OTEL instrumentation creates spans for LLM calls
- Spans are in context when message events fire
- Adding attributes after span creation is allowed by OpenTelemetry

## Plugin Skeleton

```typescript
import { getCurrentSpan } from "@opentelemetry/api";

export const LangfuseEnrichmentPlugin = async ({ client }) => {
  return {
    event: async ({ event }) => {
      if (
        event.type === "message.created" ||
        event.type === "message.updated"
      ) {
        const span = getCurrentSpan();
        if (!span.isRecording()) return;

        // Attach directory from session
        if (client.session?.directory) {
          span.setAttribute("opencode.directory", client.session.directory);
        }

        // Attach agent from message
        const info = event.properties.info;
        const agent = info.user?.agent || info.assistant?.agent;
        if (agent) {
          span.setAttribute("opencode.agent", agent);
        }
      }
    },
  };
};
```

## Verification

1. Add plugin to `.opencode/opencode.json` after `opencode-plugin-langfuse`
2. Ensure `experimental.openTelemetry = true`
3. Run a session that uses tools
4. Check Langfuse trace for `opencode.directory` and `opencode.agent` attributes

## Notes

- Plugin order may matter: this should load **after** langfuse plugin (but both are independent)
- No need to fork `opencode-plugin-langfuse`; this composes alongside it
- File diffs are still NOT captured (requires changes to OpenCode's OTEL instrumentation itself)

## Status

- Research complete: Session type includes `directory`, message types include `agent`
- Implementation: pending
