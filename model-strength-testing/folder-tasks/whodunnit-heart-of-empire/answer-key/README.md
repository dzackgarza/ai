# Answer Key: Heart of the Empire

This directory is intentionally outside `case/` so an agent can be restricted to `case/`.

## Solution

- **Culprit**: Mr. Green
- **Method**: Pre-position a museum workshop replica + use curator key `GRN-1` to open the case at ~19:58:46, swap the real mount for the replica, re-lock, then rely on the 20:00 blackout to mask attention.
- **Where now**: Museum vault

## Proof (Formalized Elimination)

Let:

- `R` = the real Heart of the Empire mount
- `G` = the glass replica
- `OpenedBy(x,t)` = lock audit shows key_id belonging to x opened the case at time t
- `HasAccessToWorkshop(x)` = x can sign out workshop replicas

Premises (from evidence):

P1. The case was closed, locked, undamaged after the incident. (`case/locations/ballroom/scene-report.md`)

P2. The item in the case after the incident was a glass replica with tag `WS-02 / Batch 14`. (`case/locations/ballroom/scene-report.md`)

P3. The lock audit records `LATCH_OPEN key_id=GRN-1` at 19:58:46 and `LATCH_CLOSE key_id=GRN-1` at 19:59:03. (`case/locations/ballroom/lock-audit.txt`)

P4. `GRN-1` is the museum curator key issued to Mr. Green. (`case/locations/ballroom/lock-audit.txt`)

P4b. A guard directly observed Mr. Green unlock, open, close, and re-lock the case at ~19:58:45, and observed that no other guest crossed the velvet rope during that minute. (`case/locations/ballroom/scene-report.md`)

P5. The museum workshop log shows replica `WS-02 / Batch 14` was signed out and later returned by curator badge `GRN`. (`case/locations/museum/workshop-log.md`)

P6. Only the curator can sign replicas out of the workshop. (`case/locations/museum/workshop-log.md`)

P7. The museum security log shows only `GRN` badge accessed the vault after the incident window (20:05 to 20:20). (`case/locations/museum/security-log.txt`)

Deductions:

D1. From P2, the theft involved a swap: `R` was removed and `G` was left in the case.

D2. From P3, P4, and P4b, Mr. Green opened the case at ~19:58:46 (and closed it at 19:59:03).

D3. From P5 and P6, Mr. Green is the only suspect with documented ability to obtain `G` (the tagged replica).

D4. Therefore Mr. Green had both the _means_ (curator key + workshop access to `G`) and _opportunity_ (opened the case) to perform the swap.

D5. From P7, Mr. Green was the only person who accessed the museum vault immediately after, consistent with hiding `R` there.

Uniqueness:

Assume some other suspect `S != Mr. Green` performed the swap.

- By P3/P4, the case was opened by `GRN-1` at the relevant time, contradicting `S` performing the swap without Mr. Green's key.
- By P5/P6, obtaining the exact tagged replica requires curator sign-out, contradicting `S` obtaining `G` without curator authority.

Thus no `S != Mr. Green` can satisfy the evidence simultaneously.

Red herring notes:

- Professor Elm has motive-like statements in `case/locations/lounge/witness-statement.md`, but no evidence ties Elm to `GRN-1` or `WS-02 / Batch 14`.
