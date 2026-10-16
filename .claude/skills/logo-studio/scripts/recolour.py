#!/usr/bin/env python3
"""Recolour logo SVGs: explicit maps, mono versions, automatic inverse, and contrast checks.

  recolour.py A1.svg --map "#3B2A33=#FFF4EA" "#E8643A=#FF8A5B" --out A1-inverse.svg
  recolour.py A1.svg --mono "#000000" --out A1-black.svg
  recolour.py A1.svg --auto-inverse --out A1-inverse.svg      # dark colours -> light, keeps accents
  recolour.py --contrast "#E8643A" "#FFF4EA"                    # prints ratio (logos need >= 3:1)

Module: from recolour import recolour_map, mono, auto_inverse, contrast, colours_in
"""
import argparse, re, sys
from pathlib import Path

COLOR_RE = re.compile(r'((?:fill|stroke|stop-color)\s*[:=]\s*"?\s*)(#[0-9a-fA-F]{3,8}\b|currentColor|black|white)')
NAMED = {"black": "#000000", "white": "#ffffff"}


def norm(c):
    c = NAMED.get(c.lower(), c).lower()
    if re.fullmatch(r"#[0-9a-f]{3}", c):
        c = "#" + "".join(ch * 2 for ch in c[1:])
    return c[:7]


def lum(c):
    c = norm(c)
    r, g, b = (int(c[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return round((la + 0.05) / (lb + 0.05), 2)


def colours_in(svg):
    return sorted({norm(m.group(2)) for m in COLOR_RE.finditer(svg) if m.group(2) != "currentColor"})


def _has_unfilled_shapes(svg):
    # shapes with no fill attribute render black by default
    return bool(re.search(r"<(path|circle|rect|polygon|ellipse)(?![^>]*\bfill=)[^>]*>", svg)) and 'fill="' not in svg.split(">", 1)[0]


def recolour_map(svg, mapping):
    m = {norm(k): v for k, v in mapping.items()}
    out = COLOR_RE.sub(lambda x: x.group(1) + m.get(norm(x.group(2)) if x.group(2) != "currentColor" else "", x.group(2)), svg)
    if "#000000" in m and _has_unfilled_shapes(svg):
        out = out.replace("<svg ", f'<svg fill="{m["#000000"]}" ', 1)
    return out


def mono(svg, colour):
    out = COLOR_RE.sub(lambda x: x.group(1) + colour, svg)
    return re.sub(r"<svg ", f'<svg fill="{colour}" ', out, count=1) if 'fill="' not in out.split(">", 1)[0] else out


def auto_inverse(svg, dark_bg="#111111", light="#FFFFFF", min_ratio=3.0):
    """Swap every colour that fails contrast on dark_bg to `light`; keep colours that already work."""
    mapping = {c: light for c in colours_in(svg) if contrast(c, dark_bg) < min_ratio}
    if _has_unfilled_shapes(svg):
        mapping["#000000"] = light
    return recolour_map(svg, mapping)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("svg", nargs="?")
    ap.add_argument("--map", nargs="+", help='pairs like "#111=#fff"')
    ap.add_argument("--mono"); ap.add_argument("--auto-inverse", action="store_true"); ap.add_argument("--dark-bg", default="#111111")
    ap.add_argument("--contrast", nargs=2, metavar=("FG", "BG")); ap.add_argument("--out")
    a = ap.parse_args()
    if a.contrast:
        r = contrast(*a.contrast); print(f"{r}:1 {'ok' if r >= 3 else 'FAILS 3:1 for logos'}"); return
    if not a.svg:
        ap.error("svg required")
    s = Path(a.svg).read_text()
    if a.map: s = recolour_map(s, dict(p.split("=", 1) for p in a.map))
    if a.mono: s = mono(s, a.mono)
    if a.auto_inverse: s = auto_inverse(s, a.dark_bg)
    if a.out: Path(a.out).write_text(s); print(a.out)
    else: sys.stdout.write(s)


if __name__ == "__main__":
    main()
