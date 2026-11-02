#!/usr/bin/env python3
"""
LEGO Bricks worksheet — the Wants & Needs layer.

The "god-tier" teardown move: break each top video into its 7 component bricks,
then read which bricks are HELD CONSTANT across the winners (that's the formula —
copy these) vs which VARY (your creative freedom). This script scaffolds that
worksheet from analyzed-video data and computes the constant/variable split on
the fields Sandcastles actually labels.

The 7 LEGO bricks:
  1 Topic              5 Visual Format
  2 Angle              6 Key Visuals
  3 Hook (spoken+visual+text)   7 Audio
  4 Storytelling Style

Field mapping (auto, best-effort — Sandcastles labels only some bricks):
  Topic            <- topic
  Hook (spoken)    <- spoken_hook / spoken_hook_category / spoken_hook_madlib
  Storytelling     <- narrative_structure / storytelling_style / structure
  Visual Format    <- format_category
  (Angle, Key Visuals, Audio, Visual Hook usually need you to WATCH the video —
   the worksheet leaves them blank with a TODO so you fill them in.)

NON-VERBAL HANDLING: if the top videos carry no spoken_hook / transcript (comedy
skits, stitch clips, audio-only), the Spoken-Hook and Writing/Script bricks are
non-factors. The script detects this, sets `non_verbal_channel: true`, and marks
those bricks N/A so you don't waste time (and so hook-machine's spoken-hook
grading is skipped — analyze the VISUAL hook instead).

Pure stdlib. Input = analyzed videos JSON (same format as the other scripts).

Usage:
  python3 lego_bricks.py analyzed.json [--top-k 10] [--out worksheet.json]
"""
import argparse, json, sys
from statistics import mean

BRICKS = ["Topic", "Angle", "Hook", "Storytelling Style",
          "Visual Format", "Key Visuals", "Audio"]

FIELD_MAP = {
    "Topic": ["topic"],
    "Hook": ["spoken_hook_category", "spoken_hook", "hook_category", "visual_hook"],
    "Storytelling Style": ["narrative_structure", "storytelling_style",
                            "structure", "story_structure"],
    "Visual Format": ["format_category", "visual_format"],
}
TODO_BRICKS = ["Angle", "Key Visuals", "Audio"]  # almost always need eyes-on


def load(path):
    data = json.load(open(path, encoding="utf-8"))
    raw = data.get("videos", []) if isinstance(data, dict) else data
    out = []
    for v in raw:
        if v.get("outlier_score") is None:
            continue
        v = dict(v); v["_o"] = float(v["outlier_score"])
        v["_cap"] = (v.get("title") or v.get("caption") or "")[:70]
        v["_url"] = v.get("sandcastles_url") or v.get("platform_url")
        out.append(v)
    out.sort(key=lambda x: -x["_o"])
    return out


def first_present(v, keys):
    for k in keys:
        val = v.get(k)
        if isinstance(val, str) and val.strip():
            return val.strip()
    return None


def is_non_verbal(v):
    # non-verbal if no spoken hook text/category present
    return not (first_present(v, ["spoken_hook", "spoken_hook_category",
                                  "spoken_hook_madlib", "transcript"]))


def brick_value(v, brick, non_verbal):
    if brick == "Hook" and non_verbal:
        # prefer a visual hook label if present, else flag N/A-spoken
        vis = first_present(v, ["visual_hook", "format_category"])
        return (f"[visual] {vis}" if vis else "N/A (non-verbal — watch visual hook)")
    if brick in FIELD_MAP:
        return first_present(v, FIELD_MAP[brick]) or "(needs viewing)"
    if brick in TODO_BRICKS:
        return "(needs viewing)"
    return "(needs viewing)"


def constants_vs_variables(rows, bricks):
    out = {}
    for b in bricks:
        vals = [r["bricks"][b] for r in rows
                if r["bricks"][b] and not r["bricks"][b].startswith(("(needs", "N/A"))]
        if not vals:
            out[b] = {"status": "unlabeled"}
            continue
        tab = {}
        for x in vals:
            tab[x] = tab.get(x, 0) + 1
        top_val, top_n = max(tab.items(), key=lambda kv: kv[1])
        share = top_n / len(vals)
        out[b] = {
            "modal_value": top_val,
            "modal_share": round(share, 2),
            "verdict": ("HOLD CONSTANT (formula)" if share >= 0.7
                        else "VARIABLE (your freedom)" if share <= 0.5
                        else "mostly constant"),
            "distinct_values": tab,
        }
    return out


def analyze(vids, top_k=10):
    if len(vids) < 3:
        return {"status": "insufficient_data", "n": len(vids)}
    top = vids[:top_k]
    nv_flags = [is_non_verbal(v) for v in top]
    non_verbal_channel = sum(nv_flags) >= max(1, len(top) // 2)
    bricks = list(BRICKS)
    rows = []
    for v in top:
        nv = is_non_verbal(v)
        row = {b: brick_value(v, b, nv) for b in bricks}
        if non_verbal_channel:
            # spoken-only sub-brick is moot; keep Hook (covers visual) but note
            pass
        rows.append({"outlier": v["_o"], "caption": v["_cap"],
                     "url": v["_url"], "non_verbal": nv, "bricks": row})
    cv = constants_vs_variables(rows, bricks)
    formula = [b for b, d in cv.items() if d.get("verdict", "").startswith("HOLD")]
    freedom = [b for b, d in cv.items() if d.get("verdict", "").startswith("VARIABLE")]
    return {
        "status": "ok",
        "top_k": len(top),
        "non_verbal_channel": non_verbal_channel,
        "non_verbal_note": ("Top videos have no transcript — IGNORE the Spoken-Hook "
                            "and Script bricks; analyze the VISUAL hook, structure, "
                            "and audio instead." if non_verbal_channel else None),
        "todo_bricks": TODO_BRICKS + (["Hook (visual)"] if non_verbal_channel else []),
        "constants_vs_variables": cv,
        "formula_hold_constant": formula,
        "your_creative_freedom": freedom,
        "worksheet": rows,
    }


def summary(r):
    if r["status"] != "ok":
        return f"[{r['status']}] n={r.get('n')}"
    L = [f"LEGO BRICKS over top {r['top_k']}"
         + ("  [NON-VERBAL channel]" if r["non_verbal_channel"] else "")]
    if r["non_verbal_note"]:
        L.append("  " + r["non_verbal_note"])
    L.append(f"  FORMULA (hold constant): {', '.join(r['formula_hold_constant']) or '—'}")
    L.append(f"  YOUR FREEDOM (varies):   {', '.join(r['your_creative_freedom']) or '—'}")
    for b, d in r["constants_vs_variables"].items():
        if d.get("verdict"):
            L.append(f"   - {b:18} {d['verdict']:24} modal: {d.get('modal_value')} "
                     f"({int(d.get('modal_share',0)*100)}%)")
    L.append(f"  TODO (watch the videos): {', '.join(r['todo_bricks'])}")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("videos_json"); ap.add_argument("--top-k", type=int, default=10)
    ap.add_argument("--out")
    a = ap.parse_args()
    r = analyze(load(a.videos_json), top_k=a.top_k)
    if a.out:
        json.dump(r, open(a.out, "w", encoding="utf-8"), indent=2)
    print(summary(r))
    print("\n--- JSON ---")
    print(json.dumps(r, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
