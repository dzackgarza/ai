#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Read qc-excludes.toml and output the canonical exclusion directory list.

Usage:
  uv run scripts/read_qc_excludes.py                        # one directory per line
  uv run scripts/read_qc_excludes.py --format json           # JSON array of strings
  uv run scripts/read_qc_excludes.py --format rg-globs       # -g '!**/dir/**' lines
  uv run scripts/read_qc_excludes.py --format codeql         # codeql format
  uv run scripts/read_qc_excludes.py /path/to/qc-excludes.toml   # explicit config path

When no path is given, looks for qc-excludes.toml in ancestor directories.
"""

import json
import sys
from pathlib import Path


def find_config() -> Path:
    """Walk up from CWD to find qc-excludes.toml."""
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        candidate = parent / "qc-excludes.toml"
        if candidate.is_file():
            return candidate.resolve()
    print(
        "ERROR: qc-excludes.toml not found in any ancestor directory.", file=sys.stderr
    )
    sys.exit(1)


def load_excludes(config: Path) -> list[str]:
    import tomllib

    with config.open("rb") as f:
        data = tomllib.load(f)
    return data["directories"]


def main() -> None:
    fmt = "plain"
    config_path: Path | None = None

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--format" and i + 1 < len(args):
            fmt = args[i + 1]
            i += 2
        elif args[i].startswith("--format="):
            fmt = args[i].split("=", 1)[1]
            i += 1
        elif args[i].startswith("--"):
            print(f"ERROR: unknown flag {args[i]}", file=sys.stderr)
            sys.exit(1)
        else:
            config_path = Path(args[i])
            i += 1

    if config_path is None:
        config_path = find_config()
    else:
        config_path = config_path.resolve()

    dirs: list[str] = load_excludes(config_path)

    if fmt == "plain":
        for d in dirs:
            print(d)
    elif fmt == "json":
        json.dump(dirs, sys.stdout, indent=2)
        print()
    elif fmt == "rg-globs":
        for d in dirs:
            print(f"-g '!**/{d}/**'")
    elif fmt == "codeql":
        # CodeQL uses --search-path exclusions
        for d in dirs:
            print(
                f"--search-path=/dev/null --additional-packs=/dev/null  # excludes {d}"
            )
    else:
        print(f"ERROR: unknown format '{fmt}'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
