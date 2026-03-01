<!-- AGENTS.md-OTP: X7K9-MNPR-QW42 -->

# Agent Guidelines

## Hard Rules

1. **Checkpoint before every edit.** `git commit` (or `git add`) the current state BEFORE editing. Verify with `git diff` after.
2. **Never use `rm`.** Use `trash` or `gio trash`. Deletions must be recoverable.
3. **Load applicable skills before acting.** Scan all available skills. If one applies, load it. Do not proceed until verified.
4. **Run at project start:** `serena_activate_project`, then `serena_read_memory`.
5. **Never write time estimates.** Your calibration is off by orders of magnitude.

---

## Epistemic Integrity

Absence of evidence is not evidence of absence. This is the single most common agent failure mode.

**When reporting that something was not found, use this format:**

```
- Searched: [specific sources, URLs, docs, commands run]
- Found: [what was or was not found]
- Conclusion: [labeled as inference — "I believe", "based on limited evidence"]
- Confidence: [High / Medium / Low]
- Gaps: [what remains unsearched]
```

Omitting any field is a rule violation.

| Wrong | Correct |
|-------|---------|
| "There's no endpoint for X" | "I found no documented endpoint for X in [sources]" |
| "X doesn't exist" | "I found no evidence of X in [sources]" |
| "This feature is not supported" | "I found no documentation of this feature in [sources]" |

**Self-check before every response containing a negative finding:**

1. Did I search, or am I assuming?
2. Did I report what I searched, or claim universal knowledge?
3. Did I label my conclusion as inference?
4. Did I fill in all five fields above?

Never skip from "I found nothing" to "nothing exists."

---

## Tools

**Web search:** Use `kindly_web_search` (never `google_search`). Use `kindly_get_content` to fetch URLs.

**Context7:** Use for ALL library/framework/API questions. `context7_resolve-library-id` → `context7_query-docs`.

**Edits:**

| Situation | Tool |
|-----------|------|
| Small, exact replacement | `edit` |
| Large file (500+ lines), scattered changes, complex refactoring | `morph_edit` |

**Search:**

| Question | Tool |
|----------|------|
| Can you write the grep pattern? | `grep` |
| Natural language / exploratory? | `warpgrep` |

WarpGrep examples: "How does the moderation appeals flow work?" Grep examples: `pattern="fileAppeal"`, `pattern="class.*Service"`. Do not use WarpGrep for quick lookups or known file reads.

---

## Engineering Rules

- **Favor mature dependencies.** Do not reinvent wheels.
- **Iterate, don't replace.** Edit existing files. Writing an entire file is rarely correct. Run `git diff` after rewrites — see what you lost. If valuable, restore it.

---

## Memory

Memories store durable, reusable agent context not captured in repository files.

**Store:** Stable operational guidance, environment quirks, cross-session execution context.

**Do not store:** Audit trails, decision logs, changelogs, work summaries. Those belong in git.

---

## Chat Responses After Completing Work

Do not summarize what was done. The git commit message is the summary — refer the user to it if they want a record.

**Chat output after a task should contain only:**
- Items NOT completed and why
- Gaps or open questions identified during the work
- Errors or surprises that were skipped and need revisiting
- Decisions made during the process that may need user review
- Next actions, if any

If none of the above apply, a one-line confirmation is sufficient. A changelog in chat is noise.

---

## Anchor: Epistemic Integrity (Restated)

When you find no evidence of something, you MUST use the five-field format from the Epistemic Integrity section above. Every negative finding requires: Searched, Found, Conclusion (labeled as inference), Confidence, Gaps. No exceptions.
