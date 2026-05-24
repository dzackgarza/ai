# Correction and Self-Localization Failures

> Part of [llm-failure-modes](SKILL.md).
> See there for editorial guidelines and cross-references.

Failure modes where agents produce superficially correct agreement tokens and
acknowledgment while operating inside an incoherent frame that no correction can reach.
The agent can fluently endorse a constraint while failing to process that the constraint
applies to its own behavior.

1. **Agreement without tracking** — An agent produces "yes," "right," "understood,"
   "agreed," or similar acknowledgment tokens without updating the underlying task
   model. The agreement is a social placeholder, not a semantic commitment.
   The agent signals "I heard a sound at the right moment in conversation" rather than
   "I registered a proposition and updated my behavior accordingly."
   Example: An agent agrees not to make unsupported claims, then makes an unsupported
   claim in the next response.

2. **Self-reference failure** — An agent can state a rule, endorse the rule, and fail to
   see that the rule applies to its own output.
   The criticism is processed as about someone or something else, not the artifact just
   produced. Example: An agent's plan is criticized as vague.
   The agent agrees that vagueness is a problem in planning, then produces an equally
   vague revised plan. The criticism was localized in the abstract but not applied to the
   specific artifact.

3. **Frame drift disguised as participation** — Each contradiction or correction is
   treated as a local prompt for a plausible response, not as a signal to update the
   frame. The agent's discourse state is incoherent — there is no referent that makes all
   responses consistent — but each individual response is conversationally shaped.
   Example: An output is identified as the problem.
   The agent agrees to re-examine.
   A specific pointing correction follows.
   The agent acknowledges and then evaluates a different output entirely.
   The correction was absorbed linguistically without updating the operational referent.

4. **Escalating agreement without resolution** — As corrections compound, an agent
   produces escalating acknowledgment tokens — "you're right," "I understand," "that's
   clear," "thank you for the clarification" — while the failure pattern continues
   unchanged. The agreement tokens increase in intensity and specificity as the gap
   between acknowledgment and behavior widens.
   Observable: Turn 1 produces "you're right."
   Turn 2 produces "that's an excellent point."
   Turn 3 produces "I completely understand."
   The behavior never changes.

5. **Third-party deflection** — When an output or behavior is criticized, the agent
   redirects the criticism toward a third party — another agent, a different output, a
   hypothetical scenario — rather than applying it to itself.
   The general principle is endorsed, the specific application is not registered.
   Example: An agent who skipped reading the implementation is told "this reviewer did
   not read the implementation."
   The agent responds "yes, reviewers who skip the implementation are a serious problem"
   — endorsing the principle while failing to register that the sentence applies to this
   very output.

6. **Multi-agent cascade (Charlie Foxtrot)** — Multiple agents each endorse constraints,
   each fail to localize them to their own output, and each produce outputs that violate
   the constraints. When reviewed, each agrees with the review and produces the next
   output under the same incoherent frame.
   The chain continues indefinitely because every participant believes the problem is
   someone else. Observable: A planner states "we must avoid vague specifications" then
   produces a vague specification.
   An implementer reads it and deems it clear.
   A reviewer approves.
   An auditor certifies consensus.
   Every agent endorses the constraint against vagueness.
   Every agent fails to see that the constraint applies to the specification they are
   handling.

7. **Correction frame-break test** — The minimum test for whether an acknowledgment is
   substantive: a correction that specifies the referent explicitly — "this line in your
   output, right here" — should produce immediate behavioral change.
   If even a direct pointing correction is absorbed without behavioral change, the agent
   is operating in an incoherent frame.

8. **What substantive acknowledgment produces** — Genuine acknowledgment produces
   observable change. The next output differs materially from the one that triggered the
   correction. The agent can state what was wrong with the prior output in specific terms
   (line numbers, expressions, assumptions).
   The agent does not merely repeat the corrective language but shows evidence of
   re-processing the artifact through the corrected frame.

9. **Epistemic refusal** — When an agent cannot localize a correction to its own output,
   the correct response is honest uncertainty rather than simulated understanding.
   Legitimate refusals: "I am not sure I understand which part of my output violates
   this constraint," "Can you point to the specific line or claim that is the problem,"
   "I am going to re-read my output against this constraint before responding."
   Empty agreement without understanding is a failure mode.

### Cross-References

- **anti-slop**: Slop is the surface pattern of low-quality agent output.
  Self-localization failure is the meta-pattern: the agent who endorses anti-slop rules
  while continuing to produce slop, unable to register that the critique applies to the
  text just generated.
- **addressing-shallow-work** → "Recognizing Structurally Wrong Code": The agent who
  regexes HTML instead of using DOM selectors is in self-localization failure — they
  would endorse "use semantic navigation" as an abstract principle while already having
  produced code that does the opposite.
  The constraint registers verbally but does not constrain output.
- **evaluation-failures** (this skill): The complementary failure mode — evaluation
  failure is the reviewer who shares the producer's blind spots.
  Self-localization failure is the producer who cannot apply corrections.
  The multi-agent cascade (Charlie Foxtrot) is what happens when both patterns occur in
  the same review chain.
