import type { Plugin } from '@opencode-ai/plugin';

// Store lint feedback by sessionID for injection via system transform
const lintFeedback = new Map<string, string>();

export const LintPlugin: Plugin = async ({ client, $, directory }) => {
  return {
    // 1. After tool execution, check for lint issues and store feedback
    'tool.execute.after': async (input) => {
      if (input.tool === 'edit' || input.tool === 'write') {
        const filePath = input.args.filePath as string;
        const sessionID = input.sessionID;

        // Check Python files
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

            lintFeedback.set(
              sessionID,
              `Python lint/format check failed for ${filePath}:\n\n${feedback}\n\nYou should run the 'format' tool or fix the issues manually.`,
            );
          }
        }

        // Check justfiles
        if (filePath.endsWith('justfile') || filePath.includes('justfile')) {
          await client.app.log({
            service: 'lint-plugin',
            level: 'info',
            message: `Syntax checking justfile`,
          });

          const justResult =
            await $`just --unstable --fmt --check --justfile ${filePath}`.nothrow();

          if (justResult.exitCode !== 0) {
            lintFeedback.set(
              sessionID,
              `Justfile check failed: ${justResult.stderr.toString()}\n\nYou should run the 'format' tool or fix the issues manually.`,
            );
          }
        }
      }
    },

    // 2. Before LLM processes messages, inject lint feedback as system message
    'experimental.chat.system.transform': async (input, output) => {
      const sessionID = (input as { sessionID?: string }).sessionID ?? '';

      if (sessionID && lintFeedback.has(sessionID)) {
        const feedback = lintFeedback.get(sessionID)!;
        output.system.push(`[LINT FEEDBACK]\n${feedback}`);
        lintFeedback.delete(sessionID); // Clear after injection
      }
    },
  };
};
