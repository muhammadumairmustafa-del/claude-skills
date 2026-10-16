# Font performance checklist

Fonts are often the second-largest render-blocking asset after CSS. The goals are no invisible text, no layout shift when the font swaps in, and as few bytes as possible. Work through this list in order. The first items matter most.

## 1. Fewer files
- **Two families is plenty**: one for headings, one for body, plus a mono if code shows. Every extra family costs a request plus a visible swap.
- **Variable vs static**: one variable woff2 (≈40–100 KB Latin) replaces 3+ static weights (≈20–25 KB each). Using 3 or more weights? Go variable. Using just 400 + 700? Two statics are smaller.
- Don't load italics unless the content uses them. Browsers fake italics from the upright, which looks poor in headlines but is acceptable for rare inline emphasis.
- Drop weights nobody uses: grep the CSS for `font-weight` values.

## 2. Self-host woff2
- woff2 only. Every browser in use supports it, so a woff/ttf fallback `src` is dead weight.
- Self-hosting (Fontsource, next/font, `fonts.py download`) removes a DNS + TLS hop to fonts.gstatic.com. Browsers partition caches per site, so the old shared-CDN cache argument is gone.
- Long cache: `Cache-Control: public, max-age=31536000, immutable`.

## 3. Load only the scripts you need (unicode-range)
`fonts.css` from `fonts.py download`, Fontsource and Google all split files by subset with `unicode-range`. The browser downloads the Arabic file only when Arabic characters appear on the page. Keep this split. Don't merge subsets into one file for the web.

## 4. Subset further when it pays
- Big wins: CJK (MB → KB), Nastaliq (≈480 KB), icon-like display fonts used for a few words, and logo/wordmark fonts.
- `fonts.py subset font.ttf --text-from ./src` keeps exactly the characters the project uses. Only do this for text you control: CMS content, translations and user input will fall back for missing glyphs.
- `fonts.py subset font.ttf --preset latin` matches Google's Latin subset.
- The script keeps all OpenType layout features by default (kerning, ligatures, Arabic joining). Never strip GSUB/GPOS from an Arabic font, or the letters stop connecting.
- `--drop-hinting` saves 10–30% more. Hinting only matters for Windows at small sizes.
- woff2 output needs the `brotli` module (`pip install brotli`, or in a venv / `pipx`). Without it, the script writes woff.

## 5. Preload just the critical file
- `<link rel="preload" as="font" type="font/woff2" crossorigin href="...">` for the **body** font's main subset only (and maybe the hero heading). Preloading everything delays the LCP image.
- next/font preloads automatically. Set `preload: false` on secondary fonts.

## 6. Choose font-display deliberately
| Value | Behaviour | Use for |
|---|---|---|
| `swap` | Fallback shows immediately, swaps when loaded | Default. Brand fonts that must appear. |
| `optional` | ~100 ms window, else fallback for this page view (cached for the next) | Body text on content and SEO sites. Zero layout shift. |
| `fallback` | ~100 ms block, then ~3 s swap window | Compromise. |
| `block` | Invisible text up to 3 s | Icon fonts only, never text. |

## 7. Kill layout shift with metric-matched fallbacks
When the web font swaps in, text reflows if the fallback has different widths and line heights. Fix this with a fallback `@font-face` that adjusts a local system font:
```css
@font-face {
  font-family: 'Inter Fallback';
  src: local('Arial'), local('ArialMT'), local('Liberation Sans'), local('Arimo');
  size-adjust: 107.48%; ascent-override: 90.14%; descent-override: 22.44%; line-gap-override: 0%;
}
body { font-family: 'Inter', 'Inter Fallback', system-ui, sans-serif; }
```
`fonts.py fallback <id>` generates this from measured metrics (same maths as fontaine, capsize and next/font). `download` and `tokens` include it automatically. next/font does it for you, so skip it there. For a brand font that isn't on Fontsource: `fonts.py fallback "Brand Sans" --file brand.ttf`.

## 8. Avoid FOUT jank in apps
- Native apps (iOS/Android/Flutter/RN): bundle fonts; don't fetch them at runtime.
- SPA route changes: fonts are cached after the first view, so nothing more to do.
- Canvas, PDF and OG rendering: `await document.fonts.ready` (or `document.fonts.load(...)`) before drawing.

## 9. Measure
- Chrome DevTools → Network → Font filter: count and size of files. Coverage of `unicode-range` downloads.
- Lighthouse: "Ensure text remains visible during webfont load" and the CLS score.
- `document.fonts.check('16px "Inter Variable"')` in the console tells you whether the family name you wrote actually matches a loaded face (it catches the "Inter" vs "Inter Variable" bug).

## Budget guide
| Situation | Target total font bytes (first view) |
|---|---|
| Marketing / landing page | ≤ 150 KB |
| App UI | ≤ 100 KB |
| Bilingual Latin + Arabic | ≤ 200 KB (Arabic file loads only on Arabic pages) |
| Urdu Nastaliq | Subset; full Noto Nastaliq is ≈ 480 KB |
