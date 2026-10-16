# Craft: building a mark in SVG that holds up

Writing SVG by hand is drawing blind. These rules exist because the failure modes are predictable: wobbly geometry, near-miss angles, hairlines that vanish, type that is just a font, and marks that only work because of colour.

## Construction
- **Describe it before drawing.** Write the construction in words first: canvas, grid unit, primitives, radii, angles, and which parts are cut. For example: "256 grid, unit 16. Circle r=96 at centre. Subtract a 32-wide bar rotated 45° through the centre. A dot r=16 at (192,64)." Then write the SVG from that description. This one habit removes most wobbly geometry.
- **Canvas.** Icons use `viewBox="0 0 256 256"` and keep the live area inside 16..240 (about 6% padding). Wordmarks and lockups use whatever the type needs; text2path gives the bounds.
- **Grid and snapping.** Coordinates should be multiples of 8, or 4 for fine details. Use radii from one family: 8, 16, 24, 32, 48, 64, 96, 112. Use angles 0/15/30/45/60/90 only. 22.5° and 67.5° are allowed for 8-fold constructions.
- **Compute curves.** Build arcs, spirals, stars, polygons, petals and radial repeats with `scripts/shapes.py`, or a snippet that prints path data. Never eyeball them. Round coordinates to 2 decimals.
- **Draw black first.** Build every concept in pure #000 on white. Colour comes after the form works in silhouette.
- **Cut, don't paint.** Make holes with `shapes.diff()`, or `fill-rule="evenodd"`, never with white shapes on top. A mark has to work on any background.
- **Strokes become shapes.** Design with `shapes.stroke(centreline, width, cap="round")`, which turns a line into a filled outline that can then be cut or merged. Final files contain no `stroke=` attributes; run `shapes.py outline file.svg` on any that slipped through.
- **Weights.** At 256, minimum stroke or gap is 12, and 16+ is better. At 16 px, anything under 1/16 of the mark disappears.
- **Few parts.** 1–5 shapes is the sweet spot, and 3 colours at most. One focal point.
- **No `<text>` in finals.** Outline type with `scripts/text2path.py`. It shapes with HarfBuzz, so kerning, ligatures and Arabic/Urdu joining are correct.
- **Group and name the parts.** Use `<g id="icon">` and `<g id="wordmark">` so feedback ("make the icon heavier") maps onto the code.

## Optical corrections (why "mathematically correct" looks wrong)
- Round and pointed shapes need about 3–5% **overshoot** past flat edges to look the same size.
- The **optical centre** is slightly above the geometric centre, so nudge a lone symbol up about 2%.
- A circle next to a square of the same width looks smaller. Enlarge it about 5–8%.
- Where strokes meet at an acute angle, the junction gets dark. Thin the strokes into the joint ("ink traps").
- Horizontal strokes look heavier than vertical ones of the same width, so make horizontals about 5–10% thinner.
- In all-caps wordmarks, open up the tracking a little (+20 to +60). In large lower-case wordmarks, tighten it (−10 to −30).

## Type
- A wordmark is never just a font. Make at least one deliberate move:
  - a custom ligature
  - a cut or notch
  - a swapped glyph
  - a joined pair
  - a modified terminal
  - an unusual case mix
  - a single colour accent
- **To modify a glyph,** use `text_to_path(...)["glyphs"]`. Each entry has its own `d`, `x`, `advance` and `bounds`, so you can:
  - cut a notch: `diff(g["d"], rect(...))`;
  - fill a counter: `union(g["d"], circle(...))`;
  - drop a letter and draw your own shape in its slot;
  - colour one glyph, such as Arabic or Urdu dots, which come out as separate glyphs in many fonts.
- **Pick fonts with character for wordmarks.** Neutral UI fonts (Inter, Roboto, plain Jost) are fine for a quiet secondary line. A wordmark built on one needs a strong custom move.
- Lockup ratio: the wordmark cap height should be about 50–60% of icon height, with a gap of about 25–35% of icon height. `pack.py` uses 55% and 30%.
- When the wordmark is wide (tracked caps, long names), the 55% rule makes the icon look tiny. Use cap height ≈ 40–45% of icon height, or a stacked lockup as the primary.
- Pair at most two families, and usually one is enough.

## Bilingual lockups (Latin + Arabic/Urdu)
- **Match visual weight, not point size.** Arabic and Urdu look smaller at the same size. Set the Arabic so its main letter bodies sit level with the Latin x-height, about 1.2–1.4× the Latin size, then judge by eye on the proof.
- **Alignment.** Stacked lockups: Latin left-aligned, Arabic right-aligned, both to the same width. For mirror symmetry, centre both. In a bilingual horizontal lockup, the icon usually sits on the side that starts the primary script: left for English-first, right for Arabic-first.
- **Clearance.** Leave a gap ≥ 0.35× the Latin cap height between lines, measured from Latin descenders (g, y, p) to the tops of Arabic ascenders and dots. Check the actual glyph bounds from text2path; descenders colliding with dots is the classic failure.
- **Matching widths.** Stretch the Arabic with a kashida (insert U+0640 'ـ' inside a word) rather than scaling it horizontally. Kashida only goes between letters that join, never after a non-joining letter (ا د ذ ر ز و).
- **Font pairs that work:**
  - Inter Tight / IBM Plex Sans Arabic
  - Plus Jakarta Sans / Readex Pro
  - Space Grotesk / Tajawal
  - Fraunces / Amiri
  - Reem Kufi on its own (it has Latin too)
  - Urdu: Gulzar or Noto Nastaliq Urdu beside a humanist serif or sans
- **Check the spelling.** Note in the presentation that a native speaker should confirm the Arabic or Urdu spelling.

## Colour
- Start from the theme palette, then check the contrast of the logo against its background. Anything under 3:1 needs a different version for that background.
- Every concept needs an inverse version for dark backgrounds. Run `recolour.py A1.svg --auto-inverse --out A1-inverse.svg`, then adjust with `--map` if the brand wants specific light colours.
- **Contrast.** `svg_lint.py --bg "<background>"` warns for any colour under 3:1. Small accents (a dot, a tittle) are the usual offenders; darken them rather than ignore the warning.
- Colour carries meaning, so avoid the category's default colour unless the brief asks for it. Fintech blue, organic green and food red are all clichés.

## The critique pass (do it on every proof sheet)
Look at `proof.png` and answer honestly for each concept:
0. **Ambition test.** Is the signature move visible right away at 64 px? If the logo is a plain font with a small accent, push it further or replace it.
1. **Small-size test.** At 16 px and 32 px, is it still one clear shape, or mush? If it's mush, simplify or make a small-size cut.
2. **Silhouette test.** In pure black, does it still have its idea? If the idea lives in the colour, it isn't a mark yet.
3. **Squint test.** Blurred, is there one dominant shape, or several fighting?
4. **Letter test.** Does every modified letter still read as itself?
5. **Accident test.** Mirrored or rotated 180°, does it accidentally form a rude, political or competitor-like shape? Check swastika-like rotations, body parts and the logos of other well-known brands.
6. **Cliché test.** Is it on the banned list from the brief (lightbulb for ideas, globe for global, swoosh, speech bubble for chat, leaf for eco, brain or circuit for AI)? If so, it needs a twist, or it goes.
7. **Swap test.** Could this logo belong to a competitor unchanged? If so, it's generic.
8. **App-tile test.** In the proof's app-tile column, is it one confident shape filling about 60% of the tile? Thin, wide or busy marks need an icon cut.
9. **Distinctness test.** Compare against the other concepts in the set at 32 px. Any two that read alike: redo the weaker one in a different mark type.
10. **Geometry test.** Look for near-misses: things that are almost aligned, almost centred, almost equal. Either make them exactly equal or clearly different.

Fix, re-render, look again. Two refine loops is the norm before anything is shown.

## Common SVG mistakes
- Forgetting the `viewBox`, or leaving wide empty margins. Crop to the content, plus padding.
- Strokes in the final file that scale badly in lockups: keep `vector-effect` off, and outline strokes if the mark will be scaled non-uniformly.
- Gradient IDs colliding when several SVGs are inlined on one page (gallery.py renames them, but keep IDs descriptive).
- A transform stack nobody can edit. Bake simple transforms into the coordinates.
