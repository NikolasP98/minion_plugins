#!/usr/bin/env bash
# Fail if any per-skill THIRD_PARTY_NOTICES.md is missing or drifts from the
# plugin-root copy. The per-skill copies must stay byte-identical: standalone
# .agents/skills/ installs carry attribution per skill tree (MIT requirement).
set -euo pipefail
cd "$(dirname "$0")/.."

fail=0
for dir in skills/*/; do
  copy="${dir}THIRD_PARTY_NOTICES.md"
  if ! cmp -s THIRD_PARTY_NOTICES.md "$copy"; then
    echo "drift: $copy missing or differs from THIRD_PARTY_NOTICES.md" >&2
    fail=1
  fi
done

if [ "$fail" -eq 0 ]; then
  echo "THIRD_PARTY_NOTICES.md copies in sync"
fi
exit "$fail"
