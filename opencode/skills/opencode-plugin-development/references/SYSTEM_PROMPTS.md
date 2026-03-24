# System Prompt Injection for Plugins

Plugins add system prompts to chat through the `experimental.chat.system.transform` hook, which allows them to modify the system prompt array before it's sent to the LLM.

## How It Works

### 1. Hook Interface

Plugins implement the `experimental.chat.system.transform` hook which receives:

- **input**: Contains `sessionID` and model information
- **output**: Contains a `system` string array that can be modified

### 2. System Prompt Construction

In the session prompt flow, the system prompt is built from multiple sources:

1. Environment context
2. Agent skills
3. Instruction prompts

### 3. Plugin Hook Execution

After building the initial system prompt, the system triggers the plugin hook to allow modifications.

## Example Plugin

```typescript
import type { Plugin } from '@opencode-ai/plugin';

export const CustomSystemPromptPlugin: Plugin = async (ctx) => {
  return {
    'experimental.chat.system.transform': async (input, output) => {
      // Add custom system prompts
      output.system.push(
        'You are an expert in TypeScript and React development.',
        'Always provide type-safe code examples.',
        'Consider performance implications in your suggestions.',
      );
    },
  };
};
```

The plugin can modify the `output.system` array by:

- Pushing new prompts
- Removing existing ones
- Reordering the entire array

This allows customization of system prompt behavior for the chat session.

## Notes

- This is an **experimental hook** (`experimental.chat.system.transform`) as indicated by its name
- The hook is called **after** the default system prompt components are assembled but **before** it's sent to the LLM
- Plugins have **full control** over the system prompt array and can completely replace it if needed
- The hook receives session context which allows for conditional system prompt modifications based on the specific session or model being used
