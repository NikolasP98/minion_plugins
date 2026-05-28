---
name: thermonuclear-code-quality-review
description: Use any time someone asks for a thermonuclear review or a thorough/intense code review of a PR or some changes. Adversarially hunts for the highest-severity correctness, security, data-loss, and concurrency issues with file:line evidence and a terse, severity-grouped report.
---

# Thermonuclear code quality review

Adversarially hunt for the highest-quality, highest-severity issues in a set of changes. Lead with the conclusion, support every claim with file:line evidence, and stay brutally concise.

## TL;DR (do this)

1. **Get the diff.** Prefer an explicit base/range from the user. If absent, infer the smallest correct range (see "Selecting the change set").
2. **Read the surrounding code, not just the patch.** Open changed files and their call sites; understand the contract before judging behavior.
3. **Hunt adversarially.** Look for the failure modes in the checklist. Prefer correctness, security, data-loss, and concurrency issues over style.
4. **Verify before claiming.** Don't report an issue unless you can point to the exact `file:line` and explain the trigger and impact.
5. **Report tersely.** Group by severity. Each finding: one-line claim → why it matters → minimal fix. Include a "Top 3" up top.

## Selecting the change set

- If the user gives a base branch, SHA, or range, use it verbatim.
- For a feature branch, diff against the merge-base with the trunk (e.g. `git merge-base HEAD origin/main`), not the raw tip, to avoid noise from unrelated commits.
- For "my uncommitted work," review the working tree + staged changes.
- When in doubt, state the range you chose and proceed.

## What to hunt for (priority order)

1. **Correctness / logic errors** — off-by-one, inverted conditions, wrong operator, missing return, mishandled null/undefined, incorrect error handling, broken invariants.
2. **Security** — injection (SQL/shell/HTML), authz/authn gaps, secrets in code/logs, unsafe deserialization, SSRF, path traversal, missing input validation on trust boundaries.
3. **Data loss / integrity** — destructive migrations, unbounded deletes/updates, missing transactions, race conditions on shared state.
4. **Concurrency** — data races, deadlocks, check-then-act, non-atomic read-modify-write, unsafe shared mutable state.
5. **Resource & performance** — leaks (fd/conn/memory), N+1 queries, unbounded growth, accidental O(n^2), missing pagination/timeouts.
6. **API & contract** — breaking changes, inconsistent error semantics, violated invariants, backward-incompat serialization.
7. **Tests** — missing coverage for the risky path, tests that assert nothing, flaky timing assumptions.

## Severity rubric

- **Critical** — exploitable security hole, data loss, or guaranteed production breakage.
- **High** — wrong results on a common path, race that will trigger under normal load, resource leak that compounds.
- **Medium** — edge-case bug, missing validation behind a less-common path, performance cliff under load.
- **Low** — minor correctness nit, fragile-but-currently-correct code, missing test for a non-critical path.

Drop anything below Low. Do not pad the report.

## Output format

Start with the conclusion. Keep it skimmable.

```
## Thermonuclear review — <range or description>

**Top 3**
1. <Critical/High>: <one-line claim> — `path:line`
2. ...
3. ...

### Critical
- **<claim>** — `path:line`
  - Why: <trigger + impact in 1-2 sentences>
  - Fix: <smallest correct change>

### High
- ...

### Medium
- ...

### Low
- ...

**Verdict:** <ship / fix-criticals-first / needs-rework>, plus 1-2 line rationale.
```

Rules for the report:

- Lead with the **Top 3** so the reader gets value immediately.
- Every finding needs a concrete `file:line` (or a tight range) — no vague "somewhere in X".
- One finding per bullet. No repetition across severities.
- Prefer the **smallest correct fix**; show a 1-3 line patch only when it clarifies.
- If you find nothing at a severity, omit the section. If the change is clean, say so plainly and stop.
- No filler, no praise, no restating the diff. Brutal concision.

## Anti-patterns (don't do this)

- Reporting style/formatting as if it were severity-worthy.
- "Consider maybe possibly" hedging. Make the call.
- Dumping the whole diff back at the user.
- Claiming a bug without a trigger path. If you can't explain how it breaks, it's not a finding.
- Inventing line numbers. Verify against the actual file.
