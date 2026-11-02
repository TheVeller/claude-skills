#!/usr/bin/env python3
"""
fetch_channel.py - FREE channel pull with yt-dlp (no Apify, no account, no cookies).

Supported for free:
  youtube  -> the channel's /shorts tab (or /videos with --tab videos)
  tiktok   -> the profile grid (needs curl_cffi for stability; can be flaky)
NOT supported for free:
  instagram -> Instagram redirects to login. Use the Apify actor
               apify/instagram-reel-scraper (paid per reel) and pass its dataset
               JSON to normalize.py instead.

Output: normalized JSON {"channel": {...}, "videos": [...]} ready for
outlier_score.py (same field names the creator-breakdown scripts read).

Usage:
  python3 fetch_channel.py --platform youtube --handle mkbhd --limit 60 --out raw.json
  python3 fetch_channel.py --platform tiktok  --handle mkbhd --limit 60 --out raw.json
  [--tab shorts|videos] [--no-detail]   (youtube: --no-detail skips per-video
                                         calls, so there are NO publish dates)
"""
import argparse, json, subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from normalize import normalize_items

YTDLP = os.environ.get("YTDLP", "yt-dlp")


def run_json(args, timeout=180):
    p = subprocess.run([YTDLP, *args], capture_output=True, text=True, timeout=timeout)
    if p.returncode != 0 or not p.stdout.strip():
        raise RuntimeError((p.stderr or "yt-dlp failed").strip().splitlines()[-1])
    return p.stdout


def fetch_youtube(handle, limit, tab, detail):
    h = handle.lstrip("@")
    url = handle if handle.startswith("http") else f"https://www.youtube.com/@{h}/{tab}"
    flat = json.loads(run_json(["--flat-playlist", "-I", f"1:{limit}", "-J", url]))
    channel = {"platform": "youtube", "handle": "@" + h if not handle.startswith("http") else flat.get("uploader_id"),
               "name": flat.get("channel"), "follower_count": flat.get("channel_follower_count"),
               "url": flat.get("channel_url") or url}
    items = []
    for i, e in enumerate(flat.get("entries") or []):
        if detail:
            try:
                full = json.loads(run_json(["-j", "--skip-download", e.get("url") or e["id"]], timeout=120))
                items.append(full)
                print(f"  [{i+1}/{len(flat['entries'])}] {full.get('upload_date')} {full.get('view_count')} views",
                      file=sys.stderr)
                continue
            except Exception as ex:  # keep the flat row, note the failure
                print(f"  [{i+1}] detail failed: {ex}", file=sys.stderr)
        e = dict(e); e["_flat_only"] = True
        items.append(e)
    return channel, items


def fetch_tiktok(handle, limit):
    h = handle.lstrip("@")
    url = handle if handle.startswith("http") else f"https://www.tiktok.com/@{h}"
    last = None
    for attempt in range(3):  # TikTok extraction is flaky; retry
        try:
            flat = json.loads(run_json(["--flat-playlist", "-I", f"1:{limit}", "-J", url]))
            break
        except Exception as ex:
            last = ex
    else:
        raise RuntimeError(f"TikTok pull failed after 3 tries: {last}. Fallback: Apify "
                           f"clockworks/tiktok-scraper (paid, ask first).")
    entries = flat.get("entries") or []
    fc = None
    for e in entries:
        fc = fc or e.get("channel_follower_count")
    channel = {"platform": "tiktok", "handle": "@" + h, "name": flat.get("uploader") or h,
               "follower_count": fc, "url": url}
    return channel, entries


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--platform", required=True, choices=["youtube", "tiktok", "instagram"])
    ap.add_argument("--handle", required=True)
    ap.add_argument("--limit", type=int, default=60)
    ap.add_argument("--tab", default="shorts", choices=["shorts", "videos"])
    ap.add_argument("--no-detail", action="store_true")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.platform == "instagram":
        sys.exit("Instagram has no free path (login wall). Run Apify apify/instagram-reel-scraper "
                 "after the user approves the cost, then: normalize.py --source apify-ig-reels ...")
    if a.platform == "youtube":
        ch, items = fetch_youtube(a.handle, a.limit, a.tab, not a.no_detail)
        src = "ytdlp"
    else:
        ch, items = fetch_tiktok(a.handle, a.limit)
        src = "ytdlp"
    vids = normalize_items(items, src, platform=a.platform, handle=ch["handle"],
                           follower_count=ch.get("follower_count"))
    json.dump({"channel": ch, "videos": vids}, open(a.out, "w", encoding="utf-8"), indent=1,
              ensure_ascii=False)
    print(f"{ch['handle']} ({a.platform}): {len(vids)} videos -> {a.out}")


if __name__ == "__main__":
    main()
