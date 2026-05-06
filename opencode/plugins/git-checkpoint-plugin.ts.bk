import type { Plugin } from '@opencode-ai/plugin';

export const GitCheckpointPlugin: Plugin = async ({ client, $ }) => {
  return {
    'tool.execute.before': async (input) => {
      // 1. Strictly intercept only the 'edit' tool
      if (input.tool !== 'edit') return;

      // 2. Verify we are in a git repository
      const gitCheck = await $`git rev-parse --is-inside-work-tree 2>/dev/null`
        .quiet()
        .nothrow();
      if (gitCheck.exitCode !== 0) return;

      // 3. Check if the current version differs from the latest committed version (repo-wide)
      const statusCheck = await $`git status --porcelain`.quiet().nothrow();
      const isDirty = statusCheck.stdout.toString().trim().length > 0;

      if (isDirty) {
        // 4. Block and demand a descriptive checkpoint commit
        throw new Error(
          `Cannot proceed with edit: the repository has uncommitted changes. ` +
            `You must first checkpoint the specific file you intend to touch: ` +
            `git add <file> && git commit -m "<message describing your current goal and how this edit advances it>". ` +
            `Do not stage unrelated files.`,
        );
      }
    },
  };
};
