# OpenCode Automation Harness

This directory is in retirement mode. The primary harness now lives in the external
repo `dzackgarza/opencode-manager` as the `ocm` CLI.

Use these entrypoints:

```bash
just opencode-harness run --help
just opencode-session --help
```

Direct commands via `uvx`:

```bash
uvx --from git+https://github.com/dzackgarza/opencode-manager.git ocm --help
```

`./opx` and `./opx-session` remain only as compatibility wrappers during the
cutover.
