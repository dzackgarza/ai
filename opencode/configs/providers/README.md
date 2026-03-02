# Google Provider Configuration (via Antigravity Auth)

This directory configures the `google` provider, which is uniquely augmented by the `opencode-antigravity-auth` plugin to access internal Google IDE (Antigravity) endpoints alongside standard Gemini CLI developer preview endpoints.

## Model Slugs and Routing Behavior

The `opencode-antigravity-auth` plugin performs complex quota rotation and model-name aliasing.

If you use the official plugin documentation, you might see "legacy" model slugs documented with the `antigravity-` prefix (e.g. `antigravity-gemini-3-flash`). To ensure strict adherence to the OpenCode `models.dev` JSON schema and to use the plugin's modern native routing engine, **this configuration deliberately avoids those legacy prefixes.**

Instead, we use standard slugs for Gemini and specific proxy slugs for Claude:

### 1. Gemini Models

Use standard schema slugs like `"google/gemini-3-flash-preview"` and `"google/gemini-3.1-pro-preview"`.

The plugin's internal resolver will automatically intercept these and default to routing them through the internal Antigravity endpoint. If your Antigravity quota is exhausted, the plugin automatically falls back to the public Gemini CLI endpoint.

### 2. Claude Models (via Google)

Google's public API does not host Anthropic's Claude. However, the Antigravity proxy does.

To trick OpenCode into routing a Claude request to the `google` provider, the plugin exposes specific "proxy" aliases prefixed with `gemini-claude-`.

You must use these exact custom slugs:

- `"google/gemini-claude-sonnet-4-6"`
- `"google/gemini-claude-opus-4-6-thinking"`

The plugin will intercept these, strip the `gemini-` compatibility prefix, and route the request to Claude using your Google credentials. Note: these specific proxy slugs must be injected into the JSON schema during the config build pipeline because they are non-standard.

### Reference

See the plugin's repository and source code for details on the routing fallback logic and the `MODEL_ALIASES` definitions:
[https://github.com/NoeFabris/opencode-antigravity-auth#readme](https://github.com/NoeFabris/opencode-antigravity-auth#readme)
