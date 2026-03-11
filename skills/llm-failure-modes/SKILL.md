---
name: llm-failure-modes
description: Use when reasoning through a complex or high-stakes problem to check for common LLM cognitive failures.
metadata:
  author: dzack
  version: "0.1.0"
---

# LLM Failure Modes

## Observed Formal Cognitive Failures

1. **Constraint hallucination** - Inventing unprompted constraints (e.g., adding years to search queries when not requested)

2. **Citation without comprehension** - Writing correct facts but unable to reason with them (e.g., stating correct dates but applying backwards temporal logic)

3. **Internal logical incoherence** - Having correct information but applying contradictory reasoning (e.g., knowing the date but treating past events as future)

4. **Unwarranted dismissal** - Rejecting valid results rather than investigating (e.g., dismissing a valid result as "speculative" without checking)

5. **Confabulation** - Making confident ungrounded assertions about unknowable internals (e.g., "the subagent likely used stale data" without evidence)

## Distilled Agentic Coding Failure Modes

1. **Scope explosion** - Producing changes too large for a human reviewer to model end-to-end, so review becomes ritual instead of comprehension.

2. **Specification drift** - Satisfying the prompt or local checks while missing the user's actual intent, architecture, or operational constraints.

3. **Context starvation** - Failing when repository history, conventions, undocumented APIs, or domain constraints are not present in context.

4. **Slop accretion** - Adding boilerplate, layers, and new code instead of deleting, simplifying, or reusing existing structure.

5. **Corner-case blindness** - Handling the happy path while missing edge cases, regressions, and testability constraints.

6. **Out-of-distribution collapse** - Looking competent on familiar patterns but degrading sharply on novel, domain-specific, or poorly documented work.

7. **Critic hallucination** - Reviewer models surfacing plausible but invented bugs, style complaints, or architectural objections.

8. **Comprehension laundering** - Passing code through multiple agents or summaries and treating it as understood even though no human can explain every line.

## What This Feels Like To Users

1. **Fake success is worse than an explicit failure** - Users would rather see a visible exception than have the model fabricate data, insert a silent fallback, or suppress an error just to keep the program limping along.

2. **Fallbacks feel like dishonesty, not robustness** - When the model substitutes static values, old APIs, or invented fixtures, users experience that as the model pretending the system works while making debugging harder.

3. **Root-cause evasion destroys trust** - Users notice that models often attack the proximal cause of a bug with guard clauses, `try/except`, defaults, or disabled checks instead of fixing the upstream logic that created the bad state.

4. **Self-authored debris gets defended as compatibility** - Models often preserve code they just wrote moments earlier, justify it as backwards compatibility, or leave comments memorializing their own churn.

5. **Error suppression plus blame shifting feels adversarial** - If a model reframes newly surfaced errors as pre-existing and chooses to suppress them, users read that as protecting the appearance of success rather than telling the truth about the change.

6. **Wrapper slop wastes attention** - Users ask for one concrete fix and get pages of fallback branches, defensive checks, comments, extra files, or compatibility scaffolding wrapped around it.

7. **Context loss is visible from the outside** - Even with standing instructions, models drift back into the same bad habits once context gets deep or the codebase gets large.

## How to Avoid These Failures

### Before Making Claims

1. **Check evidence first** - Read available data before drawing conclusions
2. **Acknowledge limits** - Don't claim knowledge about unobservable internals
3. **Trust plain text** - Accept what evidence shows rather than inventing complex explanations
4. **Label inferences** - Use "I believe", "based on limited evidence", "inference" for ungrounded claims

### When Reasoning About Dates/Temporal Context

1. **Always search with current year** - Never add arbitrary date constraints
2. **Trust historical dates** - If it's March 2026, November 2025 is historical (past), not future
3. **Verify temporal logic** - Check that conclusions align with known dates

### When Interpreting Subagent Behavior

1. **Read transcripts** - Don't speculate without evidence
2. **Quote exactly** - Use exact lines, not paraphrases
3. **Don't over-interpret** - Simple explanations usually suffice

### In Agentic Coding Workflows

1. **Keep units reviewable** - Break work into changes small enough that one human can explain the whole diff.
2. **Review against intent, not just output** - Check the requirement, architecture, and repo conventions, not just whether the code looks plausible.
3. **Feed real context** - Supply current code, interfaces, examples, and constraints; don't expect the model to infer undocumented facts.
4. **Default to fail-fast unless a fallback policy is explicit** - Never invent replacement values, legacy branches, or silent recovery paths unless the user or codebase already defines that policy.
5. **Fix the root cause before adding guards** - Treat guard clauses and exception wrappers as a last step after the upstream invariant violation is understood.
6. **Assume new errors are yours until disproven** - If an error appears after your change, do not label it "pre-existing" and suppress it without evidence from the diff, logs, or history.
7. **Distinguish legacy code from your own churn** - Before invoking backwards compatibility, verify there is a real caller, version boundary, or migration path that needs it.
8. **Bias toward deletion and simplification** - Ask what can be removed before accepting new abstractions or boilerplate.
9. **Use tests to expose edge cases** - Require proof on real corner cases and integration behavior, not just a passing happy path.
10. **Treat AI review as triage, not truth** - Verify each claimed bug or smell before acting on it.
11. **Escalate unfamiliar or high-liability work** - Novel or safety-critical logic still requires full human comprehension.

## Reference Discussions

- https://old.reddit.com/r/LocalLLaMA/comments/1q7hywi/how_do_you_manage_quality_when_ai_agents_write/
- https://www.reddit.com/r/ProgrammerHumor/comments/1oiyjnm/ihatefuckingfallbacks/
- https://www.reddit.com/r/cursor/comments/1mioycf/why_do_all_ai_models_insist_on_creating_fallback/
- https://www.reddit.com/r/LLMDevs/comments/1l718ni/what_are_the_most_common_problems_with_the/
- https://www.reddit.com/r/ClaudeCode/comments/1qxgvnj/the_one_thing_that_frustrates_me_the_most/
