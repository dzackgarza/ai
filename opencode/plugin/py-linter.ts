import type { Plugin } from "@opencode-ai/plugin";

export const PyLinterPlugin: Plugin = async ({ client, $ }) => {
  return {
    "tool.execute.after": async (input) => {
      // 1. Check if tool was an edit or write and the file is a Python file
      if (
        (input.tool === "edit" || input.tool === "write") &&
        typeof input.args.filePath === "string" &&
        input.args.filePath.endsWith(".py")
      ) {
        const filePath = input.args.filePath;

        await client.app.log({
          service: "py-linter-plugin",
          level: "info",
          message: `Running linter on ${filePath}`,
        });

        // 2. Run the linter (using ruff)
        // .nothrow() prevents the plugin from crashing on non-zero exit codes
        const result = await $`ruff check ${filePath}`.quiet().nothrow();

        // 3. If linter found issues, prompt the agent with the output
        if (result.exitCode !== 0) {
          const linterFeedback =
            result.stdout.toString() || result.stderr.toString();

          await client.session.prompt({
            path: { id: input.sessionID },
            body: {
              parts: [
                {
                  type: "text",
                  text: `Linter feedback for ${filePath}:\n\n${linterFeedback}`,
                },
              ],
            },
          });
        }
      }
    },
  };
};
