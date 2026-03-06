# Google Provider Configuration (via Antigravity Auth)

This directory configures the `google` provider, which is uniquely augmented by
the `opencode-antigravity-auth` plugin to access internal Google IDE
(Antigravity) endpoints alongside standard Gemini CLI developer preview
endpoints.

## Model Slugs And Routing Behavior

The `opencode-antigravity-auth` plugin performs quota rotation and model-name
aliasing.

If you use the official plugin documentation, you might see legacy model slugs
documented with the `antigravity-` prefix. This config deliberately avoids
those legacy prefixes so the provider files stay aligned with the OpenCode
`models.dev` schema and the plugin's native routing path.

### Gemini Models

Use standard schema slugs such as:

- `"google/gemini-3-flash-preview"`
- `"google/gemini-3.1-pro-preview"`

The plugin resolver intercepts these and prefers the internal Antigravity
endpoint, then falls back to the public Gemini CLI endpoint if needed.

### Claude Models Via Google

Google's public API does not host Claude, but the Antigravity proxy does.
OpenCode reaches those models through compatibility aliases:

- `"google/gemini-claude-sonnet-4-6"`
- `"google/gemini-claude-opus-4-6-thinking"`

The plugin strips the compatibility prefix and routes the request to Claude
through Google credentials. These proxy slugs must stay injected into the build
pipeline because they are non-standard.

## Reference

- <https://github.com/NoeFabris/opencode-antigravity-auth#readme>
