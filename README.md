# claude-skills

Personal design skills for Claude Code:

| Skill | What it does |
|---|---|
| `studio` | End-to-end UI/UX: structure, a fresh visual direction per project, tokens, quality floor, screenshot audit |
| `theme` | Colour palettes from Sanzo Wada's combinations → contrast-checked tokens |
| `fonts` | Font choice, pairing (incl. Arabic/Urdu), self-hosting, fallbacks, type scales |
| `logo-studio` | Distinct SVG logo concepts → full brand kit |

## Install

On any machine:

```bash
curl -fsSL https://raw.githubusercontent.com/muhammadumairmustafa-del/claude-skills/main/install.sh | bash
```

For **Claude Code cloud sessions** (claude.ai/code), add that line to your cloud environment's **setup script**, so every cloud session in every repo gets the skills.

Set `SKIP_SKILL_DEPS=1` to skip installing the optional Python helpers (fontTools, brotli, Playwright).

## Updating

Edit the skills in `~/.claude/skills/` on the Mac, then run `./sync.sh` here to push the changes.
