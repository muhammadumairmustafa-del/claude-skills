#!/usr/bin/env python3
"""Build the full logo pack + mockups for a chosen concept, all from the SAME source paths.

  pack.py --icon icon.svg --wordmark wordmark.svg --brand "Falak" \
          --primary "#0B1026" --accent "#F4C95D" --background "#F7F3EA" \
          [--inverse-icon icon-inverse.svg --inverse-wordmark wordmark-inverse.svg] \
          [--tagline "Read the sky"] [--domain falak.app] [--out pack/]

Inputs: icon.svg (symbol only, square-ish) and wordmark.svg (outlined text, no <text>).
If no inverse files are given, inverse versions are made automatically: every colour that is
under 3:1 on --primary becomes white (accents that already work are kept).
App icon: --app-bg "#0B1026" gives a dark tile (inverse mark is used automatically),
--app-scale sets how much of the tile the mark fills, --app-icon uses a hand-made tile instead.
--font sets the mockup text font (Google Font) so mockups match the brand.

Outputs (in --out):
  svg/   icon, wordmark, lockup-horizontal, lockup-stacked, each in colour / black / white / inverse
  png/   icon 16-1024, lockups @1x/@2x, app-icon-1024, apple-touch-icon-180, android-512,
         social-avatar-400, og-image-1200x630
  favicon.ico (16/32/48)
  mockups/ business-card, app-homescreen, website-header, social-profile, signage  (.png)
  index.html  brand sheet: all versions, clear space, min sizes, colours, usage notes
"""
import argparse, base64, html, io, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from recolour import auto_inverse, lum, mono  # noqa: E402


def read_svg(p):
    return read_svg_text(Path(p).read_text(), str(p))


def read_svg_text(s, name="svg"):
    s = re.sub(r"<\?xml[^>]*>|<!DOCTYPE[^>]*>", "", s).strip()
    m = re.search(r'viewBox="([^"]+)"', s)
    if not m:
        sys.exit(f"{name}: needs a viewBox")
    x, y, w, h = map(float, m.group(1).replace(",", " ").split())
    inner = re.sub(r"^<svg[^>]*>|</svg>\s*$", "", s, flags=re.S).strip()
    return {"vb": (x, y, w, h), "inner": inner}


def nest(svg, x, y, w, h):
    vx, vy, vw, vh = svg["vb"]
    return f'<svg x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" viewBox="{vx} {vy} {vw} {vh}">{svg["inner"]}</svg>'


def wrap(body, w, h, bg=None):
    rect = f'<rect width="{w:.2f}" height="{h:.2f}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}">{rect}{body}</svg>\n'


def lockup_h(icon, word, icon_h=100):
    """Icon left, wordmark right. Wordmark cap-height ~ 55% of icon height, gap = 30% of icon."""
    iw = icon_h * icon["vb"][2] / icon["vb"][3]
    wh = icon_h * 0.55
    ww = wh * word["vb"][2] / word["vb"][3]
    gap = icon_h * 0.30
    W, H = iw + gap + ww, icon_h
    return wrap(nest(icon, 0, 0, iw, icon_h) + nest(word, iw + gap, (H - wh) / 2, ww, wh), W, H)


def lockup_v(icon, word, icon_h=100):
    iw = icon_h * icon["vb"][2] / icon["vb"][3]
    ww = max(iw * 1.6, icon_h * 1.4)
    wh = ww * word["vb"][3] / word["vb"][2]
    if wh > icon_h * 0.45:
        wh = icon_h * 0.45; ww = wh * word["vb"][2] / word["vb"][3]
    gap = icon_h * 0.22
    W = max(iw, ww); H = icon_h + gap + wh
    return wrap(nest(icon, (W - iw) / 2, 0, iw, icon_h) + nest(word, (W - ww) / 2, icon_h + gap, ww, wh), W, H)


def b64(s):
    return "data:image/svg+xml;base64," + base64.b64encode(s.encode()).decode()


def render_many(jobs, out_dir):
    """jobs: list of (svg_text, out_name, width_px, background or None)"""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch(); page = br.new_page()
        for svg, name, w, bg in jobs:
            page.set_content(f'<html><body style="margin:0;background:{bg or "transparent"}"><img id="i" src="{b64(svg)}" style="display:block;width:{w}px"></body></html>')
            page.wait_for_load_state("networkidle")
            page.locator("#i").screenshot(path=str(out_dir / name), omit_background=bg is None)
        br.close()


def padded_square(icon_svg, size, bg, pad_ratio, radius=0):
    """pad_ratio = empty margin on each side as a fraction of the tile (0.19 -> mark fills 62%)."""
    icon = read_svg_text(icon_svg)
    vw, vh = icon["vb"][2], icon["vb"][3]
    inner = size * (1 - 2 * pad_ratio)
    if vw >= vh: w, h = inner, inner * vh / vw
    else: w, h = inner * vw / vh, inner
    rect = f'<rect width="{size}" height="{size}" rx="{radius}" fill="{bg}"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">{rect}{nest(icon, (size-w)/2, (size-h)/2, w, h)}</svg>'


MOCK_CSS = """
*{box-sizing:border-box}body{margin:0;padding:40px;background:#d9d6cf;font-family:-apple-system,Helvetica,sans-serif;display:flex;flex-direction:column;gap:40px;align-items:flex-start}
.mock{position:relative;overflow:hidden}
img{display:block}
"""


def mockups_html(c):
    p, a, bg = c["primary"], c["accent"], c["background"]
    icon, inv_icon, lock, inv_lock, stack = c["icon"], c["inv_icon"], c["lock"], c["inv_lock"], c["stack"]
    brand, tag, dom = html.escape(c["brand"]), html.escape(c["tagline"]), html.escape(c["domain"])
    font_link = f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={c["font"].replace(" ", "+")}:wght@400;600;700&display=block">' if c["font"] else ""
    font_css = f"body,body *{{font-family:'{c['font']}',-apple-system,Helvetica,sans-serif}}" if c["font"] else ""
    return f"""<!doctype html><html><head><meta charset="utf-8">{font_link}<style>{MOCK_CSS}{font_css}</style></head><body>
<div class="mock" id="business-card" style="width:1200px;height:700px;background:#cfcabf;display:flex;gap:60px;align-items:center;justify-content:center">
  <div style="width:525px;height:300px;background:{bg};border-radius:10px;box-shadow:0 30px 60px rgba(0,0,0,.25);display:flex;align-items:center;justify-content:center;transform:rotate(-4deg)">
    <img src="{b64(stack)}" style="height:150px"></div>
  <div style="width:525px;height:300px;background:{p};border-radius:10px;box-shadow:0 30px 60px rgba(0,0,0,.25);padding:34px;display:flex;flex-direction:column;justify-content:space-between;transform:rotate(3deg)">
    <img src="{b64(inv_icon)}" style="height:54px;width:auto;align-self:flex-start">
    <div style="color:#fff;font-size:15px;line-height:1.6;opacity:.92"><b style="font-size:19px">Your Name</b><br>Founder<br>hello@{dom}<br><span style="color:{a}">{dom}</span></div></div>
</div>
<div class="mock" id="app-homescreen" style="width:700px;height:900px;background:linear-gradient(160deg,#2b3550,#7a5c7e 60%,#e0a96d);display:flex;align-items:center;justify-content:center">
  <div style="width:380px;height:780px;border-radius:56px;background:rgba(0,0,0,.25);border:10px solid #111;padding:70px 28px;display:grid;grid-template-columns:repeat(4,1fr);gap:26px 18px;align-content:start">
    {''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:6px"><div style="width:62px;height:62px;border-radius:15px;overflow:hidden;background:rgba(255,255,255,{0.18 if i!=5 else 0})">' + (f'<img src="{b64(c["app_icon"])}" style="width:62px;height:62px;border-radius:15px">' if i==5 else '') + f'</div><span style="color:#fff;font-size:11px">{brand if i==5 else "App"}</span></div>' for i in range(16))}
  </div></div>
<div class="mock" id="website-header" style="width:1440px;height:560px;background:{bg}">
  <div style="height:110px;display:flex;align-items:center;justify-content:space-between;padding:0 56px;border-bottom:1px solid rgba(0,0,0,.08)">
    <img src="{b64(lock)}" style="height:52px"><div style="display:flex;gap:34px;align-items:center;color:{p};font-size:15px">
    <span>Product</span><span>Pricing</span><span>About</span><span style="background:{p};color:#fff;padding:8px 18px;border-radius:999px">Get started</span></div></div>
  <div style="padding:90px 56px;color:{p}"><div style="font-size:64px;font-weight:700;letter-spacing:-.03em;max-width:900px;line-height:1.05">{tag or brand}</div>
  <div style="margin-top:18px;font-size:20px;opacity:.7">{dom}</div></div></div>
<div class="mock" id="social-profile" style="width:1000px;height:560px;background:#fff">
  <div style="height:250px;background:{p};display:flex;align-items:center;justify-content:flex-end;padding-right:60px"><img src="{b64(inv_lock)}" style="height:60px"></div>
  <div style="position:absolute;left:50px;top:170px;width:160px;height:160px;border-radius:50%;border:6px solid #fff;overflow:hidden"><img src="{b64(c['avatar'])}" style="width:100%;height:100%"></div>
  <div style="padding:100px 50px 0;color:#111"><div style="font-size:28px;font-weight:700">{brand}</div><div style="color:#666;margin-top:4px">@{brand.lower().replace(' ','')} · {dom}</div></div></div>
<div class="mock" id="signage" style="width:1200px;height:700px;background:linear-gradient(#bfb8ab,#8f877a);display:flex;align-items:center;justify-content:center">
  <div style="width:860px;height:300px;background:{p};border-radius:6px;box-shadow:0 40px 80px rgba(0,0,0,.35),inset 0 0 0 10px rgba(255,255,255,.06);display:flex;align-items:center;justify-content:center">
    <img src="{b64(inv_lock)}" style="height:120px"></div></div>
</body></html>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--icon", required=True); ap.add_argument("--wordmark", required=True)
    ap.add_argument("--inverse-icon"); ap.add_argument("--inverse-wordmark")
    ap.add_argument("--brand", required=True); ap.add_argument("--tagline", default=""); ap.add_argument("--domain", default="")
    ap.add_argument("--primary", required=True); ap.add_argument("--accent", default=None); ap.add_argument("--background", default="#FFFFFF")
    ap.add_argument("--app-bg", help="app icon / avatar background colour (default --background). Use the brand's dark colour for a dark tile")
    ap.add_argument("--app-variant", choices=["auto", "colour", "inverse"], default="auto", help="which icon goes on the tile; auto = inverse on dark tiles")
    ap.add_argument("--app-scale", type=float, default=0.62, help="share of the tile the mark fills (0.5-0.75)")
    ap.add_argument("--app-icon", help="hand-made 1024 tile SVG; overrides the generated app icon")
    ap.add_argument("--font", default="", help="Google Font for mockup text, e.g. 'Plus Jakarta Sans'")
    ap.add_argument("--out", default="pack")
    a = ap.parse_args()
    a.accent = a.accent or a.primary
    a.domain = a.domain or re.sub(r"\W", "", a.brand.lower()) + ".com"
    out = Path(a.out); (out / "svg").mkdir(parents=True, exist_ok=True); (out / "png").mkdir(exist_ok=True); (out / "mockups").mkdir(exist_ok=True)

    icon_t, word_t = Path(a.icon).read_text(), Path(a.wordmark).read_text()
    inv_icon_t = Path(a.inverse_icon).read_text() if a.inverse_icon else auto_inverse(icon_t, a.primary)
    inv_word_t = Path(a.inverse_wordmark).read_text() if a.inverse_wordmark else auto_inverse(word_t, a.primary)

    variants = {"colour": (icon_t, word_t), "inverse": (inv_icon_t, inv_word_t),
                "black": (mono(icon_t, "#000000"), mono(word_t, "#000000")),
                "white": (mono(icon_t, "#FFFFFF"), mono(word_t, "#FFFFFF"))}
    files = {}
    for v, (it, wt) in variants.items():
        i, w = read_svg_text(it), read_svg_text(wt)
        files[f"icon-{v}"] = it; files[f"wordmark-{v}"] = wt
        files[f"lockup-horizontal-{v}"] = lockup_h(i, w); files[f"lockup-stacked-{v}"] = lockup_v(i, w)
    for k, s in files.items():
        (out / "svg" / f"{k}.svg").write_text(s)

    app_bg = a.app_bg or a.background
    dark_tile = lum(app_bg) < 0.2
    tile_icon = inv_icon_t if (a.app_variant == "inverse" or (a.app_variant == "auto" and dark_tile)) else icon_t
    pad = (1 - a.app_scale) / 2
    app_icon = Path(a.app_icon).read_text() if a.app_icon else padded_square(tile_icon, 1024, app_bg, pad, 0)
    avatar = padded_square(tile_icon, 400, app_bg, pad + 0.04)
    lh = read_svg_text(files["lockup-horizontal-inverse"]); lw = 640; lhh = lw * lh["vb"][3] / lh["vb"][2]
    if lhh > 220: lhh = 220; lw = lhh * lh["vb"][2] / lh["vb"][3]
    og = wrap(nest(lh, (1200 - lw) / 2, (630 - lhh) / 2, lw, lhh), 1200, 630, a.primary)

    jobs = [(icon_t, f"icon-{s}.png", s, None) for s in (16, 32, 48, 64, 128, 256, 512, 1024)]
    for v in ("colour", "inverse", "black", "white"):
        for k in ("lockup-horizontal", "lockup-stacked"):
            jobs += [(files[f"{k}-{v}"], f"{k}-{v}@1x.png", 600, None), (files[f"{k}-{v}"], f"{k}-{v}@2x.png", 1200, None)]
    jobs += [(app_icon, "app-icon-1024.png", 1024, None), (padded_square(tile_icon, 180, app_bg, pad, 0), "apple-touch-icon-180.png", 180, None),
             (padded_square(tile_icon, 512, app_bg, max(pad, 0.28)), "android-maskable-512.png", 512, None),
             (avatar, "social-avatar-400.png", 400, None), (og, "og-image-1200x630.png", 1200, None)]
    render_many(jobs, out / "png")

    from PIL import Image
    big = Image.open(out / "png" / "icon-256.png").convert("RGBA")
    big.save(out / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

    (out / "svg" / "app-icon.svg").write_text(app_icon)
    ctx = dict(font=a.font, primary=a.primary, accent=a.accent, background=a.background, brand=a.brand, tagline=a.tagline, domain=a.domain,
               icon=icon_t, inv_icon=inv_icon_t, lock=files["lockup-horizontal-colour"], inv_lock=files["lockup-horizontal-inverse"],
               stack=files["lockup-stacked-colour"], app_icon=app_icon, avatar=avatar)
    mh = out / "mockups" / "mockups.html"; mh.write_text(mockups_html(ctx))
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch(); page = br.new_page(viewport={"width": 1600, "height": 1000}, device_scale_factor=1.5)
        page.goto(mh.resolve().as_uri()); page.wait_for_load_state("networkidle")
        for el in page.locator(".mock").all():
            el.screenshot(path=str(out / "mockups" / f"{el.get_attribute('id')}.png"))
        br.close()

    # brand sheet
    def tile(name, bg):
        return f'<figure><div class="t" style="background:{bg}"><img src="svg/{name}.svg"></div><figcaption>{name}</figcaption></figure>'
    tiles = "".join(tile(f"{k}-{v}", {"colour": "#fff", "inverse": a.primary, "black": "#fff", "white": "#222"}[v])
                    for v in ("colour", "inverse", "black", "white") for k in ("lockup-horizontal", "lockup-stacked", "icon", "wordmark"))
    sw = "".join(f'<div class="sw"><span style="background:{c}"></span>{n}<br><code>{c}</code></div>' for n, c in (("Primary", a.primary), ("Accent", a.accent), ("Background", a.background)))
    mocks = "".join(f'<img class="m" src="mockups/{m}.png">' for m in ("business-card", "app-homescreen", "website-header", "social-profile", "signage"))
    (out / "index.html").write_text(f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(a.brand)} brand kit</title><link rel="icon" href="favicon.ico"><style>
body{{margin:0;font:15px/1.5 -apple-system,Helvetica,sans-serif;background:#f5f4f0;color:#18181b}}main{{max-width:1200px;margin:auto;padding:40px 16px}}
h1{{font-size:36px;margin:0 0 4px}}h2{{margin:40px 0 14px}}.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}}
figure{{margin:0}}.t{{height:170px;border-radius:12px;display:flex;align-items:center;justify-content:center;padding:28px;border:1px solid #e4e2dc}}
.t img{{max-width:100%;max-height:100%}}figcaption{{font-size:12px;color:#666;margin-top:6px}}
.sw{{display:inline-block;margin-right:28px}}.sw span{{display:block;width:120px;height:80px;border-radius:10px;margin-bottom:6px;border:1px solid #ddd}}
.m{{width:100%;border-radius:12px;margin-bottom:16px}}ul{{padding-left:18px}}</style></head><body><main>
<h1>{html.escape(a.brand)}</h1><p>{html.escape(a.tagline)}</p>
<h2>Logo versions</h2><div class="g">{tiles}</div>
<h2>Colours</h2>{sw}
<h2>Usage</h2><ul><li>Clear space: keep at least the height of the icon × 0.5 empty around the logo.</li>
<li>Minimum size: icon 16 px; horizontal lockup 100 px wide (screen) / 25 mm (print).</li>
<li>Use the inverse or white version on dark or photographic backgrounds; never recolour the mark outside the palette, stretch, rotate, add effects or outline it.</li></ul>
<h2>Mockups</h2>{mocks}
<h2>Files</h2><p><code>svg/</code> vector masters · <code>png/</code> raster exports · <code>favicon.ico</code></p>
</main></body></html>""")
    print(out / "index.html")


if __name__ == "__main__":
    main()
