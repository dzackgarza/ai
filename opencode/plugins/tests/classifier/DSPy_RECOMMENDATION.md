# DSPy for Task Classification

DSPy is recommended as a framework for **generating correct classification prompts** and **fine-tuning injected prompts** within the `prompt-router.ts` plugin.

## Purpose

- **Prompt Generation**: Use DSPy's optimizer to automatically arrive at the most effective static prompt for one-shot classification, replacing manual trial-and-error.
- **Fine-Tuning**: Use the `cases.yaml` dataset to systematically fine-tune the instructions injected into the agent's context for each tier.

## Workflow

1. Define the classification signature.
2. Optimize against the existing test cases to generate a manual static prompt.
3. Extract the winning prompt for use in the production plugin.
