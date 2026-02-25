# Style and Conventions

## Operating Rules (Hard Constraints)
1. **Edit Workflow**: Read → Commit Checkpoint → Edit → Verify.
2. **Safe Deletion**: NEVER use `rm`. Use `trash` or `gio trash`.
3. **Skills**: Mandatory scanning before any action. Load immediately if applicable.
4. **Project Start**: Always run `serena_activate_project` and `serena_read_memory`.
5. **No Time Estimates**: Never write time estimates in responses.

## Code Style
- Markdown for prompts and documentation.
- JSON/YAML for configuration files.
- Use absolute paths for all file operations.

## Communication Style
- Concise responses (fewer than 3 lines of explanation).
- No emojis or filler phrases.
- Reference code in `file_path:line_number` format.
- Use `todowrite` for all nontrivial tasks (5+ items).