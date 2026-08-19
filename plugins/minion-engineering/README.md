# minion-engineering

Curated MINION engineering discipline, precise technical writing, and advisory-only
deterministic prose auditing, packaged as three namespaced progressive-disclosure skills.

## Skills

- `minion-engineering` — implementation, debugging, testing, review, blast-radius,
  TypeScript and boundary discipline, idempotency, and structural prevention.
- `minion-technical-writing` — human-facing technical prose and agent-facing material
  (`AGENTS.md`, `CLAUDE.md`, skills, prompts) where exact symbols and commands must survive.
- `minion-unslop` — deterministic phrase, structure, silhouette, and readability scans over
  English Markdown, plus the fact-preservation tools used to check a requested rewrite.

Each `SKILL.md` loads its own references on demand; read those rather than duplicating
their guidance here.

## UNSLOP authority limits

`minion-unslop` is **report-only by default, advisory, English-only, and preservation-first**.
A scanner match never authorizes a rewrite, verdict, publication, merge, or approval, and
the skill rewrites nothing unless a human explicitly asks in the current task. Upstream's
latest valid public result is **NO-SHIP**. See
[skills/minion-unslop/references/core-contract.md](skills/minion-unslop/references/core-contract.md)
for the full contract.

## Install

Installs with the marketplace (see the repository [README](../../README.md)). The skills also
run under Cursor and Codex; the repository README documents the project-local
`.agents/skills/` copy those harnesses need.

## Attribution

Vendored and adapted MIT-licensed material with exact upstream commit pins is listed in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
