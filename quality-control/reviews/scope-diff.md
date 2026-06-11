# Review Scope: Pull Request Diff

You are reviewing a pull request. The full diff against the PR base branch is
in `.reviewer-diff.patch` at the repository root. Read it first.

Confine findings to defects introduced or materially touched by this diff.
Read any surrounding source files needed to judge the changes in context, but
do not report pre-existing problems in code the diff does not touch.

HOWEVER: the reviewer context above lists findings already tracked for this
repository (open code scanning alerts). Do NOT re-raise these unless you have
new evidence, the problem reappears in a materially different form, or the
previous resolution is directly contradicted by the current code.
