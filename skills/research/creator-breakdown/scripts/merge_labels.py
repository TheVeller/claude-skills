#!/usr/bin/env python3
"""
merge_labels.py - copy the agent-filled labels from prep_video.py folders
(DIR/*/analysis.json -> "labels") back into a scored videos file, so
lego_bricks.py / signature_diff.py (which read topic, *_category, *hook*,
format_category ...) can use them. Matches on meta.uuid, else on URL.
Videos without a filled label keep their fields untouched; empty labels
(None / "") are never written.

Usage:
  python3 merge_labels.py scored.json analyses_dir/ --out analyzed.json
"""
import argparse, glob, json, os


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scored"); ap.add_argument("analyses_dir"); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = json.load(open(a.scored, encoding="utf-8"))
    by_uuid = {v.get("uuid"): v for v in d["videos"]}
    by_url = {v.get("platform_url"): v for v in d["videos"]}
    merged = 0
    for p in glob.glob(os.path.join(a.analyses_dir, "*", "analysis.json")):
        an = json.load(open(p, encoding="utf-8"))
        v = by_uuid.get((an.get("meta") or {}).get("uuid")) or by_url.get(an.get("url"))
        if not v:
            continue
        labels = {k: x for k, x in (an.get("labels") or {}).items() if x not in (None, "")}
        if not labels:
            continue
        v.update(labels); v["analyzed"] = True
        if an.get("transcript"):
            v["transcript"] = an["transcript"]
        merged += 1
    json.dump(d, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"merged labels into {merged} videos -> {a.out}")


if __name__ == "__main__":
    main()
