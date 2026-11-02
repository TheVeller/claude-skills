#!/usr/bin/env python3
"""
watchlist.py - local watchlist (replaces the Sandcastles watchlist) + feed reports.

Watchlist file (default /workspace/exports/bot-video/watchlist.json):
  {"channels": [{"platform": "youtube|tiktok|instagram", "handle": "@x",
                 "added": "YYYY-MM-DD", "note": ""}]}

Commands:
  list
  add    --platform tiktok --handle @x [--note "..."]
  remove --platform tiktok --handle @x
  pull   [--limit 40] [--outdir DIR]      free pull (yt-dlp) for youtube/tiktok;
                                          instagram entries are SKIPPED and
                                          listed with the paid Apify call + cost
  report --mode outliers|recent --scored scored.json
         [--days 7] [--limit 10|25] [--min-outlier 1.0]

`pull` writes DIR/<platform>_<handle>.json, then run outlier_score.py on them.
Outlier scores need ~90 days of history per channel, so pull enough videos
(limit 40-60), even though the report only shows the last 7 days.
"""
import argparse, json, os, subprocess, sys
from datetime import datetime, timezone, timedelta, date

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = "/workspace/exports/bot-video/watchlist.json"
IG_REEL_PRICE_FREE_TIER = 0.0026  # apify/instagram-reel-scraper, per reel, FREE tier, read 2026-10-29
IG_START = 0.001


def load(path):
    if not os.path.exists(path):
        return {"channels": []}
    return json.load(open(path, encoding="utf-8"))


def save(path, d):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(d, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)


def norm_handle(h):
    return h if h.startswith("http") else "@" + h.lstrip("@")


def abbr(n):
    if n is None:
        return "n/a"
    for div, s in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
        if n >= div:
            x = n / div
            return (f"{x:.1f}".rstrip("0").rstrip(".")) + s
    return str(int(n))


def parse_dt(s):
    s = (s or "").replace("Z", "+00:00")
    try:
        d = datetime.fromisoformat(s)
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def report(scored, mode, days, limit, min_outlier):
    vids = json.load(open(scored, encoding="utf-8"))["videos"]
    cut = datetime.now(timezone.utc) - timedelta(days=days)
    recent = [v for v in vids if parse_dt(v.get("published_at")) and parse_dt(v["published_at"]) >= cut]
    if mode == "outliers":
        rows = [v for v in recent if (v.get("outlier_score") or 0) >= min_outlier]
        rows.sort(key=lambda v: (-(v.get("outlier_score") or 0), -(v.get("view_count") or 0)))
        rows = rows[:limit]
        if not rows:
            return (f"Nothing on the watchlist broke {min_outlier}x in the last {days} days. "
                    f"Want me to widen the window?")
        out = [f"Watchlist outliers ({min_outlier}x+) - last {days} days, ranked by outlier score:", ""]
        for i, v in enumerate(rows, 1):
            flag = " (young, views still growing)" if v.get("immature") else ""
            fb = " (baseline: all scraped videos)" if v.get("baseline") == "fallback_all" else ""
            t = (v.get("title") or "").splitlines()[0][:80] if v.get("title") else "(no caption)"
            out.append(f"{i}. [{v['outlier_score']}x · {abbr(v.get('view_count'))} views] {t} - {v.get('handle')}{flag}{fb}")
            out.append(f"   {v.get('platform_url')}")
        return "\n".join(out)
    rows = sorted(recent, key=lambda v: v["published_at"], reverse=True)
    more = len(rows) > limit
    rows = rows[:limit]
    if not rows:
        return f"The watchlist was quiet in the last {days} days. Want me to widen the window?"
    out = [f"Your watchlist feed - everything posted in the last {days} days, newest first:", ""]
    for i, v in enumerate(rows, 1):
        o = f"{v['outlier_score']}x" if v.get("outlier_score") is not None else "n/a"
        t = (v.get("title") or "").splitlines()[0][:80] if v.get("title") else "(no caption)"
        out.append(f"{i}. [{v['published_at'][:10]} · {o} · {abbr(v.get('view_count'))} views] {t} - {v.get('handle')}")
        out.append(f"   {v.get('platform_url')}")
    if more:
        out.append(f"\n(showing the most recent {limit}; more exist in {scored})")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["list", "add", "remove", "pull", "report"])
    ap.add_argument("--file", default=DEFAULT)
    ap.add_argument("--platform", choices=["youtube", "tiktok", "instagram"])
    ap.add_argument("--handle"); ap.add_argument("--note", default="")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--outdir", default="/workspace/exports/bot-video/work/watchlist-pulls/" + date.today().isoformat())
    ap.add_argument("--mode", choices=["outliers", "recent"])
    ap.add_argument("--scored"); ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--min-outlier", type=float, default=1.0)
    a = ap.parse_args()
    d = load(a.file)
    if a.cmd == "list":
        for c in d["channels"]:
            print(f"{c['platform']:9} {c['handle']}  {c.get('note','')}")
        print(f"({len(d['channels'])} channels in {a.file})")
    elif a.cmd == "add":
        h = norm_handle(a.handle)
        if any(c["platform"] == a.platform and c["handle"].lower() == h.lower() for c in d["channels"]):
            print("already on the watchlist"); return
        d["channels"].append({"platform": a.platform, "handle": h,
                              "added": date.today().isoformat(), "note": a.note})
        save(a.file, d); print(f"added {a.platform} {h}")
    elif a.cmd == "remove":
        h = norm_handle(a.handle).lower()
        n = len(d["channels"])
        d["channels"] = [c for c in d["channels"] if not (c["platform"] == a.platform and c["handle"].lower() == h)]
        save(a.file, d); print("removed" if len(d["channels"]) < n else "not found")
    elif a.cmd == "pull":
        lim = a.limit or 40
        os.makedirs(a.outdir, exist_ok=True)
        ig = []
        for c in d["channels"]:
            if c["platform"] == "instagram":
                ig.append(c["handle"]); continue
            out = os.path.join(a.outdir, f"{c['platform']}_{c['handle'].lstrip('@')}.json")
            p = subprocess.run([sys.executable, os.path.join(HERE, "fetch_channel.py"), "--platform",
                                c["platform"], "--handle", c["handle"], "--limit", str(lim), "--out", out],
                               capture_output=True, text=True)
            print((p.stdout or p.stderr).strip().splitlines()[-1] if (p.stdout or p.stderr) else "?")
        if ig:
            est = len(ig) * (lim * IG_REEL_PRICE_FREE_TIER + IG_START)
            print(f"\nSKIPPED {len(ig)} Instagram channel(s) (no free path): {', '.join(ig)}")
            print(f"Paid option: Apify apify/instagram-reel-scraper, input "
                  f'{{"username": {json.dumps([h.lstrip("@") for h in ig])}, "resultsLimit": {lim}}} '
                  f"~US${est:.3f} at FREE-tier prices. Ask the user before running.")
        print(f"\nnext: python3 {HERE}/outlier_score.py {a.outdir}/*.json --out {a.outdir}/scored.json")
    elif a.cmd == "report":
        print(report(a.scored, a.mode, a.days, a.limit or (10 if a.mode == "outliers" else 25), a.min_outlier))


if __name__ == "__main__":
    main()
