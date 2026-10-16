# Open-source font repositories on GitHub

Star counts checked 17 Oct 2026. Everything here is free for commercial use (mostly OFL-1.1, which allows bundling, self-hosting and modifying, but not selling the font file on its own; keep the licence file next to the fonts). Excluded on purpose: San-Francisco-Pro-Fonts (Apple's licence doesn't allow redistribution), PragmataPro (paid), and icon fonts (Font Awesome, Devicons), which are a different job.

Use this file when the curated catalogue doesn't cover a need, or to point the user at a source repo.

## Contents
1. Libraries and delivery
2. UI / brand sans-serifs
3. Serifs and display
4. Arabic / Urdu / Persian
5. Monospace / code
6. CJK
7. Tooling
8. Curated lists

## 1. Libraries and delivery
| Repo | Stars | Use |
|---|---|---|
| google/fonts | 20.6k | Every Google Fonts family (1,800+) with METADATA.pb, licences and sources. |
| fontsource/fontsource | 6.2k | Every open font as npm packages (`@fontsource/x`, `@fontsource-variable/x`). Self-hosting with zero config. API: api.fontsource.org/v1. CDN: cdn.jsdelivr.net/fontsource/fonts. |
| fontsource/font-files | 0.5k | The actual woff2/woff/ttf files behind Fontsource, split per subset/weight/style. |
| majodev/google-webfonts-helper | 13.1k | Web UI to download Google Fonts + CSS for self-hosting. |
| notofonts/notofonts.github.io | 0.3k | Index of all Noto script projects (Noto covers almost every writing system). |
| googlefonts/noto-emoji | 5.1k | Noto Color Emoji; self-host for identical emoji across platforms. |

## 2. UI / brand sans-serifs
| Repo | Stars | Character |
|---|---|---|
| rsms/inter | 20.0k | The modern UI default. Variable with opsz, tabular figures, huge charset. |
| IBM/plex | 11.7k | Sans, Serif, Mono, Condensed and Plex Sans Arabic/Devanagari/Thai/JP/KR. Corporate, bilingual. |
| github/mona-sans | 4.2k | Variable width + weight; expressive display. Sibling: github/hubot-sans. |
| uswds/public-sans | 4.7k | Neutral, trustworthy, government-grade. |
| adobe-fonts/source-sans | 3.8k | Humanist workhorse. |
| vercel/geist-font | 3.6k | Geist Sans + Mono; the developer-product look. |
| arrowtype/recursive | 3.9k | Sans/mono variable with a casual axis. |
| floriankarsten/space-grotesk | 1.8k | Quirky geometric grotesk. |
| weiweihuanghuang/Work-Sans | 1.7k | Screen grotesque. |
| indestructible-type/Jost | 0.8k | Futura-style geometric. |
| orioncactus/pretendard | 3.6k | Korean system-ui alternative (Inter + Source Han). |

## 3. Serifs and display
| Repo | Stars | Character |
|---|---|---|
| adobe-fonts/source-serif | 2.4k | Transitional text serif with optical sizes. |
| undercasetype/Fraunces | 0.8k | Soft old-style display with WONK/SOFT/opsz axes. |
| theleagueof/league-spartan | 0.6k | Bold geometric display. |
| productiontype/Newsreader, Spectral | – | Editorial serifs (on Google Fonts). |

## 4. Arabic / Urdu / Persian
| Repo | Stars | Notes |
|---|---|---|
| rastikerdar/vazirmatn | 3.3k | Best modern Arabic-script UI font, variable 100–900, Latin included. |
| IBM/plex (Plex Sans Arabic) | – | Arabic designed to match Plex Latin. |
| aliftype/amiri | 0.5k | Classical Naskh (Bulaq style). |
| aliftype/aref-ruqaa | 0.1k | Ruqaa calligraphic display. |
| aliftype/reem-kufi | – | Fatimid Kufi display. |
| aminabedi68/Estedad | 0.4k | Arabic-Latin sans. |
| Gue3bara/Cairo | 0.2k | Contemporary Arabic + Latin, common in the Gulf. |
| notofonts/arabic | – | Noto Sans/Naskh/Kufi Arabic sources. |
| notofonts/nastaliq | – | Noto Nastaliq Urdu: the standard Urdu Nastaliq. |
| nuqayah/kitab-font | 0.1k | Classical Naskh for books. |
| emran-alhaddad/Saudi-Riyal-Font | 0.1k | The new SAR currency symbol (U+20C1) as a font, for KSA price UIs until system fonts catch up. |

## 5. Monospace / code
| Repo | Stars |
|---|---|
| tonsky/FiraCode | 82.1k |
| ryanoasis/nerd-fonts | 64.9k (patcher that adds 3,600+ icon glyphs to coding fonts; terminals/editors, not websites) |
| subframe7536/maple-font | 29.3k |
| microsoft/cascadia-code | 27.9k |
| be5invis/Iosevka | 23.1k |
| adobe-fonts/source-code-pro | 20.5k |
| githubnext/monaspace | 19.7k |
| source-foundry/Hack | 17.4k |
| JetBrains/JetBrainsMono | 13.1k |
| intel/intel-one-mono | 10.2k |
| rubjo/victor-mono | 3.8k |
| rektdeckard/departure-mono | 3.6k (pixel) |
| evilmartians/mono | 2.7k (Martian Mono) |

## 6. CJK
adobe-fonts/source-han-sans (17.3k), adobe-fonts/source-han-serif (9.8k), lxgw/LxgwWenKai (26.3k), be5invis/Sarasa-Gothic (12.9k), atelier-anchor/smiley-sans (14.9k), orioncactus/pretendard (3.6k). CJK files are huge (several MB): always use Fontsource/Google's sliced subsets on the web, never one full file.

## 7. Tooling
| Repo | Stars | Use |
|---|---|---|
| fonttools/fonttools | 5.3k | Python: `pyftsubset`, ttx, instancing variable fonts (`fonttools varLib.instancer`), merging. Powers `fonts.py subset`. |
| google/woff2 | 1.8k | Reference woff2 compressor (`woff2_compress`). |
| zachleat/glyphhanger | 0.9k | Crawl a site, list the characters used, subset to them. |
| ecomfe/fontmin | 6.2k | Node font minifier for build pipelines. |
| unjs/fontaine | 2.0k | Auto metric-matched fallback fonts (Vite/Nuxt/webpack plugin). `fonts.py fallback` does the same calculation. |
| seek-oss/capsize | 1.7k | Trim the space above and below text so it aligns exactly; `@capsizecss/metrics` has metrics for every Google font. |
| pixel-point/fontpie | 0.4k | CLI: fallback @font-face from a font file. |
| opentypejs/opentype.js | 5.0k | Read/write fonts in JS (text to SVG paths, metrics in the browser). |
| harfbuzz/harfbuzz | 6.2k | The shaping engine browsers use; `hb-view`/`hb-shape` to debug Arabic shaping. |
| googlefonts/fontbakery | 0.7k | QA checks for font files. |
| bramstein/fontfaceobserver | 4.3k | Font load events (mostly superseded by the CSS Font Loading API: `document.fonts.load()`). |
| system-fonts/modern-font-stacks | 3.5k | Zero-download system stacks by style (bundled in `fonts.py stacks`). |

## 8. Curated lists
ubuwaits/beautiful-web-type (7.3k: best open fonts with pairings), brabadu/awesome-fonts (2.1k), Jolg42/awesome-typography (1.5k), braver/programmingfonts (1.8k: test-drive coding fonts), chrissimpkins/codeface (6.5k), jaywcjlove/free-font (4.1k: free commercial fonts incl. Chinese).
