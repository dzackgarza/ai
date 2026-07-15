# Session Freeze and Handoff

Owner file for ending a research session and transferring state to the next agent
(or to yourself after a context reset). Parent: [[mathematical-research/SKILL|mathematical-research]].

## When to freeze

Freeze at every session end, before switching the working agent, and immediately after
banking a major result. A freeze is a dated, immutable snapshot; later work supersedes
it, never edits it.

## Bundle contents

Work inside a git repository and hand off by reference (commit hash + paths). Build a
copy-based bundle only when the workspace is not a repo — then a SHA-256 `MANIFEST.tsv`
is mandatory, because hashes become the only provenance. Root files:

| file | job |
|---|---|
| `START_HERE.md` | The single authoritative entry point (structure below). |
| `CLAIM_LEDGER.tsv` | Canonical claim statuses ([[mathematical-research/references/claim-status|claim-status]]). |
| `SUPERSESSION_AND_ERRATA.md` | Names each stale or false statement in earlier documents, by file. |
| `RUNS.tsv` | Run ledger ([[mathematical-research/references/computation|computation]]). |
| `BUILD_AND_VERIFY.md` | Exact auditor commands with exact expected PASS lines. |
| `ENVIRONMENT.md` | Hosts, versions, images, compute policy for reproduction. |
| `EXCLUDED_FILES.md` | What was deliberately left out, grouped by reason (stale/unsafe, non-evidence, hygiene). Curation is explicit, never silent. |
| `AGENTS.md` | Nonnegotiable environment and compute rules for the incoming agent. |

Organize content as numbered directories in reading order
(`01_current_theory/ … 06_background_with_errata/`), so the reading order survives
even when the reader ignores instructions.

## START_HERE structure

1. **Bottom line first**: is the main question open or closed, in two sentences,
   before any narrative. If a result exists, state it; if not, say "remains open, no
   counterexample found" plainly.
2. What this session actually advanced (numbered, each with its claim-ledger id).
3. Numbered reading order over the bundle.
4. A one-page self-contained proof sketch of the headline result — the next agent
   should be able to re-derive it without opening any other file (the exponent-8
   page in [[mathematical-research/references/worked-example|worked-example]] is the
   model).
5. Current frontier state with exact counts, plus the instruction to rerun the
   read-only auditors before quoting counts (live lanes may have advanced).
6. **Highest-value next work**, ranked.
7. **Explicit do-not-do list**: retired lanes, bypassed timeouts, stale advice in older
   documents. Name the documents ("X has stale principal counts; do not launch tasks
   16/17"). Negative guidance prevents the most expensive waste. Record dead ends
   with their cost and reason ("heaviest job, lost 19 h twice, cannot checkpoint —
   do not rerun unchanged") so the next agent inherits the lesson, not the bill.
8. A continuation checklist of the specific misreadings the material invites
   (terminology traps, scope confusions, which artifacts are truth sources).

Also write the **short recovery handoff**: the entire headline result — object,
defining data, decisive calculation, verify commands — compressed onto one page. The
long handoff serves resumption; the short one survives context loss.

## Format anti-patterns (each one is observed scar tissue)

- **Banner-stacking**: prepending "supersedes everything below" banners to a stale
  narrative. Three stacked banners over a dead body is not a handoff. Write a fresh
  authoritative document and demote the old one whole.
- **Copy-based duplication**: byte-copying heavy theory documents and scripts into
  each new bundle. The observed endpoint is the canonical theory file existing in
  three mutually inconsistent versions at once. One canonical copy, referenced by
  hash and path.
- **Double storage inside one bundle**: a flat `scripts/` mirror plus per-topic
  copies of the same files. Every canonical artifact lives in exactly one place in a
  bundle; indexes point to it.
- **Per-stratum forks** of near-identical auditors/parsers that then drift —
  parameterize instead ([[mathematical-research/references/computation|computation]]).
- **Prose counts**: frontier counts quoted in narrative documents go stale and
  propagate ("158/190" survived into two shipped bundles). Counts live in
  auditor-regenerable ledgers; prose points at the auditor.

## Supersede loudly

- Exactly one handoff is authoritative at any time; it says so, and every older
  handoff is either moved under `archive/` or named in `SUPERSESSION_AND_ERRATA.md`.
- A document that overstates results (e.g. claims case exhaustion it does not have) is
  listed as **do not cite**, even if parts remain useful.
- A stale claim in an old handoff is treated as dangerous, not as harmless history:
  the observed failure mode is the next agent re-launching retired work or repeating a
  false statement because an unmarked old file said so.

## Receiving a handoff

1. Read `AGENTS.md` (environment rules), then `START_HERE.md`.
2. Run every `BUILD_AND_VERIFY.md` auditor and match the PASS banners **before
   believing any claim**. The handoff's own prose is untrusted until the audits pass.
3. Read `SUPERSESSION_AND_ERRATA.md` before any background or theory document.
4. Check `CLAIM_LEDGER.tsv` for the status and caveat of any claim before extending it.
5. Treat inherited live processes as inconclusive snapshots; monitor, do not bank.
6. Before quoting any frontier count, rerun the read-only auditor that produces it.
