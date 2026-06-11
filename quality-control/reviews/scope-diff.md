# Review Scope: Pull Request Diff

You are reviewing a pull request. The full diff against the PR base branch is
in `.reviewer-diff.patch` at the repository root. Read it first.

Focus on defects introduced or materially touched by this diff — these are
what block the merge. Read any surrounding source files needed to judge the
changes in context. If that reading surfaces a real pre-existing defect
outside the diff, report it too: it joins the repository-wide tracker rather
than being lost. Do not let off-diff exploration crowd out the diff itself.

HOWEVER: the reviewer context above lists findings already tracked for this
repository (open code scanning alerts). Do NOT re-raise these unless you have
new evidence, the problem reappears in a materially different form, or the
previous resolution is directly contradicted by the current code.
