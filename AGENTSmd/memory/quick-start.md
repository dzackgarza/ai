---
order: 10
title: Quick Start
---

```bash
# Initialize the memory store in a project
iwe init

# Create a new memory
iwe new "My Memory"

# Retrieve a memory with surrounding context
iwe retrieve -k my-memory

# Search across all memories (fuzzy text + YAML field filters)
iwe find "search term"

# Count memories matching criteria
iwe count --filter 'status: draft'

# Normalize all memories to consistent formatting
iwe normalize

# View the hierarchy tree from any starting point
iwe tree

# Analyze the memory store
iwe stats

# Export the memory graph as DOT for visualization
iwe export -f dot
```
