import type { Plugin } from '@opencode-ai/plugin';

export const LintPlugin: Plugin = async ({ client, $ }) => {
  return {
    'tool.execute.after': async (input) => {
      // 1. Check if tool was an edit or write
      if (input.tool === 'edit' || input.tool === 'write') {
        const filePath = input.args.filePath as string;

        // 2. Syntax check Python files
        if (filePath.endsWith('.py')) {
          await client.app.log({
            service: 'lint-plugin',
            level: 'info',
            message: `Syntax checking Python file: ${filePath}`,
          });

          const checkResult = await $`uvx ruff check --quiet ${filePath}`.nothrow();
          const fmtResult =
            await $`uvx ruff format --check --quiet ${filePath}`.nothrow();

          if (checkResult.exitCode !== 0 || fmtResult.exitCode !== 0) {
            const feedback = [
              checkResult.exitCode !== 0
                ? `Ruff check issues:\n${checkResult.stdout.toString()}${checkResult.stderr.toString()}`
                : '',
              fmtResult.exitCode !== 0
                ? `Ruff format issues (file needs formatting)`
                : '',
            ]
              .filter(Boolean)
              .join('\n\n');

            await client.session.promptAsync({
              path: { id: input.sessionID },
              body: {
                parts: [
                  {
                    type: 'text',
                    text: `Python lint/format check failed for ${filePath}:\n\n${feedback}\n\nYou should run the 'format' tool or fix the issues manually.`,
                  },
                ],
              },
            });
          }
        }

        // 3. Syntax check Justfiles
        if (filePath.endsWith('justfile') || filePath.includes('justfile')) {
          await client.app.log({
            service: 'lint-plugin',
            level: 'info',
            message: `Syntax checking justfile`,
          });

          // Check justfile syntax and formatting
          const justResult =
            await $`just --unstable --fmt --check --justfile ${filePath}`.nothrow();

          if (justResult.exitCode !== 0) {
            await client.session.promptAsync({
              path: { id: input.sessionID },
              body: {
                parts: [
                  {
                    type: 'text',
                    text: `Justfile check failed: ${justResult.stderr.toString()}\n\nYou should run the 'format' tool or fix the issues manually.`,
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
