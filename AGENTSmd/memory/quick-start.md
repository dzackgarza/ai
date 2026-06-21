---
order: 10
title: Quick Start
---

```bash
# Create a memory (types: decision, trap, advice, context, reference, plan)
agent-memory add --scope project --type decision --title "Parser choice" --content "Use the existing parser boundary."

# Retrieve a memory by key
agent-memory retrieve projects/<project-id>/decisions/parser-choice

# Default search when unsure which mode fits (returns deduped JSON)
agent-memory search --scope both "parser"

# Explicit search modes
agent-memory search keys --scope project "parser"
agent-memory search content --scope both --mode exact "literal text"
agent-memory search content --scope both --mode fuzzy "approximate topic"
agent-memory search content --scope both --mode ranked "semantic context"
agent-memory search metadata --scope project --type decision --tag project

# Read-only inspection of a large vault
agent-memory inspect overview --scope both --format json
agent-memory inspect tree --scope project --depth 2 --format json
```

Run `agent-memory --help` and `agent-memory <subcommand> --help` for the full surface.
