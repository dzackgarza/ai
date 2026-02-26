# Completion Guidelines

When a task is completed in the OpenCode repository:

1. **Format & Lint**: Run the appropriate formatting and linting commands for the files touched.
   - For Python: `uvx ruff format` and `uvx ruff check --fix`.
   - For other files: `npx prettier --write`.
2. **Verify**: If the change involves model configurations or tool definitions, run the relevant test scripts (e.g., `./test-models-comprehensive.sh`) to ensure no regressions.
3. **Commit**: Use descriptive commit messages following the project's history style.
4. **Update Documentation**: If new models or tools are added, ensure `opencode.json` is updated and relevant test scripts are adjusted if necessary.
