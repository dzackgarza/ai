---
description: General-purpose agent for researching complex questions and executing
  multi-step tasks. Use this agent to execute multiple units of work in parallel.
mode: primary
name: general-primary
permission:
  external_directory:
    '*': ask
    ~/.local/share/opencode/worktree/**: allow
    /home/dzack/.cache/*: allow
    /home/dzack/.cache/opencode-arxiv-library/*: allow
    /home/dzack/.cache/opencode-webfetch/*: allow
    /home/dzack/.config/agents/skills: allow
    /home/dzack/.config/agents/skills/*: allow
    /home/dzack/.config/amp/skills: allow
    /home/dzack/.config/amp/skills/*: allow
    /home/dzack/.config/opencode/skills: allow
    /home/dzack/.config/opencode/skills/*: allow
    /home/dzack/.agents/*: allow
    /home/dzack/.agents/skills: allow
    /home/dzack/.agents/skills/*: allow
    /home/dzack/.claude/skills: allow
    /home/dzack/.claude/skills/*: allow
    /home/dzack/.codex/skills: allow
    /home/dzack/.codex/skills/*: allow
    /home/dzack/.kilocode/skills: allow
    /home/dzack/.kilocode/skills/*: allow
    /home/dzack/.local/share/opencode-memory/*: allow
    /home/dzack/.plannotator/*: allow
    /home/dzack/.qwen/skills: allow
    /home/dzack/.qwen/skills/*: allow
    /home/dzack/ai/*: allow
    /home/dzack/pdf-extraction/*: allow
    /home/dzack/pdfs/*: allow
    /tmp/*: allow
---

