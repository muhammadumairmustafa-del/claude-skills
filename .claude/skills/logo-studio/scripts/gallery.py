#!/usr/bin/env python3
"""Build a self-contained HTML gallery from concepts.json (SVGs are inlined).

  gallery.py path/to/concepts.json [--out gallery.html] [--png gallery.png]

concepts.json shape (paths relative to the json file):
{
  "brand": "Falak", "tagline": "optional", "brief": "one-paragraph summary of the brief",
  "title": "optional heading, e.g. 'Falak — round 2: refining B2'",
  "themes": [{"id": "A", "name": "Celestial geometry", "mood": "precise, calm, nocturnal"}],
  "concepts": [{
    "id": "A1", "theme": "A", "name": "Orbit F", "archetype": "lettermark",
    "idea": "The F's crossbar is an orbit path ...",          # the concept in one or two sentences
    "why": "Reads at 16px; ownable; ...",                       # why it fits the brief
    "palette": ["#0B1026", "#F4C95D"], "fonts": ["Space Grotesk 700"],
    "files": {"primary": "concepts/a1.svg",                    # required: full logo (lockup)
              "icon": "concepts/a1-icon.svg",                   # optional: symbol only
              "inverse": "concepts/a1-inverse.svg",             # optional: version for dark bg (else automatic)
              "app": "concepts/a1-app.svg"}                     # optional: finished app tile (else generated)
  }]
}
"""
import argparse, html, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from recolour import auto_inverse, colours_in, lum  # noqa: E402


def inline_svg(p, text=None) -> str:
    s = text if text is not None else p.read_text()
    s = re.sub(r"<\?xml[^>]*>", "", s)
    s = re.sub(r"<!DOCTYPE[^>]*>", "", s)
    # make ids unique per inclusion so gradients/clipPaths don't collide across cards
    tag = re.sub(r"\W", "", p.stem)
    ids = set(re.findall(r'id="([^"]+)"', s))
    for i in ids:
        s = s.replace(f'id="{i}"', f'id="{tag}-{i}"').replace(f"#{i})", f"#{tag}-{i})").replace(f'"#{i}"', f'"#{tag}-{i}"')
    return s.strip()


CSS = """
:root{--bg:#f4f3ef;--card:#fff;--ink:#16161a;--muted:#6b6b72;--line:#e3e1db}
:root[data-theme=dark]{--bg:#0e0e11;--card:#17171c;--ink:#ececf0;--muted:#9a9aa3;--line:#2a2a31}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 Inter,-apple-system,Helvetica,sans-serif}
header{padding:40px 48px 24px;display:flex;justify-content:space-between;gap:24px;align-items:flex-start}
h1{font-size:34px;margin:0 0 6px;letter-spacing:-.02em}.brief{max-width:760px;color:var(--muted);margin:0}
button{font:inherit;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:999px;padding:8px 14px;cursor:pointer}
section{padding:8px 48px 36px}.theme h2{font-size:20px;margin:18px 0 2px}.theme p{margin:0 0 16px;color:var(--muted)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:20px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden}
.stage{display:grid;grid-template-columns:1fr 1fr}.stage>div{height:200px;display:flex;align-items:center;justify-content:center;padding:28px}
.stage .l{background:#fff}.stage .d{background:#111}
.stage svg{max-width:100%;max-height:100%;width:auto;height:auto}
.small{display:flex;gap:14px;align-items:center;padding:10px 16px;border-top:1px solid var(--line);background:var(--bg)}
.small svg{width:auto}.small .sp{flex:1}
.tile{width:56px;height:56px;border-radius:13px;display:flex;align-items:center;justify-content:center;box-shadow:0 1px 3px rgba(0,0,0,.25);overflow:hidden}
.tile svg{width:64%;height:64%}.tile.full svg{width:100%;height:100%}
.meta{padding:14px 16px 18px}.meta h3{margin:0;font-size:16px}.tag{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
.meta p{margin:6px 0 0;font-size:14px}.why{color:var(--muted)}
.chips{display:flex;gap:6px;margin-top:10px;flex-wrap:wrap;align-items:center}.chip{width:22px;height:22px;border-radius:6px;border:1px solid var(--line)}
.fonts{font-size:12px;color:var(--muted);margin-left:6px}
@media(max-width:600px){header,section{padding-left:16px;padding-right:16px}.grid{grid-template-columns:1fr}}
"""


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("concepts"); ap.add_argument("--out"); ap.add_argument("--png")
    a = ap.parse_args()
    src = Path(a.concepts); root = src.parent
    data = json.loads(src.read_text())
    out = Path(a.out) if a.out else root / "gallery.html"
    themes = data.get("themes") or [{"id": None, "name": "Concepts", "mood": ""}]
    parts = []
    for t in themes:
        cs = [c for c in data["concepts"] if t["id"] is None or c.get("theme") == t["id"]]
        if not cs:
            continue
        cards = []
        for c in cs:
            f = c["files"]
            ptxt = (root / f["primary"]).read_text()
            primary = inline_svg(root / f["primary"])
            inverse = inline_svg(root / f["inverse"]) if f.get("inverse") else inline_svg(root / (f["primary"] + "-auto"), auto_inverse(ptxt))
            itxt = (root / f["icon"]).read_text() if f.get("icon") else None
            if itxt:
                icon = inline_svg(root / f["icon"])
                small = "".join(icon.replace("<svg", f'<svg style="height:{s}px"', 1) for s in (16, 24, 32, 48))
            else:  # pure wordmark/emblem: show it at small widths instead of tiny heights
                small = "".join(primary.replace("<svg", f'<svg style="width:{w}px;height:auto"', 1) for w in (48, 72, 110))
            if f.get("app"):
                tile = f'<div class="tile full">{inline_svg(root / f["app"])}</div>'
            else:
                src = itxt or ptxt
                cols = colours_in(src) or ["#111111"]
                bg = min(cols, key=lum); bg = bg if lum(bg) < 0.25 else "#111111"
                tile = f'<div class="tile" style="background:{bg}">{inline_svg(root / ((f.get("icon") or f["primary"]) + "-tile"), auto_inverse(src, bg))}</div>'
            small += f'<span class="sp"></span>{tile}'
            chips = "".join(f'<span class="chip" style="background:{html.escape(p)}" title="{html.escape(p)}"></span>' for p in c.get("palette", []))
            fonts = f'<span class="fonts">{html.escape(" · ".join(c.get("fonts", [])))}</span>' if c.get("fonts") else ""
            cards.append(f"""<article class="card"><div class="stage"><div class="l">{primary}</div><div class="d">{inverse}</div></div>
<div class="small">{small}</div><div class="meta"><span class="tag">{html.escape(c.get('id',''))} · {html.escape(c.get('archetype',''))}</span>
<h3>{html.escape(c.get('name',''))}</h3><p>{html.escape(c.get('idea',''))}</p><p class="why">{html.escape(c.get('why',''))}</p>
<div class="chips">{chips}{fonts}</div></div></article>""")
        head = f'<div class="theme"><h2>{html.escape((t["id"] + " · ") if t["id"] else "")}{html.escape(t["name"])}</h2><p>{html.escape(t.get("mood",""))}</p></div>'
        parts.append(f"<section>{head}<div class='grid'>{''.join(cards)}</div></section>")
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(data.get('title') or (data.get('brand','Logo') + ' logo concepts'))}</title><style>{CSS}</style></head><body>
<header><div><h1>{html.escape(data.get('title') or (data.get('brand','') + ' — logo concepts'))}</h1><p class="brief">{html.escape(data.get('brief',''))}</p></div>
<button onclick="var r=document.documentElement;r.dataset.theme=r.dataset.theme==='dark'?'light':'dark'">Light / dark</button></header>
{''.join(parts)}</body></html>"""
    out.write_text(doc)
    print(out)
    if a.png:
        import subprocess, sys
        subprocess.run([sys.executable, str(Path(__file__).with_name("render.py")), "shot", str(out), "--out", a.png, "--width", "1440"], check=True)


if __name__ == "__main__":
    main()
