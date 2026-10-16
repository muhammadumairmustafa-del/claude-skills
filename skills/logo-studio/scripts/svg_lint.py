#!/usr/bin/env python3
"""Lint logo SVGs for things that make marks fragile or unprofessional.

  svg_lint.py concepts/*.svg [--bg "#F7F3EA"]

Flags (ERROR = fix before showing; WARN = check it is intentional):
  ERROR live <text>/<tspan> (outline it with text2path.py), <image>/raster data, <filter>,
        <foreignObject>, external href, missing viewBox
  WARN  more than 3 distinct fill/stroke colours, gradients (form should work flat),
        stroke widths under 1/64 of the viewBox (hairlines die at small sizes),
        transform rotations that miss a clean angle by <2° (near-miss angles look like mistakes),
        opacity < 1 (overlaps should be designed shapes, not transparency), file > 25 KB,
        stroked shapes in a final (outline with `shapes.py outline`),
        any colour under 3:1 contrast against --bg (default #FFFFFF; *-inverse files are checked
        against --dark-bg, default #111111)
"""
import argparse, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from recolour import colours_in, contrast  # noqa: E402
import xml.etree.ElementTree as ET

CLEAN = [0, 15, 22.5, 30, 45, 60, 67.5, 75, 90]


def colours(s):
    vals = re.findall(r'(?:fill|stroke|stop-color)\s*[:=]\s*"?\s*(#[0-9a-fA-F]{3,8}|rgb\([^)]*\)|[a-zA-Z]+)', s)
    return {v.lower() for v in vals if v.lower() not in ("none", "currentcolor", "transparent", "inherit")}


def lint(p: Path, bg="#FFFFFF", dark_bg="#111111"):
    s = p.read_text()
    errs, warns = [], []
    try:
        root = ET.fromstring(s)
    except ET.ParseError as e:
        return [f"invalid XML: {e}"], []
    tags = {el.tag.split("}")[-1] for el in root.iter()}
    for t in ("text", "tspan"):
        if t in tags: errs.append(f"live <{t}> - outline letters with text2path.py")
    for t in ("image", "filter", "foreignObject"):
        if t in tags: errs.append(f"<{t}> present - logos must be pure vector shapes")
    if re.search(r'href="(https?:|data:image/(png|jpe?g))', s): errs.append("external or raster href")
    vb = root.get("viewBox")
    if not vb:
        errs.append("missing viewBox")
        size = None
    else:
        _, _, w, h = map(float, vb.replace(",", " ").split())
        size = max(w, h)
    cols = colours(s)
    if len(cols) > 3: warns.append(f"{len(cols)} colours ({', '.join(sorted(cols))}) - strong marks rarely need >3")
    if "linearGradient" in tags or "radialGradient" in tags: warns.append("gradient - make sure the form works in flat colour first")
    if size:
        for sw in re.findall(r'stroke-width\s*[:=]\s*"?([\d.]+)', s):
            if float(sw) < size / 64: warns.append(f"stroke-width {sw} < 1/64 of viewBox ({size/64:.1f}) - hairline at small sizes")
    for ang in re.findall(r"rotate\(\s*(-?[\d.]+)", s):
        a = abs(float(ang)) % 90
        near = min(abs(a - c) for c in CLEAN)
        if 0 < near < 2: warns.append(f"rotate({ang}) is {near:.1f}° off a clean angle")
    if re.search(r'(?:fill-)?opacity\s*[:=]\s*"?0?\.\d', s): warns.append("partial opacity - prefer designed overlap shapes")
    if re.search(r'stroke\s*[:=]\s*"?\s*(#|[a-z])', s) and not re.search(r'stroke\s*[:=]\s*"?\s*none', s):
        warns.append("stroked shapes - outline them for finals: shapes.py outline file.svg")
    ref = dark_bg if p.stem.endswith("inverse") else bg
    for c in colours_in(s):
        r = contrast(c, ref)
        if r < 3: warns.append(f"{c} is {r}:1 on {ref} (logos need >= 3:1) - darken/lighten it or make a version for this background")
    kb = p.stat().st_size / 1024
    if kb > 25: warns.append(f"{kb:.0f} KB - simplify paths")
    return errs, warns


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("svgs", nargs="+")
    ap.add_argument("--bg", default="#FFFFFF"); ap.add_argument("--dark-bg", default="#111111")
    a = ap.parse_args()
    bad = 0
    for f in a.svgs:
        e, w = lint(Path(f), a.bg, a.dark_bg)
        status = "FAIL" if e else ("warn" if w else "ok")
        print(f"[{status}] {f}")
        for x in e: print(f"   ERROR {x}")
        for x in w: print(f"   WARN  {x}")
        bad += bool(e)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
