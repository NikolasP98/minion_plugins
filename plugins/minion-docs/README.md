# minion-docs

Minion codebase documentation expert, code reviewer, and best-practice advisor with structured assessment output.

## What it does

Serves as an expert on Minion conventions and patterns:

- **Code Review**: Structured assessments with file:line references
- **Best Practices**: Finds existing implementations and explains why they're better
- **Documentation Navigation**: Searches local docs, CHANGELOG, and GitHub issues
- **Upstream Analysis**: Categorizes and explains recent upstream changes
- **Pattern Guidance**: Shows correct patterns for CLI commands, error handling, config access, etc.

## Prerequisites

This plugin is designed for the Minion project and works best with:

- The Minion codebase available locally
- Access to `docs/` directory for documentation
- GitHub CLI (`gh`) for issue searches

## Skills

- `minion-docs` — Documentation expert and code reviewer

## Usage

Trigger with: "minion docs", "is this good practice", "code review", "what's new", "explain change"
