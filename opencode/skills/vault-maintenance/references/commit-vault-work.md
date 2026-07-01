# Commit Vault Work

The normal end state is an empty vault worktree with all validated changes committed.

1. Re-run the checks that match the touched surfaces:

   ```bash
   agent-memory doctor
   agent-memory plan validate
   ```

2. Stage the validated vault changes:

   ```bash
   git -C <vault> add --all .
   git -C <vault> diff --cached --stat
   ```

3. Commit with a message that names the durable state change, not the recovery mechanics:

   ```bash
   git -C <vault> commit -m "<scope>: <durable memory change>"
   ```

4. Confirm the vault is clean:

   ```bash
   git -C <vault> status --short
   ```

If the commit fails, return to the repair workflow with the exact Git stderr.
If validation fails, do not commit; repair first or surface the blocker.
