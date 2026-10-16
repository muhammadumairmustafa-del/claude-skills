# Arabic, Urdu and bilingual (RTL) typography

Read this whenever a project shows Arabic, Urdu or Persian text, or must work in both English and Arabic (KSA/UAE/Pakistan work: stc, Jazz, TonePerks, CallPerks). Most RTL font bugs come from treating Arabic like Latin with the direction flipped. These rules cover the differences.

## Choosing the face

| Need | Pick | Why |
|---|---|---|
| Bilingual enterprise UI (Latin + Arabic look like one family) | **IBM Plex Sans Arabic** + IBM Plex Sans | Arabic was drawn to match the Latin's weight, height and rhythm. |
| Modern Arabic-script app UI, variable weights | **Vazirmatn** | Clean, wide weight range, includes Latin, renders well small. |
| Gulf consumer look (KSA/UAE apps) | **Tajawal**, **Almarai**, **Cairo**, **Alexandria** | Match regional conventions. Tajawal and Almarai have no Latin, so pair them with DM Sans / Inter. Tajawal also lacks Urdu letters. |
| Readability-first / accessibility | **Readex Pro** | Arabic extension of Lexend. Arabic only: missing Urdu letters. |
| Long-form Arabic reading, formal or religious text | **Noto Naskh Arabic**, **Amiri**, **Markazi Text** | Naskh is the reading style. Amiri is classical. |
| Headlines with heritage feel | **Aref Ruqaa**, **Reem Kufi**, **El Messiri** | Calligraphic and Kufi display. Not for body text. |
| Urdu reading text, poetry, news | **Noto Nastaliq Urdu** (body), **Gulzar** (display) | Urdu readers expect Nastaliq. Naskh reads as "Arabic", not Urdu. |
| Urdu inside dense UI (buttons, tabs, lists, tables) | **Vazirmatn** or **Noto Sans Arabic** | Nastaliq is very tall and slanted, so it breaks compact controls. Use Naskh-style for UI and keep Nastaliq for headlines and paragraphs. |

Check Urdu-specific letters render: ٹ ڈ ڑ ں ھ ہ ے ۓ ک گ. Measured (Oct 2026): **Tajawal, Readex Pro and Rubik are missing several**, so don't use them for Urdu. Full coverage: Vazirmatn, Noto Sans/Naskh/Kufi Arabic, IBM Plex Sans Arabic, Almarai, Cairo, Alexandria, Amiri, Markazi Text, El Messiri, Changa, Reem Kufi, Aref Ruqaa, Baloo Bhaijaan 2, plus the Nastaliq faces. `fonts.py find --script urdu-letters` lists every font that passes (refresh re-checks this), and `--script urdu` lists the Nastaliq faces.

## Two Urdu faces is normal
Use Nastaliq (Noto Nastaliq Urdu, Gulzar for display) for headings and paragraphs, and a Naskh-style UI face (Vazirmatn, Noto Sans Arabic) for buttons, tabs, inputs, prices and nav. `fonts.py tokens --arabic noto-nastaliq-urdu --arabic-display gulzar --arabic-ui vazirmatn` (or `--pairing urdu-editorial`) generates exactly this. Self-host both: Nastaliq pinned to one weight and subset (`subset --preset urdu --wght 400`, ≈120 KB), plus Vazirmatn's Arabic subset (≈45 KB).

## HTML/CSS rules
- **Use `lang`, not just `dir`.** Font switching keys off `:lang(ar|ur)`, which inherits to every descendant, so nested sections and paragraphs all switch. Don't switch fonts by redefining a CSS variable on the RTL container alone: children inherit the parent's *computed* `font-family`, not the variable, so a `<p>` inside would stay Latin.
- Put the Latin body face second in Arabic/Urdu stacks (`'Noto Nastaliq Urdu', 'Source Serif 4', …`) so digits, "Rs" and English words inside Urdu use the Latin design, not the Arabic font's Latin glyphs. `tokens` does this.
- Scale Urdu with a variable (`--script-scale: 1.15`) multiplied into each size, never `font-size: 1.15em` on `:lang(ur)`: the `em` version compounds at every nesting level and overrides heading sizes.
- Set direction in markup: `<html lang="ar" dir="rtl">` (or `lang="ur"`). Don't do it with CSS `direction`, because screen readers and the bidi algorithm rely on the attribute.
- For mixed content, put `dir="auto"` on user-generated text and `<bdi>` around names and numbers inside sentences.
- **Never letter-space Arabic script.** `letter-spacing` inserts gaps between joined letters and breaks words apart visually. Reset it inside `:lang(ar), :lang(ur), [dir=rtl]` (the generated tokens do). Uppercase-style tracking has no Arabic equivalent.
- **No `text-transform`, no faux bold or italic.** Arabic has no case. Synthetic italic slants the joins badly. Use real weights and avoid italics; for emphasis use weight or colour.
- **Line height**: Naskh/Sans ≈ 1.7–1.9. Nastaliq ≈ 2.1–2.4, because diacritics and the diagonal baseline need the room. Too tight, and marks collide with the line above or get clipped in buttons.
- **Size balance**: Arabic glyphs look smaller than Latin at the same font-size. Bump Arabic text ~10–15% (Nastaliq ~15–20%), or use `size-adjust` on the Arabic `@font-face` so mixed lines match.
- Use logical properties everywhere (`margin-inline-start`, `padding-inline`, `text-align: start`, `inset-inline-end`) so layouts mirror without separate CSS.
- Icons with direction (arrows, back chevrons, progress) must mirror. Logos, media controls and checkmarks don't.
- Justification: avoid `text-align: justify` for Arabic on the web. Browsers stretch spaces rather than using kashida (tatweel), which looks wrong. Use `start`.

## Numbers
- Gulf and KSA consumer UIs mostly use **Western digits (0–9)** for prices, phone numbers and dates. Government and formal content may use **Arabic-Indic (٠١٢٣٤٥٦٧٨٩)**. Urdu uses **Extended Arabic-Indic (۰۱۲۳۴۵۶۷۸۹)** in formal text but Western digits in apps. Ask, or follow the brand.
- Format with `Intl.NumberFormat('ar-SA')` (Arabic-Indic) vs `'ar-SA-u-nu-latn'` (Western digits in Arabic locale). Urdu: `'ur-PK'` (Western by default) / `'ur-PK-u-nu-arabext'`.
- Phone numbers and IBANs stay LTR inside RTL text: wrap them in `<bdi dir="ltr">` or `<span dir="ltr">`.
- Saudi Riyal: the official symbol is U+20C1 (2025). Fonts and OSes are still catching up. Use the text "ر.س" / "SAR", or the Saudi-Riyal-Font repo, until the symbol renders everywhere.
- `font-variant-numeric: tabular-nums` works for Western digits in most Arabic fonts with Latin. Check the Arabic-Indic digits separately.

## Bilingual font stacks
Order matters. Put the Latin face first when Latin dominates; the browser then picks the Arabic face per glyph for Arabic characters:
```css
--font-body: 'Inter', 'IBM Plex Sans Arabic', 'Inter Fallback', system-ui, sans-serif;
```
Or switch the whole stack per language (what the generated tokens do), which gives tighter control over line height and size:
```css
:lang(ar), [dir=rtl] { --font-body: var(--font-arabic); letter-spacing: 0; line-height: 1.8; }
```
Platform Arabic fallbacks (`fonts.py stacks arabic`): Geeza Pro / SF Arabic (Apple), Segoe UI / Tahoma (Windows), Noto Sans Arabic (Android/Linux).

## Subsetting Arabic
- Keep every OpenType layout feature (`init`, `medi`, `fina`, `isol`, `rlig`, `calt`, `mark`, `mkmk`, `curs`). `fonts.py subset` keeps them all by default.
- Include ZWJ/ZWNJ (U+200C/D) and direction marks (U+200E/F). The `arabic`/`urdu` presets do.
- Subsetting by scanned text is risky for Arabic. Contextual forms come from the same code points, which is fine, but any new word with an unseen letter falls back mid-word, which looks broken. Prefer the `arabic` or `urdu` presets over `--text-from` unless the text is truly fixed (a logo, a hero line).

## Native apps
- iOS: SF Arabic is excellent by default. Bundle a custom Arabic font only for brand reasons. `.environment(\.layoutDirection, .rightToLeft)` for previews.
- Android: set `android:supportsRtl="true"`. Keep `includeFontPadding` on for Arabic. Nastaliq needs generous `lineHeight`.
- React Native: `I18nManager.forceRTL`, then restart. Set `lineHeight` explicitly for Arabic styles. Android clips marks otherwise.
- Flutter: `Directionality`/locale-driven, `fontFamilyFallback` for mixed strings, `height: 1.7` (Nastaliq 2.2).

## QA checklist
- [ ] Letters join (no isolated forms mid-word). If they don't, layout features were stripped or the wrong font is used.
- [ ] No clipped diacritics at the top or bottom of buttons, inputs and tab bars.
- [ ] Punctuation and brackets mirror correctly (؟ ، ؛ and parentheses).
- [ ] Mixed English words and numbers inside Arabic sentences sit in the right order.
- [ ] The Latin and Arabic sizes look balanced on the same line.
- [ ] Urdu-specific letters render in the chosen font (ٹ ڈ ڑ ں ے).
- [ ] Nothing has letter-spacing applied in RTL.
