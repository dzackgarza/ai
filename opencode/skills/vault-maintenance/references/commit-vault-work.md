# Commit Vault Work

The dispatched subagent's recovery end state is a validated, pushed commit for the paths involved in recovery. Unrelated vault changes may remain untouched.

1. Re-run the checks that match the recovered surfaces:

   ```bash
   agent-memory doctor
   agent-memory plan validate
   ```

2. Stage only the validated recovery paths:

   ```bash
   git -C <vault> add -- <paths>
   git -C <vault> diff --cached --stat -- <paths>
   ```

3. Commit with a message that names the durable state change, not the recovery mechanics:

   ```bash
   git -C <vault> commit -m "<scope>: <durable memory change>" -- <paths>
   ```

4. Push the recovery commit:

   ```bash
   git -C <vault> push
   ```

5. Confirm that the recovery paths are clean:

   ```bash
   git -C <vault> diff -- <paths>
   git -C <vault> diff --cached -- <paths>
   ```

If the commit or push fails, return to the repair workflow with the exact Git stderr.
If validation fails, do not commit; repair first or escalate the exact failure to the parent.
