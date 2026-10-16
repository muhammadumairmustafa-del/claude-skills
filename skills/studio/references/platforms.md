# Platforms and languages

## iOS (SwiftUI / React Native / Expo)
- Follow HIG structure: tab bar (≤5) for top-level, navigation stack with large titles that collapse, sheets for focused sub-tasks (with detents), no hamburger menus.
- Never override the edge back-swipe. Primary actions in the bottom half (thumb reach); destructive actions red and confirmed via action sheet.
- Dynamic Type including accessibility sizes — layouts must reflow, not truncate. Text never below 11pt. SF Pro / SF Rounded are fine defaults on iOS if the direction's font doesn't need to cross platforms; custom fonts must scale with `UIFontMetrics`/`relativeTo:`.
- Semantic system colours or tokens with light + dark variants; respect Increase Contrast and Reduce Transparency.
- Haptics: light impact on toggles/selection, success/error notifications on outcomes. Not on scroll.
- Safe areas, Dynamic Island and home indicator respected; keyboard avoidance on every form.
- SF Symbols for icons where possible, matched to text weight.

## Android (Material 3 / Compose / RN)
- Navigation bar (3–5) or rail on tablets; top app bar; FAB only for the single most common creation action.
- System back (and predictive back) must always work and never trap the user.
- 48dp targets; edge-to-edge with proper insets; Material You dynamic colour is optional — brand tokens can override.
- Ripple feedback on touch; respect font scale up to 200%.

## Cross-platform apps
Share tokens (colour, type scale, spacing, radius) and content; let navigation, controls, sheets and gestures follow each platform's conventions. A direction expresses itself through colour, type, imagery and the signature moment — not by making iOS feel like Android or vice versa.

## RTL: Arabic and Urdu
- Set `dir="rtl"` and `lang` (`ar`, `ur`) on the root (or per block for mixed content). Use logical CSS properties everywhere: `margin-inline-start`, `padding-inline`, `inset-inline-end`, `text-align: start`, `border-start-start-radius`. In RN use `start/end`, `I18nManager`; in SwiftUI `.leading/.trailing` handle it.
- Mirror: layout direction, navigation order, back/forward chevrons, progress, sliders, carousels, timeline direction. Don't mirror: media playback controls, clocks, charts' numeric axes (usually), logos, checkmarks, phone numbers.
- Numbers: decide Western (123) vs Eastern Arabic (١٢٣) digits per audience (KSA consumer apps often accept both; be consistent). Keep numbers LTR inside RTL text with `<bdi>` / `unicode-bidi: isolate`.
- Fonts: Arabic — IBM Plex Sans Arabic, Readex Pro, Alexandria, Tajawal, Cairo, Noto Naskh Arabic; Urdu — Noto Nastaliq Urdu or Gulzar for Nastaliq feel, Noto Naskh Arabic for UI legibility at small sizes. Pair the Latin direction font with an Arabic face of similar weight/contrast, and size-match visually (Arabic often needs ~110–120% to look equal).
- Line-height: Arabic 1.6–1.8; **Nastaliq needs ~2.0–2.2** and extra vertical padding in buttons/inputs or ascenders and descenders clip. Never use letter-spacing on Arabic script (it breaks joining). No all-caps/italic equivalents — use weight or colour for emphasis.
- Test with real copy (not lorem): Arabic and Urdu strings run 20–30% different in length; check truncation and wrapping in both directions, and mixed RTL/LTR strings (brand names, URLs, numbers).
- Icons with direction (arrows, send, reply, undo) need RTL variants.
