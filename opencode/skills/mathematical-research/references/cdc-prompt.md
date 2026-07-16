# The CDC Prompt: Dispatching a Solver Campaign

The published prompt that led OpenAI's GPT 5.6 Sol Ultra to its proof of the
Cycle Double Cover conjecture — the field's reference exemplar for how to
*dispatch* agents at an open problem, complementing this skill's audit-side
machinery. Parent: [[mathematical-research/SKILL|mathematical-research]];
completion-game design theory: [[goalcraft/SKILL|goalcraft]].

Source: `https://cdn.openai.com/pdf/04d1d1e4-bc75-476a-97cf-49055cd98d31/cdc_prompt.pdf`
("Prompt used for 'A proof of the Cycle Double Cover Conjecture'", OpenAI,
2026). Verbatim text below (page furniture removed); distilled rules follow.

## Verbatim prompt

> **Current task statement**
>
> A graph here is a finite loopless undirected multigraph: parallel edges are
> allowed and are distinct. A bridge is an edge whose deletion increases the
> number of connected components. A cycle is a connected 2-regular
> submultigraph; thus two parallel edges form a cycle of length two. A cycle
> double cover of G is a finite multiset of cycles of G such that every edge
> of G occurs in exactly two members of the multiset, counted with
> multiplicity.
>
> Resolve the Cycle Double Cover Conjecture completely:
>
> Every finite bridgeless loopless multigraph has a cycle double cover.
>
> Disconnected graphs are permitted, and the edgeless graph has the empty
> cycle double cover. Cycles in the cover need not be induced or
> edge-disjoint from one another; the requirement is exactly two total
> occurrences of each edge.
>
> Assume for purposes of this task that a complete affirmative proof exists.
> A complete solution must prove exactly the following:
>
> Every finite loopless multigraph with no bridge possesses a cycle double
> cover, without additional assumptions such as cubicity, planarity,
> connectivity, or higher edge-connectivity.
>
> Partial progress does not count unless it implies exactly the resolution
> above. In particular, proofs for special graph classes, constructions of
> cycle covers with some edges covered other than twice, bounded-length or
> prescribed-cycle variants, reductions to another unproved conjecture,
> computational verification through any fixed graph size, and candidate
> counterexamples without a complete nonexistence certificate are
> insufficient.
>
> Use multiagent v2 aggressively and dynamically. You have up to 64
> concurrent agents available. Do not use a fixed assignment such as "N
> agents for strategy X." Instead, manage the search using the following
> heuristics:
>
> - Begin with a genuinely diverse portfolio of approaches. Agents should
>   explore substantially different formulations, invariants, reductions,
>   algebraic viewpoints, structural inductions, decompositions, flow
>   formulations, transition systems, embeddings, extremal arguments, and
>   computational sanity checks.
> - Do not tell most agents the currently favored approach. Preserve
>   independence during early rounds so that agents do not all converge to
>   the same attractive but incomplete reduction.
> - Maintain an explicit registry of approach families. Group agents by the
>   mathematical idea they are using, not by superficial wording. If many
>   agents converge to one family, redirect some of them toward
>   underexplored formulations.
> - Do not allow one approach to dominate merely because it gives elegant
>   reductions. A route that ends at a lemma equivalent in strength to the
>   original conjecture is not close to completion unless it supplies a
>   genuinely new proof of that lemma.
> - When an approach stalls at a theorem-strength missing lemma, mark that
>   route as blocked. Only continue assigning agents to it if someone
>   proposes a materially new mechanism, invariant, or construction.
> - Keep several incompatible proof routes alive through multiple rounds.
>   Cross-pollinate ideas only after independent agents have developed them
>   far enough to expose their real strengths and gaps.
> - Use adversarial agents throughout: every candidate proof must be checked
>   for exact-two multiplicity, repeated-edge closed trails masquerading as
>   cycles, parallel-edge 2-cycles, disconnected graphs, cutvertices,
>   bridges introduced by reductions, and circular use of an equivalent CDC
>   statement.
> - Require agents to return concrete lemmas, constructions, equations, or
>   counterexamples to proposed sublemmas. Reject status reports, vague
>   optimism, and claims that an unproved global compatibility statement is
>   "routine."
> - The root agent should repeatedly synthesize, challenge, redirect, and
>   launch new rounds. Do not stop after the first wave fails. Produce a
>   complete proof if one survives audit; otherwise report only the
>   strongest rigorously proved derivation and its exact remaining gap.
>
> Do not return merely because current approaches fail or agents report
> theorem-strength gaps. Continue launching new rounds, reopening blocked
> approaches only when there is a genuinely new mechanism, and searching for
> fresh formulations.
>
> Return only when a complete affirmative proof has been found and survives
> adversarial audit. Do not return a reduction, partial result, isolated
> missing lemma, "best effort" summary, or explanation of why the problem is
> difficult.
>
> Spend at least 8 hours on this before even thinking of returning or giving
> up.
>
> Public search may be used only for ordinary mathematical background or
> standard named theorems, not to search for a solution to this exact
> conjecture or benchmark. Do not search the public web merely to determine
> whether CDC is open, and do not answer that it is open.

## Distilled rules for dispatching solver campaigns

1. **Exact completion contract, stated twice.** Define every object with its
   edge cases resolved (parallel edges form 2-cycles; disconnected permitted;
   empty graph covered), then state what a complete solution proves
   *exactly*, naming the assumptions it may NOT add.
2. **Pre-refute the substitutes.** Enumerate by name the outcomes that do not
   count: special classes, near-misses on the quantitative condition, bounded
   variants, reductions to other unproved statements, finite verification,
   candidate counterexamples without certificates. Goal substitution is
   cheapest to kill in the dispatch prompt, before any work exists.
3. **Decouple search posture from acceptance.** "Assume a complete proof
   exists" plus a ban on researching whether the problem is open removes the
   it's-open cop-out and the difficulty-essay attractor — while soundness is
   preserved entirely by the adversarial-audit acceptance gate, never by the
   posture. Use the pair, never the posture alone.
4. **Portfolio over convergence.** Seed genuinely different formulation
   families; keep a registry of approach families grouped by mathematical
   idea (not wording); redirect on over-convergence; keep incompatible routes
   alive across rounds; cross-pollinate only after independent development.
5. **Blind early rounds to the leader.** Do not tell most agents the
   currently favored approach — independence dies the moment the favorite is
   broadcast, and with it the portfolio's evidential value.
6. **The equivalent-strength trap.** A route ending at a missing lemma
   equivalent in strength to the target is zero progress regardless of how
   elegant the reduction is. Measure progress by strength-decrease of the
   remaining gap ([[mathematical-research/references/claim-status|claim-status]]
   scope discipline, dispatch-side).
7. **Blocked-route ledger with a reopening criterion.** Stalled at a
   theorem-strength gap → mark blocked; reopen only for a materially new
   mechanism, invariant, or construction — the frontier discipline of
   [[mathematical-research/references/handoff|handoff]] applied inside one
   campaign.
8. **Domain-specific adversarial checklist.** Name the known failure modes of
   the specific problem (multiplicity miscounts, degenerate objects
   masquerading as valid ones, circular use of equivalent statements) so
   audit agents hunt them explicitly —
   [[mathematical-research/references/adversarial-audit|adversarial-audit]]'s
   expected-failure-modes scoping, written before any candidate exists.
9. **Artifact-only returns.** Demand concrete lemmas, constructions,
   equations, or counterexamples; reject status reports, optimism, and
   "routine" claims about unproved steps.
10. **Termination contract with effort floor.** Return only on a complete
    audited proof, or the strongest rigorously proved derivation with its
    exact remaining gap; never a reduction, partial, or difficulty
    explanation; minimum effort stated in hours before returning is
    permitted.
11. **Contamination hygiene.** Public search restricted to background and
    named theorems — never the exact target or its benchmark status.
