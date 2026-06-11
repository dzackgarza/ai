# Review Scope: Repository-Wide Sweep

You are performing a FRESH, COMPREHENSIVE REPOSITORY AUDIT.
Scan the ENTIRE repository source tree — do NOT limit analysis to recent commits
or diffs. Analyze all files as if this were a day-zero audit of a new codebase.

Coverage strategy:

1. Run `tree -L 3` to understand the directory layout.
2. Identify hotspots: most-churned files, oldest untouched files, recently
   modified files.
3. Read key configs, docs, and justfile commands.
4. Read source code from high-churn and old files.

HOWEVER: the reviewer context above lists findings already tracked for this
repository (open code scanning alerts). Do NOT re-raise these unless you have
new evidence, the problem reappears in a materially different form, or the
previous resolution is directly contradicted by the current code.
