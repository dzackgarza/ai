# MCP Tool Interface Design

Agent-facing tool design is behavior design. Tool names, descriptions, ordering,
and parameter schemas change which tools agents notice, select, and keep using.

## Selection Behavior

- Use descriptive action names. A precise verb-object name is more likely to be
  selected correctly than a terse internal abbreviation.
- Keep tools ordered by common workflow: diagnostic canary, discovery/listing,
  read/query, mutation, cleanup. Agents tend to follow visible tool families
  once they start down one path.
- Expose real capability through parameters. A richer parameter schema is useful
  when it represents actual control, validation, or filtering. Do not add fake
  optional knobs that only create ambiguity.
- Include a simple canary tool or health-check call when the server owns a
  network, database, model, or filesystem boundary. Test the canary before
  interpreting failures from richer tools.
- Keep a thin MCP adapter. Put protocol parsing, tool registration, and response
  formatting at the edge; keep domain algorithms, validation, and formatting in
  ordinary modules that can be tested directly.

## Discovery And Validation

For remote services that advertise MCP through a wrapper, check whether a native
endpoint exposes a more complete tool surface before concluding the integration
is limited. Common Gradio Spaces endpoints include:

```text
/gradio_api/mcp/sse
/gradio_api/mcp/http
```

Validate both the wrapper and the direct endpoint with a real tool call. A
successful connection or listed Space is not enough; the endpoint must expose the
expected tools and return a real result through the configured client.

## Error And Result Shape

- Normalize heterogeneous upstream responses before exposing them as MCP tool
  results.
- Return structured errors with stable fields, not prose-only failure messages.
- Bound request sizes, timeouts, and retry behavior at the tool boundary.
- Cache repeated expensive discovery calls when the upstream service is slow or
  quota-limited, but treat cache hits as stale when reporting availability.
