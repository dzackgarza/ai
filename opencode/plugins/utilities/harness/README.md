# OpenCode Automation Harness (`opx`)

This directory is in retirement mode. The primary harness now lives in the private
repo `dzackgarza/opencode-manager`.

Use these entrypoints:

```bash
just opencode-harness run --help
just opencode-session --help
```

Direct GitHub-backed commands:

```bash
npx --yes --package=git+ssh://git@github.com/dzackgarza/opencode-manager.git opx --help
npx --yes --package=git+ssh://git@github.com/dzackgarza/opencode-manager.git opx-session --help
```

`./opx` remains only as a compatibility wrapper to the external package during the
cutover.
