# Proof: Heart of the Empire (Logical Elimination)

This proof is written to be checkable against the evidence under `../case/`.

## Claim

The unique culprit is **Mr. Green**.

## Evidence Premises

P1. After the incident, the ballroom case is closed, locked, and undamaged. (`../case/locations/ballroom/scene-report.md`)

P2. After the incident, the ballroom case contains a glass replica with tag `WS-02 / Batch 14`. (`../case/locations/ballroom/scene-report.md`)

P3. The lock audit shows the case was opened and closed with `key_id=GRN-1` at 19:58:46..19:59:03. (`../case/locations/ballroom/lock-audit.txt`)

P4. `GRN-1` is the museum curator's key issued to **Mr. Green**. (`../case/locations/ballroom/lock-audit.txt`)

P5. A guard reports observing **Mr. Green** unlock, open, close, and re-lock the case at ~19:58:45, and that no other guest crossed the velvet rope during that minute. (`../case/locations/ballroom/scene-report.md`)

P6. The museum workshop log shows the replica `WS-02 / Batch 14` was signed out and later returned by the curator badge `GRN`. (`../case/locations/museum/workshop-log.md`)

P7. Only the curator can sign replicas out of the workshop. (`../case/locations/museum/workshop-log.md`)

P8. The museum security log shows only badge `GRN` accessed the vault at 20:05..20:20, and the curator badge requires fingerprint match (no failed reads). (`../case/locations/museum/security-log.txt`)

## Deductions

D1 (Swap occurred). From P2, the real diamond mount is not in the case after the incident, while a replica is. Therefore, the incident involved replacing the real item with the replica.

D2 (Who accessed the case). From P3 and P4 (and corroborated by P5), the person who opened the case in the critical pre-blackout minute was **Mr. Green**.

D3 (Who could supply that exact replica). From P6 and P7, the only person with authorized ability to obtain the replica tagged `WS-02 / Batch 14` is the curator; among suspects, that is **Mr. Green**.

D4 (Who hid the real item). From P8, the only person who accessed the museum vault immediately after the incident window was **Mr. Green**, consistent with storing the real item there.

## Uniqueness

Assume, for contradiction, some suspect `S != Mr. Green` performed the swap.

- By P3/P4/P5, the case opening event at 19:58:46..19:59:03 is attributable to Mr. Green using `GRN-1`, and no other guest had access behind the rope during that minute. So `S` could not have performed the swap.
- By P6/P7, the specific replica left in the case is obtainable only by the curator, again pointing to Mr. Green.

Thus any `S != Mr. Green` contradicts the evidence. Therefore the culprit is uniquely **Mr. Green**.

## Machine-checkable version

See `./proof.smt2`.
