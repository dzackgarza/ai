---
order: 20
title: Mutations
---

```bash
# Rename a memory (all links update automatically)
iwe rename old-key new-key

# Delete a single memory (references cleaned up)
iwe delete memory-key

# Bulk delete by filter
iwe delete --filter 'status: archived'

# Overwrite a memory body
iwe update -k memory-key -c "new content"

# Update frontmatter fields
iwe update --filter 'status: draft' --set reviewed=true

# Extract a section into its own memory
iwe extract memory-key --section "Title"

# Inline a referenced memory back into its parent
iwe inline memory-key --reference "other-memory"

# Attach a memory via a configured action (e.g., daily notes)
iwe attach --to today -k memory-key
```

Use `iwe --help` and `iwe <subcommand> --help` to discover the full set of commands and options.
