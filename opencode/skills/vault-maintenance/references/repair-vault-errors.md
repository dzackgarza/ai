# Repair Vault Errors

Repair only after inspecting the dirty paths and the failing validation output.

1. Classify each dirty path:

   - intended memory or plan content from the interrupted operation;
   - generated index, DAG, metadata, or symlink state that should be regenerated;
   - malformed or partial content that must be corrected before commit;
   - unrelated local debris that must be surfaced as a blocker before proceeding.

2. Fix malformed memory files in their authored Markdown form.
   Preserve frontmatter fields, vault-relative links, and project/global scope directories.

3. Fix malformed plan cards in the card file itself, then rerun:

   ```bash
   agent-memory plan validate
   ```

4. Regenerate indexes or DAG artifacts only through the owning command when one exists.
   Do not hand-edit generated output unless the owning command is the failing surface and the manual edit is the smallest repair needed to unblock validation.

5. For commit failures, fix the failing Git condition in the vault and retry the commit workflow.
   Examples include a broken signing agent, invalid vault Git config, or an interrupted index.
   Keep the repair in the vault; do not route around the failure with a different storage location.

If the right repair is unclear, stop with the dirty path list, the inspected diff summary, and the exact failing command.
