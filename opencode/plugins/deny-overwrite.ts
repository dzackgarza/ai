import type { Plugin } from '@opencode-ai/plugin';

export const DenyOverwritePlugin: Plugin = async () => {
  return {
    'tool.execute.before': async (input) => {
      if (input.tool !== 'write') return;

      const filePath = (input as any).args?.filePath as string | undefined;
      if (!filePath) return;

      const exists = await Bun.file(filePath).exists();
      if (exists) {
        throw new Error(
          `Refusing to overwrite existing file '${filePath}'. Use the 'edit' tool to perform precise modifications instead.`
        );
      }
    },
  };
};
