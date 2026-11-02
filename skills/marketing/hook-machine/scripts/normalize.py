#!/usr/bin/env python3
"""
normalize.py - turn raw scraper output into ONE video schema.

Sources (field names confirmed from each tool's real output, 2026-10-29):
  ytdlp            yt-dlp -j / --flat-playlist entries (YouTube, TikTok)
  apify-tiktok     clockworks/tiktok-scraper dataset items
  apify-ig-reels   apify/instagram-reel-scraper dataset items
  apify-yt-shorts  streamers/youtube-shorts-scraper dataset items

Normalized video fields (the creator-breakdown scripts read these names):
  uuid, platform, handle, title (FULL caption), published_at (ISO, UTC),
  view_count, like_count, comment_count, share_count, engagement_rate,
  platform_url, duration_s, thumbnail, follower_count, is_pinned,
  paid_partnership, outlier_score (filled later by outlier_score.py)

engagement_rate = (likes + comments + shares) / views. This is OUR definition;
Sandcastles' exact formula is not public. Shares are missing on YouTube and on
Instagram unless the paid add-on is on, so ER is likes+comments there.

Usage:
  python3 normalize.py --source apify-ig-reels dataset.json --out norm.json
"""
import argparse, json, sys
from datetime import datetime, timezone


def _iso_from_ts(ts):
    try:
        return datetime.fromtimestamp(int(ts), tz=timezone.utc).isoformat().replace("+00:00", "Z")
    except Exception:
        return None


def _iso_from_ymd(s):
    if not s or len(s) != 8:
        return None
    return f"{s[:4]}-{s[4:6]}-{s[6:8]}T00:00:00Z"


def _er(v):
    views = v.get("view_count") or 0
    if not views:
        return None
    tot = sum((v.get(k) or 0) for k in ("like_count", "comment_count", "share_count"))
    return round(tot / views, 4)


def _dur(s):
    if s is None:
        return None
    if isinstance(s, (int, float)):
        return float(s)
    parts = [int(p) for p in str(s).split(":") if p.isdigit()]
    t = 0
    for p in parts:
        t = t * 60 + p
    return float(t) if parts else None


def from_ytdlp(e, platform):
    pub = _iso_from_ts(e.get("timestamp")) or _iso_from_ymd(e.get("upload_date"))
    url = e.get("webpage_url") or e.get("url")
    if platform == "youtube" and e.get("id"):
        url = f"https://www.youtube.com/shorts/{e['id']}"
    caption = e.get("description") if platform == "tiktok" else None
    title = (e.get("title") or "")
    if platform == "youtube" and e.get("description"):
        title = f"{title}\n{e['description']}"  # keep full caption for CTA detection
    elif caption and len(caption) > len(title):
        title = caption
    thumbs = e.get("thumbnails") or []
    return {
        "uuid": f"{platform}:{e.get('id')}",
        "platform": platform,
        "title": title.strip(),
        "published_at": pub,
        "view_count": e.get("view_count"),
        "like_count": e.get("like_count"),
        "comment_count": e.get("comment_count"),
        "share_count": e.get("repost_count"),
        "platform_url": url,
        "duration_s": _dur(e.get("duration")),
        "thumbnail": e.get("thumbnail") or (thumbs[-1]["url"] if thumbs else None),
        "follower_count": e.get("channel_follower_count"),
        "is_pinned": None,
        "paid_partnership": None,
    }


def from_apify_tiktok(e, platform="tiktok"):
    am = e.get("authorMeta") or {}
    vm = e.get("videoMeta") or {}
    return {
        "uuid": f"tiktok:{e.get('id')}",
        "platform": "tiktok",
        "handle": "@" + am["name"] if am.get("name") else None,
        "title": (e.get("text") or "").strip(),
        "published_at": e.get("createTimeISO") or _iso_from_ts(e.get("createTime")),
        "view_count": e.get("playCount"),
        "like_count": e.get("diggCount"),
        "comment_count": e.get("commentCount"),
        "share_count": e.get("shareCount"),
        "save_count": e.get("collectCount"),
        "platform_url": e.get("webVideoUrl"),
        "duration_s": _dur(vm.get("duration")),
        "thumbnail": vm.get("coverUrl"),
        "follower_count": am.get("fans"),
        "is_pinned": e.get("isPinned"),
        "paid_partnership": bool(e.get("isSponsored") or e.get("isAd")),
    }


def from_apify_ig(e, platform="instagram"):
    return {
        "uuid": f"instagram:{e.get('shortCode') or e.get('id')}",
        "platform": "instagram",
        "handle": "@" + e["ownerUsername"] if e.get("ownerUsername") else None,
        "title": (e.get("caption") or "").strip(),
        "published_at": e.get("timestamp"),
        # videoPlayCount = plays shown on the reel; videoViewCount is often null
        "view_count": e.get("videoPlayCount") or e.get("videoViewCount"),
        "like_count": e.get("likesCount"),
        "comment_count": e.get("commentsCount"),
        "share_count": e.get("sharesCount"),  # only with the paid shares add-on
        "platform_url": e.get("url"),
        "duration_s": _dur(e.get("videoDuration")),
        "thumbnail": e.get("displayUrl"),
        "follower_count": None,  # not in reel output; use apify/instagram-profile-scraper followersCount
        "is_pinned": e.get("isPinned"),
        "paid_partnership": e.get("paidPartnership"),
        "transcript": e.get("transcript") or None,
    }


def from_apify_yt(e, platform="youtube"):
    return {
        "uuid": f"youtube:{e.get('id')}",
        "platform": "youtube",
        "handle": "@" + e["channelUsername"] if e.get("channelUsername") else None,
        "title": "\n".join(x for x in [e.get("title"), e.get("text")] if x).strip(),
        "published_at": e.get("date"),
        "view_count": e.get("viewCount"),
        "like_count": e.get("likes"),
        "comment_count": e.get("commentsCount"),
        "share_count": None,
        "platform_url": e.get("url"),
        "duration_s": _dur(e.get("duration")),
        "thumbnail": e.get("thumbnailUrl"),
        "follower_count": e.get("numberOfSubscribers"),
        "is_pinned": None,
        "paid_partnership": e.get("isPaidContent"),
    }


SOURCES = {"apify-tiktok": from_apify_tiktok, "apify-ig-reels": from_apify_ig,
           "apify-yt-shorts": from_apify_yt}


def normalize_items(items, source, platform=None, handle=None, follower_count=None):
    out, seen = [], set()
    for e in items:
        if e.get("error"):
            continue
        v = from_ytdlp(e, platform) if source == "ytdlp" else SOURCES[source](e)
        if handle and not v.get("handle"):
            v["handle"] = handle
        if follower_count and not v.get("follower_count"):
            v["follower_count"] = follower_count
        if e.get("_flat_only"):
            v["_note"] = "flat listing only: no publish date / likes"
        v["engagement_rate"] = _er(v)
        v["outlier_score"] = None
        if v["uuid"] in seen:
            continue
        seen.add(v["uuid"]); out.append(v)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, choices=["ytdlp", *SOURCES])
    ap.add_argument("--platform", help="needed for --source ytdlp")
    ap.add_argument("--handle")
    ap.add_argument("raw_json", nargs="+")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    items = []
    for p in a.raw_json:
        d = json.load(open(p, encoding="utf-8"))
        if isinstance(d, dict):
            d = d.get("entries") or d.get("items") or d.get("videos") or [d]
        items += d
    vids = normalize_items(items, a.source, platform=a.platform, handle=a.handle)
    json.dump({"videos": vids}, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{len(vids)} videos -> {a.out}")


if __name__ == "__main__":
    main()
