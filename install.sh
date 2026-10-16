#!/usr/bin/env bash
# Installs these skills into ~/.claude/skills (personal skills for every Claude Code session).
# Used by the claude.ai/code cloud environment setup script, and safe to run on any machine:
#   curl -fsSL https://raw.githubusercontent.com/muhammadumairmustafa-del/claude-skills/main/install.sh | bash
# Updates files in place; never deletes local-only files (history logs, venvs).
set -euo pipefail

REPO="https://github.com/muhammadumairmustafa-del/claude-skills"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

if command -v git >/dev/null 2>&1; then
  git clone --depth 1 --quiet "$REPO" "$TMP/repo"
else
  curl -fsSL "$REPO/archive/refs/heads/main.tar.gz" | tar -xz -C "$TMP"
  mv "$TMP"/claude-skills-main "$TMP/repo"
fi

mkdir -p "$DEST"
for skill in "$TMP"/repo/.claude/skills/*/; do
  name="$(basename "$skill")"
  # Copy over the existing folder instead of replacing it: files that only exist locally
  # (history logs, the fonts .venv, anything else) are never deleted.
  mkdir -p "$DEST/$name"
  cp -R "$skill". "$DEST/$name/"
  echo "installed skill: $name"
done

# Optional helpers (never fail the setup if these can't install):
#  - fontTools + brotli for the fonts skill's woff2 subsetting
#  - Playwright + Chromium for studio's screenshot/audit step and logo-studio proofs
if command -v python3 >/dev/null 2>&1 && [ "${SKIP_SKILL_DEPS:-0}" != "1" ]; then
  python3 -m pip install --quiet --user fonttools brotli playwright 2>/dev/null \
    || python3 -m pip install --quiet --break-system-packages fonttools brotli playwright 2>/dev/null \
    || echo "note: couldn't pip-install fonttools/brotli/playwright (skills still work, minus those helpers)"
  python3 -m playwright install --with-deps chromium >/dev/null 2>&1 \
    || python3 -m playwright install chromium >/dev/null 2>&1 \
    || echo "note: Playwright Chromium not installed; studio will fall back to the browser pane"
fi
echo "done: skills are in $DEST"
