#!/usr/bin/env python3
"""Generate distinct design directions and remember which ones were used.

A direction = one option from each axis in data/axes.json. Options are weighted
by how well their tags match the brief, then candidates are chosen to be as
different as possible from each other AND from directions used on past projects
(data/history.json), so every new app starts from somewhere new.

  direction.py suggest --brief "astrology app for gen-z in KSA" --platform mobile [--mode persuade] [-n 3] [--seed 7] [--lock type=T3] [--wild 1]
  direction.py record --project "Falak" --code L9-T4-C10-S6-E3-M5-D1-I8-G13-V6 [--note "..."]
  direction.py history [--last 10]
  direction.py show CODE
  direction.py axes
"""
import argparse, json, math, random, re, sys, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AXES = json.loads((ROOT / "data" / "axes.json").read_text())
HIST = ROOT / "data" / "history.json"
ORDER = [a["id"] for a in AXES["axes"]]
BY_ID = {o["id"]: (a, o) for a in AXES["axes"] for o in a["options"]}

# Mode nudges: an "operate" app UI shouldn't get a scroll-film hero by default.
MODE_BIAS = {
    "operate":    {"tags": ["data", "trust", "technical", "calm"], "avoid": ["M4", "G3", "L14", "L5", "L4", "L3", "G7", "G14", "G15"]},
    "persuade":   {"tags": ["bold", "premium", "editorial"], "avoid": ["L7", "D3"]},
    "read":       {"tags": ["editorial", "calm"], "avoid": ["L7", "M3", "G3", "D3", "L8"]},
    "experience": {"tags": ["bold", "playful", "premium", "mystic"], "avoid": ["L7", "D3", "M1"]},
}


def load_hist():
    try:
        return json.loads(HIST.read_text())
    except Exception:
        return []


def brief_tags(brief):
    text = " " + (brief or "").lower() + " "
    tags = {}
    for tag, words in AXES["keywords"].items():
        for w in words:
            if re.search(r"\b" + re.escape(w) + r"\b", text):
                tags[tag] = tags.get(tag, 0) + 1
    return tags


def allowed(opt, platform, mode):
    if platform and opt.get("platforms") and platform not in opt["platforms"]:
        return False
    if mode and opt["id"] in MODE_BIAS.get(mode, {}).get("avoid", []):
        return False
    return True


def weight(opt, tags, mode):
    w = 1.0
    for t in opt.get("tags", []):
        if t in tags:
            w += 1.2 * min(tags[t], 2)
    if mode and set(opt.get("tags", [])) & set(MODE_BIAS[mode]["tags"]):
        w += 0.6
    return w


def conflicts(pick):
    ids = set(pick.values())
    for i in ids:
        for c in BY_ID[i][1].get("conflicts", []):
            if c in ids:
                return True
    return False


def sample(rng, tags, platform, mode, locks, wild_axes):
    pick = {}
    for axis in AXES["axes"]:
        aid = axis["id"]
        if aid in locks:
            pick[aid] = locks[aid]
            continue
        opts = [o for o in axis["options"] if allowed(o, platform, mode)] or axis["options"]
        if aid in wild_axes:  # deliberate surprise: ignore brief affinity
            ws = [1.0] * len(opts)
        else:
            ws = [weight(o, tags, mode) for o in opts]
        pick[aid] = rng.choices(opts, weights=ws)[0]["id"]
    return pick


def score(pick, tags, mode):
    return sum(math.log(weight(BY_ID[i][1], tags, mode)) for i in pick.values())


def dist(a, b):
    return sum(1 for k in ORDER if a.get(k) != b.get(k))


def code_of(pick):
    return "-".join(pick[k] for k in ORDER)


def parse_code(code):
    parts = code.strip().upper().split("-")
    pick = {}
    for p in parts:
        if p not in BY_ID:
            sys.exit(f"unknown option id {p!r}")
        pick[BY_ID[p][0]["id"]] = p
    return pick


def recent_usage(hist, n=15):
    """How often each option id appeared in the last n recorded projects."""
    use = {}
    for h in hist[-n:]:
        for i in h["code"].split("-"):
            use[i] = use.get(i, 0) + 1
    return use


def describe(pick, wild=()):
    lines = []
    for aid in ORDER:
        axis, o = BY_ID[pick[aid]]
        star = " (wildcard)" if aid in wild else ""
        extra = ""
        if aid == "type":
            fonts = ", ".join(o["fonts"])
            extra = f" — display: {fonts}" + (f"; body: {', '.join(o['body'])}" if o.get("body") else "")
        if aid == "color":
            size = o.get("size", 3)
            moods = " ".join(f"--mood {m}" for m in o["wada"])
            extra = f" — palette: `theme.py find {moods} --size {size}`"
        lines.append(f"  - **{axis['label']}**: {o['name']}{star}. {o['desc']}{extra}")
    return "\n".join(lines)


def nickname(pick, rng):
    a = BY_ID[pick["color"]][1]["name"].split()[0].strip(",").lower()
    b = BY_ID[pick["layout"]][1]["name"].split()[-1].lower()
    c = BY_ID[pick["signature"]][1]["name"].split()[0].lower()
    return f"{a}-{c}-{b}"


def cmd_suggest(args):
    rng = random.Random(args.seed)
    tags = brief_tags(args.brief)
    platform = {"ios": "mobile", "android": "mobile", "desktop": "web"}.get(args.platform, args.platform)
    mode = args.mode
    locks = {}
    for l in args.lock or []:
        k, v = l.split("=")
        locks[k] = v.upper()
    hist = load_hist()
    use = recent_usage(hist)
    past = [parse_code(h["code"]) for h in hist[-15:]]

    pool = []
    for _ in range(1500):
        free = [a for a in ORDER if a not in locks]
        wild = set(rng.sample(free, min(args.wild, len(free))))
        p = sample(rng, tags, platform, mode, locks, wild)
        if conflicts(p):
            continue
        fit = score(p, tags, mode)
        stale = sum(use.get(i, 0) for i in p.values())       # penalise over-used options
        novelty = min((dist(p, q) for q in past), default=len(ORDER))
        pool.append((fit - 0.35 * stale + 0.25 * novelty, p, wild))

    pool.sort(key=lambda t: -t[0])
    chosen = [pool[0]]
    for _ in range(args.n - 1):  # greedy max-min diversity among the good candidates
        best = max(pool[:400], key=lambda t: min(dist(t[1], c[1]) for c in chosen) * 10 + t[0])
        chosen.append(best)

    print(f"Brief tags detected: {', '.join(f'{k}×{v}' for k, v in tags.items()) or 'none (pure exploration)'}")
    print(f"Platform: {platform or 'any'} · Mode: {mode or 'unspecified'} · Past projects considered: {len(past)}\n")
    for n, (s, p, wild) in enumerate(chosen, 1):
        print(f"### Direction {n}: \"{nickname(p, rng)}\"")
        print(f"code: `{code_of(p)}`")
        print(describe(p, wild))
        print()
    print("Treat these as starting provocations, not specs: adapt any axis that fights the brief, and say why.")
    print("After the user picks, record it:  direction.py record --project NAME --code CODE")


def cmd_record(args):
    parse_code(args.code)
    hist = load_hist()
    hist.append({"project": args.project, "code": args.code.upper(), "note": args.note or "",
                 "date": datetime.date.today().isoformat()})
    HIST.write_text(json.dumps(hist, indent=1))
    print(f"recorded {args.project}: {args.code.upper()} ({len(hist)} projects in history)")


def cmd_history(args):
    hist = load_hist()
    if not hist:
        print("no projects recorded yet")
    for h in hist[-args.last:]:
        names = ", ".join(BY_ID[i][1]["name"] for i in h["code"].split("-")[:3])
        print(f"{h['date']}  {h['project']:<22} {h['code']}  ({names}) {h.get('note','')}")
    use = recent_usage(hist)
    if use:
        top = sorted(use.items(), key=lambda t: -t[1])[:8]
        print("\nmost-used recently: " + ", ".join(f"{BY_ID[i][1]['name']} ×{c}" for i, c in top))


def cmd_show(args):
    print(describe(parse_code(args.code)))


def cmd_axes(args):
    for a in AXES["axes"]:
        print(f"{a['id']} ({a['label']}): " + "; ".join(f"{o['id']} {o['name']}" for o in a["options"]))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("suggest")
    s.add_argument("--brief", default="")
    s.add_argument("--platform", choices=["web", "mobile", "ios", "android", "desktop"])
    s.add_argument("--mode", choices=list(MODE_BIAS))
    s.add_argument("-n", type=int, default=3)
    s.add_argument("--seed", type=int)
    s.add_argument("--lock", action="append", help="axis=OPTION, e.g. type=T3 (repeatable)")
    s.add_argument("--wild", type=int, default=1, help="axes per direction that ignore the brief (surprise)")
    r = sp.add_parser("record")
    r.add_argument("--project", required=True)
    r.add_argument("--code", required=True)
    r.add_argument("--note")
    h = sp.add_parser("history")
    h.add_argument("--last", type=int, default=20)
    sh = sp.add_parser("show")
    sh.add_argument("code")
    sp.add_parser("axes")
    args = ap.parse_args()
    {"suggest": cmd_suggest, "record": cmd_record, "history": cmd_history,
     "show": cmd_show, "axes": cmd_axes}[args.cmd](args)


if __name__ == "__main__":
    main()
