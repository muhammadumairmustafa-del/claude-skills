# Mark types, methods and form generators

Distinctness comes from varying the **mark type**, the **idea method** and the **form generator** independently. Two concepts may share at most one of the three. Two concepts that share all three are one concept with different paint.

## 1. Mark types (what the logo *is*)

| Type | What it is | Choose when | Watch out |
|---|---|---|---|
| Wordmark | The name, custom-set or modified type | Short, distinctive name (≤ 8 letters); name *is* the brand | Bad if it's just a font. Needs a custom move: ligature, cut, swapped glyph, unique spacing |
| Lettermark / monogram | 1–3 initials as a compact unit | Long names, needs an app icon | Every monogram looks like every other — needs a real idea in the letter construction |
| Letterform symbol | One letter rebuilt into a symbol (Facebook f, Airbnb-ish) | You need a strong icon plus a link to the name | Letter must still read (letter test) |
| Pictorial | A recognisable object, simplified | The object is ownable and not a category cliché | Literal = forgettable. Only with a twist |
| Abstract | A non-representational form carrying a feeling or principle | Broad or changing offerings, tech, finance | Easy to be generic; must have a reason you can say in one sentence |
| Negative space | Two readings in one figure/ground | There's a genuine double meaning in the brief | Forced double meanings feel like puzzles |
| Emblem / badge | Symbol + text contained in a shape | Heritage, food & drink, clubs, education, government | Poor at small sizes; always design a stripped icon too |
| Mascot / character | A character | Consumer, kids, gaming, community | Hardest to draw well in SVG; keep geometric |
| Combination | Symbol + wordmark designed as a system | Default for most new brands | Design the symbol to stand alone |
| Dynamic / system | A rule that generates variants (grid, colour, frame) | Media, platforms, events, multi-product brands | Must still have a fixed anchor (wordmark) |

## 2. Idea methods (how the concept is *found*)

Pick a different method per concept. These come from the "24 methods" approach to black-and-white marks.

1. **Visual pun:** two things fused because they share a shape (a pen nib that is also a leaf).
2. **Negative space:** a second form hiding in the gaps.
3. **Letter fusion:** two letters share strokes or a counter.
4. **Initial deformation:** one letter is bent to perform the brand's verb.
5. **Square module:** everything built from one repeated cell on a grid.
6. **Constructivist:** bold diagonals, wedges and bars, Russian-poster energy.
7. **Bold black mass:** one heavy silhouette with a single precise cut.
8. **Directional offset:** a shape displaced or sheared to show motion or progress.
9. **Repetitive rhythm:** the same unit repeated 3–7× with a progression.
10. **Spatial translation:** a 2D form implying 3D (fold, ribbon, isometric).
11. **Action translation:** draw the verb (open, connect, lift, listen), not the noun.
12. **Emotional graph:** the brand's feeling as a curve or line gesture.
13. **Cultural motif:** a pattern, script or craft from the brand's place, stripped back (see the Cultural themes in themes.md).
14. **Containment:** something held, framed or protected by another shape.
15. **Interruption:** a regular shape with one break, gap or missing piece.
16. **Single continuous line:** one stroke draws the whole mark.
17. **Overlap / transparency (as designed shapes):** overlapping zones get their own flat colour.
18. **Cropping:** a fragment of a larger form, so the viewer completes it.
19. **Stacking / building:** blocks or layers that build up.
20. **Orbit / path:** an element travelling on a path.
21. **Split / duality:** halves that differ (old/new, human/machine).
22. **Typographic quirk:** one glyph replaced by a symbol, or one swash or ligature.
23. **Counter play:** a letter's enclosed space becomes the symbol.
24. **Seal / stamp:** a circular or official mark used playfully.

## 3. Form generators (what the mark is *built from*)

These are construction systems, from op7418's pattern library. Each gives a very different texture.

- **Dot grid:** circles, rounded squares, capsules or hexagons on a grid; the shape is formed by which dots are present or absent, or by dot size.
- **Boolean cut:** big primitives (circle, square, triangle) with subtractions; `fill-rule="evenodd"`.
- **Monoline:** a single stroke weight, round caps, built on arcs and straights. Outline the strokes before the final export only if needed.
- **Parallel lines:** 3–9 lines that bend, shift or are cut to make a form (the "line fill" look).
- **Node network:** points and connectors. Avoid the generic "molecule" look by giving it a strict geometric arrangement.
- **Petal / radial:** one unit rotated n times (n = 3, 4, 5, 6, 8, 12) around a centre.
- **Wave / spiral:** sinusoidal or Archimedean curves; always constructed mathematically, never freehand.
- **Folded plane / ribbon:** flat shapes with 2–3 tones implying folding.
- **Stencil:** solid letterforms with bridges or gaps.
- **Pixel / bitmap:** a strict low-res grid (5×5, 7×7, 8×8). Retro-tech.
- **Brush-geometric:** geometric shapes with one tapered, calligraphic stroke.
- **Isometric:** 30° projection, cubes and planes.

## Distinctness matrix (fill this in before drawing)

```
| id | theme | mark type      | method            | generator     | silhouette at 32px     |
| A1 | A     | letterform     | counter play      | boolean cut   | heavy circle with notch |
| A2 | A     | abstract       | orbit / path      | monoline      | open ring + dot         |
| B1 | B     | wordmark       | typographic quirk | –             | wide text bar           |
...
```
Reject any pair with the same type **and** the same generator, or the same expected silhouette. In the final set, at least half the concepts should use different mark types.
