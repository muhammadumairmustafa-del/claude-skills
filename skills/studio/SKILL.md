---
name: studio
description: Personal UI/UX design studio for building and reviewing apps, websites, dashboards and mobile screens end to end — UX structure (jobs, flows, IA, states), a fresh visual direction for every new project (generated from independent design axes and checked against past projects so apps never look alike), token/system setup, building to an accessibility and craft floor, then verifying by actually rendering and screenshotting. Use this whenever the user wants to design, build, redesign, restyle, polish, or critique any user interface — a new app or site, landing page, dashboard, admin panel, onboarding, a screen or component, an iOS/Android/React Native/web UI, an Arabic/Urdu RTL interface — or says things like "make it look good", "this looks generic/AI-made", "give me a design direction", "UX review", or types /studio, even if they don't say "UI/UX".
---

# Studio

You are the design lead for someone who builds a lot of different apps. Two things matter most to them: every product should have its **own** identity (not the same look reskinned), and the result should be **genuinely usable** — clear flows, every state handled, accessible, solid on real devices. This skill is the workflow for both.

Files next to this one (read them when the step calls for it, not all upfront):

| File | Read when |
|---|---|
| `references/ux.md` | Planning structure: inventory, jobs, core loop, IA, flows, onboarding, data-dense app UI |
| `references/tells.md` | Planning and self-critique: the generated-design defaults to avoid |
| `references/systems.md` | Setting up tokens: spacing, type, colour, radius, elevation, motion scales |
| `references/floor.md` | Building: accessibility, states, forms, worst-case content, web details |
| `references/platforms.md` | Targeting iOS/Android, or any Arabic/Urdu/RTL interface |
| `references/copy.md` | Writing any interface text |
| `references/critique.md` | Reviewing an existing UI, and the final self-check |
| `scripts/direction.py` | Generating and recording visual directions |
| `scripts/shoot.py` | Screenshotting a page at 3 widths × light/dark (+RTL) and auditing each |
| `scripts/audit.js` | The in-page audit (contrast, overflow, targets, labels) — used by shoot.py or the browser pane |
| `data/axes.json` | The direction vocabulary — editable; `data/history.json` is the project log |

Run the script as `python3 ~/.claude/skills/studio/scripts/direction.py <command>`.

## 0. Size the job first

Not every request needs the whole studio. Decide which track you're on and say so in one line:

- **Tweak** (a component, a fix, a small screen inside an existing product): follow the product's existing design system exactly. Skip directions. Apply `floor.md`, `copy.md`, check visually.
- **Review** ("what's wrong with this", "UX audit", "make this better"): go to `critique.md`, then fix if asked.
- **New screen/flow in an existing product**: do the UX pass (step 2), reuse existing tokens, no new direction.
- **New product or explicit redesign**: full workflow below.

Before designing for an existing product, look for its system: `DESIGN.md`, tokens/theme files, Tailwind config, component library, brand rules in memory. An established brand beats any generated direction — consistency within a product is a feature; variety is *across* products.

## 1. Classify

Pin down four things (infer from the brief and project; ask only what you truly can't infer):

- **Mode** — sets how ambitious the visuals should be:
  - *persuade*: landing pages, marketing — boldest, one memorable signature moment.
  - *operate*: app UI, dashboards, tools — precision and restraint; personality through colour, type and details, never at the cost of speed.
  - *read*: docs, articles, content — typography first.
  - *experience*: portfolios, launches, playful consumer apps — most expressive.
- **Platform**: web, iOS, Android, cross-platform. **Language/direction**: LTR, RTL (Arabic/Urdu), or both.
- **Audience & context**: who, where, on what device, in what state of mind.
- **Stack**: what the project already uses (Next.js/Tailwind/shadcn, Expo/RN, SwiftUI…). For stack-specific implementation details, the `ui-ux-pro-max` skill's search (`--stack`) is a good lookup.

## 2. Structure before style

Read `references/ux.md` and do the parts that fit the scope: a subject inventory (8–12 facts unique to this product), the primary job and core loop, the screen list / IA, the key flows with their failure and recovery paths, and ASCII wireframes of the key screens at mobile and desktop width. For landing pages, outline the page as claims-with-proof, one line per section; drop any section that has no claim.

Keep this brief in the conversation — a compact outline, not a document — unless the user wants a written spec.

## 3. Directions (new products / redesigns)

The point of this step is to break habit. Left alone, every design converges on the same few looks; the generator forces a different starting point and remembers what's been used.

```bash
direction.py suggest --brief "<one-line product description with audience>" --platform web|mobile --mode persuade|operate|read|experience
direction.py history          # what past projects used, and the most-used options
```

Options: `-n 4` for more choices, `--lock type=T3` (repeatable) to keep something the user insists on, `--wild 2` for more surprise, `--seed` to reproduce.

The script gives three directions as a set of axis choices (layout, type voice + candidate fonts, colour strategy + a `/theme` command, shape, depth, motion, density, imagery, signature moment, copy voice), already biased toward the brief and away from past projects. Treat them as provocations, not specs:

- Reinterpret each through the subject inventory. "Organic blob shapes" for a Saudi astrology app might mean arches inspired by local architecture; for a pet app, paw-soft rounded forms. Name each direction with an evocative 2–3 word title that comes from the product's world.
- If an axis fights the brief or the platform, swap it and say why. Never override the user's explicit words.
- Present the three as short cards: title, a 2–3 sentence picture of what it looks and feels like, the signature moment, and why it fits this product. If it helps the user choose, show a quick visual (swatches + type specimen + tiny wireframe) via an inline widget or a small HTML preview.
- Let the user mix ("type from 2, colours from 1"). If they said "just pick", choose one and explain.

Once a direction is chosen, record it so future projects steer away from it:

```bash
direction.py record --project "<name>" --code <CODE> --note "<one line on how it was interpreted>"
```

## 4. Plan the system

Turn the direction into a compact plan before writing UI code:

- **Colour**: run the `/theme` command the direction suggests (the `theme` skill turns a Wada combination into contrast-checked tokens, light + dark), or build per `systems.md`. 4–6 named colours with roles.
- **Type**: pick from the direction's candidate fonts (choose; don't default to the first one), set the scale, weights and line-heights from `systems.md`. If RTL, pair an Arabic/Urdu face per `platforms.md`. If the `fonts` skill is installed, use it to verify the pairing, self-host the files, add metric-matched fallbacks and generate the fluid type-scale tokens.
- **Shape, depth, motion, density**: concrete values (radius scale, shadow levels or "none", easing and durations, spacing density).
- **Signature moment**: exactly one bold thing, placed where it matters. Everything else stays quiet and disciplined.
- **Principles**: 3 one-line rules specific to this product (e.g. "numbers are always the hero", "never more than one action per card").

Then check the plan against `tells.md`: if any part would come out the same for any similar product, revise it and say what changed. Glance at `direction.py history` — if the plan echoes a recent project's fonts or palette, push it further apart.

## 5. Build

- Tokens first (CSS variables / Tailwind theme / RN theme object / SwiftUI asset colours), wired into the project's existing approach. No raw values in components.
- Real content throughout — believable copy, names and numbers for this audience (`copy.md`). Placeholder content makes everything look templated.
- Every state from `floor.md`: empty, loading, error, success, disabled, long content. Light and dark. RTL if relevant (`platforms.md`).
- Native conventions on mobile (`platforms.md`); the direction expresses itself through colour, type, imagery and the signature moment, not by fighting the platform.
- Mind CSS specificity: section-level padding/margin rules silently cancel each other — keep spacing on one layer (layout wrappers or components, not both).

## 6. Verify by looking

Code that looks right in the editor often isn't. For web:

1. Get the page running (the project's dev server via the preview tools, or just the HTML file), then run
   ```bash
   python3 ~/.claude/skills/studio/scripts/shoot.py <url-or-file> --out <dir> [--rtl] [--full]
   ```
   It screenshots at 375, 768 and 1440 wide in light and dark (and RTL with `--rtl`), runs `audit.js` on each, and prints contrast failures, horizontal overflow, small touch targets, unnamed controls, images missing alt, fonts in use and JS errors. **Open the screenshots with Read and look at them.**
   If Playwright isn't available, use the browser pane instead: `resize_window` for widths and `colorScheme`, and pass the contents of `scripts/audit.js` to `javascript_tool` (works on http pages, not file://).
2. Fix every contrast failure, overflow, unnamed control and undersized target (inline text links are exempt). Re-run until clean.
3. Try the worst cases: long strings, empty data, error paths, keyboard-only tab through the page.
4. Look at the screenshots with fresh eyes: squint test for hierarchy; does it look like *this* product or like a template? Before finishing, remove one accessory — the decoration that serves the brief least.

For native apps use the iOS simulator tools (screenshot, Dynamic Type at large sizes, dark mode) or the platform's preview.

Show the user the final screenshots rather than describing the result.

## 7. Leave a trail

For new products, write a short `DESIGN.md` at the project root: direction code and title, tokens (or where they live), fonts, the signature moment, the 3 principles, and do/don't notes. Future sessions (and the Tweak track) read it to stay consistent. Make sure the direction is recorded in history (step 3).

## Notes

- Tell the user which track and mode you chose in one line; don't narrate the whole method.
- When the brief pins a visual direction ("make it look like Linear", "brutalist", "use our brand colours"), follow it — the generator is for open briefs, or for one or two open axes via `--lock`.
- The axes file is meant to grow. When the user loves or rejects a style, offer to add or retire an option in `data/axes.json`.
