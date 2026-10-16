#!/usr/bin/env bash
# Run on the Mac after editing a skill in ~/.claude/skills: copies the latest versions here and pushes,
# so cloud sessions pick up the change on their next start.
set -euo pipefail
cd "$(dirname "$0")"
for s in studio theme fonts logo-studio; do
  rsync -a --delete --exclude '.venv' --exclude '__pycache__' --exclude 'history.json' --exclude 'history.jsonl' \
    --exclude '*.pyc' --exclude '.DS_Store' "$HOME/.claude/skills/$s/" "skills/$s/"
done
git add -A
git diff --cached --quiet && { echo "nothing changed"; exit 0; }
git commit -qm "Sync skills $(date +%F)"
git push -q
echo "pushed"
