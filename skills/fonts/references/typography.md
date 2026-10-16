# Choosing, pairing and setting type

Read this when choosing fonts for a new brand or product, when a design "looks generic", or when setting up a type scale. It's the judgement layer on top of the catalogue.

## Choosing: start from the voice, not the font
Write down three words for how the product should feel (e.g. "calm, precise, premium"), plus where the text mostly lives (dense UI, long reading, big marketing headlines, code). Then:
- **UI-heavy product**: a neutral, large-x-height sans with tabular figures (Inter, Geist, IBM Plex Sans, Public Sans, Manrope). Personality comes from the heading font and colour, not the body.
- **Content/reading**: a text serif with optical sizes (Source Serif 4, Newsreader, Literata) or a humanist sans (Source Sans 3, Fira Sans).
- **Brand/marketing**: one characterful display face (Fraunces, Instrument Serif, Bricolage Grotesque, Syne, Space Grotesk, Unbounded) over a quiet body.
- **Trust (banking, telecom, government, health)**: low-contrast, open, familiar shapes. Avoid quirky display faces for core flows.

**Overused defaults** that make work look templated: Poppins, Montserrat, Roboto, Open Sans and Lato as the *only* face, and Inter on everything with no heading contrast. They're not wrong, but if the brief says "distinctive", pick something else or pair them with a characterful heading. Check the user's other projects (the `studio` skill tracks past directions) so apps don't all share one font.

## Pairing principles
1. **Contrast or kinship, never near-miss.** Pair clearly different faces (serif display + sans body), or members of one superfamily (Plex Sans + Plex Serif). Two similar geometric sans fonts look like a mistake.
2. **Match x-height and proportion.** Body and heading fonts with similar x-heights sit well together in mixed lines. Very small x-height display serifs over a tall x-height sans need larger heading sizes.
3. **One personality per page.** The display face gets the personality; the body stays neutral. Two expressive faces fight.
4. **Max two families + mono.** A third face is almost always better handled with weight, size, case or colour.
5. **Bilingual: match the Arabic to the Latin's tone**, not just "an Arabic font". Geometric Latin → Kufi/geometric Arabic (Alexandria, Noto Kufi). Humanist Latin → Naskh-based (Vazirmatn, Plex Arabic). Serif editorial → Naskh text (Amiri, Markazi). See `pairings.json` for tested combinations.

## Type scale
- Use a modular scale: ratio 1.125–1.2 for dense apps and dashboards, 1.2–1.25 for general sites, 1.25–1.333+ for marketing and editorial heroes.
- Go fluid: `clamp(min, intercept + slope·vw, max)` lets headings grow with the viewport without breakpoints. `fonts.py tokens` generates a fluid scale (default 16→18 px base, 1.2→1.25 ratio, 360→1280 px viewport).
- Body text: 16–18 px on web (never below 16 px for paragraphs on mobile, or iOS zooms inputs below 16 px). Native: follow platform defaults (iOS body 17 pt, Android 16 sp) and support Dynamic Type / font scaling.
- 4–6 sizes are enough for most products. Too many sizes look accidental.

## Rhythm and readability
- **Line length (measure)**: 45–75 characters, ideally ~66 (`max-width: 66ch`). Long lines tire the eye; very short lines feel choppy.
- **Line height**: body 1.5–1.7 (wider measure → more). Headings 1.05–1.25 (bigger → tighter). Arabic 1.7–1.9; Nastaliq 2.1–2.4.
- **Letter-spacing**: tighten large headings slightly (−0.01 to −0.03 em for sans). Open up ALL CAPS and small labels (+0.04 to +0.1 em). Leave body text at 0. Never track Arabic.
- **Weights**: body 400 (or 450 with a variable font on dark backgrounds), emphasis 600, headings 600–800. On dark backgrounds text looks heavier, so drop one step or use the font's `GRAD` axis if it has one (Roboto Flex).
- **Numbers**: `font-variant-numeric: tabular-nums` in tables, prices, timers and anything that updates. `lining-nums` with serifs that default to old-style figures.
- **Optical sizing**: fonts with an `opsz` axis (Inter, Fraunces, Source Serif 4, Newsreader, Literata, DM Sans) adjust their design per size automatically with `font-optical-sizing: auto`. It's free quality, so keep it on.
- `text-wrap: balance` on headings (even line lengths), `text-wrap: pretty` on paragraphs (avoids single-word last lines).
- **Hierarchy check**: blur your eyes (or screenshot and scale to 25%). If the heading, subhead and body don't separate, increase the size ratio or weight contrast rather than adding colours.

## Variable font axes worth using
| Axis | Effect | Fonts |
|---|---|---|
| `wght` | weight | almost all variable fonts |
| `opsz` | optical size (auto via `font-optical-sizing`) | Inter, Fraunces, Source Serif 4, Newsreader, Literata, DM Sans, Bodoni Moda, Bricolage Grotesque |
| `wdth` | width | Mona Sans, Hubot Sans, Archivo, Roboto Flex, Bricolage Grotesque |
| `SOFT`, `WONK` | rounded / quirky letterforms | Fraunces |
| `CASL`, `MONO` | casual and monospace mix | Recursive |
| `GRAD` | weight change without reflow (dark mode, hover) | Roboto Flex |
| `ital`/`slnt` | italic or slant | Inter, Recursive |

Use `font-variation-settings: "SOFT" 100, "WONK" 1;` for custom axes. Standard axes have CSS properties (`font-weight`, `font-stretch`, `font-optical-sizing`). With Fontsource, import `@fontsource-variable/<id>/full.css` (or the axis-specific CSS) to get axes beyond `wght`.

## Licensing in one paragraph
Everything in the catalogue is OFL-1.1 or Apache-2.0: free for commercial use, embedding in apps, self-hosting and logos. OFL forbids selling the font file on its own and requires renaming modified versions ("Reserved Font Name"). Ship the licence file with self-hosted fonts (`fonts.py download` writes `LICENSE.txt`). Fonts from "free font" sites, system fonts (SF Pro, Segoe UI, Helvetica) and commercial foundries are *not* covered. SF Pro is licensed only for Apple-platform UI mockups and apps, never for websites or Android.
