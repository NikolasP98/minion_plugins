# fork-sync

Multi-phase fork synchronization workflow with resumable upstream evaluation, conflict resolution script generation, and git worktree isolation.

## What it does

Manages the full lifecycle of keeping a fork in sync with upstream:

- **Phase 0**: Clean mirror branch (ensure no custom commits)
- **Phase 1**: Fast-forward mirror to upstream/main
- **Phase 1.5-1.7**: Systematic upstream evaluation with auto-categorization and conflict resolution script generation
- **Phase 2**: Merge into DEV using isolated git worktree
- **Phase 2.5**: Post-merge alias fixup for renamed exports

## Skills

- `fork-sync` — Main workflow with all phases

## Companion files

- `evaluation-reference.md` — Detailed heuristics, schema, and module presentation format for Phase 1.6
- `state/` — Runtime directory for evaluation.json (generated during Phase 1.6)
- `scripts/` — Runtime directory for resolve-conflicts.sh (generated during Phase 1.7)

## Usage

```
/fork-sync
```

Or trigger with: "sync fork", "update from upstream", "evaluate upstream", "resume evaluation"
