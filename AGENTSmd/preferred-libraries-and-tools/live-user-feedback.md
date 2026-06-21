---
order: 10
title: Live User Feedback
---

File all plans as memories with `agent-memory` (type `plan`; see the Memory section).
Never begin implementation without a user-approved plan.

When the user asks to read or give feedback on a plan, generate the review surface on the fly:

- Render the entire plan as a single self-contained HTML page that visualizes it.
- Serve it on a quick ephemeral local server for review.
- Build in a small inline annotation tool and a global **Post** button that saves the annotation data to a file.
- Read that file back and act on the annotations.

This is a bespoke, on-demand review tool — generate it when requested, not a standing service.
