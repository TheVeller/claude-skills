---
name: sandcastles-watchlist-outliers
description: >-
  Use when the user wants only the outlier videos (1.0x+ of the channel's own
  3-month average) posted in the last 7 days by the channels on the local
  watchlist, ranked with links; free for YouTube/TikTok, no Sandcastles.
metadata:
  origin: external-adapted
  source: "content.game (Kallaway / Content Dept.)"
  credit: "Adapted from content.game material by Kallaway / Content Dept.; rebuilt by TheVeller to run without Sandcastles."
  upstream_license: "sin dato (upstream terms not confirmed)"
---

> Source: adapted from content.game (Kallaway / Content Dept.) "Outlier Video Pulse" (`sandcastles-watchlist-outliers`), claimed 2026-10-29. Rebuilt on 2026-10-29 to run without Sandcastles: yt-dlp + optional Apify + local outlier math. Original in /workspace/exports/bot-video/work/content-game/outliervideopulse/.

# Watchlist Outliers (1x+)

Surface only the videos that are punching above their weight across the
watchlist: anything with an outlier score of 1.0x or higher, ranked by outlier
score, delivered as a clean ordered list with direct video links. This is a
quick scan, not a deep dive: never analyze hooks, formats or topics, and never
start a paid Apify run without an explicit yes.

**Outlier score** = the video's views / the mean views of the same channel's
videos posted in the 90 days before it (computed locally by
`scripts/outlier_score.py`). It is our approximation of Sandcastles' score, built
only from what we scraped. See `references/data-sources.md` for sources, prices
and limits.

## Requirements
- A watchlist file: `/workspace/exports/bot-video/watchlist.json`
  (`{"channels":[{"platform":"youtube|tiktok|instagram","handle":"@x"}]}`).
  Manage it with `scripts/watchlist.py list | add --platform P --handle @x | remove ...`.
- If the watchlist is empty or missing, say so and offer to add channels. Do not invent results.
- yt-dlp (free) for YouTube and TikTok. Instagram channels need the paid Apify
  actor `apify/instagram-reel-scraper`; skip them unless the user approved the cost.

## Two modes

### Mode A: generate the report (default)
1. Pull each watchlist channel (free platforms only):
   `python3 scripts/watchlist.py pull --limit 40`
   - It pulls ~40 recent videos per channel (not just 7 days): the outlier
     baseline needs the previous 90 days of history.
   - For Instagram entries it prints the paid Apify call and its estimated cost
     and skips them. Only run it after the user says yes (steps in
     `references/data-sources.md`), then add the normalized file to the folder.
   - If a TikTok pull fails 3 times, report that channel as "couldn't fetch"
     (paid fallback: `clockworks/tiktok-scraper`, ask first).
2. Score: `python3 scripts/outlier_score.py <pull-dir>/*.json --out <pull-dir>/scored.json`
3. Report: `python3 scripts/watchlist.py report --mode outliers --scored <pull-dir>/scored.json --days 7 --limit 10 --min-outlier 1.0`
   - Filter: posted in the last 7 days, outlier score >= 1.0, no view floor,
     no engagement floor, all platforms.
   - Ranked by outlier score (highest first), ties by views.
4. If zero videos clear 1.0x in the window, say nothing on the watchlist broke
   1x in the last 7 days and offer to widen the window. Do not invent results.

Do not download, transcribe or label videos in this skill.

### Mode B: set up the daily schedule
If the user asks to "set up", "schedule", "turn on" or "automate" this report,
create a recurring routine with the `routines` skill instead of generating it:
- Daily 07:00 America/Lima unless the user names another time.
- Delivery: chat message to the user.
- Prompt: self-contained: run Mode A of this skill (pull with limit 40, score,
  report --mode outliers --days 7 --limit 10 --min-outlier 1.0); skip Instagram
  unless a standing approval and budget exist; post the ranked list with each
  platform URL; do not analyze.
- It runs on the box; no desktop app needs to stay open.

## Output format
```
Watchlist outliers (1x+) - last 7 days, ranked by outlier score:

1. [<outlier_score>x · <view_count> views] <title> - @<handle>
   <platform_url>
2. ...
```
Rules: numbered in final ranked order (1 = highest outlier score); outlier as a
multiplier (`1.4x`); views abbreviated (`136K`); titles truncated to ~80 chars;
the bare platform URL on its own line is the deliverable. The helper adds
"(young, views still growing)" for videos under 2 days old and "(baseline: all
scraped videos)" when fewer than 3 prior videos were in the 90-day window; keep
those notes. Add one line naming any channel that was skipped (Instagram
without approval, failed TikTok pull).

## Known gaps vs. the original
- Scores are computed from our own scrape, not Sandcastles' full index.
- TikTok views from the free path are rounded (e.g. 1.3M), so close calls near 1.0x are approximate.
- Instagram has no free path.
