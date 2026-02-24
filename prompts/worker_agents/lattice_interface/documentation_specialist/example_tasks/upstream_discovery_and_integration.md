# Example Task: Upstream Discovery and Integration

## Goal

Pick one in-scope package. **Survey ALL local upstream docs, research ALL online sources, integrate ALL missing documentation.** Do not stop until the complete upstream surface is captured locally.

## Process

1. First, **select ONE in-scope package** — e.g., `g6k`
2. Then, **inventory ALL local upstream files** — list every file in `docs/<pkg>/upstream/`
3. Then, **research online for ALL missing docs** — check official repo, releases, wiki, API docs
4. Then, **fetch ALL missing upstream files** — add them to the local collection
5. Then, **verify reference doc coverage** — check if newly added docs reveal new gaps
6. Then, **accumulate ALL findings** — what was added, what still missing
7. Then, **show evidence**: "Package X: local upstream has Y files, added Z new files from [sources]. Here's evidence [list of files added]..."

Show your reasoning at each step. Do not skip steps.

## Workflow

1. **Select a package** — e.g., `g6k`
2. **Inventory local upstream docs:**
   - List all files under `docs/g6k/upstream/`
   - Note what API surfaces they cover (e.g., siever.pyx, README, algorithms/)
3. **Research online:**
   - Find the official repository (e.g., `github.com/fplll/g6k`)
   - Check for documentation not captured locally:
     - README, INSTALL, CONTRIBUTING files
     - Wiki pages or GitHub Pages docs
     - API reference generators (Sphinx, Doxygen output)
     - Tutorial/example notebooks
     - Release notes with new API surfaces
4. **Integrate missing docs:**
   - Fetch missing files into `docs/g6k/upstream/`
5. **Verify reference doc coverage:**
   - After integration, check if reference doc covers all newly added upstream material

## Example Output

```markdown
Added to docs/g6k/upstream/:
- CONTRIBUTING.md (API stability notes)
- docs/siever_params.rst (parameter reference)
- examples/challenge_svp.ipynb (usage patterns)
```

## Purpose

This task ensures local upstream collections are complete, not just convenient.

## Network Contingency

If a known/canonical upstream URL is discovered via web results but direct shell retrieval fails (DNS/TLS/connectivity failure):
- Retry the same URL a small fixed number of times (`<=2`)
- Treat this as an environment access failure, not proof that upstream docs do not exist
- If a source is genuinely unreachable and the gap is actionable, write a Serena memory with the URL and the specific method-surface gap it would fill
- Then pivot to substantial offline work from existing local snapshots
