/**
 * Provider routing for TypeScript plugins that construct OpenAI-compatible clients directly.
 *
 * ⚠️  CANONICAL SOURCE: scripts/llm/providers.py owns the provider registry.
 *     This file mirrors slugs, baseURLs, and env var names from that module's PROVIDERS dict.
 *     When updating a provider entry, update scripts/llm/providers.py first, then mirror here.
 *
 * This file provides:
 *   - endpointFor()  — resolve a slug to baseURL + apiKey for direct OpenAI client use
 *   - parseModel()   — parse an OpenCode session API model spec string
 *
 * Most LLM calls should go through utilities/shared/llm.ts (Python bridge) instead of
 * constructing OpenAI clients here. Only use endpointFor() for streaming or non-classification
 * calls that cannot be routed through the Python bridge.
 */

// ---------------------------------------------------------------------------
// Provider routing
// ---------------------------------------------------------------------------

export interface ProviderEndpoint {
  baseURL: string;
  modelId: string;
  apiKey: string;
}

/**
 * Resolves a model slug to its provider endpoint.
 *
 * Slug prefix convention:
 *   (none)    → OpenRouter  (https://openrouter.ai/api/v1)
 *   groq/     → Groq        (https://api.groq.com/openai/v1)
 *   nvidia/   → NVIDIA NIM  (https://integrate.api.nvidia.com/v1)
 *   ollama/   → Ollama      (http://localhost:11434/v1, no auth needed)
 */
export function endpointFor(model: string): ProviderEndpoint {
  if (model.startsWith("ollama/")) {
    return {
      baseURL: "http://localhost:11434/v1",
      modelId: model.slice("ollama/".length),
      apiKey: "ollama",
    };
  }
  if (model.startsWith("groq/")) {
    return {
      baseURL: "https://api.groq.com/openai/v1",
      modelId: model.slice("groq/".length),
      apiKey: process.env.GROQ_API_KEY ?? "",
    };
  }
  if (model.startsWith("nvidia/")) {
    return {
      baseURL: "https://integrate.api.nvidia.com/v1",
      modelId: model.slice("nvidia/".length),
      apiKey: process.env.NVIDIA_API_KEY ?? "",
    };
  }
  // Default: OpenRouter
  return {
    baseURL: "https://openrouter.ai/api/v1",
    modelId: model,
    apiKey: process.env.OPENROUTER_API_KEY ?? "",
  };
}

// ---------------------------------------------------------------------------
// OpenCode model spec parsing
// ---------------------------------------------------------------------------

export interface ModelSpec {
  providerID: string;
  modelID: string;
}

/**
 * Parses an OpenCode model spec string (e.g. "openrouter/anthropic/claude-3-5-sonnet")
 * into { providerID, modelID } for use with the OpenCode session API.
 *
 * Returns undefined if the string is falsy or has no slash.
 */
export function parseModel(model?: string): ModelSpec | undefined {
  if (!model) return undefined;
  const [providerID, ...rest] = model.split("/");
  if (!providerID || rest.length === 0) return undefined;
  return { providerID, modelID: rest.join("/") };
}
