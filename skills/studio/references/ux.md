# UX structure: before pixels

Most UI problems are structure problems wearing a visual costume. Do this pass before choosing a direction for anything bigger than a single component.

## 1. Subject inventory
List 8–12 facts that belong only to this product: who uses it, the one job they hire it for, the moment they open it (where, how stressed, how much time), real nouns from their world, real numbers, constraints (language, connectivity, device, regulation), competitors they know. Distinctive design comes from here, not from a style list.

## 2. Jobs and the core loop
- Primary job in one sentence: "When ___, I want to ___, so I can ___."
- The core loop: the 3–5 steps a returning user repeats. This loop gets the best real estate, fewest taps, and fastest feedback. Everything else is secondary navigation.
- Time-to-value: how many steps from first open to the first useful result? Cut until it's as few as possible; defer sign-up until value is shown when the business allows.

## 3. Information architecture
- Inventory objects (things users manage) and actions (what they do to them). Name them with the user's words.
- Navigation depth ≤3 for frequent tasks. 3–5 top-level destinations (mobile tab bar: max 5).
- Each screen has one primary action. If a screen has two, it's probably two screens or one is secondary.
- Sitemap or screen list as a short indented list; flows as arrows: `Home → Reading detail → Share sheet`.

## 4. Flows
For each key flow, write the steps and for each step: what the user sees, decides, and does; what can go wrong; how they recover; where they can leave and come back (save progress). Check: back always works, nothing is a dead end, errors never lose user input.

## 5. Onboarding
Show, don't tour. Prefer: one personalising question → immediate tailored result → ask for account/permissions at the moment they're needed with a reason ("Allow notifications so we can send your daily reading at 8am"). Never a 5-screen carousel before the product.

## 6. Data-dense app UI (operate mode)
- Tables: left-align text, right-align numbers (tabular figures), sticky header and first column, row hover, density toggle, column sort/hide, inline row actions on hover + overflow menu, bulk-select with a contextual action bar.
- Filters: visible as chips with counts, URL-persisted, one-click clear, saved views.
- Dashboards: answer "is everything okay?" in the first second (status summary), then "what changed?" (deltas vs. a stated period), then detail. Size panels by how often they're used, not symmetry. Every chart has a title that states the insight, units and a time range.
- Keyboard: command palette (⌘K), shortcuts for frequent actions, visible shortcut hints.
- Empty dashboards guide setup instead of showing zero-filled charts.

## 7. Wireframe
ASCII wireframe of the key screen(s) at mobile and desktop widths before styling. Check hierarchy with the squint test: blur your eyes — is the primary action and the most important information still the most prominent?
