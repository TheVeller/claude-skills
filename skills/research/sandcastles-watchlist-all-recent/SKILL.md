---
name: sandcastles-watchlist-all-recent
description: >-
  Use when the user wants every video the local watchlist channels posted in the
  last 7 days, newest first with links and no performance filter; free for
  YouTube/TikTok, no Sandcastles.
metadata:
  origin: external-adapted
  source: "content.game (Kallaway / Content Dept.)"
  credit: "Adapted from content.game material by Kallaway / Content Dept.; rebuilt by TheVeller to run without Sandcastles."
  upstream_license: "sin dato (upstream terms not confirmed)"
---

> Source: adapted from content.game (Kallaway / Content Dept.) "Outlier Video Pulse, all recent" (`sandcastles-watchlist-all-recent`), claimed 2026-10-29. Rebuilt on 2026-10-29 to run without Sandcastles: yt-dlp + optional Apify + local outlier math. Original in /workspace/exports/bot-video/work/content-game/outliervideopulse/.

# Watchlist: All Recent Posts

Surface everything the watchlist creators posted recently, with no performance
bar: a straight chronological feed, newest first, each with a direct link. This
is a quick scan, not a deep dive: never analyze videos, and never start a paid
Apify run without an explicit yes.

See `references/data-sources.md` for sources, prices and limits.

## Requirements
- A watchlist file: `/workspace/exports/bot-video/watchlist.json`
  (`{"channels":[{"platform":"youtube|tiktok|instagram","handle":"@x"}]}`).
  Manage it with `scripts/watchlist.py list | add --platform P --handle @x | remove ...`.
- If the watchlist is empty or missing, say so and offer to add channels. Do not invent results.
- yt-dlp (free) for YouTube and TikTok. Instagram channels need the paid Apify
  actor `apify/instagram-reel-scraper`; skip them unless the user approved the cost.

## Two modes

### Mode A: generate the feed (default)
1. Pull each watchlist channel (free platforms only):
   `python3 scripts/watchlist.py pull --limit 40`
   (40 so the outlier score shown as context has a 90-day baseline; use
   `--limit 15` if the user only wants the feed and doesn't care about the
   score). Instagram entries are skipped with the paid call and its cost
   printed; run it only after a yes (`references/data-sources.md`). Report any
   TikTok channel whose pull failed 3 times.
2. Score (context only): `python3 scripts/outlier_score.py <pull-dir>/*.json --out <pull-dir>/scored.json`
3. Feed: `python3 scripts/watchlist.py report --mode recent --scored <pull-dir>/scored.json --days 7 --limit 25`
   - Everything posted in the last 7 days, no outlier/view/engagement gate.
   - Sorted by `published_at`, newest first.
   - If more than 25 exist, the helper says so; show the rest only if the user wants them.
4. If nothing was posted in the window, say the watchlist was quiet in the last
   7 days and offer to widen the window. Do not invent results.

Do not download, transcribe or label videos in this skill.

### Mode B: set up the daily schedule
If the user asks to "set up", "schedule", "turn on" or "automate" this feed,
create a recurring routine with the `routines` skill instead:
- Daily 07:00 America/Lima unless the user names another time.
- Delivery: chat message to the user.
- Prompt: self-contained: run Mode A of this skill (pull, score, report --mode
  recent --days 7 --limit 25); skip Instagram unless a standing approval and
  budget exist; post the chronological list with each platform URL; do not analyze.
- It runs on the box; no desktop app needs to stay open.

## Output format
```
Your watchlist feed - everything posted in the last 7 days, newest first:

1. [<published_at date> · <outlier_score>x · <view_count> views] <title> - @<handle>
   <platform_url>
2. ...
```
Rules: numbered in final order (1 = most recent post); show the post date;
include the outlier score and abbreviated views as context but do NOT sort by
them; `n/a` when a score couldn't be computed; titles truncated to ~80 chars;
the bare platform URL on its own line is the deliverable. Add one line naming
any skipped channel.

## Known gaps vs. the original
- Outlier scores are our own approximation (see `references/data-sources.md`).
- TikTok free-path views are rounded; Instagram has no free path.
- Dates are UTC (the platforms' timestamps); say so if a post is near midnight.
