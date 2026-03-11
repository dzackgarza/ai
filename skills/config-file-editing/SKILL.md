---
name: config-file-editing
description: Use when editing JSON or YAML config files — covers safe read/modify/write patterns with jq, yq, and Python to prevent syntax errors and indentation corruption.
---

# Config File Editing

## Core Rule

**Never edit JSON or YAML directly with text patch tools.** Direct edits introduce indentation errors, syntax corruption, and missed escaping. Always parse → modify → dump.

## Quick Reference

| Task | Tool |
|---|---|
| Read/query JSON | `jq` |
| Read/query YAML | `yq` |
| Modify JSON or YAML | Python (parse → modify → dump) |

Never use `grep`, `head`, `tail`, or `sed` to parse config files.

## Python Pattern (JSON)

```python
import json, pathlib

path = pathlib.Path("config.json")
data = json.loads(path.read_text())

data["key"] = "new_value"          # modify in memory

path.write_text(json.dumps(data, indent=2) + "\n")
```

## Python Pattern (YAML)

```python
import yaml, pathlib

path = pathlib.Path("config.yml")
data = yaml.safe_load(path.read_text())

data["key"] = "new_value"          # modify in memory

path.write_text(yaml.dump(data, default_flow_style=False, allow_unicode=True))
```

## jq / yq for Read-Only Queries

```bash
# Read a value (JSON)
jq '.servers[0].host' config.json

# Read a value (YAML)
yq '.servers[0].host' config.yml
```

Use these for inspection only. For writes, always use the Python pattern above.

## Why This Matters

Direct patch-tool edits on JSON/YAML fail silently when:
- Indentation changes break YAML block scalars
- Commas or brackets are inserted in wrong positions in JSON
- Special characters in values require escaping that text substitution misses

The Python parse → modify → dump cycle handles all of this automatically.
