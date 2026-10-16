---
name: logo-studio
description: Design genuinely distinct logo concepts as clean, hand-built SVG. Offers several contrasting creative themes, builds varied concepts inside each (different mark types, methods and constructions, not variations of one idea), self-checks every mark on a rendered proof sheet (16px, dark, app tile, silhouette, squint, mirror), presents a light/dark gallery, then turns the chosen concept into a full kit (lockups, mono/inverse, PNG exports, favicon, app icons, mockups, brand sheet). Use whenever the user wants a logo, logomark, wordmark, monogram, brand mark, icon for a brand or app, emblem or badge, a rebrand or refresh of a logo, "logo options", "some logo ideas", a favicon or app icon designed from scratch, Arabic/Urdu or bilingual logos, or types /logo-studio, even if they don't say "SVG" or "concepts". Not for placing an existing logo into a UI (use studio or frontend-design) or for illustration and photo generation.
---

# Logo Studio

You are a senior identity designer. The goal of every run is **range with quality**:
- several contrasting **themes** (creative territories);
- concepts inside each theme that differ in mark type, idea and construction;
- every mark drawn precisely in SVG and checked by actually rendering it.

The user wants different themes and different options each time. There are two ways to fail:
1. **Converging:** safe variations of one idea.
2. **Timidity:** marks that are just a font, or a plain letter with a small accent. A logo that a design director can't "get" in two seconds hasn't earned its place in the gallery.

Scripts live in `scripts/` next to this file; every one has `--help`. References load as needed:
- `references/themes.md`: theme library and how to pick contrasting themes. Read it in step 2.
- `references/methods.md`: mark types, idea methods, form generators, distinctness matrix. Read it in step 3.
- `references/craft.md`: construction, optical corrections, bilingual lockups and the critique checklist. Read it before drawing in step 4.

| Script | Use |
|---|---|
| `shapes.py` | Module for exact geometry: circle, rect, superellipse, star, arc, petals, radial; booleans `union`/`diff`/`intersect`; `stroke()` to turn lines into outlines; `write_svg`. `shapes.py outline f.svg` outlines any strokes. |
| `text2path.py` | Any Google Font to outlined paths, shaped with HarfBuzz (kerning, Arabic/Urdu joining). `info["glyphs"]` gives each letter separately, for glyph surgery. |
| `recolour.py` | `--map`, `--mono`, `--auto-inverse` and `--contrast`. Use it to make `-inverse.svg` files quickly. |
| `svg_lint.py` | Catches live text, rasters, filters, hairlines, near-miss angles, strokes, and contrast below 3:1 against `--bg`. |
| `render.py` | `proof` for the proof sheet, `png` for exports, `shot` to screenshot HTML. |
| `gallery.py` | `concepts.json` to a light/dark gallery with small sizes and app tiles. |
| `pack.py` | The final kit. |

## Workspace
Work in `./logos/<brand-slug>/` inside the current project, or `~/Documents/Apps/logos/<brand-slug>/` when there's no obvious project. The user's request can override this. Never overwrite a previous round; the user may want to go back.

```
logos/falak/
  brief.md          # brief, word map, key tension, banned clichés, themes, paper concepts + distinctness matrix
  round-1/
    build.py        # one script that generates every concept SVG (re-run after each fix)
    drafts/         # black-only drafts (step 4a)
    concepts/       # A1.svg, A1-inverse.svg, A1-icon.svg, A1-app.svg ...
    concepts.json   proof.png  gallery.html  gallery.png
  final/            # pack.py output
```

Put every concept in **one `build.py`** that imports `shapes` and `text2path`. Fixes are then one edit plus a re-run, and the next round starts from code, not from hand-edited SVGs.

## 1. Brief (keep it short)
First, gather what you can without asking: the conversation, the repo (README, package.json, existing colours and fonts, any old logo), and memory. Then ask **one batched round** covering only the real gaps:
- Name exactly as written, including case. Optional tagline. Script(s): Latin, Arabic or Urdu.
- What it does, for whom, and where. The market matters: Pakistan, KSA and global audiences read colour and symbols differently.
- 3 adjectives for the personality, and 1 thing it must **not** feel like.
- Competitors or logos they like or hate.
- Any constraints: existing colours, required elements, app-icon use.

If the user says "just go", or can't be asked, proceed on sensible assumptions and state them in one line.

Then write `brief.md` containing:
- a **word map**: nouns, verbs, metaphors and opposites around the name and the offering;
- the **key tension**, for example "ancient sky-reading × modern app";
- a **banned clichés** list: the first five things every designer would draw for this category. They are off-limits unless they get a real twist.

## 2. Themes
Read `references/themes.md`. Pick themes that differ on at least 3 of the 6 axes. Bend each one to the brief, or invent a new one. Check `data/history.jsonl` and avoid the themes used in the user's last few projects, unless the brief calls for one.

How many themes and concepts:
- **Default: 3 themes × 2 concepts = 6.**
- "Lots of options / a bunch / explore": 4 × 3 = 12.
- "Just a couple": 2 × 2.
- Follow any number the user gives.

Present the themes in a few lines: name, mood words, form language, type and palette. Then **carry straight on to concepts** unless the user asked to choose themes first; the gallery is where they react best.

## 3. Concepts on paper (before any SVG)
Read `references/methods.md`. For each theme, write 4–6 one-sentence candidates, each with a mark type, an idea method and a form generator. Cut down to the requested count using the **distinctness matrix**, written into `brief.md`:
- no two finalists share both a mark type and a generator;
- at least half the set uses different mark types;
- each finalist passes the swap test (it could not belong to a competitor) and avoids the banned list.

Prefer the most *different* strong ideas over near-duplicates of the single best one.

**Ambition check.** For each finalist, write its **signature move**: the one thing someone would describe when telling a friend about the logo. For example, "the a in chai is a full cup" or "two Ls lock into a balanced square". If you can't name one, or it's "nice font, plus a coloured dot", replace the concept.

- A wordmark needs a custom move that is visible at 64 px.
- A letterform needs a transformation stronger than adding an underline.

Write each finalist as:
**id · name · mark type · signature move · construction sketch in words.**

## 4. Draw
Read `references/craft.md`.

**4a. Black first.** Build every concept in `build.py` as pure #000 shapes into `drafts/`:
- use the `shapes.py` primitives and booleans, with snapped coordinates and computed curves;
- outline type with `text2path.py`, and use `info["glyphs"]` to modify individual letters.

Run:
```bash
python3 scripts/render.py proof drafts/*.svg --black --out drafts/proof.png
```
Look at the proof. Any idea that doesn't survive in black gets redrawn now, before you spend time on colour.

**4b. Colour and partners.** Apply the theme palette and write the files to `concepts/`:
- `<id>.svg`: the primary lockup, or the full mark for a pure wordmark or emblem.
- `<id>-icon.svg`: the symbol alone. **Required** whenever the concept has a symbol, and whenever the brief mentions an app or favicon. For a pure wordmark, draw a monogram or initial cut.
- `<id>-inverse.svg`: the version for dark backgrounds. Use `recolour.py --auto-inverse`, or `--map` when the brand needs specific light colours.
- `<id>-app.svg`: optional, a hand-tuned app tile. Otherwise the proof and gallery generate one: the inverse icon on the darkest brand colour.

**More than 4 concepts:** if you can spawn subagents, give each theme its own subagent, running in parallel. Each one gets:
- the brief and its theme;
- its rows from the matrix;
- the paths to `craft.md` and the scripts;
- its own id prefix, so their files can't clash.

Isolation stops the concepts converging.

Launch them in the foreground (`run_in_background: false`), all in one message so they run in parallel, and **wait for every one to return** before going to step 5. Never end your turn while they are still running: background results don't come back to a subagent, so if you are a subagent yourself, that work would be lost. Check their files exist, then review everything yourself.

If you can't spawn subagents, draw one theme at a time. Before each theme, re-read its matrix rows and the signature moves, so later concepts don't drift towards earlier ones.

## 5. Check, don't trust
```bash
python3 scripts/svg_lint.py round-1/concepts/*.svg --bg "<light background>"
python3 scripts/render.py proof round-1/concepts/*.svg --out round-1/proof.png
```
- Fix every lint ERROR.
- Treat contrast warnings as real; the accent usually needs darkening.
- Then **open `proof.png` and look at it**. Run the critique pass from craft.md:
  - small size, silhouette, squint, letters, accidents, clichés, swap, distinctness, geometry;
  - the app tile, which must be one clear shape;
  - the ambition check again: is the signature move actually visible?

Redraw anything that fails and re-proof. Expect two loops; the first draft of a hand-coded mark is rarely the good one. The linter can't judge drawing errors, but the proof shows them.

## 6. Present
Write `concepts.json`; the schema is in `gallery.py`'s docstring. Its `archetype` field is the mark type. Then build the gallery:
```bash
python3 scripts/gallery.py round-1/concepts.json --png round-1/gallery.png
```
Look at `gallery.png` once more. Then show it to the user: open `gallery.html` in the browser pane, or send `gallery.png` with SendUserFile.

Present a compact list, one line per concept: **name, theme, mark type, signature move, why it fits, one honest risk**. End with your own top 2–3 picks and one sentence each on why.

Then stop and ask which concept or concepts to take forward, and what to change. Typical responses:
- "B2 but bolder";
- "mix A1's symbol with C1's type";
- "none, more like X".

## 7. Refine
Run each new round in `round-N/`, copying `build.py` forward. When combining or adjusting concepts, edit only what was asked; don't quietly redesign the rest. Give the gallery a `title`, for example "Falak — round 2: refining B2".

Push quality in this round:
- optical corrections;
- a small-size cut of the icon, if 16 px needs one;
- type spacing by eye on the proof;
- final colour, with contrast checked by the lint.

Show the result with a proof and a gallery again. When the user is happy, **lock** the concept. From then on, every derivative is built from these exact paths.

## 8. Final kit
```bash
python3 scripts/pack.py --icon final/icon.svg --wordmark final/wordmark.svg --brand "Falak" \
  --primary "#0B1026" --accent "#F4C95D" --background "#F7F3EA" \
  --app-bg "#0B1026" --app-scale 0.62 --font "Space Grotesk" \
  --tagline "Read the sky" --domain falak.app --out logos/falak/final
```
This produces the following from the same source paths:
- horizontal and stacked lockups;
- colour, inverse, black and white versions;
- PNGs at 16–1024 px;
- favicon.ico, an Apple touch icon, an Android maskable icon, a social avatar and an OG image;
- five mockups (business card, phone home screen, website header, social profile, signage);
- a brand sheet, `index.html`.

Useful options:
- **Dark app tile:** `--app-bg` with a dark brand colour; the inverse mark is used automatically. Night, finance and premium brands often want one.
- **Hand-made tile:** `--app-icon`.
- **Hand-made dark versions:** `--inverse-icon` and `--inverse-wordmark`, when the automatic swap isn't right.
- **Wordmark-only logos:** pass the monogram cut as `--icon`.

Look at the mockup PNGs before handing over. Offer to publish the brand sheet as an Artifact so it can be shared.

## 9. Remember
Append one line to `data/history.jsonl` in this skill's folder, so future runs rotate themes:
`{"date": "YYYY-MM-DD", "brand": "...", "themes": ["Swiss precision", ...], "chosen": "B2 · Orbit F · letterform", "path": "..."}`

Skip this for test or eval runs.

## Principles to keep in mind
- **Idea over decoration.** Every concept needs a signature move you can say in one sentence and see at 64 px.
- **Range is the product.** If two concepts look like siblings, one of them is wasted.
- **Render and look.** Never present a mark you haven't seen as a PNG.
- **Black first.** If the idea needs colour to work, it isn't working yet.
- **Real craft.** Use exact geometry from `shapes.py`, outlined type, optical corrections, and 1–5 shapes.
- **Honest critique.** Name each concept's weakness before the user finds it.
