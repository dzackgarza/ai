import type { Plugin } from '@opencode-ai/plugin';

export const LintPlugin: Plugin = async ({ client, $ }) => {
  return {
    'tool.execute.after': async (input) => {
      // 1. Check if tool was an edit or write
      if (input.tool === 'edit' || input.tool === 'write') {
        const filePath = input.args.filePath as string;

        // 2. Lint/Format Python files
        if (filePath.endsWith('.py')) {
          await client.app.log({
            service: 'lint-plugin',
            level: 'info',
            message: `Linting/Formatting Python file: ${filePath}`,
          });

          await $`uvx ruff check --fix --quiet ${filePath}`.nothrow();
          const fmtResult = await $`uvx ruff format --quiet ${filePath}`.nothrow();

          if (fmtResult.exitCode !== 0) {
            const feedback = fmtResult.stderr.toString();
            await client.session.promptAsync({
              path: { id: input.sessionID },
              body: {
                parts: [
                  {
                    type: 'text',
                    text: `Ruff format feedback for ${filePath}:\n\n${feedback}`,

                  },
                ],
              },
            });
          }
        }

        // 3. Lint/Format Justfiles
        if (filePath.endsWith('justfile') || filePath.includes('justfile')) {
          await client.app.log({
            service: 'lint-plugin',
            level: 'info',
            message: `Linting/Formatting justfile`,
          });

          // Attempt to format justfile automatically
          const justResult = await $`just --unstable --fmt`.nothrow();

          if (justResult.exitCode !== 0) {
            await client.session.promptAsync({
              path: { id: input.sessionID },
              body: {
                parts: [
                  {
                    type: 'text',
                    text: `Justfile formatting failed: ${justResult.stderr.toString()}`,

                  },
                ],
              },
            });
          }
        }
      }
    },
  };
};
