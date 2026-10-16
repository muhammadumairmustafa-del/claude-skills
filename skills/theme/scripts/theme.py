#!/usr/bin/env python3
"""Pick and export palettes from Sanzo Wada's A Dictionary of Color Combinations.

Commands
  show N [N ...]          print combination(s) by number (1-348)
  color NAME              every combination that uses a colour (fuzzy name match)
  find [filters]          rank combinations by mood/size/hex closeness
  tokens N [--dark] [--format css|tailwind|json|scss] [--prefix p]
                          assign UI roles with WCAG contrast checks and export tokens
  colors                  list all 159 colours

find filters (all optional, combine freely):
  --mood warm cool muted vivid pastel light dark earthy contrast soft
         (repeatable; e.g. --mood warm --mood muted)
  --size 2|3|4            number of colours in the combination
  --near "#hex"           favour combinations containing a colour close to this hex
  --has NAME              must include this colour (fuzzy)
  --limit N               default 8
"""
import argparse, colorsys, json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(HERE, "..", "data", "wada.json")))
COLORS = [dict(i=i, name=n, hex=h.lower(), cmyk=k, rgb=r) for i, (n, h, k, r) in enumerate(DATA["colors"])]
COMBOS = [dict(n=n + 1, ids=ids) for n, ids in enumerate(DATA["combos"])]


# ---------- colour maths ----------
def hex_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(rgb):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def hls(rgb):
    h, l, s = colorsys.rgb_to_hls(*(c / 255 for c in rgb))
    return h * 360, l, s


def lab(rgb):
    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (f(c) for c in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    t = lambda v: v ** (1 / 3) if v > 0.008856 else 7.787 * v + 16 / 116
    fx, fy, fz = t(x), t(y), t(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def dist(a, b):
    return math.dist(lab(a), lab(b))


def mix(rgb, target, t):
    return tuple(round(c + (d - c) * t) for c, d in zip(rgb, target))


def to_hex(rgb):
    return "#%02x%02x%02x" % tuple(rgb)


# ---------- lookup ----------
def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def find_color(q):
    nq = norm(q)
    exact = [c for c in COLORS if norm(c["name"]) == nq]
    if exact:
        return exact
    part = [c for c in COLORS if nq in norm(c["name"])]
    if part:
        return part
    sys.exit(f"No colour matches '{q}'. Run `theme.py colors` to list names.")


def combo_colors(n):
    if not 1 <= n <= 348:
        sys.exit("Combination numbers run from 1 to 348.")
    return [COLORS[i] for i in COMBOS[n - 1]["ids"]]


def describe(n):
    cs = combo_colors(n)
    lines = [f"No. {n:03d}  ({len(cs)} colours)"]
    for c in cs:
        k = c["cmyk"]
        lines.append(f"  {c['hex']}  rgb({', '.join(map(str, c['rgb']))})  C{k[0]} M{k[1]} Y{k[2]} K{k[3]}  {c['name']}")
    return "\n".join(lines)


# ---------- mood scoring ----------
def traits(n):
    cs = combo_colors(n)
    h = [hls(c["rgb"]) for c in cs]
    L = [x[1] for x in h]
    S = [x[2] for x in h]
    warm = sum(1 for (hu, l, s) in h if s > 0.15 and (hu < 70 or hu > 330)) / len(h)
    cool = sum(1 for (hu, l, s) in h if s > 0.15 and 150 < hu < 300) / len(h)
    lums = [lum(c["rgb"]) for c in cs]
    span = max(contrast(a["rgb"], b["rgb"]) for a in cs for b in cs)
    return dict(
        warm=warm, cool=cool,
        vivid=sum(S) / len(S) * (1 - abs(sum(L) / len(L) - 0.5)),
        muted=1 - sum(S) / len(S),
        pastel=sum(1 for l, s in zip(L, S) if l > 0.72) / len(L),
        light=sum(lums) / len(lums),
        dark=1 - sum(lums) / len(lums),
        earthy=sum(1 for (hu, l, s) in h if 15 < hu < 75 and 0.15 < s < 0.65 and 0.2 < l < 0.6) / len(h),
        contrast=min(span / 12, 1),
        soft=1 - min(span / 12, 1),
    )


def cmd_find(a):
    pool = [c["n"] for c in COMBOS]
    if a.size:
        pool = [n for n in pool if len(combo_colors(n)) == a.size]
    if a.has:
        want = {c["i"] for c in find_color(a.has)}
        pool = [n for n in pool if want & set(COMBOS[n - 1]["ids"])]
    scored = []
    near = hex_rgb(a.near) if a.near else None
    for n in pool:
        t = traits(n)
        s = sum(t[m] for m in a.mood) if a.mood else 0
        if near:
            s += max(0, 1 - min(dist(near, c["rgb"]) for c in combo_colors(n)) / 40) * 2
        scored.append((s, n))
    scored.sort(key=lambda x: (-x[0], x[1]))
    for s, n in scored[: a.limit]:
        print(describe(n))
        print()


# ---------- role assignment ----------
def roles(n, dark=False):
    """Map a combination onto UI roles, keeping every original colour intact
    and deriving only what is missing for legible text."""
    cs = combo_colors(n)
    by_l = sorted(cs, key=lambda c: lum(c["rgb"]), reverse=not dark)
    base = by_l[0]
    # A page background has to be genuinely light (or dark). If the combination
    # has no such colour, tint/shade its lightest (darkest) one, and keep every
    # original colour available as text or accent.
    ok_bg = lum(base["rgb"]) >= 0.45 if not dark else lum(base["rgb"]) <= 0.03
    if ok_bg:
        bg_rgb, bg_src, rest = base["rgb"], base["name"], by_l[1:]
    else:
        far = (250, 249, 246) if not dark else (14, 14, 16)
        t, bg_rgb = 0.0, base["rgb"]
        while (lum(bg_rgb) < 0.6 if not dark else lum(bg_rgb) > 0.015) and t < 0.97:
            t += 0.03
            bg_rgb = mix(base["rgb"], far, t)
        bg_src, rest = f"{'tint' if not dark else 'shade'} of {base['name']}", by_l
    # text: the combo colour with the best contrast on bg, if it reaches 4.5:1
    best = max(rest, key=lambda c: contrast(c["rgb"], bg_rgb))
    if contrast(best["rgb"], bg_rgb) >= 4.5:
        text = (best["hex"], best["name"])
        rest = [c for c in rest if c is not best]
    else:
        # derive an ink from the strongest colour so it still belongs to the palette
        src = best
        target = (0, 0, 0) if not dark else (255, 255, 255)
        t, ink = 0.0, src["rgb"]
        while contrast(ink, bg_rgb) < 7 and t < 1:
            t = min(1, t + 0.05)
            ink = mix(src["rgb"], target, t)
        text = (to_hex(ink), f"{'shade' if not dark else 'tint'} of {src['name']}")
    out = {"background": (to_hex(bg_rgb), bg_src), "text": text}
    # surface = cards/panels: lighter than the page in light mode, slightly raised in dark mode
    surf = mix(bg_rgb, (255, 255, 255), 0.45 if not dark else 0.07)
    out["surface"] = (to_hex(surf), f"surface from {bg_src}")
    # accents ordered by visual weight (saturation x distance from bg)
    rest.sort(key=lambda c: -(hls(c["rgb"])[2] + contrast(c["rgb"], bg_rgb) / 10))
    for k, c in enumerate(rest):
        out["accent" if k == 0 else f"accent-{k + 1}"] = (c["hex"], c["name"])
    # what to put on top of the main accent
    if "accent" in out:
        a = hex_rgb(out["accent"][0])
        on = max([hex_rgb(out["background"][0]), hex_rgb(text[0]), (255, 255, 255), (17, 17, 17)],
                 key=lambda x: contrast(x, a))
        out["on-accent"] = (to_hex(on), "best contrast on accent")
    return out


def cmd_tokens(a):
    r = roles(a.n, a.dark)
    p = a.prefix
    tb, tt = hex_rgb(r["background"][0]), hex_rgb(r["text"][0])
    checks = [f"text on background {contrast(tt, tb):.1f}:1"]
    if "accent" in r:
        ac = hex_rgb(r["accent"][0])
        checks.append(f"accent on background {contrast(ac, tb):.1f}:1"
                      + ("" if contrast(ac, tb) >= 3 else "  (below 3:1: use for fills, not text or thin lines)"))
        checks.append(f"on-accent on accent {contrast(hex_rgb(r['on-accent'][0]), ac):.1f}:1")
    if a.format == "json":
        print(json.dumps({"combination": a.n, "mode": "dark" if a.dark else "light",
                          "roles": {k: {"hex": v[0], "source": v[1]} for k, v in r.items()},
                          "contrast": checks}, indent=2))
        return
    print(f"/* Wada No. {a.n:03d} · {'dark' if a.dark else 'light'} · " + "; ".join(checks) + " */")
    if a.format == "css":
        print(":root {")
        for k, (h, src) in r.items():
            print(f"  --{p}{k}: {h}; /* {src} */")
        print("}")
    elif a.format == "scss":
        for k, (h, src) in r.items():
            print(f"${p}{k}: {h}; // {src}")
    elif a.format == "tailwind":
        print("// tailwind.config.js -> theme.extend.colors")
        print("colors: {")
        for k, (h, src) in r.items():
            print(f"  '{p}{k}': '{h}', // {src}")
        print("}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("show"); s.add_argument("n", type=int, nargs="+")
    s = sp.add_parser("color"); s.add_argument("name", nargs="+")
    sp.add_parser("colors")
    s = sp.add_parser("find")
    s.add_argument("--mood", action="append", default=[],
                   choices=["warm", "cool", "muted", "vivid", "pastel", "light", "dark", "earthy", "contrast", "soft"])
    s.add_argument("--size", type=int, choices=[2, 3, 4])
    s.add_argument("--near"); s.add_argument("--has"); s.add_argument("--limit", type=int, default=8)
    s = sp.add_parser("tokens"); s.add_argument("n", type=int)
    s.add_argument("--dark", action="store_true")
    s.add_argument("--format", default="css", choices=["css", "tailwind", "json", "scss"])
    s.add_argument("--prefix", default="")
    a = ap.parse_args()

    if a.cmd == "show":
        print("\n\n".join(describe(n) for n in a.n))
    elif a.cmd == "colors":
        for c in COLORS:
            k = c["cmyk"]
            uses = sum(1 for x in COMBOS if c["i"] in x["ids"])
            print(f"{c['hex']}  C{k[0]} M{k[1]} Y{k[2]} K{k[3]}  {c['name']}  ({uses} combos)")
    elif a.cmd == "color":
        for c in find_color(" ".join(a.name)):
            ns = [x["n"] for x in COMBOS if c["i"] in x["ids"]]
            print(f"{c['name']} {c['hex']} appears in {len(ns)} combinations:\n")
            print("\n\n".join(describe(n) for n in ns))
            print()
    elif a.cmd == "find":
        cmd_find(a)
    elif a.cmd == "tokens":
        cmd_tokens(a)


if __name__ == "__main__":
    main()
