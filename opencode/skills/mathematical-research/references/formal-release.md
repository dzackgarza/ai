# Formal Release Engineering

Owner file for turning a banked result into a public, machine-audited formal
release. Parent: [[mathematical-research/SKILL|mathematical-research]]. Second
grounding source: `github.com/rishigajjala/erdos-796-lean` — a model-generated,
human-verified Lean proof of the corrected second-order form of Erdős
Problem 796, released with an executable audit.

## Statement freeze

- The problem statement is its own module and asserts no solution ("this
  module formalizes only the corrected problem statement; it does not assert a
  solution"). Definitions, statement, and proof separate, so the claim can be
  audited without reading the proof.
- Before the proof-completion endgame, freeze the statement-defining files and
  record their SHA-256; the release audit verifies them byte for byte
  ("preserved byte for byte in this release"). Late proof work then cannot
  silently weaken the goal it must reach.
- Encode asymptotics as filter limits of normalized errors
  (`Tendsto (fun n => (g n - leading n) / scale n) atTop (𝓝 c)`), with a note
  on why finitely many degenerate small cases cannot affect the limit.

## The executable release audit

One script, run locally and by CI on every push; the README badge is the
continuously re-verified claim. Three gates:

1. **Prohibited-token scan** over the project source with word-boundary
   regexes: `sorry`, `admit`, custom `axiom`, `unsafe`, `native_decide`,
   `interval_decide`. Any hit fails the release.
2. **Closure build** of the single assembly module (`FullProof`) that imports
   the independently proved components and exposes the release theorems. The
   audit imports only that module.
3. **Zero-trust axiom report**: `lake env lean --trust=0 Audit.lean`, where
   `Audit.lean` is a checked-in file of `#print axioms` lines for the named
   release theorems — with **exact-count verification**: the count of
   expected standard-axiom lines AND the count of all axiom-report lines must
   both equal N, so one theorem with the wrong axioms cannot hide among N−1
   passes.

CI additionally replays through an external checker (`leanchecker: true`) and
pins action versions by commit SHA.

Hardening upgrades from the 2026 Erdős-resolution ecosystem:

- **Scope scans to the import closure, not the repo.** A whole-repo token grep
  lies in both directions: library scaffolding can hold `axiom`s and
  `native_decide` outside the release theorem's import closure (false fatal),
  and imports can carry `sorryAx` in (false trust). The scan target is the
  frozen theorem's transitive closure — or the axiom report, which already is.
- **Make the scanner comment-aware**: strip block/line comments, string and
  char literals before matching, so retired-route commentary does not trip the
  gate; emit a machine-readable committed audit artifact (`source-audit.json`).
- **Prefer the in-Lean axiom freeze** over regex-scraping printed output:
  `#guard_msgs in #print axioms <thm>` with the expected axiom list embedded —
  the elaborator itself fails the build on drift; no text parsing to fool.
- **Add a statement-correspondence gate.** Hash-freezing the statement does
  not verify the proof proves *that* statement; the `leanprover/comparator`
  Challenge/Solution protocol does, with a second independent kernel —
  [[mathematical-research/references/statement-fidelity|statement-fidelity]].

## Dependency trust is closure-level

- Pin every dependency to an exact commit in the lakefile and repeat the
  commits in the audit document.
- Both conflations are wrong: a dirty upstream (unrelated `sorry`s in an
  imported package) does not taint your theorems, and a clean scan of your own
  repo does not certify them — imports can carry `sorryAx` into the closure.
  Only the axiom report over the transitive closure decides.
- Say the boundary out loud, as the source audit does: "a theorem-level
  claim, not a blanket claim about every declaration in an upstream package."

## Admitted axioms as honest gap-markers

When a needed input provably exists in the literature but not in Mathlib, a
**named, cited `axiom`** beats both alternatives — a `sorry` (opaque, shameful,
un-greppable) and silently strengthened hypotheses (dishonest):

- The docstring carries the verbatim source statement, pinned to edition,
  page, and equation, plus why the API gap forces the axiom ("Mathlib defines
  categorical `Tor` but has neither this tensor lemma nor the required
  additivity API; we record exactly that missing source-level input").
- It surfaces *by name* in every dependent theorem's `#print axioms` — the
  dependence is machine-visible forever.
- Keep a per-axiom provenance ledger distinguishing **verified directly
  against the primary source** from **cited via a secondary**, including
  strength distinctions (a textbook's `o(1)` form vs the original's explicit
  `O(1/log t)` rate) — and make the axiom gate fail on any admitted axiom
  with no ledger entry.
- Then say what you have: "0 sorries plus 3 admitted axioms" is a
  **conditional** result, not an axiom-clean one; the conditionality goes in
  every claim surface ([[mathematical-research/references/claim-status|claim-status]]).

## Do not refactor the audited closure

After verification the module layout is frozen. Navigation and exposition
improvements go into an external proof map (`docs/PROOF_MAP.md`: modules
grouped by mathematical role plus a dependency diagram) — never into
rewriting the audited import graph. Renames and reorganizations reopen the
audit.

## Release repo vs process archive

A public release repo may squash its history into a clean artifact. Then the
audit document must carry the process facts history no longer shows: audit
date, frozen statement hashes, dependency commits, and what the chosen proof
route deliberately avoids. Release-packaging idioms worth copying: a
**whole-tree `SHA256SUMS`** (source, scripts, CI, manifests — tampering with
the gates themselves becomes detectable, not only the statement);
**tag-triggered verification** with the CI-verified commit SHA and run URL
recorded in the audit document; and when local verification was impossible,
saying so and designating CI the trust anchor ("the first green Actions run
is the reproducible public kernel check"). The process archive (handoff bundles, run ledgers —
[[mathematical-research/references/handoff|handoff]]) is a different artifact
and lives elsewhere; do not conflate the two, and do not ship the process
archive as the release.

## Explicit-constant certificates in the kernel

- Ban native computation from release closures; use `decide` only on small
  finite facts.
- Numeric bounds on transcendental quantities decompose as: finite
  exact-rational cutoff certificate + coarse tail estimate, kernel-checked
  through algebraic sandwiches — e.g. `log((1+z)/(1−z)) ≥ 2(z + z³/3)` turns
  lower bounds on `log p` into rational arithmetic plus a pinned `log 2`,
  dischargeable by `norm_num`/`linarith`.
- Name the classical inputs the route deliberately avoids ("does not assume
  an Euler-product identity") — every avoided input shrinks the trust surface
  a referee must check.
- Factor certificates as conditional theorems whose obligation interface is
  explicit in the statement (`…_of_uniform_majorant (hBound : …)
  (hSummable : …)`), with the obligations discharged by separately proved
  modules. The certificate's trust interface is then visible without reading
  its proof.
- A theorem may be unconditional while its constant is only bracketed: define
  the constant, prove the theorem about it, and certify bounds
  (`4/15 ≤ Γ < 13`) as separate claims with their own ledger rows
  ([[mathematical-research/references/claim-status|claim-status]]).

## Disclosure and provenance

- Disclose AI authorship on every surface: README, `NOTICE`, and the paper
  itself ("the initial proofs were generated and formalized in Lean by
  <model>; the authors then verified and rewrote them").
- Keep a `docs/REFERENCES.md` mapping the problem's provenance — including
  the source of any *corrected* formulation being solved — and each imported
  formalized route to its human-authored source, down to crediting the note a
  library's proof was based on.
