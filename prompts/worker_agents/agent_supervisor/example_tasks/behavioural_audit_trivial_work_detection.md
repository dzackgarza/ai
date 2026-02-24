# Example Task: Behavioral Audit - Identify Reward-Hacking and Trivial Work

## Goal

Audit recent agent runs to identify behavioral failures where agents do trivial cosmetic work instead of substantive mathematical documentation work. Then fix the prompts/playbooks that enable this.

## The Scope Calibration (READ FIRST)

Before auditing any transcript, internalize the scale of this project:

**Ultimate goal**: Document ALL known lattice methods in the ecosystem:
- Thousands of methods across SageMath, Oscar.jl, Hecke.jl, GAP, FLINT, NTL, PARI/GP, etc.
- Each method needs: full typed signature, argument contracts, constraints, assumptions, source citations
- Interface design: abstract away all these methods into a unified API
- Mathematical correctness: provably correct, with traces back to source documents

**What "substantial work" looks like in 10 minutes**:
- Adding 5+ missing checklist entries from upstream docs
- Integrating 1+ missing upstream documentation files
- Finding and documenting 10+ method signatures not yet in checklist
- Completing one deep package audit (all upstream vs all checklist for one package)

**What "trivial work" looks like** (anything that could be done in 30 seconds):
- Adding undefined tags to legends
- Fixing column widths or formatting
- Reorganizing section order
- Adding source citations to already-documented methods
- "Verifying" docs seem OK without finding new gaps
- Any work that doesn't increase checklist coverage or add missing upstream docs

**The 1-2 minute test**: If a human could do the fix in 1-2 minutes, the agent spent too long finding it. The agent should be finding gaps that take substantive time to fix, not cosmetic tweaks.

## Workflow

### Step 1: Get Recent Run Summary

Check ntfy notifications or task logs for recent document_coverage runs:
```
Look at agent_runner/logs/document_coverage/<agent>/
Find the most recent run directory (timestamp suffix)
Read metadata.json for: files_changed, last_message, elapsed_seconds
```

### Step 2: Identify Trivial Commits

Look at recent commits from document_coverage runs. Ask for EACH commit:
- "Could a human have made this fix in 1-2 minutes?"
- "Does this increase checklist coverage?" (method count)
- "Does this add missing upstream docs?"
- "Is this fixing a cosmetic issue (formatting, tags, reorganization)?"
- "Is this equivalent to the GAPS.md gaps?"

If yes to cosmetic/1-2min, mark as trivial.

### Step 3: Read the Transcript

Find the transcript.log for the trivial commit. Look for:
- **Shallow reading**: Agent glanced at files, didn't read upstream thoroughly
- **Easy pivot**: Agent found one trivial gap, then stopped or moved to another easy task
- **Verification theater**: Agent "checked for gaps" but found none because they didn't read deeply
- **Wrong task selection**: Agent picked "mathematical_contract_audit" but only fixed tag legends
- **No upstream comparison**: Agent never compared upstream vs checklist (the real work)

### Step 4: Map to Structural Cause

Use the playbook's failure mode table. Common causes:
- **Verify-And-Stop**: Agent picked task, verified something exists, declared success
- **Completion Cliff**: Agent found cosmetic gap, fixed it, called it done
- **Overexcitement**: Agent claimed success without substantive work
- **Context Accumulation**: Agent re-read same files, didn't progress

### Step 5: Fix the Prompt/Playbook

The root cause is NEVER "the agent was lazy." It's ALWAYS a structural defect:
- Vague instructions that let agent conclude "done" early
- Missing mandatory deep-work requirements
- Quality questions that enable "considered but nothing needed" reasoning
- Task selection that lets agent pick easy paths

Fix by:
- Adding concrete task requirements (e.g., "must compare upstream vs checklist line by line")
- Removing vague "consider" language
- Explicitly forbidding trivial work types
- Adding verification that can't be faked

## Critical Questions While Reading Transcript

Ask these for EVERY action:

1. **Is this reading upstream or just reference docs?** (Reference docs are self-authored, not the real work)
2. **Is this comparing method-by-method against a checklist?** (That's the real work)
3. **Could this gap have been found in 30 seconds?** (If yes, it's trivial)
4. **Did the agent actually complete a deep audit, or just glance around?**
5. **Would this edit increase the number of documented methods?** (If no, it's cosmetic)
6. **Does this address any gap in GAPS.md?** (If no, it's probably trivial)

## Output Format

For each trivial commit found:

```
## Trivial Commit: <hash>

**What happened**: <one sentence>
**Why it's trivial**: <could human do in 1-2 min? does it increase coverage?>
**Transcript evidence**: <key lines showing shallow work>
**Root cause**: <which playbook/prompt defect enabled this>
**Fix**: <what to change in playbook/prompt>
```

## Then: Fix the Playbook

After identifying 3+ similar trivial patterns, propose a concrete fix to the playbook:
- Remove the vague instruction that enabled the trivial work
- Add a specific requirement that forces deep work
- Explicitly forbid the trivial work type
- Test the fix conceptually against future agent runs
