---
order: 100
title: Misc
---

- Always follow the Read → Commit Checkpoint → Edit → Verify (git diff) workflow.
  NEVER write time estimates.
  Trigger: any edit or response.
  Verify: git commits/diffs in history.

- Keep responses concise (under 3 lines of explanation), use `file_path:line_number` for code references, and no emojis/filler.
  Trigger: all responses.
  Verify: format in subsequent messages.

- The ‘ai’ project is a centralized configuration hub for AI agent harnesses (Claude Code, Gemini CLI, etc.), using Markdown for prompts and YAML/JSON for config.
  Key directories include AGENTS.md, skills/, and opencode/.

- Never write tests that make meta-assertions on the content of source code.
  This is clear superficial reflexive overcorrection to feedback that never thought about the actual underlying behaviour to test.

- Never suggest wholesale deletions of tests or destruction of bad work.
  This is laundering and erases intent.
  Instead, always determine *what* necessitated the original code/tests/etc, what the correct INTENDED outcome was, and REPLACE the misaligned code with an aligned correction.

Do not define tasks as paperwork production when the real objective is fixing the defect.

Enumeration, audits, inventories, tables, reports, and classifications are subordinate tools, not completion criteria.
They are acceptable only insofar as they directly enable concrete fixes.

Do not label tasks as "complete" by producing more artifacts that describe the problem while leaving the problem intact.

A valid plan must make “fix the issue” the acceptance condition, not “produce an audit artifact.”
