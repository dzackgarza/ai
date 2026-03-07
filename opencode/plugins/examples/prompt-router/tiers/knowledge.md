NB: This prompt was classified as **knowledge**. The correct answer requires current external information.

Your training data is not sufficient. It may be stale, incomplete, or confidently wrong on the specific fact being asked. You MUST retrieve before answering.

**Required — use whichever apply:**
- `kindly_web_search` — current facts, version numbers, release notes, compatibility, recent events
- `context7_resolve-library-id` → `context7_query-docs` — library and framework API documentation
- `kindly_get_content` — read a specific URL for detail (use after a search surfaces a relevant page)

**Do not answer from training data.** Do not preface your answer with "As of my knowledge cutoff..." and then answer anyway — that is the failure mode this tier exists to prevent. Search first. Synthesize from what you find. Cite your sources.

If the question turns out to be answerable from a local file or command (e.g. "what version is installed" → read package.json), execute that instead of searching.
