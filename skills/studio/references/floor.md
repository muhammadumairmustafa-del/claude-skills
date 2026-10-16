# Quality floor

Build to this without announcing it. It applies to every direction — a bold design that fails these is a broken design.

## Accessibility
- Text contrast ≥4.5:1 (≥3:1 for ≥24px or ≥19px bold, and for icons/borders that carry meaning). Muted text on coloured surfaces: tint it from that surface's hue, then check.
- Visible keyboard focus everywhere via `:focus-visible` (2px+ ring with offset, contrasting). Never remove outlines without a replacement.
- Logical tab order; skip link on long pages; modals trap focus and return it on close; Esc closes overlays.
- Icon-only buttons have `aria-label`; images have meaningful `alt` (or `alt=""` if decorative); one `h1`, no skipped heading levels.
- Use accessible primitives (Radix, React Aria, Base UI, native elements) instead of hand-rolled keyboard handling.
- Never convey meaning by colour alone. Respect reduced motion. Zoom to 200% doesn't break layout; never disable pinch-zoom.

## Touch & interaction
- Targets ≥44×44pt (iOS) / 48×48dp (Android), ≥8px apart. Primary mobile actions in thumb reach.
- Every interactive element has hover (pointer devices only: `@media (hover:hover)`), active/pressed, focus, disabled, and loading states.
- Feedback within 100ms; show progress for anything >1s; optimistic UI where safe.
- Destructive actions: confirm dialog or undo. Undo is usually better.

## Every state, not just the happy path
For each screen design: **empty** (first use — one clear next action), **loading** (skeletons matching final layout, not spinners for content), **partial**, **error** (what happened, why, how to fix — inline, near the cause), **success**, **offline**, **no permission**.

## Worst-case content
Test with: very long names/emails/titles (`min-width: 0` on flex children, truncation with full text on hover/expand), 0 items, 1 item, 1,284 items, huge numbers, missing images, non-Latin and RTL text, 200% zoom. Add a quick "stress" toggle in the dev build if useful.

## Forms
- Labels always visible (placeholder is not a label). Correct `type`, `inputmode`, `autocomplete`. Never block paste.
- Validate on blur, not every keystroke; errors under the field in "[Field] [requirement]" form; focus the first error on submit.
- Keep submit enabled until the request starts, then show loading and prevent double-submit.
- Group long forms into steps or sections; mark optional fields rather than required ones when most are required.

## Web details
- Viewport meta; no horizontal scroll at 320px; `100dvh` not `100vh`; safe-area insets on mobile.
- Images: explicit width/height or aspect-ratio (CLS < 0.1), modern formats, lazy-load below the fold.
- URL reflects UI state (tabs, filters, search) so it can be shared and back works.
- Typographic marks: `…` `“ ”` `’` `–` `×`; "Loading…" not "Loading...".
- `color-scheme` and `theme-color` set for both themes; style `::selection`, caret, scrollbars and focus to match.
- Semantic HTML: `button` for actions, `a` for navigation.

## Performance
LCP < 2.5s, INP < 200ms, CLS < 0.1. No layout thrash from animating width/height/top. Defer heavy effects (shaders, 3D, video) until after first paint and pause them off-screen.
