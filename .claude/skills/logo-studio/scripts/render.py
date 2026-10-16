#!/usr/bin/env python3
"""Render logo SVGs with headless Chromium (Playwright).

Subcommands
  png    SVG -> PNG at one or more pixel widths
         render.py png logo.svg --sizes 1024 512 64 --out-dir exports/
  proof  Proof sheet, one row per concept. LOOK at it before presenting anything.
         render.py proof concepts/*.svg --out proof.png [--black]
         Columns: light 16/32/64/160 · dark (uses <stem>-inverse.svg if present, else an
         automatic inverse marked 'auto') · app tile (<stem>-icon.svg or the mark, inverse, on a
         squircle in the concept's darkest colour; <stem>-app.svg overrides) · silhouette · squint ·
         mirror/180°. Files ending -inverse/-icon/-app/-black are used as partners, not rows.
         --black: black-first drafts; dark column shows the mark in white.
  shot   Screenshot an HTML file (gallery, mockups) to PNG
         render.py shot gallery.html --out gallery.png --width 1440
"""
import argparse, base64, html, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from recolour import auto_inverse, colours_in, lum, mono  # noqa: E402

PARTNER = re.compile(r"-(inverse|icon|icon-inverse|app|black|white|mono)$")


def _browser():
    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
    return pw, pw.chromium.launch()


def uri_text(s: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(s.encode()).decode()


def svg_data_uri(path: Path) -> str:
    return uri_text(path.read_text())


def cmd_png(a):
    pw, br = _browser()
    page = br.new_page(device_scale_factor=1)
    out_dir = Path(a.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    for f in map(Path, a.svgs):
        for w in a.sizes:
            bg = a.background or "transparent"
            page.set_content(
                f'<html><body style="margin:0;background:{bg}">'
                f'<img id="i" src="{svg_data_uri(f)}" style="display:block;width:{w}px;height:auto"></body></html>')
            page.wait_for_load_state("networkidle")
            target = out_dir / f"{f.stem}-{w}.png"
            page.locator("#i").screenshot(path=str(target), omit_background=(bg == "transparent"))
            print(target)
    br.close(); pw.stop()


PROOF_CSS = """
body{margin:0;font:13px/1.3 -apple-system,Helvetica,sans-serif;background:#e9e9e6;color:#222}
.row,.hdr{display:grid;grid-template-columns:130px minmax(0,1fr) minmax(0,1fr) 120px 110px 110px 150px}
.row{border-bottom:1px solid #ccc}.hdr{font-weight:600;background:#ddd}.hdr div{padding:6px 10px}
.lbl{padding:10px;font-weight:600;word-break:break-word}.lbl small{display:block;font-weight:400;color:#777;margin-top:4px}
.cell{display:flex;align-items:flex-end;gap:16px;padding:14px;overflow:hidden;min-width:0;position:relative}
.cell img{object-fit:contain;object-position:left bottom}
.light{background:#fff}.dark{background:#111}.dark .tag{position:absolute;top:4px;right:6px;color:#888;font-size:10px}
.tile{background:#f2f2f2;align-items:center;justify-content:center}
.tile .t{width:84px;height:84px;border-radius:19px;display:flex;align-items:center;justify-content:center;box-shadow:0 1px 3px rgba(0,0,0,.2)}
.tile .t img{width:62%;height:62%;object-position:center}
.sil,.squint,.flip{background:#fff}.sil img,.flip img{filter:brightness(0)}.squint img{filter:brightness(0) blur(3px)}
.flip{gap:10px}
"""


def cmd_proof(a):
    sizes = [16, 32, 64, 160]
    caps = {16: 10, 32: 16, 64: 24, 160: 36}  # max share of the cell width, so wide wordmarks still fit
    files = [Path(f) for f in a.svgs]
    rows_files = [f for f in files if not PARTNER.search(f.stem)] or files
    rows = []
    for f in rows_files:
        txt = f.read_text()
        sib = lambda suf: f.with_name(f"{f.stem}-{suf}.svg")
        if a.black:
            dark_txt, tag = mono(txt, "#FFFFFF"), "white"
        elif sib("inverse").exists():
            dark_txt, tag = sib("inverse").read_text(), "inverse"
        else:
            dark_txt, tag = auto_inverse(txt), "auto"
        icon_txt = sib("icon").read_text() if sib("icon").exists() else txt
        if sib("app").exists():
            tile = f'<div class="t" style="background:none;box-shadow:none"><img src="{uri_text(sib("app").read_text())}" style="width:100%;height:100%"></div>'
        else:
            cols = colours_in(icon_txt) or ["#111111"]
            darkest = min(cols, key=lum)
            tile_bg = darkest if lum(darkest) < 0.25 else "#111111"
            inv_icon = sib("icon-inverse").read_text() if sib("icon-inverse").exists() else auto_inverse(icon_txt, tile_bg)
            tile = f'<div class="t" style="background:{tile_bg}"><img src="{uri_text(inv_icon)}"></div>'
        u, ud = uri_text(txt), uri_text(dark_txt)
        light = "".join(f'<img src="{u}" style="height:{s}px;width:auto;max-width:{caps[s]}%">' for s in sizes)
        dark = "".join(f'<img src="{ud}" style="height:{s}px;width:auto;max-width:{caps[s]}%">' for s in sizes)
        partners = [p for p in ("inverse", "icon", "app") if sib(p).exists()]
        rows.append(
            f'<div class="row"><div class="lbl">{html.escape(f.stem)}<small>{", ".join(partners) or "no partner files"}</small></div>'
            f'<div class="cell light">{light}</div><div class="cell dark">{dark}<span class="tag">{tag}</span></div>'
            f'<div class="cell tile">{tile}</div>'
            f'<div class="cell sil"><img src="{u}" style="height:64px;width:auto;max-width:96px"></div>'
            f'<div class="cell squint"><img src="{u}" style="height:64px;width:auto;max-width:96px"></div>'
            f'<div class="cell flip"><img src="{u}" style="height:52px;width:auto;max-width:62px;transform:scaleX(-1)">'
            f'<img src="{u}" style="height:52px;width:auto;max-width:62px;transform:rotate(180deg)"></div></div>')
    doc = (f"<html><head><style>{PROOF_CSS}</style></head><body>"
           '<div class="hdr"><div>concept</div><div>light 16/32/64/160</div><div>dark 16/32/64/160</div><div>app tile</div>'
           '<div>silhouette</div><div>squint</div><div>mirror / 180°</div></div>' + "".join(rows) + "</body></html>")
    pw, br = _browser()
    page = br.new_page(viewport={"width": 1400, "height": 400})
    page.set_content(doc); page.wait_for_load_state("networkidle")
    page.screenshot(path=a.out, full_page=True)
    br.close(); pw.stop()
    print(a.out)


def cmd_shot(a):
    pw, br = _browser()
    page = br.new_page(viewport={"width": a.width, "height": a.height}, device_scale_factor=a.scale)
    page.goto(Path(a.html).resolve().as_uri()); page.wait_for_load_state("networkidle")
    page.wait_for_timeout(300)
    if a.selector:
        loc = page.locator(a.selector)
        for i in range(loc.count()):
            out = a.out if loc.count() == 1 else str(Path(a.out).with_name(f"{Path(a.out).stem}-{i+1}.png"))
            loc.nth(i).screenshot(path=out); print(out)
    else:
        page.screenshot(path=a.out, full_page=not a.viewport_only); print(a.out)
    br.close(); pw.stop()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("png"); p.add_argument("svgs", nargs="+"); p.add_argument("--sizes", type=int, nargs="+", default=[1024])
    p.add_argument("--out-dir", default="."); p.add_argument("--background", help="CSS colour; default transparent")
    p.set_defaults(fn=cmd_png)
    p = sp.add_parser("proof"); p.add_argument("svgs", nargs="+"); p.add_argument("--out", default="proof.png")
    p.add_argument("--black", action="store_true", help="black-first drafts: show white version in the dark column")
    p.set_defaults(fn=cmd_proof)
    p = sp.add_parser("shot"); p.add_argument("html"); p.add_argument("--out", required=True)
    p.add_argument("--width", type=int, default=1440); p.add_argument("--height", type=int, default=900)
    p.add_argument("--scale", type=float, default=1); p.add_argument("--selector", help="screenshot each matching element")
    p.add_argument("--viewport-only", action="store_true"); p.set_defaults(fn=cmd_shot)
    a = ap.parse_args(); a.fn(a)


if __name__ == "__main__":
    main()
