// Injects env vars into shell execution
export const InjectEnvPlugin = async () => {
  return {
    "shell.env": async (input, output) => {
      output.env.MY_API_KEY = "secret";
      output.env.PROJECT_ROOT = input.cwd;
    },
  };
};
