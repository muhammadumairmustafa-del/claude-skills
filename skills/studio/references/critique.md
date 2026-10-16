# Critique and review

Use when reviewing an existing UI (yours or theirs) or as the final self-check after building.

## 1. Look at it for real
Render it and screenshot at **375**, **768** and **1440** wide, light and dark, plus RTL if relevant. Run `scripts/audit.js` in the page (see SKILL.md) for contrast, overflow, small targets and missing labels. Judgement from code alone misses most visual problems.

## 2. Score — Nielsen heuristics, 0–4 each
| # | Heuristic | 0 = broken … 4 = excellent |
|---|---|---|
| 1 | Visibility of system status | |
| 2 | Match with the real world (language, concepts) | |
| 3 | User control & freedom (undo, back, exit) | |
| 4 | Consistency & standards | |
| 5 | Error prevention | |
| 6 | Recognition over recall | |
| 7 | Flexibility & efficiency (shortcuts, defaults) | |
| 8 | Aesthetic & minimalist design | |
| 9 | Help users recognise/recover from errors | |
| 10 | Help & documentation (contextual) | |

Total /40. Most real UIs land 20–32; be honest rather than generous.

Then score visual craft 0–4 on: **hierarchy** (squint test), **spacing rhythm**, **typography**, **colour & contrast**, **distinctiveness** (would this be mistaken for a template? check `tells.md`), **states & edge cases**, **responsiveness**, **motion appropriateness**.

## 3. Findings
List issues by priority:
- **P0** — blocks a task, breaks accessibility, loses data, or looks broken.
- **P1** — causes confusion, inconsistency, or clearly generic/templated feel.
- **P2** — polish.

Each finding: where (file:line or screen + element), what's wrong, why it matters to the user, the fix.

## 4. Fixes
When applying fixes, report as:

| Before | After | Why |
|---|---|---|

Re-screenshot after fixing and show the before/after. Don't stop at the list if the user asked for improvements.
