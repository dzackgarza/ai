# Statement Fidelity

Owner file for the one soundness gap a proof kernel cannot close: **the kernel
verifies the proof against the formal statement, never that the formal statement
means what the informal problem says.** Every other gate in
[[mathematical-research/references/formal-release|formal-release]] assumes the
statement is right; this file owns making that assumption earn its keep.
Parent: [[mathematical-research/SKILL|mathematical-research]]. Grounded in the
2026 Erdős-resolution ecosystem: the `leanprover/comparator` protocol
(`kim-em/erdos-unit-distance`, `frenzymath/Anderson-Conjecture`,
`nick-kuhn/erdos-619`) and the `agenticsnz/unsorry` red-team findings.

## The Challenge/Solution protocol

The community-standard trust-minimization unit is a two-file split checked by
`leanprover/comparator`:

- **`Challenge.lean`** — imports *only* Mathlib, states the target theorem,
  and closes it with `sorry`. This is the **trusted statement anchor**: the
  one file a human must read. `sorry` here is deliberate and correct — the
  challenge file owns the statement, never a proof.
- **`Solution.lean`** — imports the untrusted proof library, re-declares the
  challenge's definitions verbatim, and closes the same-named theorem by
  definitional equality with the library's result.
- **`config.json`** — a declarative contract, not prose: challenge/solution
  module names, `theorem_names`, `permitted_axioms`
  (`["propext","Quot.sound","Classical.choice"]`).

Comparator rebuilds both modules in a sandbox (`landrun`), exports both with
`lean4export`, checks the solution theorem's type equals the challenge's,
checks the axiom set against the whitelist, and replays the proof through the
kernel — optionally through a second independent kernel (`nanoda`, Rust).
The resulting trust surface is stated in one line: *the Lean kernel, Mathlib,
`Challenge.lean`, and comparator itself; the proof library does NOT need to be
trusted.* This is strictly stronger than a statement-file SHA freeze: the
alignment is executable, and it catches definition drift between challenge
and solution automatically.

Operational notes:

- Turn the second kernel on. Both audited repos shipped `"enable_nanoda":
  false` — the independent-kernel replay was available and unused.
- Sandbox the verifier and **smoke-test the sandbox** before trusting its
  verdict (`erdos-619` runs `landrun … -add-exec echo hello` in CI first).
  Pin the sandbox to a released tag; a raw VCS revision can vanish.
- Any dev escape hatch must be env-gated and loud ("for non-adversarial
  wiring tests only").

## The trusted file is the whole trust surface — keep it small, audit it first

- Everything in `Challenge.lean` is trusted, **including its definitions**. A
  misformalized definition inside the challenge file is invisible to
  comparator (`Anderson-Conjecture` defines `IsQuasiComplete` inside the
  trusted file — a reviewer must check that definition by hand). Prefer
  Mathlib vocabulary; every bespoke definition in the trusted file is a new
  human obligation.
- **Audit the statement before spending prover time.** The cheapest,
  highest-leverage gate in the whole pipeline: a statement-level audit of
  `kim-em/erdos-unit-distance` caught two bugs in `key_inequality` before any
  prover compute. A wrong statement wastes every downstream token.
- Statements built on junk-value-defaulting functions can be silently
  trivial: `diam` maps disconnected graphs to `0`, `sInf`/`sSup` default to
  `0`, `Nat` subtraction truncates. Use total-honest forms (`ediam : ℕ∞`) and
  record the choice at the definition site with the reason (`erdos-619`).
- Two independent formalizations of "the same result" may prove **different,
  nested statements** — the unit-distance disproof exists in a weaker
  no-power-gain form (kim-em) and a stronger fixed-power-gain form (plby),
  and neither cites the other. Check statement identity before counting two
  artifacts as agreement.

## Vacuity and triviality attacks

Red-teamed against a live autonomous-merge system (`unsorry`), all sound at
the kernel and all wrong:

- **autoImplicit vacuity**: `theorem foo (h : p) (hn : ¬p) : ¬g` auto-binds
  `p g` as `∀ {p g : Prop}` — kernel-verified, `axioms: []`, meaningful name,
  vacuous content; the enabling option was split across two lines to defeat a
  per-line grep. Scan for `autoImplicit`/`relaxedAutoImplicit` over the
  **whole file, whitespace-collapsed** — never per-line.
- **True-but-trivial / renamed duplicate**: a one-shot `simp`/`decide` close,
  or a restatement of an existing Mathlib lemma under a new name. Machine
  probe: elaborate the statement under `import Mathlib` against a fixed
  tactic battery (`rfl | trivial | decide | norm_num | omega | simp |
  simp_all | aesop | ring | linarith | tauto`); with all of Mathlib in simp
  scope this also discharges renamed duplicates. Verdict is a trichotomy —
  and **a probe that fails to elaborate is not evidence of non-triviality**.
- **Weak-witness signatures**: `∃ _ : Witness, True` is kernel-fine and tells
  an auditor nothing; the payload is the structure's fields. Any statement
  check that reads only the final theorem's signature is fooled by a weak
  structure. Unfold witness structures when auditing.

## Bind mechanically, anchor outside the attacker's reach

- **Definitional-equality binding, not byte comparison.** Bind the proved
  declaration to the goal statement by `isDefEq` on elaborated types
  (`unsorry` ADR-011); source-level text comparison is simultaneously too
  strict (whitespace, notation) and too weak (renaming).
- **In an attacker-controlled tree, in-tree integrity checks are circular.**
  A PR that rewrites the statement file *and* its recorded SHA *and* the
  index entry passes every check derived from its own tree. The one anchor a
  PR cannot rewrite is the git base ref: make statement files **create-only**
  against the base ref; a wrong statement gets a new id and the old one is
  abandoned in place, never edited (ADR-018).
- **Vendored benchmark statements need dual fidelity proof.** When claiming
  correspondence to a benchmark repo (e.g. `google-deepmind/formal-conjectures`),
  pin the upstream merge-commit SHA, keep the vendored text byte-identical,
  *and* keep a branch with a real Lake dependency on that commit containing a
  guard `example` that fails to compile unless the vendored right-hand side
  is definitionally identical to upstream's (`erdos-619`).
- **Dual independent translation** for English→formal at scale: two
  translators with no read access to each other's output, normalized diff,
  mismatch routed to a human. Name the residue honestly: a wrong
  formalization both translators agree on passes everything — this residue
  is why the trusted-file human read never goes away.

## Resolving a problem negatively

A negation flips the statement discipline:

- Benchmark repos state open problems in solved-form scaffolding
  (`answer(sorry) ↔ RHS`). The negative resolution proves the **solved form**
  `answer(False) ↔ RHS`; state explicitly that upstream still carries the
  open form.
- **The bridge must run conjecture→conjecture** so the negation flows back.
  To refute `∃ c, ∀ V, P c V` you need one `V`: specialize the benchmark's
  arbitrary `V` to your witness type (`Fin n`) in the direction
  benchmark-conjecture → repo-conjecture, then refute the repo form. A
  bridge in the other direction proves nothing about the benchmark statement.
- Ledger the result under the *original* problem with the flip named in the
  scope ("resolved negatively; the site statement's quantifier order is …")
  — see [[mathematical-research/references/claim-status|claim-status]].

## Pin the informal source

The formal statement's meaning is anchored to an informal text — which, in
practice, is a tweet, a Zulip thread, or a CDN PDF, all mutable:

- At statement-freeze time, archive the informal source and record its
  SHA-256 alongside the statement hash. Every audited 2026 repo failed this;
  provenance pointed at live URLs only.
- Capture the problem page verbatim (`problem_statement.md`): full text,
  site status banner, tags, extraction date, and a closing attestation —
  "verbatim, no synthesis or interpretation added." Pin the exact Lean
  target name next to it so statement ambiguity is resolved in one place.
- Keep the informal proof blueprint as a first-class artifact, separate from
  the polished paper, with imported literature quoted verbatim and pinned to
  resolvable ids (`paper_id`, `theorem_id`).
