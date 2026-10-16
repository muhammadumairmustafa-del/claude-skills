# Systems: scales and tokens

Directions decide *character*; systems keep it coherent. Use these as defaults, especially for app UI (operate/read modes). For persuade/experience pages, the signature moment may break a scale on purpose — once, visibly, never by accident.

## Spacing
4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128. Neighbouring steps differ by ≥25% so choices are distinguishable. More space above a heading than below it (it belongs to what follows). Group with proximity before reaching for borders or boxes.

## Type
- Scale (px): 12 · 14 · 16 · 18 · 20 · 24 · 30 · 36 · 48 · 60 · 72 (+ one oversized display size if the direction calls for it). Mobile body ≥16px (prevents iOS zoom), never <12px.
- Body line-height 1.5–1.65 (serif a bit more); headings 1.05–1.25. Letter-spacing no tighter than −0.04em on large display; loosen small caps/labels slightly.
- Line length 45–75 characters for body (`max-width: 65ch`).
- Two or three weights. De-emphasise with colour or size before weight; nothing below 400 for body.
- `text-wrap: balance` on headings, `pretty` on paragraphs; `font-variant-numeric: tabular-nums` for numbers in tables, prices, timers.
- Load fonts with `font-display: swap` and match fallback metrics to limit layout shift.

## Colour
- Get the palette from `/theme` (Wada) when the direction says so: `python3 ~/.claude/skills/theme/scripts/theme.py find …` then `tokens N [--dark]`. It handles contrast.
- Otherwise build in OKLCH/HSL: 8–10 neutrals (tinted slightly toward the brand hue, never pure grey), 5–10 shades per hue. Start from the 500, then 900 and 100, fill between. Raise saturation toward the light and dark ends.
- Semantic tokens only in components: `--bg, --surface, --surface-2, --text, --text-muted, --border, --accent, --on-accent, --danger, --success, --warning, --focus`. No raw hex in components.
- One accent per view for action. Status colours never carry meaning alone (add icon/text).
- Dark mode is its own design, not an inversion: lift surfaces with lightness instead of shadows, desaturate accents slightly, avoid pure #000 and pure #fff text.

## Radius
Pick from the direction's shape language and make it hierarchical: small controls < cards < sheets/modals. Nested radius = outer radius − padding (concentric corners).

## Elevation (if the direction uses shadows)
Five levels tied to meaning: 0 flat, 1 resting card, 2 raised/hover, 3 dropdown/popover, 4 modal. Two-layer shadows (tight + soft ambient), shadow tinted toward the background hue.

## Motion
- Easing: ease-out for entering/responding, e.g. `cubic-bezier(0.23, 1, 0.32, 1)`; ease-in-out for moving between places; never ease-in for UI responses.
- Durations: press 100–160ms · hover/tooltip 125–200 · dropdown 150–250 · sheet/modal 200–350 · page/scene 300–500. Exit ≈ 70% of enter.
- Frequency rule: something seen 100+ times a day gets no animation. Keyboard-triggered actions don't animate.
- Animate transform and opacity only; never `transition: all`. Don't scale from 0 (use 0.95 + fade); popovers grow from their trigger; `scale(0.97)` on press.
- Respect `prefers-reduced-motion`: replace movement with fades or nothing.

## Z-index
Fixed scale: base 0 · sticky 10 · dropdown 20 · overlay 30 · modal 40 · toast 50.
