---
name: repomix
description: Use when packaging a codebase into a single file for AI analysis, third-party library inspection, security audits, or LLM context snapshots.
---
# Repomix Skill

Repomix packs entire repositories into single, AI-friendly files.
Perfect for feeding codebases to LLMs like Claude, ChatGPT, and Gemini.

## When to Use

Use when:

- Packaging codebases for AI analysis

- Creating repository snapshots for LLM context

- Analyzing third-party libraries

- Preparing for security audits

- Generating documentation context

- Investigating bugs across large codebases

- Creating AI-friendly code representations

## Quick Start

### Basic Usage

```bash
# Package current directory (generates repomix-output.xml)
npx -y repomix

# Specify output format
npx -y repomix --style markdown
npx -y repomix --style json

# Package remote repository
npx -y repomix --remote owner/repo

# Custom output with filters
npx -y repomix --include "src/**/*.ts" --remove-comments -o output.md

# Pin to a specific version
npx -y repomix@0.2.31 --remote owner/repo
```

## Core Capabilities

### Repository Packaging

- AI-optimized formatting with clear separators

- Multiple output formats: XML, Markdown, JSON, Plain text

- Git-aware processing (respects .gitignore)

- Token counting for LLM context management

- Security checks for sensitive information

### Remote Repository Support

Process remote repositories without cloning:

```bash
# Shorthand
npx -y repomix --remote yamadashy/repomix

# Full URL
npx -y repomix --remote https://github.com/owner/repo

# Specific commit
npx -y repomix --remote https://github.com/owner/repo/commit/hash
```

### Comment Removal

Strip comments from supported languages (HTML, CSS, JavaScript, TypeScript, Vue, Svelte,
Python, PHP, Ruby, C, C#, Java, Go, Rust, Swift, Kotlin, Dart, Shell, YAML):

```bash
npx -y repomix --remove-comments
```

## Common Use Cases

### Code Review Preparation

```bash
# Package feature branch for AI review
npx -y repomix --include "src/**/*.ts" --remove-comments -o review.md --style markdown
```

### Security Audit

```bash
# Package third-party library
npx -y repomix --remote vendor/library --style xml -o audit.xml
```

### Documentation Generation

```bash
# Package with docs and code
npx -y repomix --include "src/**,docs/**,*.md" --style markdown -o context.md
```

### Bug Investigation

```bash
# Package specific modules
npx -y repomix --include "src/auth/**,src/api/**" -o debug-context.xml
```

### Implementation Planning

```bash
# Full codebase context
npx -y repomix --remove-comments --copy
```

## Command Line Reference

### File Selection

```bash
# Include specific patterns
npx -y repomix --include "src/**/*.ts,*.md"

# Ignore additional patterns
npx -y repomix -i "tests/**,*.test.js"

# Disable .gitignore rules
npx -y repomix --no-gitignore
```

### Output Options

```bash
# Output format
npx -y repomix --style markdown  # or xml, json, plain

# Output file path
npx -y repomix -o output.md

# Remove comments
npx -y repomix --remove-comments

# Copy to clipboard
npx -y repomix --copy
```

### Configuration

```bash
# Use custom config file
npx -y repomix -c custom-config.json

# Initialize new config
npx -y repomix --init  # creates repomix.config.json
```

## Token Management

Repomix automatically counts tokens for individual files, total repository, and
per-format output.

Typical LLM context limits:

- Claude Sonnet 4.5: ~200K tokens

- GPT-4: ~128K tokens

- GPT-3.5: ~16K tokens

## Security Considerations

Repomix uses Secretlint to detect sensitive data (API keys, passwords, credentials,
private keys, AWS secrets).

Best practices:

1. Always review output before sharing

2. Use `.repomixignore` for sensitive files

3. Enable security checks for unknown codebases

4. Avoid packaging `.env` files

5. Check for hardcoded credentials

Disable security checks if needed:

```bash
npx -y repomix --no-security-check
```

## Implementation Workflow

When user requests repository packaging:

1. **Assess Requirements**

   - Identify target repository (local/remote)

   - Determine output format needed

   - Check for sensitive data concerns

2. **Configure Filters**

   - Set include patterns for relevant files

   - Add ignore patterns for unnecessary files

   - Enable/disable comment removal

3. **Execute Packaging**

   - Run repomix with appropriate options

   - Monitor token counts

   - Verify security checks

4. **Validate Output**

   - Review generated file

   - Confirm no sensitive data

   - Check token limits for target LLM

5. **Deliver Context**

   - Provide packaged file to user

   - Include token count summary

   - Note any warnings or issues

## Reference Documentation

For detailed information, see:

- [Configuration Reference](./references/configuration.md) - Config files,
  include/exclude patterns, output formats, advanced options

- [Usage Patterns](./references/usage-patterns.md) - AI analysis workflows, security
  audit preparation, documentation generation, library evaluation

## Additional Resources

- GitHub: https://github.com/yamadashy/repomix

- Documentation: https://repomix.com/guide/

- MCP Server: Available for AI assistant integration
