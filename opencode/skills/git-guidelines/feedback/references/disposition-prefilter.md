# Disposition Pre-Filter

Role B runs this gate on EVERY finding **before** choosing a four-way disposition
(Phase 2.5). It converts the Global Principles and Triage Rubric into a forced
first move, so a disposition is reached from policy, not from argument-from-priors.

The disposition reply MUST carry one line recording which gate rule fired (see
Recorded Result). That line is the proof the gate ran.

## Gate 1 — Threat-model relevance

The review apparatus targets **slop**, not generic correctness/perf/style. Slop is:
fake / fallback / default / mock behavior that stops the app failing when it
should; error-hiding or fail-slow paths (the user never learns of a real failure);
cross-file fragility (the next small change breaks many files); tests that prove
nothing; the app lying to the user.

- Finding implicates a slop pattern, OR a real correctness/proof issue (stale-state
  race, swallowed error, type/proof-surface gap, unbounded hang) → **in scope**,
  continue to Gate 2.
- Finding is a generic bug / perf / style preference with no slop pattern and no
  real correctness/proof implication → **Reject (out of scope)**; cite Principle #6.

Do not reject a real correctness/proof issue merely because a generic bot raised it
(Principle #2).

## Gate 2 — Forced-disposition table (first match wins; STOP at first match)

| Finding shape | Forced disposition |
| --- | --- |
| micro-opt: "faster", "cache this", "recompile per request", "make async", with NO logged/reproduced user-visible perf problem | **Reject** (Principle #6). Carve-out: if the SAME finding also names a fail-loud/proof gap, keep only that part as accept-with-modified-remediation and reject the perf framing. |
| suggests fallback / default / mock / skip / graceful-degrade / silent coercion | **Reject** (anti-slop / Principle #1). |
| describes actual slop (catch-all `.catch`, fallback, default, mock, fail-slow, stringly error) but frames it as a generic bug | **Accept**, re-named as the slop it is. Remediation REMOVES the slop (fail-loud / distinct typed errors / propagate), it does not add handling. |
| suggests adding `try/catch` or broadened error-handling around a throw | **Accept with modified remediation** = fail EARLIER / stronger assertion. Never add a swallow. |
| suggests an in-code constant table where the project drives constants from config | **Accept with modified remediation** (config-driven), or Reject if there is no real divergence harm. |
| enterprise hardening / sandbox / path-traversal / symlink-escape on single-user bespoke software | **Reject** (Principle #7) unless the app owns an explicit security boundary. |
| flags an optional / nullable / absent-data output or contract field | apply the **Optional-Field Axiom** below. |
| resolves by deletion | Principle #9 — the deletion must transfer the original burden. |
| guarded cast: a membership check that throws on miss, then casts (e.g. `ITEMS.includes(x)` then `x as T`) | **Reject** — this is fail-loud crash-at-the-boundary, not cast-as-validation. |

## Optional-Field Axiom

Default: a field is **required** and the data is fixed so it is always present.
Genuine absence is a narrow, explicitly-modeled case — not a shared `optional` that
every consumer must tolerate.

- A finding that an output/contract field is optional/nullable is **accepted**
  unless the declaration justifies the absence as a genuine, irreducible domain
  state.
- "Models real absent data" is **not** a sufficient justification by itself. State
  WHY the data is irreducibly absent and why require-and-fix is wrong. Absent that,
  the optional weakens the interface for everyone → accept (require + fix the data,
  or model true-absence as its own type). Do not defend the optional from priors.

## Gate 3 — Remediation-suggestion policy check

Even when the CLAIM is true, if the reviewer's SUGGESTED fix would add a fallback,
default, mock, in-code constant, defensive catch, or cast, the disposition is
**Accepted with modified remediation** (never "as written"). The modified
remediation restores fail-loud / config-driven / proof.

## Recorded Result (mandatory)

The disposition reply includes exactly one line:

`Pre-filter: <the gate rule that fired> | in-scope, no short-circuit`

Examples: `Pre-filter: Gate 2 micro-opt without logged perf issue -> reject` /
`Pre-filter: in-scope, no short-circuit -> four-way below`.

## Worked Examples

- "Regex recompiled on every from-source POST", no logged perf issue → Gate 2
  micro-opt → reject the perf framing; if it also notes the pattern is not
  validated at startup, keep only that (compile once at load, fail loud there).
- Catch-all `.catch` collapsing every error into one kind → Gate 2 actual-slop-
  framed-as-bug → accept, named as error-domain-flattening; remediation = distinct
  fail-loud kinds / propagate, not more handling.
- `icon: z.string().optional()` defended as "a genuinely-optional UI field" →
  Optional-Field Axiom → that is not a sufficient justification; require + fix
  unless irreducible absence is shown.
