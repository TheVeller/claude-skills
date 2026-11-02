#!/usr/bin/env python3
"""
Creator Breakdown — spike / cluster / collab analyzer.

Companion to detect_breakout.py. Where the detector looks for a *sustained*
step-change in outlier score, this script characterizes the OTHER common
shape: a transient viral CLUSTER (a launch spike) sitting in the middle of an
otherwise flat "anti-viral" series — the pattern behind newsletter-style
creator teardowns.

It:
  1. Finds the spike cluster (the tightest date window holding the top outliers).
  2. Splits history into pre-spike / spike / post-spike eras and compares them,
     so you can see whether a spike was a durable STEP or a transient SPIKE
     that mean-reverted.
  3. Flags collab/shoutout posts (heuristic on titles) and compares their
     outlier performance vs solo posts.
  4. Surfaces top videos by outlier and engagement-vs-reach mismatches
     (vanity-virality: high views, low engagement_rate).

Pure stdlib, deterministic. Same input format as detect_breakout.py:
  {"videos":[{published_at, outlier_score, view_count, engagement_rate,
              title, sandcastles_url|platform_url, ...}, ...]}

Usage:
  python3 breakdown_analyze.py <videos.json> [--out report.json]
         [--cluster-window-days N] [--top-k K]
"""
import argparse, json, sys
from statistics import median

COLLAB_KEYWORDS = [
    "@", "collab", "my friend", "go-to", "mastermind", "costa rica",
    "5 women", "shoutout", "shout out", "guest", "podcast", "interview",
    "cheffing", "keynote", "panel", "with @",
]


def load(path):
    data = json.load(open(path, encoding="utf-8"))
    raw = data.get("videos", []) if isinstance(data, dict) else data
    out = []
    for v in raw:
        if v.get("published_at") is None or v.get("outlier_score") is None:
            continue
        out.append({
            "uuid": v.get("uuid") or v.get("video_uuid"),
            "title": (v.get("title") or "").strip(),
            "d": v["published_at"][:10],
            "outlier": float(v["outlier_score"]),
            "views": v.get("view_count"),
            "eng": v.get("engagement_rate"),
            "url": v.get("sandcastles_url") or v.get("platform_url"),
        })
    seen, ded = set(), []
    for v in out:
        k = v["uuid"] or (v["d"], v["title"])
        if k in seen:
            continue
        seen.add(k); ded.append(v)
    ded.sort(key=lambda x: x["d"])
    return ded


def _d(s):
    from datetime import date
    return date(int(s[:4]), int(s[5:7]), int(s[8:10]))


def stats(seg):
    if not seg:
        return None
    o = [v["outlier"] for v in seg]
    vc = [v["views"] for v in seg if v["views"] is not None]
    return {
        "n": len(seg), "start": seg[0]["d"], "end": seg[-1]["d"],
        "median_outlier": round(median(o), 2), "max_outlier": round(max(o), 2),
        "median_views": int(median(vc)) if vc else None,
        "max_views": max(vc) if vc else None,
    }


def find_cluster(vids, top_k, window_days):
    top = sorted(vids, key=lambda v: -v["outlier"])[:top_k]
    anchor = top[0]
    a = _d(anchor["d"])
    near = [v for v in top if abs((_d(v["d"]) - a).days) <= window_days]
    near.sort(key=lambda v: v["d"])
    return near, anchor


def is_collab(v):
    t = v["title"].lower()
    return any(k in t for k in COLLAB_KEYWORDS)


def analyze(vids, top_k=6, window_days=10):
    if len(vids) < 6:
        return {"status": "insufficient_data", "n": len(vids)}
    cluster, anchor = find_cluster(vids, top_k, window_days)
    cstart, cend = cluster[0]["d"], cluster[-1]["d"]
    pre = [v for v in vids if v["d"] < cstart]
    spike = [v for v in vids if cstart <= v["d"] <= cend]
    post = [v for v in vids if v["d"] > cend]

    pre_s, spike_s, post_s = stats(pre), stats(spike), stats(post)
    verdict = "transient_spike"
    if post_s and pre_s and post_s["median_outlier"] > 1.3 * pre_s["median_outlier"]:
        verdict = "possible_durable_step"
    if post_s and post_s["median_outlier"] <= 1.1 * (pre_s["median_outlier"] if pre_s else 1):
        verdict = "transient_spike_reverted"

    collabs = [v for v in vids if is_collab(v)]
    solos = [v for v in vids if not is_collab(v)]
    co = [v["outlier"] for v in collabs] or [0]
    so = [v["outlier"] for v in solos] or [0]
    top_out = sorted(vids, key=lambda v: -v["outlier"])[:top_k]
    collab_in_top = sum(1 for v in top_out if is_collab(v))

    med_views = median([v["views"] for v in vids if v["views"]]) if vids else 0
    vanity = [v for v in vids if v["views"] and v["eng"] is not None
              and v["views"] > 2 * med_views and v["eng"] <= 0.015]

    return {
        "status": "ok",
        "n": len(vids),
        "spike_cluster": {
            "start": cstart, "end": cend, "n": len(spike),
            "anchor_video": {"title": anchor["title"][:120], "d": anchor["d"],
                              "outlier": anchor["outlier"], "views": anchor["views"],
                              "url": anchor["url"]},
            "videos": [{"d": v["d"], "outlier": v["outlier"], "views": v["views"],
                        "title": v["title"][:90], "url": v["url"]} for v in spike],
        },
        "eras": {"pre_spike": pre_s, "spike": spike_s, "post_spike": post_s},
        "verdict": verdict,
        "collab_vs_solo": {
            "collab_median_outlier": round(median(co), 2), "collab_n": len(collabs),
            "solo_median_outlier": round(median(so), 2), "solo_n": len(solos),
            "collab_share_of_top": f"{collab_in_top}/{len(top_out)}",
            "flagged_collabs": [{"d": v["d"], "outlier": v["outlier"],
                                 "views": v["views"], "title": v["title"][:80]}
                                for v in sorted(collabs, key=lambda v: -v["outlier"])],
        },
        "top_by_outlier": [{"d": v["d"], "outlier": v["outlier"], "views": v["views"],
                            "title": v["title"][:80], "url": v["url"]} for v in top_out],
        "vanity_virality": [{"d": v["d"], "views": v["views"], "eng": v["eng"],
                             "title": v["title"][:80], "url": v["url"]} for v in vanity],
    }


def summary(r):
    if r["status"] != "ok":
        return f"[{r['status']}] n={r.get('n')}"
    e = r["eras"]; sc = r["spike_cluster"]
    L = [f"SPIKE CLUSTER  {sc['start']}..{sc['end']}  ({sc['n']} videos)",
         f"  anchor: {sc['anchor_video']['title']}",
         f"          outlier {sc['anchor_video']['outlier']} | {sc['anchor_video']['views']:,} views",
         ""]
    for name in ("pre_spike", "spike", "post_spike"):
        s = e[name]
        if s and s["median_views"]:
            L.append(f"{name:11} {s['start']}..{s['end']}  n={s['n']:<3} "
                     f"median outlier {s['median_outlier']:<6} median views {s['median_views']:,}")
    L += ["", f"VERDICT: {r['verdict']}",
          f"Collab median outlier {r['collab_vs_solo']['collab_median_outlier']} "
          f"vs solo {r['collab_vs_solo']['solo_median_outlier']} "
          f"(collab share of top: {r['collab_vs_solo']['collab_share_of_top']})"]
    if r["vanity_virality"]:
        L.append(f"Vanity-virality flags: {len(r['vanity_virality'])} (high views, <=1.5% engagement)")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("videos_json")
    ap.add_argument("--out")
    ap.add_argument("--cluster-window-days", type=int, default=10)
    ap.add_argument("--top-k", type=int, default=6)
    ap.add_argument("--since", help="only analyze videos published on/after this "
                    "date (YYYY-MM-DD)")
    a = ap.parse_args()
    vids = load(a.videos_json)
    since_note = None
    if a.since:
        before = len(vids)
        vids = [v for v in vids if v["d"] >= a.since]
        since_note = (f"--since {a.since} applied: kept {len(vids)} of {before} "
                      f"videos; pre-{a.since} history excluded.")
    r = analyze(vids, top_k=a.top_k, window_days=a.cluster_window_days)
    if isinstance(r, dict) and since_note:
        r["since_filter_note"] = since_note
    if a.out:
        json.dump(r, open(a.out, "w", encoding="utf-8"), indent=2)
    print(summary(r))
    print("\n--- JSON ---")
    print(json.dumps(r, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
