#!/usr/bin/env python3
"""Exact geometry + boolean operations for logo construction (skia-pathops).

Use it as a module inside your build script - that is the normal way:

    import sys; sys.path.insert(0, "<skill>/scripts")
    from shapes import *
    ring  = diff(circle(128, 128, 112), circle(128, 128, 72))     # cut, don't paint
    notch = rect(120, 0, 16, 128)
    mark  = diff(ring, notch)
    arc_d = stroke(arc(128, 128, 92, -90, 180), 24, cap="round")   # monoline -> filled outline
    star8 = star(128, 128, 8, 112, 80, rot=22.5)
    write_svg("A1.svg", [(mark, "#111"), (star8, "#E8643A")], viewbox=(0, 0, 256, 256))

All functions take/return SVG path-data strings, so they mix freely with text2path.py output
(e.g. diff(word_d, rect(...)) to notch a letter, or union of glyph paths).

Primitives: circle, ellipse, rect (rx for rounded), superellipse (iOS squircle), polygon, regular,
            star, arc (open centreline), line, polyline, ring, petals
Booleans:   union(*ds), diff(a, *bs), intersect(a, b), xor(a, b), simplify(d)
Strokes:    stroke(d, width, cap="round"|"butt"|"square", join="round"|"miter"|"bevel")
Transforms: translate(d, dx, dy), scale(d, sx, sy=None, cx=0, cy=0), rotate(d, deg, cx=0, cy=0),
            mirror_x(d, cx), radial(d, n, cx, cy) - n rotated copies unioned
Info:       bounds(d) -> (x0, y0, x1, y1), area(d)

CLI: shapes.py outline in.svg --out out.svg   converts every stroked element in an SVG to filled
     outlines (final logos should not depend on stroke rendering), keeping fill colours.
"""
import math, re, sys
import pathops
from fontTools.svgLib.path import parse_path
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

_NT = lambda v: (f"{v:.2f}".rstrip("0").rstrip(".") or "0")


# ---------- conversion ----------
def _to_path(d) -> pathops.Path:
    if isinstance(d, pathops.Path):
        return d
    p = pathops.Path()
    parse_path(d, p.getPen())
    return p


def _to_d(p: pathops.Path) -> str:
    p.convertConicsToQuads()
    pen = SVGPathPen(None, ntos=_NT)
    p.draw(pen)
    return pen.getCommands()


def _xf(d, t):
    pen = SVGPathPen(None, ntos=_NT)
    parse_path(d, TransformPen(pen, t))
    return pen.getCommands()


# ---------- primitives ----------
def circle(cx, cy, r):
    k = 0.5522847498 * r
    return (f"M{_NT(cx+r)} {_NT(cy)}C{_NT(cx+r)} {_NT(cy+k)} {_NT(cx+k)} {_NT(cy+r)} {_NT(cx)} {_NT(cy+r)}"
            f"C{_NT(cx-k)} {_NT(cy+r)} {_NT(cx-r)} {_NT(cy+k)} {_NT(cx-r)} {_NT(cy)}"
            f"C{_NT(cx-r)} {_NT(cy-k)} {_NT(cx-k)} {_NT(cy-r)} {_NT(cx)} {_NT(cy-r)}"
            f"C{_NT(cx+k)} {_NT(cy-r)} {_NT(cx+r)} {_NT(cy-k)} {_NT(cx+r)} {_NT(cy)}Z")


def ellipse(cx, cy, rx, ry):
    return _xf(circle(0, 0, 1), (rx, 0, 0, ry, cx, cy))


def rect(x, y, w, h, rx=0):
    if not rx:
        return f"M{_NT(x)} {_NT(y)}H{_NT(x+w)}V{_NT(y+h)}H{_NT(x)}Z"
    r = min(rx, w / 2, h / 2); k = 0.5522847498 * r
    return (f"M{_NT(x+r)} {_NT(y)}H{_NT(x+w-r)}C{_NT(x+w-r+k)} {_NT(y)} {_NT(x+w)} {_NT(y+r-k)} {_NT(x+w)} {_NT(y+r)}"
            f"V{_NT(y+h-r)}C{_NT(x+w)} {_NT(y+h-r+k)} {_NT(x+w-r+k)} {_NT(y+h)} {_NT(x+w-r)} {_NT(y+h)}"
            f"H{_NT(x+r)}C{_NT(x+r-k)} {_NT(y+h)} {_NT(x)} {_NT(y+h-r+k)} {_NT(x)} {_NT(y+h-r)}"
            f"V{_NT(y+r)}C{_NT(x)} {_NT(y+r-k)} {_NT(x+r-k)} {_NT(y)} {_NT(x+r)} {_NT(y)}Z")


def superellipse(cx, cy, w, h, n=5, steps=160):
    """iOS-style squircle (n~5). Good for app-tile shapes."""
    pts = []
    for i in range(steps):
        t = 2 * math.pi * i / steps
        c, s = math.cos(t), math.sin(t)
        pts.append((cx + w / 2 * math.copysign(abs(c) ** (2 / n), c), cy + h / 2 * math.copysign(abs(s) ** (2 / n), s)))
    return polygon(pts)


def polygon(pts):
    return "M" + "L".join(f"{_NT(x)} {_NT(y)}" for x, y in pts) + "Z"


def regular(cx, cy, n, r, rot=0):
    """Regular n-gon; rot in degrees, 0 = first vertex pointing up."""
    return polygon([(cx + r * math.sin(math.radians(rot + 360 * i / n)), cy - r * math.cos(math.radians(rot + 360 * i / n))) for i in range(n)])


def star(cx, cy, n, r_out, r_in, rot=0):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + 180 * i / n)
        pts.append((cx + r * math.sin(a), cy - r * math.cos(a)))
    return polygon(pts)


def arc(cx, cy, r, start_deg, sweep_deg, steps=None):
    """Open arc centreline (0° = up/12 o'clock, clockwise positive). Feed to stroke()."""
    steps = steps or max(8, int(abs(sweep_deg) / 6))
    pts = []
    for i in range(steps + 1):
        a = math.radians(start_deg + sweep_deg * i / steps)
        pts.append((cx + r * math.sin(a), cy - r * math.cos(a)))
    return "M" + "L".join(f"{_NT(x)} {_NT(y)}" for x, y in pts)


def line(x1, y1, x2, y2):
    return f"M{_NT(x1)} {_NT(y1)}L{_NT(x2)} {_NT(y2)}"


def polyline(pts):
    return "M" + "L".join(f"{_NT(x)} {_NT(y)}" for x, y in pts)


def ring(cx, cy, r_out, r_in):
    return diff(circle(cx, cy, r_out), circle(cx, cy, r_in))


def petals(cx, cy, n, length, width, offset=0, rot=0):
    """n lens-shaped petals around a centre (flower, rosette, propeller)."""
    one = ellipse(cx, cy - offset - length / 2, width / 2, length / 2)
    return radial(one, n, cx, cy, rot)


# ---------- booleans ----------
def _op(a, b, op):
    return _to_d(pathops.op(_to_path(a), _to_path(b), op, fix_winding=True))


def union(*ds):
    out = pathops.Path()
    for d in ds:
        out = pathops.op(out, _to_path(d), pathops.PathOp.UNION, fix_winding=True)
    return _to_d(out)


def diff(a, *bs):
    for b in bs:
        a = _op(a, b, pathops.PathOp.DIFFERENCE)
    return a if isinstance(a, str) else _to_d(a)


def intersect(a, b):
    return _op(a, b, pathops.PathOp.INTERSECTION)


def xor(a, b):
    return _op(a, b, pathops.PathOp.XOR)


def simplify(d):
    return _to_d(pathops.simplify(_to_path(d), fix_winding=True))


_CAP = {"butt": pathops.LineCap.BUTT_CAP, "round": pathops.LineCap.ROUND_CAP, "square": pathops.LineCap.SQUARE_CAP}
_JOIN = {"miter": pathops.LineJoin.MITER_JOIN, "round": pathops.LineJoin.ROUND_JOIN, "bevel": pathops.LineJoin.BEVEL_JOIN}


def stroke(d, width, cap="round", join="round", miter=4):
    """Turn a centreline into a filled outline (do this before any boolean with strokes)."""
    p = _to_path(d)
    p.stroke(width, _CAP[cap], _JOIN[join], miter)
    p.convertConicsToQuads()  # round caps/joins produce conics, which booleans can't handle
    return _to_d(pathops.simplify(p, fix_winding=True))


# ---------- transforms ----------
def translate(d, dx, dy):
    return _xf(d, (1, 0, 0, 1, dx, dy))


def scale(d, sx, sy=None, cx=0, cy=0):
    sy = sx if sy is None else sy
    return _xf(d, (sx, 0, 0, sy, cx - sx * cx, cy - sy * cy))


def rotate(d, deg, cx=0, cy=0):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return _xf(d, (c, s, -s, c, cx - c * cx + s * cy, cy - s * cx - c * cy))


def mirror_x(d, cx=0):
    return _xf(d, (-1, 0, 0, 1, 2 * cx, 0))


def radial(d, n, cx, cy, rot=0):
    return union(*[rotate(d, rot + 360 * i / n, cx, cy) for i in range(n)])


# ---------- info / output ----------
def bounds(d):
    return _to_path(d).bounds


def area(d):
    return _to_path(d).area


def write_svg(path, layers, viewbox=(0, 0, 256, 256), groups=None):
    """layers: list of (d, fill) or (d, fill, id). Writes a clean, lint-ready SVG."""
    x, y, w, h = viewbox
    body = []
    for L in layers:
        d, fill = L[0], L[1]
        idattr = f' id="{L[2]}"' if len(L) > 2 else ""
        body.append(f'<path{idattr} fill="{fill}" d="{d}"/>')
    open(path, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{_NT(x)} {_NT(y)} {_NT(w)} {_NT(h)}">' + "".join(body) + "</svg>\n")
    return path


# ---------- CLI: outline strokes in an existing SVG ----------
def _outline_svg(src, dst):
    import xml.etree.ElementTree as ET
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    tree = ET.parse(src); root = tree.getroot()
    n = 0
    for el in list(root.iter()):
        tag = el.tag.split("}")[-1]
        sw = el.get("stroke-width"); st = el.get("stroke")
        style = el.get("style", "")
        m = re.search(r"stroke:\s*([^;]+)", style); st = st or (m.group(1).strip() if m else None)
        m = re.search(r"stroke-width:\s*([\d.]+)", style); sw = sw or (m.group(1) if m else None)
        if not st or st == "none" or tag not in ("path", "line", "polyline", "polygon", "circle", "ellipse", "rect"):
            continue
        if el.get("transform"):
            print(f"warning: <{tag}> has a transform; bake it into coordinates first", file=sys.stderr); continue
        g = lambda k, dflt=0: float(el.get(k, dflt))
        if tag == "path": d = el.get("d")
        elif tag == "line": d = line(g("x1"), g("y1"), g("x2"), g("y2"))
        elif tag in ("polyline", "polygon"):
            nums = list(map(float, re.findall(r"-?[\d.]+", el.get("points", ""))))
            pts = list(zip(nums[::2], nums[1::2])); d = polyline(pts) + ("Z" if tag == "polygon" else "")
        elif tag == "circle": d = circle(g("cx"), g("cy"), g("r"))
        elif tag == "ellipse": d = ellipse(g("cx"), g("cy"), g("rx"), g("ry"))
        else: d = rect(g("x"), g("y"), g("width"), g("height"), g("rx"))
        cap = el.get("stroke-linecap", "butt"); join = el.get("stroke-linejoin", "miter")
        outline = stroke(d, float(sw or 1), cap, join)
        fill = el.get("fill")
        if fill and fill != "none":
            outline = union(d, outline) if fill == st else outline  # same colour: merge
            if fill != st:
                print(f"warning: <{tag}> has different fill and stroke colours; kept stroke only", file=sys.stderr)
        new = ET.Element("{http://www.w3.org/2000/svg}path", {"d": outline, "fill": st})
        if el.get("id"): new.set("id", el.get("id"))
        parent = next(p for p in root.iter() if el in list(p))
        parent.insert(list(parent).index(el), new); parent.remove(el); n += 1
    tree.write(dst, encoding="unicode")
    print(f"{dst}: outlined {n} stroked element(s)")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("outline"); p.add_argument("svg"); p.add_argument("--out")
    a = ap.parse_args()
    _outline_svg(a.svg, a.out or a.svg)
