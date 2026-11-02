#!/usr/bin/env python3
"""
Creator Breakout Detector — inflection engine.

Reads a JSON file of Sandcastles videos and finds the point where a channel's
rolling outlier performance step-changed upward — the "breakout." Pure stdlib,
deterministic, no network. Claude calls this so the math is reproducible
instead of eyeballed.

Input JSON may be either:
  {"videos": [ {...}, ... ]}              (a single MCP page)
  [ {...}, ... ]                          (a raw list)
  {"videos": [...combined from many pages...]}

Each video needs at least `published_at` and `outlier_score`. Fields used when
present: uuid/video_uuid, title, view_count, engagement_rate, sandcastles_url,
platform_url, analyzed, spoken_hook_category, format_category, topic.

Usage:
  python3 detect_breakout.py <videos.json> [--min-segment N] [--out report.json]

Algorithm:
  1. Sort videos oldest -> newest.
  2. Work on log1p(outlier_score) so a single paid/brand-deal spike can't
     hijack the result.
  3. Scan every candidate split with at least --min-segment videos on each
     side. Score each split by a Welch-style difference-of-means t-statistic
     (upward shifts only).
  4. The best split is the inflection. The first video of the later segment
     is the trigger video. Report pre vs post stats across every dimension.
"""
import argparse
import json
import math
import sys
from statistics import mean, median


def load_videos(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    raw = data.get("videos", []) if isinstance(data, dict) else data
    out = []
    for v in raw:
        pa = v.get("published_at")
        os_ = v.get("outlier_score")
        if pa is None or os_ is None:
            continue
        out.append({
            "uuid": v.get("uuid") or v.get("video_uuid"),
            "title": (v.get("title") or "").strip(),
            "published_at": pa,
            "outlier_score": float(os_),
            "view_count": v.get("view_count"),
            "engagement_rate": v.get("engagement_rate"),
            "url": v.get("sandcastles_url") or v.get("platform_url"),
            "analyzed": bool(v.get("analyzed", False)),
            "hook_category": v.get("spoken_hook_category"),
            "format_category": v.get("format_category"),
            "topic": v.get("topic"),
        })
    # de-dupe on uuid (pages can overlap), then sort oldest -> newest
    seen, deduped = set(), []
    for v in out:
        key = v["uuid"] or (v["published_at"], v["title"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(v)
    deduped.sort(key=lambda x: x["published_at"])
    return deduped


def _variance(xs, m):
    if len(xs) < 2:
        return 0.0
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def seg_stats(seg):
    os_ = [v["outlier_score"] for v in seg]
    vc = [v["view_count"] for v in seg if v["view_count"] is not None]
    paid = sum(1 for v in seg if v.get("engagement_rate") == 0)
    return {
        "count": len(seg),
        "date_start": seg[0]["published_at"][:10],
        "date_end": seg[-1]["published_at"][:10],
        "mean_outlier": round(mean(os_), 2),
        "median_outlier": round(median(os_), 2),
        "max_outlier": round(max(os_), 2),
        "mean_views": int(mean(vc)) if vc else None,
        "median_views": int(median(vc)) if vc else None,
        "likely_paid_count": paid,
    }


def dimension_mix(seg, field):
    """Distribution of an analyzed dimension over the videos that have it."""
    vals = [v[field] for v in seg if v.get(field)]
    if not vals:
        return None
    counts = {}
    for x in vals:
        counts[x] = counts.get(x, 0) + 1
    return {
        "analyzed_videos": len(vals),
        "mix": dict(sorted(counts.items(), key=lambda kv: -kv[1])),
    }


def detect(videos, min_segment=8):
    n = len(videos)
    if n < 2 * min_segment:
        return {"status": "insufficient_data", "video_count": n,
                "min_videos_needed": 2 * min_segment}

    logos = [math.log1p(v["outlier_score"]) for v in videos]
    best = None
    for i in range(min_segment, n - min_segment + 1):
        before, after = logos[:i], logos[i:]
        mb, ma = mean(before), mean(after)
        if ma - mb <= 0:
            continue  # upward shifts only
        nb, na = len(before), len(after)
        se = math.sqrt(_variance(before, mb) / nb +
                       _variance(after, ma) / na) or 1e-9
        tstat = (ma - mb) / se
        if best is None or tstat > best["t"]:
            best = {"index": i, "t": tstat}

    if best is None:
        return {"status": "no_upward_inflection", "video_count": n,
                "note": "Performance never sustained a step-change upward."}

    i = best["index"]
    before, after = videos[:i], videos[i:]
    trigger = videos[i]
    pre, post = seg_stats(before), seg_stats(after)
    t = best["t"]
    confidence = "strong" if t >= 4 else "moderate" if t >= 2.5 else "weak"

    # catalyst = biggest single hit within +/-3 videos of the changepoint
    window = videos[max(0, i - 3):i + 4]
    catalyst = max(window, key=lambda v: v["outlier_score"])

    lift = (round(post["median_outlier"] / pre["median_outlier"], 2)
            if pre["median_outlier"] > 0 else None)

    report = {
        "status": "ok",
        "video_count": n,
        "confidence": confidence,
        "t_statistic": round(t, 2),
        "inflection_date": trigger["published_at"][:10],
        "median_outlier_lift": lift,
        "trigger_video": {
            "title": trigger["title"][:240],
            "uuid": trigger["uuid"],
            "url": trigger["url"],
            "published_at": trigger["published_at"][:10],
            "outlier_score": trigger["outlier_score"],
            "view_count": trigger["view_count"],
        },
        "catalyst_video": {
            "title": catalyst["title"][:240],
            "uuid": catalyst["uuid"],
            "url": catalyst["url"],
            "published_at": catalyst["published_at"][:10],
            "outlier_score": catalyst["outlier_score"],
        },
        "pre_inflection": pre,
        "post_inflection": post,
        "dimensions": {
            "hook_category": {
                "pre": dimension_mix(before, "hook_category"),
                "post": dimension_mix(after, "hook_category"),
            },
            "format_category": {
                "pre": dimension_mix(before, "format_category"),
                "post": dimension_mix(after, "format_category"),
            },
            "topic": {
                "pre": dimension_mix(before, "topic"),
                "post": dimension_mix(after, "topic"),
            },
        },
        "pre_video_uuids": [v["uuid"] for v in before],
        "post_video_uuids": [v["uuid"] for v in after],
    }
    analyzed_total = sum(1 for v in videos if v["analyzed"])
    if analyzed_total == 0:
        report["dimension_note"] = (
            "No videos in this workspace are analyzed, so hook/format/topic "
            "diffs are empty. Run analyze_video on a sample of pre and post "
            "videos (1 credit each) to populate them.")
    return report


def human_summary(r):
    if r["status"] != "ok":
        return f"[{r['status']}] {r.get('note', '')} ({r.get('video_count', 0)} videos)"
    tv = r["trigger_video"]
    pre, post = r["pre_inflection"], r["post_inflection"]
    pre_v = f"{pre['median_views']:,}" if pre["median_views"] else "n/a"
    post_v = f"{post['median_views']:,}" if post["median_views"] else "n/a"
    views = f"{tv['view_count']:,}" if tv["view_count"] else "n/a"
    return "\n".join([
        f"BREAKOUT DETECTED - confidence: {r['confidence']} (t={r['t_statistic']})",
        f"Inflection date : {r['inflection_date']}",
        f"Trigger video   : {tv['title'][:90]}",
        f"                  {tv['url']}",
        f"                  outlier {tv['outlier_score']}  |  {views} views",
        "",
        f"BEFORE  {pre['date_start']}..{pre['date_end']}  ({pre['count']} videos)"
        f"  median outlier {pre['median_outlier']}  median views {pre_v}",
        f"AFTER   {post['date_start']}..{post['date_end']}  ({post['count']} videos)"
        f"  median outlier {post['median_outlier']}  median views {post_v}",
        f"Median outlier lift: {r['median_outlier_lift']}x",
    ])


def main():
    ap = argparse.ArgumentParser(description="Creator Breakout Detector engine")
    ap.add_argument("videos_json", help="path to combined videos JSON")
    ap.add_argument("--min-segment", type=int, default=8,
                    help="minimum videos on each side of the split (default 8)")
    ap.add_argument("--out", help="write the full JSON report to this path")
    ap.add_argument("--since", help="only analyze videos published on/after this "
                    "date (YYYY-MM-DD); hard-scopes the window and notes the clip")
    args = ap.parse_args()

    videos = load_videos(args.videos_json)
    since_note = None
    if args.since:
        before = len(videos)
        videos = [v for v in videos if (v["published_at"] or "")[:10] >= args.since]
        since_note = (f"--since {args.since} applied: kept {len(videos)} of "
                      f"{before} videos. Pre-{args.since} history is excluded, so "
                      f"the pre-inflection baseline may be clipped.")
    report = detect(videos, min_segment=args.min_segment)
    if isinstance(report, dict) and since_note:
        report["since_filter_note"] = since_note

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

    print(human_summary(report))
    print("\n--- JSON ---")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] in ("ok", "no_upward_inflection") else 1


if __name__ == "__main__":
    sys.exit(main())
