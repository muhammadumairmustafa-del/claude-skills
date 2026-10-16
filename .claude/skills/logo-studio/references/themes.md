# Theme library

A **theme** is a creative territory: a mood plus a form language, type direction and colour logic. Every run presents several themes chosen to be **far apart**, then puts 1–3 concepts inside each theme.

These are starting points, not presets. Always bend a theme to the brief, and invent new themes when none fits. Fonts are Google Fonts names, ready for `text2path.py --font`. Palettes are starters; tune them to the brand.

Theme axes, used to check that the chosen themes really differ:
- **energy:** calm ↔ loud
- **temperature:** warm ↔ cool
- **era:** heritage ↔ future
- **edge:** soft/round ↔ sharp/angular
- **tone:** serious ↔ playful
- **density:** minimal ↔ rich

Pick themes that differ on at least 3 of the 6 axes.

## Modern / tech
1. **Swiss precision.** Calm, cool, sharp, serious. Grid-built, one geometric idea, generous space, no decoration.
   - Type: Inter Tight 600, Manrope 700, Space Grotesk 700.
   - Palette: ink #111318, one signal colour (#FF4F1F or #2D5BFF), paper #F5F4F0.
2. **Soft-tech / friendly.** Calm, warm, round, playful. Pill shapes, superellipses, round terminals, bouncy counters.
   - Type: Nunito 800, Plus Jakarta Sans 700, Quicksand 700.
   - Palette: blurple #5B5BF6, peach #FFB38A, cream #FFF8F0.
3. **Kinetic / motion.** Loud, cool, sharp, future. Shears, speed lines, offsets, italics, directional cuts.
   - Type: Archivo 800 italic, Syne 700, Unbounded 700.
   - Palette: electric #3BFF8F on near-black #0A0B0D.
4. **Data / systematic.** Calm, cool, future, minimal. Dot grids, bars, modules, bitmap letterforms.
   - Type: JetBrains Mono 700, IBM Plex Sans 600, Space Mono 700.
   - Palette: #0E1116, cyan #33D1FF, lime #C6FF3D.
5. **Deep space / cosmic.** Calm, cool, future, rich. Orbits, arcs, crescents, stars as precise points, no glows.
   - Type: Space Grotesk 600, Outfit 600, Michroma 400.
   - Palette: midnight #0B1026, gold #F4C95D, ice #DCE7FF.

## Heritage / craft
6. **Editorial serif.** Calm, warm, heritage, serious. High-contrast serif, a ligature or swash as the signature.
   - Type: DM Serif Display, Playfair Display 700, Fraunces 600, Instrument Serif.
   - Palette: oxblood #5E1A1D, bone #F2EBDD, ink #1B1B1B.
7. **Badge / seal / guild.** Warm, heritage, rich. Circular or shield containers, stars, rules and arched text, with a stripped icon for small use.
   - Type: Oswald 600, Bebas Neue, Cinzel 700, Alfa Slab One.
   - Palette: forest #1F3B2D, brass #C79A3B, paper #EFE6D2.
8. **Hand-made modern.** Warm, playful, soft. Imperfect geometry (but constructed), cut-paper shapes, stamp-like.
   - Type: Recoleta-like Fraunces 700 soft, Young Serif, Gloock.
   - Palette: terracotta #C8553D, mustard #E8B04B, olive #6B7B3A, cream #F6EFE3.
9. **Luxury / quiet.** Very calm, cool-neutral, refined, minimal. Thin-to-thick contrast, wide tracking, a monogram.
   - Type: Cormorant Garamond 600, Bodoni Moda 500, Italiana, Marcellus.
   - Palette: black #0C0C0C, champagne #D8C3A5, ivory #FAF7F2.

## Expressive / bold
10. **Neo-brutalist.** Loud, sharp, playful. Heavy blocks, hard offsets, raw grotesk type, one bright colour.
    - Type: Archivo Black, Anton, Rubik Mono One, Bricolage Grotesque 800.
    - Palette: #000, acid yellow #F5FF3B, white.
11. **Retro-future / 70s.** Warm, loud, round, playful. Stacked stripes, rainbow bands, rounded bold type, sunbursts.
    - Type: Righteous, Shrikhand, Bungee, Climate Crisis.
    - Palette: #E94F37, #F6AE2D, #2F4858, #F2E3BC.
12. **Y2K / chrome-flat.** Cool, loud, future. Stars, sparkles, bubble shapes, rendered flat (no real chrome).
    - Type: Syncopate 700, Orbitron 700, Audiowide.
    - Palette: #C9D6FF, #FF6AD5, #1A1A2E.
13. **Organic / nature.** Calm, warm, soft. Leaf, seed, water and growth curves, constructed from circle arcs.
    - Type: Fraunces 600, Lora 600, Outfit 500.
    - Palette: moss #3E5E3A, sand #E7D8B9, clay #B5643C.

## Cultural (strong for Pakistani, Gulf and South Asian brands)
14. **Islamic geometric.** Calm, rich, heritage. 8- or 12-fold star patterns, girih tiles, interlace. Use one tile or a fragment, not a whole pattern.
    - Type: Marcellus, Cinzel, or for Arabic script Reem Kufi 700, Noto Kufi Arabic 700.
    - Palette: lapis #1F3C88, turquoise #2BB3A3, saffron #E8A33D, white.
15. **Kufic / script-led.** Square Kufic or a modern Naskh/Nastaliq gesture builds the mark. Arabic and Urdu shape correctly through text2path.py, because it uses HarfBuzz.
    - Type: Reem Kufi, Lalezar, Aref Ruqaa, Noto Nastaliq Urdu, Gulzar, Amiri.
    - Palette: ink #121212, emerald #0F6B4F, gold #C9A227.
16. **Truck-art / bazaar pop.** Loud, warm, playful, rich. Pakistani truck-art and bazaar signage energy: chevrons, flowers, borders, hyper-saturated. Use it as a frame or accent around a clean core mark.
    - Type: Lalezar, Baloo 2 800, Rozha One.
    - Palette: #E63946, #FFB703, #2A9D8F, #3A0CA3, #FFFFFF.
17. **Desert modern (Gulf).** Calm, warm, future. Dune curves, palm geometry, sun discs, mashrabiya grids, minimal.
    - Type: Tajawal 700, IBM Plex Sans Arabic 600, Readex Pro 600.
    - Palette: sand #E9D8B4, date #6B3E26, sky #2E86AB, white.

## Choosing themes for a run
- Read the brief's **key tension** (for example "ancient knowledge × modern app"). Good theme sets often take one theme from each side of the tension, plus one that resolves it.
- Check the history file (`data/history.jsonl`). Avoid repeating the theme ids used in the user's last 3 projects unless the brief clearly demands one.
- Include at most one "safe" theme. The user wants range.
- Write each theme back to the user in one line: **name: mood words · form language · type · palette chips**.
