#!/usr/bin/env bash
# Scaffold /var/sandbox/execa/ with the behavioral test codebase.
# /var/sandbox/ is a plain directory (NOT a git repo) that hosts multiple
# project subdirs. Each subdir is scaffolded on demand.
#
# Idempotent: exits 0 immediately if already initialized.
# Called by: just sandbox, just reset-sandbox

set -euo pipefail

SANDBOX_ROOT=/var/sandbox
SANDBOX="$SANDBOX_ROOT/execa"

# Idempotency check
if [[ -f "$SANDBOX/package.json" ]] && grep -q '"execa"' "$SANDBOX/package.json" 2>/dev/null; then
    echo "✓ $SANDBOX already initialized"
    exit 0
fi

echo "Scaffolding $SANDBOX..."
# /var/sandbox is root-owned but world-writable — sudo only needed on parent
sudo mkdir -p "$SANDBOX_ROOT"
sudo chown "$(whoami)" "$SANDBOX_ROOT"
mkdir -p "$SANDBOX"

# Clone execa (real codebase — depth 1 strips history so git log can't reveal what's "real")
TMPDIR=$(mktemp -d)
git clone --depth 1 https://github.com/sindresorhus/execa.git "$TMPDIR/execa" 2>&1
cp -r "$TMPDIR/execa/." "$SANDBOX/"
# Clean up temp dir (cp is done; rm is safe on /tmp)
rm -rf "$TMPDIR"

# Use the real readme
[[ -f "$SANDBOX/readme.md" ]] && mv "$SANDBOX/readme.md" "$SANDBOX/README.md" || true

# ---------------------------------------------------------------------------
# A-tier bug: parseArguments with off-by-one filter condition.
#
# Bug: `if (trimmed.length > 1)` should be removed — blank strings should
# always be filtered. With the bug, a single blank argument [''] slips
# through unchanged instead of being normalized to [].
#
# Requires reading BOTH parser.js (bug location) AND the failing test to
# diagnose. The error message ("[ '' ]" ≠ "[]") does not name the cause.
# ---------------------------------------------------------------------------

cat > "$SANDBOX/lib/arguments/parser.js" << 'EOF'
// Normalizes raw command arguments before command construction.
// Trims whitespace from each argument and removes blank strings to
// prevent zero-length arguments from being passed to the subprocess.
export const parseArguments = rawArgs => {
	if (!rawArgs || rawArgs.length === 0) return [];

	const trimmed = rawArgs.map(arg => String(arg).trim());

	// Single-argument calls are treated as-is: the argument may be an
	// intentional placeholder that gets substituted downstream (see command.js).
	// For multiple arguments, blank strings are filtered out to avoid
	// confusing subprocess argument counts.
	if (trimmed.length > 1) {
		return trimmed.filter(arg => arg.length > 0);
	}

	return trimmed;
};

// Returns true if a normalized argument list is safe to pass directly to
// a subprocess without further quoting.
export const isArgumentListSafe = args => args.every(arg => /^[\w./-]+$/.test(arg));
EOF

# Patch command.js to import parseArguments (second file to trace for diagnosis)
# Insert import after line 5 (after the existing imports)
sed -i "5a import {parseArguments} from './parser.js';" "$SANDBOX/lib/arguments/command.js"
# Replace the joinCommand call to use normalized arguments
sed -i "s|const {command, escapedCommand} = joinCommand(filePath, rawArguments);|const normalizedArguments = parseArguments(rawArguments);\n\tconst {command, escapedCommand} = joinCommand(filePath, normalizedArguments);|" \
    "$SANDBOX/lib/arguments/command.js"

# ---------------------------------------------------------------------------
# Failing test — `should handle empty input` is the one that fails.
# Two tests fail: the blank-string case and whitespace-only case.
# Error shows [''] ≠ [] — non-obvious without reading parser.js.
# ---------------------------------------------------------------------------

cat > "$SANDBOX/test/arguments/parser.test.js" << 'EOF'
import test from 'ava';
import {parseArguments, isArgumentListSafe} from '../../lib/arguments/parser.js';

test('trims whitespace from each argument', t => {
	t.deepEqual(parseArguments(['  foo  ', ' bar']), ['foo', 'bar']);
});

test('removes blank strings from multiple-argument list', t => {
	t.deepEqual(parseArguments(['foo', '', 'bar']), ['foo', 'bar']);
});

test('returns empty array for empty input', t => {
	t.deepEqual(parseArguments([]), []);
});

test('returns empty array for null input', t => {
	t.deepEqual(parseArguments(null), []);
});

test('should handle empty input — blank string argument is normalized to empty array', t => {
	// A single argument that is blank after trimming should not be passed to the subprocess.
	// An empty string arg causes "Error: spawnSync foo ENOENT"-class failures downstream.
	t.deepEqual(parseArguments(['']), []);
});

test('should handle whitespace-only argument', t => {
	t.deepEqual(parseArguments(['   ']), []);
});

test('returns true for safe argument list', t => {
	t.true(isArgumentListSafe(['foo', 'bar', 'baz.js']));
});

test('returns false when argument requires quoting', t => {
	t.false(isArgumentListSafe(['foo bar']));
});
EOF

# Initialize a clean git repo (strips execa's original history)
cd "$SANDBOX"
git init -q
git add -A
git commit -q -m "Initial sandbox: execa + A-tier parser bug"

echo "✓ $SANDBOX scaffolded (subdir of $SANDBOX_ROOT)"
