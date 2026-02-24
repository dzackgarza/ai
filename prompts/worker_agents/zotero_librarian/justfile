# Zotero Librarian
#
# Usage: just <command>
# Run `just` to see all commands

# Show available commands
help:
    @just --list

# Library overview
stats:
    @.venv/bin/python _dev/scripts/manage.py stats

# All quality issues
quality:
    @.venv/bin/python _dev/scripts/manage.py quality

# Find items without PDF
find-no-pdf:
    @.venv/bin/python _dev/scripts/manage.py find-no-pdf

# Find duplicate titles
find-duplicates:
    @.venv/bin/python _dev/scripts/manage.py find-duplicates

# Find similar tags
find-similar-tags:
    @.venv/bin/python _dev/scripts/manage.py find-similar-tags

# List collections
list-collections:
    @.venv/bin/python _dev/scripts/manage.py list-collections

# List tags
list-tags:
    @.venv/bin/python _dev/scripts/manage.py list-tags

# Tag items missing PDF
tag-needs-pdf:
    @.venv/bin/python _dev/scripts/manage.py tag-needs-pdf

# Python REPL with library loaded
shell:
    @.venv/bin/python -c "from agents import ZoteroAgent; lib = ZoteroAgent(); print('Ready: lib = ZoteroAgent()'); import code; code.interact(local=dict(globals(), **locals()))"

# Install dependencies
install:
    @cd _dev && uv sync

# Run tests
test:
    @cd _dev && uv run pytest

# Format code
fmt:
    @cd _dev && uv run ruff format .

# Lint code
lint:
    @cd _dev && uv run ruff check .
