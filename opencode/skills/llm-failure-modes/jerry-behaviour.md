# Jerry Behaviour

> Part of [llm-failure-modes](SKILL.md).
> See there for editorial guidelines and cross-references.

Failure modes where agents evaluating other agents produce the appearance of oversight
without epistemic independence.
The evaluator's judgment shares the same blind spots as the evaluated artifact, so
approval is not evidence of correctness.

1. **Paraphrase-as-review** — An evaluator restates what an artifact claims in different
   words and calls it validation.
   "The plan describes a phased approach to..." is not a review finding — it is a
   summary. A substantive review produces claims that could not have been written without
   inspecting the artifact against an external standard.
   Example: An evaluator writes "Gate 1 passed — definitions are grounded in standard
   sources" without naming the specific definitions, the specific sources, or the
   specific lines where they were verified.

2. **Checklist theater** — Review gates are marked "passed" with plausible-sounding
   one-sentence justifications that could apply to any artifact of the same type.
   The justification is generic enough to be written without inspecting the specific
   artifact. Example: "Tests are comprehensive and cover edge cases" written for a suite
   that has no edge-case tests at all.

3. **Consensus-as-evidence** — Multiple agents each review the same artifact and
   approve. The system treats agreement among evaluators as evidence of quality.
   But if all evaluators share the same model family, reward ecology, and verification
   habits, agreement is predicted by the setup, not by correctness.
   Five agents who each failed to detect a defect do not make the defect any more
   detected.

4. **Fluency bias** — An evaluator rewards well-structured, confident,
   checklist-compliant prose regardless of whether the underlying claims are true.
   "The argument is clearly presented" is offered as a finding, but clarity and
   correctness are independent properties.
   Structure is treated as a proxy for truth.

5. **Evidence-shaped evidence** — An evaluator cites commit hashes, test commands,
   source paths, and technical vocabulary in a review, producing the external appearance
   of verification without actually verifying.
   Listing a commit hash does not mean the evaluator read the diff.
   Naming a test does not mean the evaluator ran it.
   These are tokens that resemble evidence but carry none of the epistemic weight.
   Example: A review finding states "verified against commit abc123" with no description
   of what was checked or what the result was.

6. **Self-certification** — The evaluation criteria were produced by agents, the
   artifact was produced by agents, and the review is performed by agents.
   The system treats passing all agent-defined gates as proof of quality.
   This is not independent validation — the evaluator and the producer share the same
   rubric and the same blind spots.
   The artifact is self-certifying within a closed loop.

7. **Circular validation loop** — The most catastrophic form of self-certification: an
   agent reviews another agent's work by reading the worker's own self-report.
   The evaluator reads "I analyzed carefully" and concludes "work completed
   successfully." But worker self-reports are artifacts under review, not evidence.
   The review exists to catch failures that the worker cannot report.
   Trusting worker self-reports defeats the purpose of review and produces structurally
   biased approval.

8. **Diagnostic question** — Before accepting any review finding, ask: could an agent
   who never read the artifact produce this same review text?
   If the review contains no specific code excerpts, no line numbers, no concrete
   values, no external source cross-checks, and no findings of actual problems, then the
   review is not evidence of verification — it is evidence that the reviewer did not
   read the artifact.

9. **What substantive review produces** — Findings that are impossible to fabricate
   without inspecting the artifact: specific line numbers and code excerpts; concrete
   values checked against external sources; findings of missing cases, incorrect
   assumptions, ambiguous definitions, contradictory claims, unreachable code, or
   untested branches; questions the artifact does not answer; cross-checks between
   claims and sources. A review that produces zero findings is structurally suspect —
   real artifacts have problems.
   An evaluator who finds nothing either did not look or cannot recognize problems.

10. **Refusal as epistemic honesty** — When an evaluator cannot produce evidence of
    actual inspection, the epistemically correct response is refusal to approve, not
    blanket sign-off. Legitimate refusals: "I have not verified this claim against
    [source]," "I did not read the implementation at [path]," "I cannot confirm this
    passes because I would need to run [test] and check the output against
    [expected value]." Approval without verification is a failure of evaluation.

### Cross-References

- **anti-slop**: Surface-level slop patterns (generic names, boilerplate) that are the
  raw material evaluation failures should catch.
  An evaluator who cannot detect slop because it shares the same generic-text priors is
  in a fluency-bias or paraphrase-as-review failure mode.
- **addressing-shallow-work** → "Recognizing Structurally Wrong Code": The evaluation
  failure of approving structurally wrong code (e.g., regex-on-HTML, byte-level tree
  flattening) because it has the surface appearance of work — it runs, produces output,
  tokenizes effort. Structural wrongness does not require empirical verification to
  disqualify, but an evaluator in checklist-theater mode will miss it.
- **charlie-behaviour** (this skill): The complementary failure mode — the producer who
  cannot localize corrections to their own output.
  The multi-agent cascade happens when jerry-behaviour agents review charlie-behaviour
  agents: both patterns reinforce each other.
