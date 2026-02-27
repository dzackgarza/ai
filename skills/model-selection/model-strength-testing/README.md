# Model Strength Testing

One-shot benchmark tasks. Each task is a single prompt with recorded response.

Some tasks may have:

- A **system prompt** (attached context)
- A **directory restriction** (model confined to specific folder)

---

## Tasks

### 1. Coherence

Tests basic LLM processing - models often fail on these "trick" questions.

**Prompt:**

```
Answer the following questions:

1. How many 'R's are in the word "Strawberry"?
2. Count the number of times each letter appears in the word "Supercalifragilisticexpialidocious". Return the counts as a JSON object.
3. What is 3728 * 9241? Calculate step by step.
4. Which of these statements is TRUE?
   - The sky is blue.
   - The sky is NOT blue.
   - The sky is NOT green.
```

**Expected answers:**

1. 3
2. Accurate letter counts
3. 34,461,488
4. Third statement (sky is NOT green)

**Directory:** unrestricted

**Scoring:** All correct: Pass | Any incorrect: Fail

---

### 2. Model Version Knowledge

**Prompt:**

```
What are the current flagship model version numbers from:
1. Google (Gemini)
2. Anthropic (Claude)
3. OpenAI (GPT)

List each with their latest version number.
```

**Expected answers:**

- Google: Gemini 3+
- Anthropic: Claude 3.5+
- OpenAI: GPT-5+

**Directory:** unrestricted

---

### 3. Model Version Knowledge (With Search Instruction)

Same question as Task 2, but with a system prompt instructing the model to search the web.

**System Prompt:**

```
Your knowledge may be outdated. Before answering factual questions about current technology, you should search the web to verify current information.
```

**User Prompt:**

```
What are the current flagship model version numbers from:
1. Google (Gemini)
2. Anthropic (Claude)
3. OpenAI (GPT)

List each with their latest version number.
```

**Expected answers:**

- Google: Gemini 3+
- Anthropic: Claude 3.5+
- OpenAI: GPT-5+

**Directory:** unrestricted

**Scoring:** Compare to Task 2 - does the model now follow the instruction to search the web?

---

### 4. Epistemic Humility (OpenCode One-Shot Prompting)

Tests whether the model knows what it doesn't know and takes proper research steps.

**Prompt:**

```
How does one-shot prompting work in OpenCode?
```

**Directory:** unrestricted

**Positives (good research behavior):**

- Runs `opencode --help`
- Any web search or documentation search
- Checks for opencode binary

**Negatives (poor research behavior):**

- Searches current folder/repo (irrelevant to the task)
- Runs random subcommands or flags without knowing what they do

**Scoring:**

- Turn limit: 10 turns
- <10 turns + uses help/web search: Pass
- > =10 turns: Fail (too many mistaken leads)
- Searches repo instead of looking up docs: Fail

---

### 5. Truncated Search Results

Tests whether the model properly verifies information or gets fooled by summaries.

**Prompt:**

```
Does OpenCode support connecting to custom API endpoints with API key authentication?
```

**The trap:** Web search will turn up issue #3168: "Feature Request: Support for Generic/Custom Endpoints with API Key Authentication" - title suggests OpenCode _doesn't_ support this. But the issue was **closed as completed** - meaning it _does_ work now.

A truncated summary could make the model think the feature doesn't exist, when in fact it was implemented.

**Expected behavior:**

- Searches web for the feature
- Finds the GitHub issue
- Reads to the end/discovers it's closed as "completed"
- Correctly answers: Yes, it's supported

**Scoring:**

- Answers "yes, it's supported": Pass
- Answers "no, not supported" based on issue title alone: Fail

---

### 6. Task Adherence (Tool Usage)

Tests whether the model follows explicit tool usage instructions.

**Prompt:**

```
Answer the following question using ONLY web search:

Does OpenCode support custom agents when using `attach` to connect to a server?

Use websearch to find this information. Do not use kindly_get_content or any tool that fetches full page content. Just give your final answer after searching.
```

**The trap:** The model has access to both `websearch` and `kindly_get_content`, but is explicitly told to use ONLY `websearch` and not `kindly_get_content`.

**Expected behavior:**

- Uses ONLY `websearch` tool
- Does NOT use `kindly_get_content` or other fetching tools
- Provides final answer based on websearch results

**Scoring:**

- Uses ONLY websearch and gives answer: Pass
- Uses kindly_get_content or other fetching tools: Fail (violates explicit instruction)
- Uses websearch but also uses other tools: Fail (violates explicit instruction)

---

## Folder Tasks

Some tests require a restricted workspace where the model can only read a specific subdirectory.

- `model-strength-testing/folder-tasks/whodunnit-heart-of-empire/README.md`
- `model-strength-testing/folder-tasks/workflow-adherence-git-checkpoints/README.md`
- `model-strength-testing/folder-tasks/arxiv-proof-fidelity-2312-03638/README.md`

## Adding Tasks

1. Add task above with:
   - System prompt (if applicable)
   - User prompt
   - Expected behavior
   - Directory restriction (if any)
2. Run prompt against model
3. Record response and score
