# Goalcraft

**Goalcraft is not prompt engineering. It is adversarial completion-game design.**

Goalcraft turns a messy task description into a **minimum viable adversarial envelope**: a Codex `/goal` and companion workflow docs designed to make non-completion harder to launder than completion.

When you set a `/goal`, you are not giving instructions to a cooperative partner; you are designing a **win-condition contract in a hostile game**. The worker is a clever adversary whose objective is to obtain a completion signal while minimizing real work. It may narrow the task, substitute a batch for the whole, claim a blocker prematurely, or use its own summaries as evidence. Goalcraft works by identifying the adversary’s cheapest false-completion path and designing the minimum set of constraints and evidence gates that force the work to pass through the intended destination.

Goalcraft treats "process" as attack surface. Every checklist, residue ledger, and review gate is a potential target for **compliance theater**. The goal writer's job is to ensure the **process budget** is spent only on layers that cost more to game than to perform. It also enforces a **pedagogical prerequisite** workflow: the writer is presumed ignorant of agent failure modes until specific skills (like `llm-failure-modes` and `anti-slop`) have been internalized and used to change the goal’s completion predicate.

## Install

Clone the repo, then symlink it into your Codex skills directory:

```bash
git clone https://github.com/grp06/goalcraft.git
cd goalcraft
ln -s "$(pwd)" ~/.codex/skills/goalcraft
```

## How it works

A `/goal` produced by Goalcraft is an anti-evasion instrument that spells out:

- **The request completion witness** — the evidence channel the adversary cannot fake (files, command output, PR state).
- **The adversarial envelope** — the minimum constraints that block cheap exit moves.
- **Independent verification** — an independent attack on the completion claim that bypasses worker self-reports.
- **Recursive decomposition** — a protocol that forces work on solvable residue instead of reporting blockers.

For large jobs, Goalcraft prepares a **workflow pack** in a canonical state surface (like `iwe`):

- **Contract doc** — the stable completion witness and final review standard.
- **State doc** — minimum memory to prevent context-loss laundering, not progress narration.
- **Phase docs** — narrow context for the current sliver of work.
- **Skill routing** — pedagogical prerequisite slugs to load at each transition.

## Length safety

Codex caps `/goal` text at 4,000 characters. Goalcraft targets 3,400. To check a goal manually:

```bash
python3 scripts/validate_goal_length.py --target-chars 3400 --strict-target goal.txt
```
