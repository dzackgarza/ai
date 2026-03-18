import type { Plugin } from '@opencode-ai/plugin';

export const DenyOverwritePlugin: Plugin = async ({ client, $ }) => {
  return {
    'tool.execute.before': async (input) => {
      // 1. Intercept only the 'write' tool
      if (input.tool !== 'write') return;

      const filePath = input.args?.filePath as string | undefined;
      if (!filePath) return;

      // 2. Check if the file already exists
      const exists = await Bun.file(filePath).exists();

      if (exists) {
        // 3. Deny the operation with the required message
        throw new Error(
          `Cannot overwrite ${filePath}: this file already exists. ` +
            `Agents should not overwrite entire files. Instead, use the 'edit' tool ` +
            `to modify the file and minimize the diff you are introducing.`,
        );
      }
    },
  };
};
