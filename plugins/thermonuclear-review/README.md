# thermonuclear-review

Adversarial, highest-severity code-quality review for pull requests and diffs.

Ships the `thermonuclear-code-quality-review` skill: it hunts for the worst issues
first — correctness, security, data-loss, concurrency — backs every claim with a
concrete `file:line` trigger, and returns a terse, severity-grouped verdict
(Top 3 → Critical → High → Medium → Low → ship / fix-criticals-first / needs-rework).

## Use locally

In any Claude Code session:

```
/thermonuclear-code-quality-review
```

or just ask for "a thermonuclear review of these changes". Give it a base/range
(branch, SHA, `main..HEAD`) when you have one; otherwise it infers the smallest
correct change set.

## Use in CI (PR review)

Reference this plugin from a GitHub Actions workflow with the official
`anthropics/claude-code-action`, so every PR gets an automated thermonuclear
review comment:

```yaml
name: Thermonuclear Code Review
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]

jobs:
  thermonuclear-review:
    if: github.event.pull_request.draft == false
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: read
      issues: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: anthropics/claude-code-action@v1
        with:
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
          plugin_marketplaces: 'https://github.com/NikolasP98/minion_plugins.git'
          plugins: 'thermonuclear-review@minion-plugins'
          prompt: |
            Use the "thermonuclear-code-quality-review" skill to review this pull
            request: ${{ github.repository }} PR #${{ github.event.pull_request.number }}
            (base branch: ${{ github.event.pull_request.base.ref }}). Follow the skill
            exactly and post a single severity-grouped review comment. If the change
            is clean, say so plainly and stop.
```

### Prerequisites per repo

- The **Claude GitHub App** installed on the repo (provides PR commenting).
- A `CLAUDE_CODE_OAUTH_TOKEN` repository secret (`claude /install-github-app` sets both up).

Generated from the personal `thermonuclear-code-quality-review` skill.
