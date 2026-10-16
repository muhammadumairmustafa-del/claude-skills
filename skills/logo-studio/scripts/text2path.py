#!/usr/bin/env python3
"""Convert text into SVG outlines using any Google Font (or a local font file).

Logos must not depend on fonts being installed on the viewer's machine, so every
wordmark/lettermark in a final SVG should be outlined paths, not <text>.

Usage (CLI):
  text2path.py "Falak" --font "Space Grotesk" --weight 700 --size 120 --tracking 40
  text2path.py "UV" --font-file /Library/Fonts/Roboto-Bold.ttf --size 200 --out uv.svg

Prints a JSON object: {"d": "<path data>", "width", "height", "ascender", "descender",
"x0", "y0", "x1", "y1"} or, with --out, writes a standalone SVG fitted to the ink bounds.
Coordinates: baseline at y=0, text grows up (negative y), like SVG text.

As a module (normal use inside a build script):
  from text2path import text_to_path
  info = text_to_path("Falak", font="Space Grotesk", weight=700, size=120, tracking=40)
  info["d"]       # whole word as one path
  info["glyphs"]  # per glyph: {"char","glyph","x","advance","d","bounds"} - modify one letter
                  # (e.g. shapes.diff(g["d"], rect(...))), recolour Arabic dots, swap a glyph.
Arabic/Urdu: shaping and joining are automatic. To lengthen a join (kashida) insert U+0640 'ـ'
between letters, e.g. "ليــدجرلي"; ss/salt features via features={"ss01": True}.
--out writes one <path id="gN" data-char=".."> per glyph inside <g id="word">.
"""
import argparse, json, os, re, sys, urllib.parse, urllib.request
from pathlib import Path

CACHE = Path(os.path.expanduser("~/.cache/logo-studio/fonts"))


def fetch_google_font(family: str, weight: int = 400, italic: bool = False) -> Path:
    """Download a static TTF for family@weight from Google Fonts (cached)."""
    CACHE.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", family.lower()).strip("-")
    out = CACHE / f"{slug}-{weight}{'i' if italic else ''}.ttf"
    if out.exists() and out.stat().st_size > 1000:
        return out
    axis = f"ital,wght@1,{weight}" if italic else f"wght@{weight}"
    url = "https://fonts.googleapis.com/css2?family=" + urllib.parse.quote_plus(family) + ":" + axis
    try:
        css = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "python"}), timeout=20).read().decode()
    except Exception as e:
        # Font may not offer that weight: retry without a weight axis
        url = "https://fonts.googleapis.com/css2?family=" + urllib.parse.quote_plus(family)
        try:
            css = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "python"}), timeout=20).read().decode()
            print(f"warning: {family} has no weight {weight}; using default weight", file=sys.stderr)
        except Exception:
            raise SystemExit(f"Could not fetch Google Font '{family}': {e}")
    m = re.search(r"src:\s*url\((https://[^)]+\.ttf)\)", css)
    if not m:
        raise SystemExit(f"No TTF found for '{family}' in Google Fonts response")
    out.write_bytes(urllib.request.urlopen(m.group(1), timeout=30).read())
    return out


def text_to_path(text, font=None, font_file=None, weight=400, italic=False, size=100.0,
                 tracking=0.0, features=None):
    """Shape `text` with HarfBuzz (kerning, ligatures) and return outline path data.

    tracking: extra space between letters in 1/1000 em (like Figma/Illustrator tracking).
    features: dict of OpenType features, e.g. {"liga": False, "ss01": True}.
    """
    import uharfbuzz as hb
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.pens.boundsPen import BoundsPen

    path = Path(font_file) if font_file else fetch_google_font(font, weight, italic)
    blob = hb.Blob.from_file_path(str(path))
    face = hb.Face(blob)
    hbfont = hb.Font(face)
    upem = face.upem
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hbfont, buf, features or {})

    tt = TTFont(str(path))
    glyphset = tt.getGlyphSet()
    order = tt.getGlyphOrder()
    scale = size / upem
    track = tracking / 1000.0 * upem

    ntos = lambda v: (f"{v:.2f}".rstrip("0").rstrip(".") or "0")
    svgpen = SVGPathPen(glyphset, ntos=ntos)
    bpen = BoundsPen(glyphset)
    glyphs = []
    x = 0.0
    n = len(buf.glyph_infos)
    for i, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        name = order[info.codepoint]
        dx, dy = x + pos.x_offset, pos.y_offset
        # flip y: font units are y-up, SVG is y-down
        t = (scale, 0, 0, -scale, dx * scale, -dy * scale)
        gpen = SVGPathPen(glyphset, ntos=ntos); gb = BoundsPen(glyphset)
        glyphset[name].draw(TransformPen(svgpen, t))
        glyphset[name].draw(TransformPen(bpen, t))
        glyphset[name].draw(TransformPen(gpen, t))
        glyphset[name].draw(TransformPen(gb, t))
        glyphs.append({"index": i, "glyph": name, "cluster": info.cluster,
                       "char": text[info.cluster:(buf.glyph_infos[i + 1].cluster if i + 1 < n and buf.glyph_infos[i + 1].cluster > info.cluster else info.cluster + 1)],
                       "x": round(dx * scale, 2), "advance": round(pos.x_advance * scale, 2),
                       "d": gpen.getCommands(), "bounds": [round(v, 2) for v in (gb.bounds or (0, 0, 0, 0))]})
        x += pos.x_advance + (track if i < n - 1 else 0)

    hhea = tt["hhea"]
    b = bpen.bounds or (0, 0, 0, 0)
    return {
        "d": svgpen.getCommands(),
        "width": round(x * scale, 2),
        "ascender": round(hhea.ascent * scale, 2),
        "descender": round(hhea.descent * scale, 2),
        "x0": round(b[0], 2), "y0": round(b[1], 2), "x1": round(b[2], 2), "y1": round(b[3], 2),
        "font_file": str(path),
        "glyphs": glyphs,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("text")
    ap.add_argument("--font", help="Google Font family name, e.g. 'DM Serif Display'")
    ap.add_argument("--font-file", help="Local .ttf/.otf instead of a Google Font")
    ap.add_argument("--weight", type=int, default=400)
    ap.add_argument("--italic", action="store_true")
    ap.add_argument("--size", type=float, default=100)
    ap.add_argument("--tracking", type=float, default=0, help="1/1000 em, can be negative")
    ap.add_argument("--no-liga", action="store_true", help="disable ligatures")
    ap.add_argument("--fill", default="#111111")
    ap.add_argument("--out", help="write a standalone SVG fitted to the ink bounds (one <path id=g0..> per glyph)")
    ap.add_argument("--glyphs", action="store_true", help="print per-glyph JSON (path, x, advance, bounds, char) for glyph surgery")
    a = ap.parse_args()
    if not (a.font or a.font_file):
        ap.error("give --font or --font-file")
    info = text_to_path(a.text, a.font, a.font_file, a.weight, a.italic, a.size, a.tracking,
                        {"liga": False} if a.no_liga else None)
    if a.out:
        pad = a.size * 0.05
        w = info["x1"] - info["x0"] + 2 * pad
        h = info["y1"] - info["y0"] + 2 * pad
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{info["x0"]-pad:.2f} {info["y0"]-pad:.2f} {w:.2f} {h:.2f}">'
               f'<g id="word" fill="{a.fill}">' + "".join(f'<path id="g{g["index"]}" data-char="{g["char"]}" d="{g["d"]}"/>' for g in info["glyphs"] if g["d"]) + '</g></svg>\n')
        Path(a.out).write_text(svg)
        print(a.out)
    elif a.glyphs:
        print(json.dumps(info["glyphs"], ensure_ascii=False, indent=1))
    else:
        info.pop("glyphs"); print(json.dumps(info))


if __name__ == "__main__":
    main()
