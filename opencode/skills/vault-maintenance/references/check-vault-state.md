# Check Vault State

Use this before deciding what kind of recovery is needed.

1. Identify the vault path from the current repository:

   ```bash
   agent-memory inspect paths --scope both --format json
   ```

2. Inspect Git state directly:

   ```bash
   git -C <vault> status --short
   git -C <vault> diff --stat
   git -C <vault> diff --cached --stat
   ```

3. Inspect the touched content, not only filenames:

   ```bash
   git -C <vault> diff
   git -C <vault> diff --cached
   ```

4. Run the repository-owned vault checks:

   ```bash
   agent-memory doctor
   agent-memory plan validate
   ```

Report the exact dirty paths and failing command if these commands cannot run.
A missing dependency, malformed card, broken index, or commit failure is still a vault recovery task; it is not permission to resume normal memory work.
