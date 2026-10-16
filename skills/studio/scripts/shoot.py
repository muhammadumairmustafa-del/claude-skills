#!/usr/bin/env python3
"""Screenshot a page at mobile/tablet/desktop widths (light + dark, optional RTL) and run audit.js on each.

  shoot.py <url-or-file> [--out DIR] [--widths 375,768,1440] [--no-dark] [--rtl] [--full]

Prints a compact audit per viewport and the screenshot paths. Needs Python Playwright
(`pip install playwright && playwright install chromium`).
"""
import argparse, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--out", default="studio-shots")
    ap.add_argument("--widths", default="375,768,1440")
    ap.add_argument("--no-dark", action="store_true")
    ap.add_argument("--rtl", action="store_true", help="also render with <html dir=rtl>")
    ap.add_argument("--full", action="store_true", help="full-page screenshots")
    a = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("Playwright missing: pip install playwright && playwright install chromium")

    url = a.target
    if "://" not in url:
        url = Path(url).resolve().as_uri()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    audit = (HERE / "audit.js").read_text()
    schemes = ["light"] + ([] if a.no_dark else ["dark"])
    dirs = ["ltr"] + (["rtl"] if a.rtl else [])

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w in [int(x) for x in a.widths.split(",")]:
            for scheme in schemes:
                for d in dirs:
                    ctx = browser.new_context(viewport={"width": w, "height": 900 if w > 500 else 812},
                                              color_scheme=scheme, device_scale_factor=1,
                                              is_mobile=w < 500, has_touch=w < 500)
                    page = ctx.new_page()
                    errors = []
                    page.on("pageerror", lambda e: errors.append(str(e)))
                    page.goto(url, wait_until="networkidle")
                    if d == "rtl":
                        page.evaluate("document.documentElement.dir='rtl'")
                    page.wait_for_timeout(600)
                    name = f"{w}-{scheme}{'-rtl' if d == 'rtl' else ''}.png"
                    page.screenshot(path=str(out / name), full_page=a.full)
                    report = page.evaluate(audit)
                    if errors:
                        report["jsErrors"] = errors[:5]
                    # keep output short: drop empty lists
                    report = {k: v for k, v in report.items() if v not in ([], None)}
                    print(f"== {name}")
                    print(json.dumps(report, ensure_ascii=False, indent=1))
                    ctx.close()
        browser.close()
    print(f"\nscreenshots in {out.resolve()}")


if __name__ == "__main__":
    main()
