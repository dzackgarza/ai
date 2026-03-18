# Memory: OpenCode Formatters Behavior

**Date:** March 18, 2026
**Tags:** OpenCode, formatters, agent feedback

## Summary

Formatter commands in OpenCode run automatically after file edits, but their outputs are completely discarded and never fed to the agent.

## Key Details

1. **Trigger:** Formats are triggered by the `File.Event.Edited` bus event
2. **Implementation File:** `/packages/opencode/src/format/index.ts` (lines 103-138)
3. **Process Spawn Configuration:**
   - `stdout: "ignore"`: All standard output from formatters is discarded
   - `stderr: "ignore"`: All standard error from formatters is discarded
4. **Error Handling:** Only the exit code is checked; failures are logged but not communicated to the agent
5. **Available Formatters:** Prettier, Gofmt, Mix, Oxfmt (experimental), Biome, Zig, Clang-format, Ktlint, Ruff, Air (R lang), Uvformat, Rubocop, Standardrb, Htmlbeautifier, Dart, Ocamlformat, Terraform, Latexindent, Gleam, Shfmt, Nixfmt, Rustfmt, Pint (Laravel), Ormolu, Cljfmt, Dfmt

## Conclusion

Formatters ensure code style consistency but do not provide any feedback to the AI agent about the formatting process or results.
