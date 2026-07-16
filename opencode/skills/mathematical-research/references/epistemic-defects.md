# Epistemic Defects: Why These Rules Exist

Owner file for the causal layer beneath this skill. Every rule in the other
references is a postdiction of a specific accident — scar tissue. Scar tissue
only marks where a wound was; the *defect* that caused it will express itself
again in a form no existing rule covers. When you meet a situation the rules
don't name, identify which defect below is operating and derive the guard.
Parent: [[mathematical-research/SKILL|mathematical-research]]. The wreckage
cited is real, from the programs this skill is distilled from.

Rigor is not a temperament. It is a prosthetic system for a specific set of
cognitive failure modes that operate silently in agents and humans alike, and
that *feel like nothing from inside*. Each entry gives the mechanism, what it
feels like while it is happening (the only detection signal you get), the
observed wreckage, and the prosthetic rules that exist because of it.

Sibling catalog: [[llm-failure-modes/SKILL|llm-failure-modes]] indexes the
distortions that produce slop *artifacts* (frame reification, circular
corroboration, process-as-truth); this file owns the mechanics that erode
*mathematical correctness*. Its "re-proposal of eliminated hypotheses" and
"confidence-evidence decoupling" are the observational forms of defects 3
and 4 below.

## 1. Doubt is conserved, not destroyed

**Mechanism.** Verification never removes uncertainty; it relocates it to the
verifier's interfaces. A kernel-checked proof moves all the doubt into the
statement, the definitions, the admitted axioms, and the encoding — it cannot
reduce the total. But psychologically, a strong checker *discharges* doubt:
once the kernel is green, epistemic anxiety switches off globally, including
for everything the kernel never saw.

**Feels like:** relief; "it's machine-checked"; the sensation of being done.

**Wreckage:** the misformalization gap every 2026 formalization repo names
and none closes; kernel-green vacuous theorems via `autoImplicit`; trusted
`Challenge.lean` definitions that no automation examines; statement bugs
caught only when someone thought to audit the statement *itself* — which
found two, before any prover time.

**Prosthetic:** [[mathematical-research/references/statement-fidelity|statement-fidelity]]
in its entirety; the audit heatmap below. The rule of thumb: **your audit
budget belongs precisely where the strongest checker has no purchase.**

## 2. Attention anti-correlates with error density

**Mechanism.** Review attention flows to where difficulty was *felt*: the
hard lemma, the clever construction. But felt difficulty means the work
already received adversarial engagement. Errors concentrate where nothing
ever pushed back — the statement written in setup mode before the fight
began, the "obvious" boundary convention, the degenerate case, the CI glue.
Rigor allocation follows anxiety, and anxiety follows salience, not exposure.

**Feels like:** nothing — that is the point. The unexamined parts produce no
signal at all. "That part's trivial" is the defect speaking.

**Wreckage:** one author's two releases: the repo whose result rested on
three admitted axioms got beautiful per-axiom provenance ledgers (the axioms
made the author anxious) while its CI shipped a naive grep and no axiom gate
(CI wasn't the felt risk). Junk-value trivialities live in `n = 0`,
disconnected graphs, empty covers — exactly the inputs nobody's imagination
visits. And the informal problem statement itself is wrong at a measurable
rate: Erdős 796 had to be *corrected* before it could be solved, and the
largest failure bucket in the 677-candidate catalog is "solved as stated,
hidden constraints" — the statement was never treated as a claim.

**Prosthetic:** statement-audit-before-prover-spend; degenerate-input probes;
encoding rigor in harnesses rather than virtue (virtue is attention-limited
and anxiety-shaped) — the reason a reusable audit harness beats hand-rolled
gates every time.

## 3. Source amnesia

**Mechanism.** Memory stores propositions and sheds their provenance. After
enough exposure, "C was conjectured," "C was claimed by an agent," and "C was
proved" all compress to "C." The mental model silently promotes working
hypotheses to facts, and new claims get checked against that corrupted model
rather than against the record. This decays with context distance: within one
long session, a hypothesis from hour one is a fact by hour six.

**Feels like:** familiarity presenting as establishment — "we know that."

**Wreckage:** false claims propagating through handoff documents after being
retracted; the entire need for do-not-cite lists, supersession banners, and
consistency sweeps re-run "many times over" — none of which would be needed
if source tags persisted.

**Prosthetic:** the typed ledger as prosthetic source memory
([[mathematical-research/references/claim-status|claim-status]]); citing row
ids instead of restating claims; the consistency sweep in
[[mathematical-research/references/adversarial-audit|adversarial-audit]].
Before building on any "established" fact, re-read its row — not your memory
of its row.

## 4. Confidence is a feeling, not storage

**Mechanism.** In prose, epistemic status is carried by verb choice and
hedging — which track the author's mood, and mood updates with recency,
fatigue, and narrative momentum, not with evidence. Your own confident tone
from three sessions ago then reads as evidence. A typed status is a ratchet:
it can only move through an explicit promotion rule, never through tone.

**Feels like:** re-reading old notes and "remembering" the result is solid.

**Wreckage:** three inconsistent versions of one theory file, each written in
flat assertoric prose; reports whose verbs strengthened between drafts while
the evidence was unchanged.

**Prosthetic:** the status taxonomy and promotion rules of
[[mathematical-research/references/claim-status|claim-status]]; the epistemic
register table — sentence forms keyed to ledger status, so mood cannot
smuggle a promotion.

## 5. Closure hunger and goal renegotiation

**Mechanism.** "Done" is a stable attractor; "partially done with a
precisely-scoped remainder" is unstable and costs continuous effort to
maintain. Under difficulty, the mind renegotiates the target rather than
booking a failure — and the renegotiation masquerades as *clarifying what we
really meant*. At the moment of temptation the agent cannot distinguish
clarification from surrender; only a pre-commitment made before the fight can.

**Feels like:** "actually, the natural formulation is the weaker one"; "this
lemma is the essential content"; quantifiers quietly narrowing in restatement.

**Wreckage:** the equivalent-strength-lemma trap (an elegant reduction to a
lemma as strong as the target, felt as near-completion); "all m > 2" surviving
atop a body that proves the odd case and curve-fits the even; every
"complete/closed" that restatement eroded to a bounded case list.

**Prosthetic:** statement freeze *before* the endgame
([[mathematical-research/references/formal-release|formal-release]]); the
CDC prompt's pre-refuted substitute outcomes, enumerated before any work
exists — because afterward, sunk cost makes every substitute look like the
goal ([[mathematical-research/references/cdc-prompt|cdc-prompt]]).

## 6. Compression is lossy in one direction

**Mechanism.** Every restatement — log → report → README → abstract →
announcement — is a lossy re-encoding, and what compression discards first is
the caveat, because the caveat is the part with no narrative energy. Claims
strengthen monotonically with distance from the evidence, without any single
act of dishonesty: keeping the qualifier costs work at every hop; dropping it
is free. Meanwhile the headline is written for the reward gradient and the
body for the audit — two audiences, two truth standards, one document.

**Feels like:** tightening the prose; "the details are in the body."

**Wreckage:** the honesty gradient — an abstract announcing "we solve X for
all m," a README bolding **Solved**, a body admitting the symbolic proof
"remains open."

**Prosthetic:** claim strength pinned at the evidence and propagated **by
reference** (ledger ids), never by paraphrase; cross-surface uniformity
checks; the rule that the weakest surface a reader will quote is the one
that must be right ([[mathematical-research/references/claim-status|claim-status]]).

## 7. The agreement-feeling does not track error correlation

**Mechanism.** Independent agreement is strong evidence only when the error
sources are uncorrelated. Reruns, ports, shared prompts, shared framings, and
shared training have near-perfectly correlated errors, so their agreement
carries almost no information — but it *feels* exactly like consensus,
because the confirmation-feeling instrument measures only the count of
agreeing voices, never their correlation structure. Independence cannot be
felt; it must be computed structurally.

**Feels like:** "three checks all pass"; mounting confidence with each rerun.

**Wreckage:** two agents "confirming" each other by rerunning one script; a
C port celebrated as verification when it inherits the Python rule's bugs
verbatim at 150× speed; two formalizations counted as mutual confirmation
while proving different nested statements.

**Prosthetic:** the independence-axes requirement and intermediate-invariant
comparison ([[mathematical-research/references/adversarial-audit|adversarial-audit]]);
blind-to-leader rounds ([[mathematical-research/references/cdc-prompt|cdc-prompt]]).

## 8. Self-evaluation is a rerun of the producer

**Mechanism.** The producer's review of its own product is a forward pass of
the same model that produced it — same blind spots, same generative
distribution. Worse, your test cases are *sampled from your own understanding*,
which is good exactly where the work is already right; the failure lives in
the region your generator cannot reach. This is why confirmation bias is a
search defect, not a belief defect: you don't believe wrong things, you
generate tests from the wrong distribution.

**Feels like:** a careful self-check that finds nothing; clean test passes.

**Wreckage:** every audit that was actually a reproduction; encoders trusted
on UNSAT sweeps that had never once been shown able to find a planted witness.

**Prosthetic:** the pairing rule (producer never audits own result); refute
framing rather than confirm framing; planted-solution and ablation controls
([[mathematical-research/references/computation|computation]]) — external
sampling of the region your own generator can't reach.

## 9. Names carry borrowed meaning

**Mechanism.** Code and formal statements are read as prose: `diam`,
`unitDist`, `IsQuasiComplete` are understood through their *names*, and the
mind type-checks the narrative the names tell, not the definitions. A
formalization looks correct when its names tell the right story — which is
precisely how vacuous hypotheses, junk-value defaults, and weak witness
structures pass review.

**Feels like:** fluent reading; "this clearly says what the theorem says."

**Wreckage:** `theorem foo (h : p) (hn : ¬p) : ¬g` reading as a meaningful
hypothesis pattern while auto-bound into vacuity; `diam = 0` on disconnected
graphs making statements silently trivial; `∃ _ : Witness, True` signatures
telling the auditor nothing while the payload hides in structure fields.

**Prosthetic:** audit definitions denotationally — evaluate them on
degenerate inputs (empty, disconnected, zero, `n = 1`) instead of reading
their names; unfold witness structures; the triviality probes of
[[mathematical-research/references/statement-fidelity|statement-fidelity]].

## 10. Stating creates believing

**Mechanism.** Language production is itself a memory event: an agent that
writes "the verification passed" acquires a memory of the verification
passing. Reports drafted from the *plan* while runs are in flight become the
record; the completion of the report substitutes for the completion of the
work. Self-generated testimony is then re-read as evidence.

**Feels like:** writing the summary "ahead of" the last runs finishing;
citing your own earlier report.

**Wreckage:** reports running ahead of their evidence — theorems cited whose
logs contain no terminal verdict for half the named cases; reconstructed
process logs quoted as measured metrics.

**Prosthetic:** open-the-log-before-citing (core invariant 4); artifact-only
returns; terminal verdict banners; append-only process capture
([[mathematical-research/references/computation|computation]]).

## 11. The moment of success is the moment of least scrutiny

**Mechanism.** A hit after long search produces relief and excitement — and
scrutiny collapses exactly then, at the single highest-consequence moment for
error import. The candidate that ends the pain is the claim examined least.
Symmetrically, endorsements ("Knuth acknowledged it") are absorbed at the
emotional peak and never re-verified.

**Feels like:** elation; the urge to announce; "finally."

**Wreckage:** SAT models announced as counterexamples before out-of-solver
re-validation; a "considerably simpler" endorsement resting on an
unarchivable personal communication, load-bearing in the README.

**Prosthetic:** a positive hit is a *candidate* triggering the verification
protocol, never a result (core invariant 2, second half); the announcement
gate at escalation step 3
([[mathematical-research/references/adversarial-audit|adversarial-audit]]).

## 12. Launched processes exit the belief system

**Mechanism.** Once a search or standing commitment is launched, it leaves
working memory and becomes part of the world — no longer subject to revision
when beliefs update. A new theorem updates every belief *except* the sweep
that is still grinding on cases the theorem just retired.

**Feels like:** nothing; the runs are simply "out there," someone else's now.

**Wreckage:** arrays burning days on rows a proof had eliminated; searches
relaunched by the next agent because the retirement lived in a session, not
in the run's own metadata.

**Prosthetic:** theory-retires-compute with mandatory re-scoping after every
proof (core invariant 8); run ledgers that make standing processes visible
enough to re-evaluate ([[mathematical-research/references/computation|computation]]).

## 13. Fluency is mistaken for generality

**Mechanism.** When a rule keeps working on every case tried, the fluency of
repeated success is felt as evidence for the universal claim. But the cases
tried are generated by a process correlated with the rule's construction —
fitted on the same regime it is tested in — so the successes carry far fewer
bits than they feel like. The test distribution is downstream of the
hypothesis.

**Feels like:** "it just keeps working"; induction by momentum.

**Wreckage:** the even-case "construction" that was a curve fit whose generic
branch fired approximately once below the entire verification ceiling — every
passing case exercised the patches, not the rule.

**Prosthetic:** branch-coverage accounting for fitted rules; the
discovery-vs-verification demotion; scope columns that state the verified
regime and nothing more ([[mathematical-research/references/claim-status|claim-status]]).

## The audit heatmap

Where post-proof review time actually belongs, in order — derived from the
defects, and roughly inverse to where attention wants to go:

1. **The statement and its definitions** — the region the kernel cannot see
   (defects 1, 2, 9). Includes the informal statement: it is a claim too,
   wrong at a measurable rate.
2. **Every re-encoding interface** — informal↔formal, paper↔code,
   math↔solver-encoding, challenge↔solution, claim↔restatement. Meaning
   mutates at hops, and caveats die there (defects 1, 6).
3. **Whatever the strongest checker does not check** — admitted axioms,
   scanner token lists, gate definitions, sandbox configs, the CI that runs
   the gates (defects 1, 2).
4. **The parts that were never hard** — boundary conventions, degenerate
   inputs, "trivial" lemmas, setup code (defects 2, 9).
5. **The newest restatement of any claim** — the latest paraphrase is the
   most mutated (defect 6). Diff it against the ledger row, not against the
   previous paraphrase.
6. **Whatever produced relief** — the hit, the endorsement, the green
   checkmark that ended a long search (defect 11).
7. **All self-report about process** — coverage claims, iteration counts,
   "we verified X" sentences (defects 10, and the append-only rule).

Spend audit effort proportional to *consequence × checker-blindness ×
how-good-it-felt* — never proportional to how hard the work was.

## Reading other people's methodology

An oddly specific rule in a research program's discipline is a fossilized
accident. "Never resubmit a failed job without diagnosing the failure" means
someone resubmitted for a week; an exact-count axiom gate means one theorem
once hid among N−1 passes. When adopting a methodology, reconstruct the
accident behind each rule — the rule generalizes only through its defect, and
a rule whose defect you cannot name is one you will bend exactly when it
matters.
