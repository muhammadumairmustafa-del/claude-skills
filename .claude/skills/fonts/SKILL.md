---
name: fonts
description: Choose, pair, install and optimise open-source fonts for websites, web apps, mobile apps (iOS, Android, React Native/Expo, Flutter), dashboards, decks and OG images, using a curated, verified catalogue of 118 fonts and 30 tested pairings (including Arabic and Urdu Nastaliq), live Fontsource/Google Fonts data, self-hosting downloads, metric-matched fallbacks that stop layout shift, subsetting, and fluid type-scale tokens (CSS, Tailwind v3/v4, JSON). Use this whenever the user asks for a font, typeface, typography, font pairing, heading/body fonts, "make the text look better", a type scale, web font loading or performance (CLS, FOUT, slow fonts), self-hosting Google Fonts, next/font, Fontsource, custom fonts in an app, Arabic/Urdu/RTL fonts, or types /fonts, even if they only say "pick a nicer font" or are restyling a site. Prefer it over guessing font names or hand-writing @font-face rules.
---

# Fonts: pick, pair, install, optimise

This skill turns "which font, and how do I wire it in properly" into a repeatable workflow. It has a hand-curated catalogue (every entry checked against Fontsource for real weights, axes, subsets and licence), tested pairings with Arabic/Urdu partners, and one script that does the fiddly parts correctly: platform-specific install code, self-hosting files, fallback metrics, subsetting and type-scale tokens.

Everything lives next to this file:

| Path | What it is |
|---|---|
| `scripts/fonts.py` | The tool. Run `python3 ~/.claude/skills/fonts/scripts/fonts.py <command>`. Use it instead of reading the JSON by hand: it keeps context small and the numbers right. |
| `data/curated.json` | Hand-picked fonts: roles, moods, notes, source repo. Edit this to add fonts, then run `refresh`. |
| `data/pairings.json` | 30 pairings: heading / body / mono / Arabic (+ Arabic display, Latin partner for Arabic-first sets). |
| `data/catalog.json` | Generated: curated data + live Fontsource metadata + measured metrics + Urdu-coverage check. |
| `assets/gallery.html` | Self-contained browsable library (filters, live previews, copy-ready commands). Open it or copy it into a project when the user wants to choose visually. |
| `references/typography.md` | How to choose and pair, type scale, measure, line height, variable axes, licensing. Read when choosing for a new brand or when something "looks generic". |
| `references/platforms.md` | Gotchas per platform: Next.js, Vite/Fontsource, Tailwind, Expo, Flutter, SwiftUI, Android, OG images, email, slides. Read before wiring fonts into a non-trivial stack. |
| `references/performance.md` | Loading checklist: woff2, unicode-range, subsetting, preload, font-display, CLS fallbacks, budgets. Read for "fonts are slow", CLS or Lighthouse work. |
| `references/arabic-urdu.md` | RTL rules: face choice, line height, no letter-spacing, numerals, bilingual stacks, Urdu letter coverage, QA. **Read whenever Arabic, Urdu or Persian text is involved.** |
| `references/repos.md` | The wider GitHub landscape (libraries, fonts, tooling, curated lists) with star counts, for needs the catalogue doesn't cover. |

## Workflow

### 1. Read the brief and the project
Work out, without interrogating the user:
- **Voice**: three adjectives (calm/precise/premium, playful/bold/young…), and the industry.
- **Where the text lives**: dense UI, long reading, marketing headlines, code, data tables.
- **Scripts**: English only? Arabic? Urdu (Nastaliq for reading, Naskh-style for UI)? CJK?
- **Stack**: look at the repo (`package.json` → next / vite / astro / expo; `pubspec.yaml` → Flutter; `.xcodeproj` → iOS; `build.gradle` → Android; plain HTML; a deck or design tool). Note what's already loaded (`next/font`, `@fontsource`, a Google Fonts `<link>`) and any brand font that must stay.

State your assumptions in a line and carry on.

### 2. Shortlist
```bash
fonts.py pair -q telecom                         # pairings by use case text
fonts.py pair --mood luxury --mood elegant       # pairings by mood
fonts.py pair --arabic-first                     # Gulf / Urdu-first sets
fonts.py find --role display --mood expressive   # single fonts by role + mood
fonts.py find --script arabic --role ui          # Arabic UI faces
fonts.py find --script urdu-letters              # fonts that really contain ٹ ڈ ڑ ں ے …
fonts.py find --role mono --google               # only fonts usable with next/font/google / Expo
fonts.py show inter fraunces                     # full details: axes, weights, repo, CSS stack
fonts.py lookup <any-fontsource-id>              # any of ~2,100 Fontsource fonts, live
```
Moods: `neutral corporate techy friendly playful elegant luxury editorial bold geometric humanist grotesque retro warm accessible minimal expressive condensed handwritten classic modern rounded`. Roles: `ui text display editorial mono arabic urdu cjk`.

Pick with taste, not by score. A law firm, a kids' app and a telecom promo want different things. Avoid defaulting to the overused set (Poppins/Montserrat/Roboto/Open Sans alone, or Inter everywhere with no heading contrast) when the brief asks for anything distinctive. If the `studio` skill is driving a design, follow its direction and use this skill to execute the type part.

Offer 2–3 options with a one-line reason each, unless the user asked you to just decide. Then pick and say why.

### 3. Show it (when choosing visually helps)
```bash
fonts.py specimen --pairing editorial-modern --pairing magazine --text "Real headline from the product" --out font-specimen.html
fonts.py specimen --fonts vazirmatn cairo alexandria --out arabic-options.html
```
The specimen renders each option with the real headline, body copy, buttons, a price, code and an Arabic/Urdu block, in light and dark. Open it in the browser pane and screenshot it, or send it to the user. For open-ended browsing, give them `assets/gallery.html` (rebuild it with `fonts.py gallery` after editing the data).

### 4. Install for the stack
```bash
fonts.py install <heading> <body> <mono> <arabic> --stack next          # next/font (google + local)
fonts.py install inter jetbrains-mono --roles body,mono --stack fontsource   # Vite/React/Vue/Svelte/Astro
fonts.py install inter --stack google-css                                # quick prototype / static HTML
fonts.py install inter --stack self                                      # self-host download commands
fonts.py install inter ibm-plex-sans-arabic --roles body,arabic --stack expo|flutter|swiftui|android
fonts.py download <id> --out public/fonts [--weights 400,700] [--subsets latin,arabic] [--italic]
fonts.py download <id> --format ttf --out assets/fonts                   # native apps / OG images: full TTFs + PostScript names
```
Ids are given in role order: `heading body mono arabic` by default. Override with `--roles`. Fonts that aren't on Google Fonts (shown as "Fontsource only") get `next/font/local` + download instructions automatically.

Wire fonts into the project's existing system (CSS variables, Tailwind theme, theme object) rather than scattering `font-family` across components. The traps that cause most bugs are in `references/platforms.md`: the Fontsource `"X Variable"` family name, static fonts needing `weight` in next/font, React Native per-weight family names, iOS PostScript names, Satori needing TTF not woff2.

### 5. Generate type tokens
```bash
fonts.py tokens --pairing saas-clean                           # CSS: families, fluid scale, base styles, RTL block, fallbacks
fonts.py tokens --pairing saas-clean --format tailwind4 --source fontsource
fonts.py tokens --heading fraunces --body source-serif-4 --arabic amiri --ratio-max 1.333
fonts.py tokens --pairing urdu-ui --source next                 # next/font provides the families
```
Options: `--format css|tailwind4|tailwind3|json`, `--source self|google|fontsource|next` (affects family names and fallbacks), `--base-min/--base-max` (px), `--ratio-min/--ratio-max` (1.125 dense UI → 1.333 editorial), `--vw-min/--vw-max`.

Arabic and Urdu: `--arabic` (body), `--arabic-display` (headings) and `--arabic-ui` (buttons, inputs, nav; e.g. Vazirmatn when the body is Nastaliq). The CSS output adds a `:lang(ar|ur|fa)` block that sets the font directly on every matching element (so nested sections work), resets letter-spacing, raises line-height (2.2 for Nastaliq) and scales Urdu by 1.15 through a variable that never compounds. Latin characters inside Urdu text (digits, "Rs 99") fall through to the Latin body font. The page must carry `lang="ur"`/`"ar"`; `dir="rtl"` alone isn't enough.

### 6. Optimise
```bash
fonts.py fallback inter fraunces                    # metric-matched fallback @font-face (no CLS on swap)
fonts.py fallback "Brand Sans" --file brand.otf     # same for a custom font file
fonts.py subset nastaliq.woff2 --preset urdu --wght 400   # pin variable → one weight, then subset: 233 KB → 119 KB
fonts.py subset logo-font.ttf --text "UVERSE"       # wordmark-only font
fonts.py subset font.ttf --text-from ./src          # keep exactly the characters a project uses
fonts.py stacks [didone|humanist|arabic|…]          # zero-download system stacks
```
`download` and `tokens` already include fallbacks (separate regular and bold faces, so bold text isn't faked during the swap). next/font makes its own, so skip `fallback` there. `subset` keeps all OpenType features (kerning, ligatures, Arabic joining) and prints a ready `@font-face` with the exact `unicode-range`. `--wght` pins a variable font to one weight, which is often the biggest single saving.

woff2 needs fontTools + brotli. They live in the skill's own venv (`~/.claude/skills/fonts/.venv`), and `fonts.py` switches into it automatically when the system Python lacks them. If the venv is missing: `python3 -m venv ~/.claude/skills/fonts/.venv && ~/.claude/skills/fonts/.venv/bin/pip install fonttools brotli`.

`download --out` is the *parent* folder: files land in `<out>/<id>/` and are referenced as `<url-prefix>/<id>/<file>`. Follow `references/performance.md` for preload and `font-display` choices.

### 7. Verify, then report
- Render it (dev server or specimen) and look. `document.fonts.check('16px "Inter Variable"')` in the browser console confirms the family name actually matches a loaded face. A silent mismatch quietly falls back to system-ui.
- For Arabic/Urdu, run the QA checklist at the end of `references/arabic-urdu.md` (joined letters, unclipped marks, no letter-spacing, Urdu letters present).
- Report: the fonts chosen and why (one line), the pairing id if one was used, files changed, total font weight if self-hosted, and anything the user must do (install a package, add files to Xcode, licence notes for non-OFL fonts).

## Keeping the catalogue current
- `fonts.py refresh` re-pulls Fontsource metadata (weights, axes, subsets) and re-checks Urdu coverage. It caches measured metrics; `--remeasure` re-downloads them. Run it after editing `curated.json` or every few months.
- To add a font: append `[id, roles, moods, note, repo]` to `curated.json` (the id must exist on fontsource.org), run `refresh`, then `gallery`. The refresh also warns if a pairing references a missing id.
- Fonts not on Fontsource (some GitHub-only fonts in `references/repos.md`): download the release from the repo, then use `fallback --file` and `subset` directly on the files.

## Ground rules
- Only use fonts whose licence allows the use: everything in the catalogue is OFL/Apache. Never pull system or commercial fonts (SF Pro, Segoe UI, Helvetica Neue, Proxima Nova, Gotham…) into a web build or app bundle. They can appear only as names in a fallback stack.
- Two families plus a mono is the ceiling. Use weight, size and case for further hierarchy.
- Self-host in production (next/font, Fontsource or `download`). The Google Fonts CDN is for prototypes.
- Never letter-space, italicise or `text-transform` Arabic-script text. Give it more line height than Latin.
