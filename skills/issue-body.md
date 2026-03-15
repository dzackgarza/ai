## Problem

Currently, the `/plannotator-annotate` slash command requires a specific file path as an argument. This is problematic because:

1. Users may not know the exact file path
2. Vague descriptions like "the test file" or "the design doc" fail
3. The current error handling just logs and exits — no helpful feedback

## Proposed Solution

### 1. New Agent Tool: `plannotator_annotate`

Add a new tool to the OpenCode plugin that kicks off the plannotation process:

```typescript
plannotator_annotate: tool({
  description:
    "Present a markdown document to the user for live annotation and feedback. Use this whenever you want to show a file to the user so they can review, annotate, and give corrections in real-time.",
  args: {
    file_path: tool.schema
      .string()
      .describe("Path to the markdown file to present for annotation"),
  },
  async execute(args) {
    // Call startAnnotateServer with the resolved file
    // After starting, respond to the user with the URL and ask them to review
  },
});
```

**Key behavior:**

- After starting the server, the tool should tell the agent to give the user the URL and wait for their feedback
- The tool can be called directly by the agent at any time (not just via slash command)

### 2. Update Slash Command

Change `/plannotator-annotate` to accept a **plain-text description** instead of a file path:

**New command message:**

```
The Plannotator Annotate UI has been triggered. Opening the annotation UI at http://localhost:19432/...

I want to annotate a markdown file. Please find the file I am describing and call the `plannotator_annotate` tool with the correct file path.

Description: [user input from the slash command]
```

The agent can then:

1. Search for files matching the description
2. Use glob/read/search tools to find the right file
3. Call `plannotator_annotate` with the resolved path

### 3. Tool Response Template

The tool response should tell the agent what to say to the user:

```
Started annotation server at http://localhost:19432/

Please share this URL with the user and ask them to review the document. The UI will open in their browser. When they submit feedback, it will be sent back to this session.
```

## Additional: Tool for Code Review

Similarly, there should be a tool for kicking off the git diff review UI:

```typescript
plannotator_review: tool({
  description:
    "Present git diff changes to the user for live code review and feedback. Use this whenever you want to show code changes to the user so they can review and annotate specific lines.",
  args: {
    diff_type: tool.schema
      .string()
      .describe(
        "Type of diff to review: uncommitted, staged, last-commit, or branch vs default",
      ),
  },
});
```

The tool should:

1. Run `git diff` with the specified type
2. Start the review server
3. Tell the agent to share the URL with the user and wait for feedback

This enables agents to trigger code review at any time, not just via the slash command.

## Benefits

- **Better UX**: Users can describe files naturally ("the test for the auth module")
- **Agent discretion**: The agent finds the file, not a brittle glob match
- **Leverages agent tools**: Uses the agent's existing search/glob capabilities
- **Consistency**: Matches how `submit_plan` tool works for plan review
- **Standalone use**: Agents can call the tool directly anytime they want user feedback

## Implementation Notes

- The tool should reuse existing `startAnnotateServer()` logic
- Should handle file-not-found gracefully (agent can try another file)
- Consider adding file browser/selector UI as an enhancement
- The slash command should still provide the URL in the initial prompt

## Related

This approach mirrors how `submit_plan` works: the slash command prompts the agent to do the work, and the agent uses tools to accomplish the task.
