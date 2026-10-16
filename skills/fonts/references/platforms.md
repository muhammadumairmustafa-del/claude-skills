# Platform recipes and gotchas

`fonts.py install <ids> --stack <stack>` prints working code for each of these. This file covers what the snippet can't: when to choose each route, and the traps.

## Contents
- Next.js (App Router)
- Vite / React / Vue / Svelte / Astro
- Plain HTML / static sites
- Tailwind v4 and v3
- React Native / Expo
- Flutter
- iOS / SwiftUI / UIKit
- Android (Compose and Views)
- Electron / Tauri
- Open Graph images, PDFs, canvas
- Email
- Slides, Figma, Canva and print

---

## Next.js (App Router)
Use `next/font`. It downloads fonts at build time, self-hosts them from your domain, adds `size-adjust` fallbacks automatically and preloads them, so you don't need `fonts.py fallback` here.
- `next/font/google` only works for fonts where `type == google` (shown in `fonts.py show`). Anything else (Monaspace, Iosevka, Commit Mono, Pretendard, Maple Mono, your brand font): `fonts.py download <id> --out public/fonts`, then `next/font/local`.
- Static (non-variable) fonts **require** `weight: [...]`. Variable fonts must not list weights unless you want static instances.
- Arabic: add `"arabic"` to `subsets`. Without it, Arabic glyphs are not preloaded, and some builds drop them entirely.
- The generated code uses `variable: "--nf-<role>"` (put the classes on `<html>`) and maps it in CSS to `--font-<role>: var(--nf-<role>), <system stack>`. The separate names matter: writing `--font-heading: var(--font-heading)` refers to itself, which makes the value invalid and silently drops to the browser default font. That trap is common with Tailwind v4 `@theme`.
- Turn off preloading for fonts that aren't above the fold (`preload: false`), typically mono and Arabic on an English-first page. Every preloaded font competes with the LCP image.
- `display: "swap"` is the default. Use `"optional"` for body text on content sites if the font is not critical: no swap flash, and the font is used on the next navigation.
- RTL pages: set `<html lang="ar" dir="rtl">` from the route locale, not with CSS.

## Vite / React / Vue / Svelte / Astro
Fontsource is the simplest self-hosting route: `npm i @fontsource-variable/inter`, then `import "@fontsource-variable/inter"` once in the entry file.
- Variable packages register the family as **"Inter Variable"**, not "Inter". This is the most common bug. `fonts.py tokens --source fontsource` handles it.
- Import only the weights you use for static fonts (`@fontsource/x/400.css`). The bare import pulls 400 only.
- Per-subset imports exist (`@fontsource/x/latin-400.css`). The default CSS already uses `unicode-range`, so unused subsets are never downloaded. Only cherry-pick subsets to shrink the CSS itself.
- For automatic fallbacks, add `fontaine` (Vite plugin) or paste `fonts.py fallback <id>` output.
- Astro 5 has a built-in Fonts API (`experimental.fonts`) that wraps Fontsource/Google and generates fallbacks. Use it when the project already does.

## Plain HTML / static sites
- Prototype: `fonts.py install ... --stack google-css` (Google Fonts CDN link).
- Production: `fonts.py download <id> --out fonts`, link `fonts/<id>/fonts.css`, and preload only the main body file:
  `<link rel="preload" href="/fonts/inter/inter-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>` (the `crossorigin` is required even on the same origin).
- Serve fonts with `Cache-Control: public, max-age=31536000, immutable`. Vercel/Netlify do this for hashed filenames. For static `/fonts/` paths, add a header rule.
- Google Fonts CDN: a German court (Munich, 2022) fined a site for leaking visitor IPs to Google. Self-host for EU-facing sites.

## Tailwind
- **v4** (CSS-first): `fonts.py tokens --format tailwind4`. In `@theme`, `--font-sans` sets the default `font-sans` utility, and any other `--font-x` creates a `font-x` utility. With next/font, use `fonts.py tokens --format tailwind4 --source next`, which emits `@theme inline { --font-sans: var(--nf-body), …; }` so the runtime variable resolves without self-reference.
- **v3**: `fonts.py tokens --format tailwind3` gives `theme.extend.fontFamily/fontSize`.
- Don't put quotes inside the Tailwind v3 array items (`"Inter Variable"` not `"'Inter Variable'"`). The generator handles this.

## React Native / Expo
- `@expo-google-fonts/<id>` packages + `useFonts`. There is no weight synthesis on Android: each weight is its own family name (`Inter_700Bold`), and `fontWeight: "700"` on `Inter_400Regular` does nothing on Android (and fakes bold on iOS). Put the per-weight family names in theme tokens (`text.heading = { fontFamily: "Inter_700Bold" }`).
- Variable fonts: Expo loads static instances only. Android does not reliably honour variable axes in RN.
- Keep the splash screen until fonts load (`SplashScreen.preventAutoHideAsync`) to avoid a flash of system font.
- Config plugin route for faster startup: `expo-font` plugin in app.json with `fonts: ["./assets/fonts/X.ttf"]` embeds fonts natively, so there's no runtime load.
- RTL: `I18nManager.forceRTL(true)` + reload. Arabic fonts need extra `lineHeight` (≈1.6–1.8× size; Nastaliq ≈2.2×) or diacritics clip on Android.

## Flutter
- Fast start: `google_fonts` package (`GoogleFonts.inter()`). It fetches over the network at runtime. For production, bundle the files (`fonts.py download <id> --format ttf`), declare them in `pubspec.yaml`, and set `GoogleFonts.config.allowRuntimeFetching = false`.
- `fonts.py download --format ttf` pulls **full** TTFs from Google (all scripts in one file, one file per weight). Fontsource TTFs are split per subset and would drop Arabic glyphs from a Latin file.
- Set `fontFamily` in `ThemeData` and `fontFamilyFallback: ['Vazirmatn']` for mixed Arabic/Latin text.
- Height: Flutter's `TextStyle.height` is a multiplier. Arabic usually needs `height: 1.6`, Nastaliq `2.0+`.

## iOS / SwiftUI / UIKit
- Bundle TTF/OTF (not woff2): `fonts.py download <id> --format ttf --out <App>/Fonts`. It prints each file's **PostScript name**.
- Add the files to the target (Target Membership) and list them in Info.plist `UIAppFonts` ("Fonts provided by application"). In SwiftUI-only projects, use the Info tab of the target.
- `Font.custom("Inter", size: 17, relativeTo: .body)` scales with Dynamic Type. Always pass `relativeTo:`. Use `.fontWeight(.bold)` with the family name, or the exact PostScript name (`Inter-Bold`) for a specific file.
- Variable TTF on iOS: works with `Font.custom(familyName)` + `.fontWeight`, but specific axes need `UIFontDescriptor` with `kCTFontVariationAttribute`. Static files are simpler.
- System Arabic (SF Arabic) is excellent. Only bundle an Arabic font when the brand needs one.

## Android (Compose and Views)
- Downloadable Google Fonts via `ui-text-google-fonts` add no APK size. The first load needs Play Services; provide a fallback.
- Bundled: put TTFs in `res/font/` with **lowercase_underscore** names (`inter_bold.ttf`), and build a `FontFamily(Font(R.font.inter_regular), Font(R.font.inter_bold, FontWeight.Bold))`.
- Views/XML: create a `res/font/inter.xml` font-family resource mapping weights to files, then `android:fontFamily="@font/inter"`.
- `includeFontPadding = false` (Compose: `PlatformTextStyle(includeFontPadding = false)`) for tighter Latin. Leave it **on** for Arabic/Urdu to avoid clipped marks.

## Electron / Tauri
Bundle woff2 with the app (`fonts.py download`). Never hit a CDN from desktop apps (offline use and privacy). `font-display: block` is fine because files are local.

## Open Graph images, PDFs, canvas
- `@vercel/og` / Satori needs **TTF/OTF/WOFF, not WOFF2**, and static weights: `fonts.py download <id> --format ttf --static`, then pass `fonts: [{ name, data, weight }]`.
- Satori has no Arabic shaping by default. For Arabic OG images, render with `@napi-rs/canvas`/resvg + HarfBuzz, or use Puppeteer/Playwright screenshots.
- PDF (Puppeteer/Playwright print): fonts must be loaded before printing: `await page.evaluate(() => document.fonts.ready)`.
- Canvas 2D: `await document.fonts.load("700 32px 'Inter Variable'")` before `ctx.fillText`, or the canvas draws in the fallback.
- pptxgenjs/python-pptx: the font must be **installed on the viewer's machine** (or embedded through PowerPoint). Pick from fonts the audience has, or ship a PDF.

## Email
Custom web fonts work in Apple Mail and iOS Mail only. Gmail and Outlook ignore them. Use `<link>` to Google Fonts in `<head>` plus a strong system fallback (`font-family: 'Inter', -apple-system, 'Segoe UI', Arial, sans-serif`), and design so the fallback looks intentional. Arabic email: `dir="rtl"` on the table cells, `Tahoma`/`Segoe UI` fallback.

## Slides, Figma, Canva and print
- Figma/Canva: most curated fonts are on Google Fonts and already available. Non-Google ones (Monaspace, Iosevka, Pretendard, Maple) must be installed locally: `fonts.py download <id> --format ttf --out ~/Library/Fonts`.
- Print/CMYK work: use static OTF/TTF from the source repo (`show <id>` gives the GitHub link). Variable fonts can misbehave in older RIPs.
