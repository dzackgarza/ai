# Provider Validation Discrepancies - Action Plan

## 1. Providers to Ignore (Not in models.dev yet)
- **cursor-acp** - Add to ignore list with comment
- **qwen-code** - Add to ignore list with comment

## 2. OpenRouter - Update to match models.dev (non-free models)
- **Issue**: 8 symmetric difference
- **Action**: Remove 3 models not in models.dev, add 5 free models from models.dev
- **Models to remove**: aurora-alpha, sherlock-dash-alpha, sherlock-think-alpha
- **Models to add**: arcee-ai/trinity-large-preview:free, nvidia/nemotron-3-nano-30b-a3b:free, openai/gpt-5.3-codex, openai/gpt-5.4, openai/gpt-5.4-pro

## 3. OpenAI - Blacklist missing models
- **Issue**: 38 models missing from config
- **Action**: Add all missing models to blacklist
- **Models to blacklist**: codex-mini-latest, gpt-3.5-turbo, gpt-4, gpt-4-turbo, gpt-4.1, +33 more

## 4. Ollama-Cloud - Strip ":cloud" suffix
- **Issue**: Config uses ":cloud" suffix but models.dev doesn't
- **Action**: Remove ":cloud" suffix before validation comparison
- **Models affected**: deepseek-v3.2:cloud, glm-4.6:cloud, glm-4.7:cloud, glm-5:cloud, kimi-k2-thinking:cloud, +5 more

## 5. Google - Blacklist Gemini <3 variants
- **Issue**: 11 models in models.dev not in config (gemini-2.5-* variants)
- **Action**: Add gemini-2.5-* variants to blacklist
- **Models to blacklist**: gemini-2.5-flash-image, gemini-2.5-flash-image-preview, gemini-2.5-flash-lite, gemini-2.5-flash-lite-preview-06-17, gemini-2.5-flash-lite-preview-09-2025, +6 more

## 6. GitHub Copilot - List differences for manual review
- **Issue**: 6 models in config not in models.dev, 6 models in models.dev not in config
- **Action**: Document differences for manual decision

### Models in config but NOT in models.dev:
- claude-opus-4.6-fast-mode-preview
- gemini-3-flash
- gemini-3-pro
- gemini-3.1-pro
- goldeneye
- +1 more

### Models in models.dev but NOT in config:
- claude-opus-41
- gemini-3-flash-preview
- gemini-3-pro-preview
- gemini-3.1-pro-preview
- gpt-5
- +1 more

## 7. Anthropic - Manual review needed
- **Issue**: 7 models missing from config
- **Action**: Review if these should be blacklisted (likely yes, as they're not free/strong enough for agentic tasks)

## 8. NVIDIA - Manual review needed
- **Issue**: 4 models in config not in models.dev
- **Action**: Review if these should be kept or removed

## Implementation Steps:

1. **Update validation script** to:
   - Add ignore list for cursor-acp and qwen-code
   - Strip ":cloud" suffix for ollama-cloud
   - Add proper handling for blacklist-only updates

2. **Update provider configs**:
   - openrouter.json - remove 3 models, add 5 free models
   - openai.json - add 38 models to blacklist
   - google.json - add gemini-2.5-* models to blacklist
   - ollama-cloud.json - remove ":cloud" suffix from models

3. **Document decisions** for manual review cases:
   - anthropic
   - nvidia
   - github-copilot