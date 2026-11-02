#!/usr/bin/env python3
"""
Funnel & Consistency analyzer — the Shelby Sapp layer.

Operationalizes three teardown ideas that pure outlier analysis misses:

  1. CONSISTENCY OVER VIRALITY. Elite funnel creators stack a tight band of
     views many times a day rather than chasing the occasional mega-spike.
     Measures posting cadence, view dispersion (CV), the max/median ratio
     (virality-reliance), and the share of videos inside the "core band."

  2. CTA COVERAGE. The lead engine only works if a CTA rides on (almost) every
     post — including the ones that have nothing to do with the offer. Detects
     CTA language in captions, reports coverage across the top-K, and — given
     a list of offer keywords — the share of CTA posts that are OFF-offer-topic
     (the "ManyChat on a Porsche post" pattern).

  3. OFFER vs NON-OFFER MIX of top performers. How many of the top-K videos are
     actually about the thing being sold? (Often only ~2 of 10 — the rest are
     lifestyle / polarizing-filter content doing audience work.)

Pure stdlib, deterministic. Same input format as the other breakdown scripts.
Caption text is read from `title` (Sandcastles puts the full caption there) or
`description`/`caption` if present.

Usage:
  python3 funnel_consistency.py videos.json [--out report.json]
        [--top-k 10] [--offer-keywords "sales,academy,bootcamp,program,course"]
"""
import argparse, json, re, sys
from datetime import date
from statistics import median, mean, pstdev

# CTA / ManyChat trigger patterns (tune per creator)
CTA_PATTERNS = [
    r"\bcomment(?:ed|s)?\b[^.!?\n]{0,30}?[\"“']?[A-Z0-9]{2,}",  # Comment BOOTCAMP / "33"
    r"\bcomment\b[^.!?\n]{0,20}\bbelow\b",
    r"\bdrop\b[^.!?\n]{0,15}(?:below|👇|a\s|the\s|\"|“)",
    r"\bdm\b|\bin your dms\b|\bsend (?:you|it|your)\b",
    r"\blink in (?:bio|my bio)\b",
    r"\bsave (?:your|you a) (?:spot|seat)\b",
    r"\b(?:join|register|sign ?up) (?:me|us|my|for|now|here|the)\b",
    r"\bfree\b[^.!?\n]{0,25}\b(?:masterclass|workshop|training|bootcamp|webinar|guide|class|challenge)\b",
    r"\bcomment\b[^.!?\n]{0,15}(?:and i('?| wi)ll|to (?:join|get|grab))",
    r"👇|⚡",
]
CTA_RE = re.compile("|".join(CTA_PATTERNS), re.I)


def caption(v):
    return (v.get("title") or v.get("caption") or v.get("description") or "")


def load(path):
    data = json.load(open(path, encoding="utf-8"))
    raw = data.get("videos", []) if isinstance(data, dict) else data
    out = []
    for v in raw:
        if v.get("published_at") is None or v.get("outlier_score") is None:
            continue
        out.append({
            "uuid": v.get("uuid") or v.get("video_uuid"),
            "cap": caption(v).strip(),
            "d": v["published_at"][:10],
            "outlier": float(v["outlier_score"]),
            "views": v.get("view_count"),
            "url": v.get("sandcastles_url") or v.get("platform_url"),
        })
    seen, ded = set(), []
    for v in out:
        k = v["uuid"] or (v["d"], v["cap"][:40])
        if k in seen:
            continue
        seen.add(k); ded.append(v)
    ded.sort(key=lambda x: x["d"])
    return ded


def _d(s):
    return date(int(s[:4]), int(s[5:7]), int(s[8:10]))


def has_cta(v):
    return bool(CTA_RE.search(v["cap"]))


def is_offer(v, kws):
    t = v["cap"].lower()
    return any(k in t for k in kws)


def consistency(vids):
    vc = [v["views"] for v in vids if v["views"] is not None]
    if len(vc) < 3:
        return {"note": "too few videos with views"}
    span_days = max(1, (_d(vids[-1]["d"]) - _d(vids[0]["d"])).days)
    med = median(vc); mn = mean(vc)
    cv = round(pstdev(vc) / mn, 2) if mn else None
    core = [x for x in vc if 0.5 * med <= x <= 2 * med]
    return {
        "n_with_views": len(vc),
        "date_span_days": span_days,
        "posts_per_week_in_sample": round(len(vids) / (span_days / 7), 2),
        "median_views": int(med),
        "view_cv": cv,  # lower = more consistent
        "max_over_median": round(max(vc) / med, 1),  # high = reliant on spikes
        "core_band_share": round(len(core) / len(vc), 2),  # high = tight & consistent
        "interpretation": (
            "tight/consistent" if cv is not None and cv < 1.2 and max(vc) / med < 6
            else "spike-reliant"),
        "caveat": "Sample may be top-by-views (cadence under-counts true posting rate).",
    }


def analyze(vids, top_k=10, offer_kws=None):
    if len(vids) < 6:
        return {"status": "insufficient_data", "n": len(vids)}
    offer_kws = [k.strip().lower() for k in (offer_kws or []) if k.strip()]
    top = sorted(vids, key=lambda v: -v["outlier"])[:top_k]

    cta_all = [v for v in vids if has_cta(v)]
    cta_top = [v for v in top if has_cta(v)]
    offer_top = [v for v in top if offer_kws and is_offer(v, offer_kws)]
    cta_nonoffer_top = [v for v in cta_top if not (offer_kws and is_offer(v, offer_kws))]

    return {
        "status": "ok",
        "n": len(vids),
        "consistency": consistency(vids),
        "cta_coverage": {
            "overall_share": round(len(cta_all) / len(vids), 2),
            "top_k": top_k,
            "top_k_with_cta": len(cta_top),
            "top_k_cta_share": round(len(cta_top) / len(top), 2),
            "note": "CTA detected from caption text; eyeball borderline captions.",
        },
        "offer_vs_nonoffer_top": {
            "offer_keywords": offer_kws or "(none supplied — pass --offer-keywords)",
            "top_k_on_offer_topic": len(offer_top) if offer_kws else None,
            "top_k_off_offer_topic": (len(top) - len(offer_top)) if offer_kws else None,
            "cta_on_nonoffer_count": len(cta_nonoffer_top) if offer_kws else None,
            "insight": ("CTAs riding on non-offer content = the 'ManyChat on a "
                        "Porsche post' pattern" if offer_kws else None),
        },
        "top_k_detail": [
            {"d": v["d"], "outlier": v["outlier"], "views": v["views"],
             "has_cta": has_cta(v),
             "on_offer_topic": (is_offer(v, offer_kws) if offer_kws else None),
             "cap": v["cap"][:80], "url": v["url"]}
            for v in top
        ],
    }


def summary(r):
    if r["status"] != "ok":
        return f"[{r['status']}] n={r.get('n')}"
    c = r["consistency"]; cta = r["cta_coverage"]; ov = r["offer_vs_nonoffer_top"]
    L = [f"CONSISTENCY  median {c.get('median_views'):,} views | CV {c.get('view_cv')} "
         f"| max/median {c.get('max_over_median')} | core-band {c.get('core_band_share')} "
         f"-> {c.get('interpretation')}",
         f"CADENCE      ~{c.get('posts_per_week_in_sample')} posts/wk in sample "
         f"(over {c.get('date_span_days')} days)",
         f"CTA COVERAGE overall {int(cta['overall_share']*100)}% | "
         f"top-{cta['top_k']} {cta['top_k_with_cta']}/{cta['top_k']} have a CTA"]
    if ov["top_k_on_offer_topic"] is not None:
        L.append(f"OFFER MIX    only {ov['top_k_on_offer_topic']}/{r['cta_coverage']['top_k']} "
                 f"top videos are on-offer-topic; {ov['cta_on_nonoffer_count']} CTAs ride non-offer content")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("videos_json")
    ap.add_argument("--out")
    ap.add_argument("--top-k", type=int, default=10)
    ap.add_argument("--offer-keywords", default="")
    a = ap.parse_args()
    vids = load(a.videos_json)
    r = analyze(vids, top_k=a.top_k,
                offer_kws=a.offer_keywords.split(",") if a.offer_keywords else None)
    if a.out:
        json.dump(r, open(a.out, "w", encoding="utf-8"), indent=2)
    print(summary(r))
    print("\n--- JSON ---")
    print(json.dumps(r, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
