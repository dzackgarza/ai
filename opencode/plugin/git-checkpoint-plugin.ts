import type { Plugin } from '@opencode-ai/plugin';

export const GitCheckpointPlugin: Plugin = async ({ client, $ }) => {
  return {
    'tool.execute.before': async (input, output) => {
      // Only intercept edit or write operations
      if (input.tool !== 'edit' && input.tool !== 'write') return;

      const filePath = input.args?.filePath as string | undefined;
      if (!filePath) return;

      // Check if we're in a git repository
      const gitCheck = await $`git rev-parse --is-inside-work-tree 2>/dev/null`
        .quiet()
        .nothrow();
      if (gitCheck.exitCode !== 0) {
        await client.app.log({
          service: 'git-checkpoint-plugin',
          level: 'debug',
          message: `Not in a git repo, skipping checkpoint for ${filePath}`,
        });
        return;
      }

      // Check if there are uncommitted changes to this file
      const diffCheck = await $`git diff --quiet HEAD -- ${filePath}`.quiet().nothrow();
      const hasChanges = diffCheck.exitCode !== 0;

      if (hasChanges) {
        // Block the edit and prompt the agent to make a descriptive checkpoint commit
        throw new Error(
          `Cannot edit ${filePath}: uncommitted changes detected. ` +
            `You must first make a descriptive checkpoint commit explaining your intentions before editing. ` +
            `Run: git add -A && git commit -m "your descriptive message here"`,
        );
      }

      await client.app.log({
        service: 'git-checkpoint-plugin',
        level: 'debug',
        message: `No uncommitted changes for ${filePath}, allowing edit`,
      });
    },
  };
};
