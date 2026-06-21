---
order: 20
title: Mutations
---

```bash
# Update a memory body
agent-memory update projects/<project-id>/decisions/parser-choice --content "Updated Markdown body."

# Delete a memory
agent-memory delete projects/<project-id>/decisions/parser-choice

# Restructure (kept separate from normal CRUD)
agent-memory maintain move <key> --to global/traps
agent-memory maintain split <key> --section "Section Title"
agent-memory maintain merge <key> --reference <other-key>
agent-memory maintain squash <key> --depth 3
```
