# Program Shape: Repository, Manuscripts, Endgame

Owner file for how a research program is laid out on disk, how manuscripts move
through stages, and how a finished result exits the program. Parent:
[[mathematical-research/SKILL|mathematical-research]].

## Repository layout

Run the program inside git from day one — the observed alternative (a cloud-synced
folder) forced hash-manifest provenance and copy-based handoffs, and roughly a third
of the eventual archive was duplicate copies. Canonical layout:

```
README.md            # map + "start here" + handoff protocol for agents
manuscripts/
  main/              # current results, current audits
  drafts/            # incomplete proof boundary — not citable yet
  archive/           # superseded constructions, kept, each README says why
docs/                # dated reports and project-level audits
notes/               # frontier working notes (dated, one topic each)
scripts/             # verification and search programs
m2/  lean/  ...      # per-system computational sources
handoff/             # the current live handoff, if any
archive/handoffs/    # frozen historical bundles ([[mathematical-research/references/handoff|handoff]])
```

- The top-level README carries the agent handoff protocol: read order, which
  construction is primary, "treat archive/ as historical context, not a current claim
  ledger", and the recording rule for new computations (host, versions, parameters,
  commit hash, output path, verification status).
- Keep generated logs, caches, run outputs, ZIPs, and LaTeX intermediates out of
  commits. Frozen *terminal* evidence logs selected by an auditor are the exception —
  they are evidence, not debris.
- Name frozen evidence artifacts with dates (`X_RESULT_2026-07-10.md`); dated names
  make cross-references from audits stable. Living documents (README, current
  handoff) keep stable undated names.

## Manuscript staging

The staging axis is **proof-boundary completeness**, not recency or size. Each tier's
README states its epistemic status and citation rules:

- `main/`: the central theorem has a complete, audited proof. The README ranks the
  files by role ("read X first; Y and Z are companion documents").
- `drafts/`: a named proof gap remains, and the README says exactly which
  ("intentionally separated while the remaining odd-prime certificate work is
  completed"), with the gating rule spelled out: "check each file's stated proof
  boundary before treating a claim as established."
- `archive/`: superseded but still carrying specific citable content; "new claims
  should start from ../main/ and cite an archive file only for its specific
  additional result."

- `drafts/ → main/` promotion requires the formal proof boundary to be complete: no
  conditional scaffolding in a main-track manuscript beyond claims explicitly marked
  conditional. A construction whose proof rests on an undischarged package stays in
  drafts, with the boundary documented. When the paper's prose and the
  formalization's proof boundary disagree about whether a step is proved, the
  stricter judgment decides the stage.
- `main/ → archive/` demotion happens when a simpler construction supersedes it.
  Archive, never delete: superseded constructions retain distinct structural content
  (the observed archived example still carried the subgroup/deformation analysis the
  new one lacked). The archive README says what each item still offers.
- Simplification is a research phase, not polish: after a result lands, spend sessions
  shrinking it (smaller base, fewer relations, human-checkable scale). Each
  simplification round gets its own audit before replacing the primary.
- Papers state the theorem and construction first; failed searches do not lead. Keep a
  short discovery-chronology section with methodological lessons, and keep
  solver-conditional claims (e.g. minimality) visibly separate from the theorem.
- The hand proof is the evidence of record; machine computation is corroboration. The
  companion-audit appendix states the division of labor explicitly: which claims are
  proved formally in the text, and which polynomial identities the script audits.
- Cite machine verification as a full reproducibility packet: dated script path, tool
  version, exact invocation, runtime and exit status, the expected *symbolic* output
  lines (the actual Groebner basis, the actual normal forms — not just "it passes"),
  and SHA-256 digests. Cite a formalization by namespace, main theorem name, and
  axiom footprint ("depends only on `propext`, `Classical.choice`, `Quot.sound`; no
  `sorry`"), with the toolchain pinned.
- Verify the attribution of the *question* itself against primary sources before
  claiming to answer it — editions differ (a printed 1970 statement and its annotated
  re-edition may carry different hypotheses), and the historical-claims check is a
  named human-gate item.
- Every manuscript and module records which agents produced it. Disclose AI authorship
  wherever the receiving venue requires it (mathlib requires it in the PR body); in
  the manuscripts, use role-descriptor author fields ("Independent algebraic and
  computational verification") rather than fabricated names.
- Dating: `\date{}` empty for timeless primary papers; explicit dates on audits and
  snapshots; notes carry a `Date:` header field. Version by co-existing dated files
  and staging demotion — supersession is recorded in prose and README, files are not
  overwritten.
- Writing standards for the mathematics itself:
  [[mathematical-writing/SKILL|mathematical-writing]]; epistemic register per claim
  status: [[mathematical-research/references/claim-status|claim-status]]; paper
  mechanics: [[research-writing/SKILL|research-writing]]; compile QA:
  [[latex-compile-qa/SKILL|latex-compile-qa]].

## Endgame pipeline

A banked headline result exits through, in order:

1. **Simplify** until a human can check it end-to-end (the "human-scale" pass).
2. **Formalize**: Lean project pinned to a toolchain; build warning-free with the
   standard linter set; `#lint` clean; `#print axioms` on every main theorem showing
   only the standard axioms; no `sorry`. Route through
   [[lean4/skills/lean4/SKILL|lean4]] / [[aristotle/SKILL|aristotle]].
3. **Upstream/publish** with a dedicated handoff document that includes: exact scope
   ("one file"), the venue's conventions already applied, reproduction commands,
   anticipated reviewer objections with prepared answers, and what is deliberately
   *not* submitted yet (conditional frameworks are not PR-ready and say so).
4. **Human gate**: attribution, historical claims, bibliography, and sign conventions
   are verified by a human expert before external announcement. This is a named
   not-proved item in the ledger until done.

## Working style that paid off

- Alternate theory passes and computation passes; each session's handoff names which
  kind comes next and why ([[mathematical-research/references/handoff|handoff]]).
- Reports are dated, single-topic, and paired with audits
  ([[mathematical-research/references/adversarial-audit|adversarial-audit]]).
- When several agents work the same frontier, one bundle is authoritative and every
  push gets a written `RESPONSE_TO_*` review rather than silent merge.
- Run the program as a relay of seats — theory pushes, compute sweeps, audit/banking —
  with the audit seat held by a different agent than the producer of the artifact
  under review ([[mathematical-research/references/adversarial-audit|adversarial-audit]]).
  The audit seat banks or downgrades claims, records deaths in the errata file, and
  writes the prioritized asks for the next agent.
- The negative-results ledger lives in dated notes with a `Verdict` header that
  states both the finding and its limit ("length nine is the smallest fully verified
  example, not a proved global minimum"), reproduction commands, and a machine-
  readable results ledger path.
