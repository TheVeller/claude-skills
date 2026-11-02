#!/usr/bin/env python3
"""
outlier_score.py - local replacement for Sandcastles' outlier score.

  outlier_score = video views / mean views of the SAME channel's videos
                  published in the 90 days BEFORE it (the video itself excluded)

This is the definition content.game gives ("views / channel's trailing 3-month
average"). It is an approximation of Sandcastles' number, not a copy:
  - Sandcastles has the channel's full history; we only have what was scraped.
    If the scrape misses older/low-view videos the baseline is biased.
  - Views are a snapshot taken now. Very young videos (< MIN_AGE_DAYS) have not
    finished accumulating views; they are flagged `immature: true`.
  - If fewer than --min-baseline prior videos exist in the window (start of
    the scraped history), the baseline falls back to the mean of ALL other
    scraped videos of that channel and the row is flagged
    `baseline: "fallback_all"`.
Rows without views or publish date get outlier_score null (never invented).

Input: one or more normalized JSON files ({"videos":[...]}) - mixing channels
is fine, baselines are computed per (platform, handle).
Output: {"videos":[...]} with outlier_score, baseline_mean, baseline_n,
baseline, age_days, immature added. Compatible with the creator-breakdown
scripts (detect_breakout / breakdown_analyze / funnel_consistency / ...).

Usage:
  python3 outlier_score.py a.json [b.json ...] --out scored.json
         [--window-days 90] [--min-baseline 3] [--min-age-days 2]
"""
import argparse, json, sys
from datetime import datetime, timezone, timedelta
from statistics import mean


def parse_dt(s):
    if not s:
        return None
    s = s.replace("Z", "+00:00")
    try:
        d = datetime.fromisoformat(s)
    except ValueError:
        try:
            d = datetime.strptime(s[:10], "%Y-%m-%d")
        except ValueError:
            return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def score(videos, window_days=90, min_baseline=3, min_age_days=2, now=None):
    now = now or datetime.now(timezone.utc)
    groups = {}
    for v in videos:
        groups.setdefault((v.get("platform"), v.get("handle")), []).append(v)
    for key, vids in groups.items():
        usable = [v for v in vids if v.get("view_count") is not None and parse_dt(v.get("published_at"))]
        for v in vids:
            dt = parse_dt(v.get("published_at"))
            v["age_days"] = round((now - dt).total_seconds() / 86400, 1) if dt else None
            v["immature"] = bool(dt and v["age_days"] < min_age_days)
            if v.get("view_count") is None or dt is None:
                v.update(outlier_score=None, baseline_mean=None, baseline_n=0,
                         baseline="missing_views_or_date")
                continue
            lo = dt - timedelta(days=window_days)
            prior = [u["view_count"] for u in usable
                     if u is not v and lo <= parse_dt(u["published_at"]) < dt]
            mode = "trailing_%dd" % window_days
            if len(prior) < min_baseline:
                prior = [u["view_count"] for u in usable if u is not v]
                mode = "fallback_all"
            if not prior or mean(prior) == 0:
                v.update(outlier_score=None, baseline_mean=None, baseline_n=len(prior),
                         baseline="no_baseline")
                continue
            b = mean(prior)
            v.update(outlier_score=round(v["view_count"] / b, 2), baseline_mean=round(b),
                     baseline_n=len(prior), baseline=mode)
    return videos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--window-days", type=int, default=90)
    ap.add_argument("--min-baseline", type=int, default=3)
    ap.add_argument("--min-age-days", type=float, default=2)
    a = ap.parse_args()
    vids = []
    for p in a.inputs:
        d = json.load(open(p, encoding="utf-8"))
        vids += d.get("videos", []) if isinstance(d, dict) else d
    seen, ded = set(), []
    for v in vids:
        k = v.get("uuid") or (v.get("platform_url"))
        if k in seen:
            continue
        seen.add(k); ded.append(v)
    score(ded, a.window_days, a.min_baseline, a.min_age_days)
    json.dump({"videos": ded}, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    n = sum(1 for v in ded if v.get("outlier_score") is not None)
    fb = sum(1 for v in ded if v.get("baseline") == "fallback_all")
    print(f"scored {n}/{len(ded)} videos ({fb} with fallback baseline) -> {a.out}")


if __name__ == "__main__":
    main()
