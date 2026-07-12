# Check Vault State

Use this only after a concrete recovery trigger: an `agent-memory` commit or validation failure, or an explicit vault-repair request. A dirty worktree alone does not trigger recovery.

1. Identify the vault path from the current repository:

   ```bash
   agent-memory inspect paths --scope both --format json
   ```

2. Inspect Git state to identify paths involved in the observed failure:

   ```bash
   git -C <vault> status --short
   git -C <vault> diff --stat
   git -C <vault> diff --cached --stat
   ```

3. Inspect the affected content, not only filenames:

   ```bash
   git -C <vault> diff
   git -C <vault> diff --cached
   ```

4. Run the repository-owned vault checks:

   ```bash
   agent-memory doctor
   agent-memory plan validate
   ```

Report the affected paths and failing command if these commands cannot run. Preserve unrelated paths; they do not block normal memory work.
