# pr-workflow

Three-phase GitHub PR pipeline: script-first review with structured findings, automated preparation with CI gates, and deterministic squash merge with co-author trailers.

## What it does

Provides three complementary skills for the full PR lifecycle:

### /review-pr
- Sets up isolated worktree for PR review
- Checks existing implementation on main baseline
- Reads PR description, diff, and runs optional tests
- Produces structured `.local/review.md` (sections A-J) and `.local/review.json`
- Read-only — never pushes or modifies code

### /prepare-pr
- Resolves BLOCKER and IMPORTANT findings from review
- Commits scoped changes with concise subjects
- Runs CI gates via wrapper scripts
- Pushes safely with `--force-with-lease` and SHA verification

### /merge-pr
- Validates all artifacts and required checks
- Deterministic squash merge pinned to head SHA
- Adds co-author trailers for PR author and reviewer
- Posts merge comment and cleans up worktree

## Scripts

Bundled bash scripts in `scripts/`:

- `pr-review` — Worktree setup and branch mode switching
- `pr-prepare` — Init, gates, push subcommands
- `pr-merge` — Verify and merge subcommands
- `pr` — Multi-command dispatcher
- `committer` — Explicit-file-list commit wrapper

## Skills

- `review-pr` — Phase 1: Read-only review
- `prepare-pr` — Phase 2: Fix findings and push
- `merge-pr` — Phase 3: Deterministic merge

## Usage

```
/review-pr 123
/prepare-pr 123
/merge-pr 123
```
