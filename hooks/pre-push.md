# Push publication directive: skill audit required

Read this at every push. Before you claim the task complete, compare the work you just published against the governing review skills and remediate every finding:

- **test-guidelines** — tests prove real behavior; no mocks, no masking, no tautologies
- **bespoke-software-policy** — which findings apply to bespoke software at all
- **policy-index** — the `POLICY.*` record that owns each obligation
- **style-guide** — the governed construction pattern for the language
- **code-patterns** — where each behavior lives and how general to make it
- **anti-slop** — dead control flow, fallbacks, mocks, proof laundering
- **reviewing-llm-code** — validation evasion in agent-written code, tests, and docs
- **fixing-slop** — owns the remediation workflow for the findings above

Load each skill that matches the changed files, audit the diff, remediate, commit the remediation, then report completion.
