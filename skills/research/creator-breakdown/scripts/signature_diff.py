#!/usr/bin/env python3
"""
Signature Diff — isolate the ONE thing that changed at the inflection.

The Ryan To layer. detect_breakout.py tells you *when* a channel stepped up;
this tells you *what changed* — and specifically whether a new, repeating
"signature element" (often a VISUAL hook / format wrinkle) emerged at that
point and became a moat.

Given analyzed videos (carrying dimension labels) and an inflection date, for
every dimension it computes, per value:
  - pre_share / post_share and EMERGENCE (post_share - pre_share),
  - persistence (post_share = how often it repeats after = signature strength),
  - mean outlier of post videos that use it (does it correlate with winning?).

It then reports:
  - emergent_signatures : values that were ~absent before and become common
    after (the candidate signature / moat),
  - held_constant       : values common both before and after (the "he kept X,
    changed only Y" half of the story),
  - faded               : values common before and gone after.

Dimensions scanned: every video key ending in `_category`, plus `topic`, plus
any key containing `visual` or `hook` (so it adapts to whatever the Sandcastles
analysis payload exposes). Values of None/"" are ignored. Pure stdlib.

NOTE ON DATA: dimension labels only exist for videos that have been run through
`analyze_video`. If too few are analyzed, the script says so — analyze a sample
of pre- and post-inflection videos first (see the SKILL.md). And some visual
signatures are too subtle for a category label — always eyeball the trigger
video + a few post-inflection winners to name the visual element in words.

Usage:
  python3 signature_diff.py analyzed.json --inflection 2025-06-01 [--out s.json]
        [--min-analyzed 8]
"""
import argparse, json, sys
from statistics import mean

PASSTHROUGH_HINTS = ("_category",)
EXTRA_FIELDS = ("topic",)
FUZZY_HINTS = ("visual", "hook")


def load(path):
    data = json.load(open(path, encoding="utf-8"))
    raw = data.get("videos", []) if isinstance(data, dict) else data
    out = []
    for v in raw:
        if v.get("published_at") is None or v.get("outlier_score") is None:
            continue
        v = dict(v)
        v["_d"] = v["published_at"][:10]
        v["_o"] = float(v["outlier_score"])
        out.append(v)
    out.sort(key=lambda x: x["_d"])
    return out


def dimension_fields(vids):
    fields = set()
    for v in vids:
        for k in v.keys():
            if k.startswith("_") or k in ("published_at", "outlier_score"):
                continue
            kl = k.lower()
            if (any(kl.endswith(h) for h in PASSTHROUGH_HINTS)
                    or k in EXTRA_FIELDS
                    or any(h in kl for h in FUZZY_HINTS)):
                # only keep string-valued, label-like fields
                val = v.get(k)
                if isinstance(val, str) and val.strip():
                    fields.add(k)
    return sorted(fields)


def share_table(vids, field):
    vals = [v.get(field) for v in vids if isinstance(v.get(field), str) and v.get(field).strip()]
    n = len(vals)
    tab = {}
    for x in vals:
        tab[x] = tab.get(x, 0) + 1
    return {k: c / n for k, c in tab.items()} if n else {}, n


def analyze(vids, inflection, min_analyzed=8):
    fields = dimension_fields(vids)
    analyzed = [v for v in vids if any(isinstance(v.get(f), str) and v.get(f).strip()
                                       for f in fields)]
    if len(analyzed) < min_analyzed or not fields:
        return {"status": "needs_analysis",
                "analyzed_with_labels": len(analyzed),
                "dimension_fields_found": fields,
                "note": "Run analyze_video on a pre/post sample to populate "
                        "format_category / hook / visual labels, then re-run."}

    pre = [v for v in vids if v["_d"] < inflection]
    post = [v for v in vids if v["_d"] >= inflection]
    result = {"status": "ok", "inflection": inflection,
              "pre_n": len(pre), "post_n": len(post), "dimensions": {}}

    for f in fields:
        pre_sh, _ = share_table(pre, f)
        post_sh, _ = share_table(post, f)
        emergent, constant, faded = [], [], []
        for val in set(list(pre_sh) + list(post_sh)):
            a, b = pre_sh.get(val, 0.0), post_sh.get(val, 0.0)
            post_vals = [v["_o"] for v in post if v.get(f) == val]
            rec = {"value": val, "pre_share": round(a, 2), "post_share": round(b, 2),
                   "emergence": round(b - a, 2),
                   "post_mean_outlier": round(mean(post_vals), 2) if post_vals else None}
            if a <= 0.15 and b >= 0.40:
                emergent.append(rec)
            elif a >= 0.40 and b >= 0.40:
                constant.append(rec)
            elif a >= 0.40 and b <= 0.15:
                faded.append(rec)
        emergent.sort(key=lambda r: -r["post_share"])
        faded.sort(key=lambda r: -r["pre_share"])
        constant.sort(key=lambda r: -r["post_share"])
        if emergent or constant or faded:
            result["dimensions"][f] = {"emergent_signatures": emergent,
                                       "held_constant": constant, "faded": faded}

    # headline signature = strongest emergent across all dims (by post_share,
    # tiebreak post_mean_outlier)
    cand = []
    for f, d in result["dimensions"].items():
        for r in d["emergent_signatures"]:
            cand.append({**r, "dimension": f})
    cand.sort(key=lambda r: (-r["post_share"], -(r["post_mean_outlier"] or 0)))
    result["headline_signature"] = cand[0] if cand else None
    result["note"] = ("Category labels can't capture every visual wrinkle — "
                      "eyeball the trigger video + post-inflection winners and "
                      "name the visual signature in words.")
    return result


def summary(r):
    if r["status"] != "ok":
        return f"[{r['status']}] analyzed_with_labels={r.get('analyzed_with_labels')} :: {r.get('note','')}"
    L = [f"INFLECTION {r['inflection']}  (pre {r['pre_n']} / post {r['post_n']})"]
    h = r.get("headline_signature")
    if h:
        L.append(f"HEADLINE SIGNATURE -> [{h['dimension']}] '{h['value']}': "
                 f"{int(h['pre_share']*100)}% pre -> {int(h['post_share']*100)}% post "
                 f"(post mean outlier {h['post_mean_outlier']})")
    else:
        L.append("No clear emergent signature in the labeled dimensions.")
    for f, d in r["dimensions"].items():
        if d["emergent_signatures"]:
            es = ", ".join(f"{x['value']} ({int(x['post_share']*100)}%)"
                           for x in d["emergent_signatures"])
            L.append(f"  emerged in {f}: {es}")
        if d["held_constant"]:
            hc = ", ".join(x["value"] for x in d["held_constant"])
            L.append(f"  held constant {f}: {hc}")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("videos_json")
    ap.add_argument("--inflection", required=True, help="YYYY-MM-DD (from detect_breakout.py)")
    ap.add_argument("--min-analyzed", type=int, default=8)
    ap.add_argument("--out")
    a = ap.parse_args()
    vids = load(a.videos_json)
    r = analyze(vids, a.inflection, min_analyzed=a.min_analyzed)
    if a.out:
        json.dump(r, open(a.out, "w", encoding="utf-8"), indent=2)
    print(summary(r))
    print("\n--- JSON ---")
    print(json.dumps(r, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
