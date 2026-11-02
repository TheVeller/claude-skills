---
name: sandcastles-channel-diagnostic
description: >-
  Use when someone wants to deep dive, analyze or reverse-engineer one or more
  creator channels (top topics, hooks, hidden insights, formats) as an HTML
  report, built from scraped metrics, local transcripts and frames; no
  Sandcastles.
metadata:
  origin: external-adapted
  source: "content.game (Kallaway / Content Dept.)"
  credit: "Adapted from content.game material by Kallaway / Content Dept.; rebuilt by TheVeller to run without Sandcastles."
  upstream_license: "sin dato (upstream terms not confirmed)"
---

> Source: adapted from content.game (Kallaway / Content Dept.) "Deep Channel Analysis" (`sandcastles-channel-diagnostic`), claimed 2026-10-29. Rebuilt on 2026-10-29 to run without Sandcastles: yt-dlp / optional Apify for metrics, local outlier math, local transcription (faster-whisper) and frames (ffmpeg); the agent writes the labels. Original in /workspace/exports/bot-video/work/content-game/deepchannelanalysis/.

# Channel Diagnostic

Turn any list of social channels into a per-channel diagnostic that answers one
question for each channel: **what is actually working here, and what can I steal?**

Think of yourself as a film editor handed hours of raw footage. The scrapers
and the local tools give you the raw clips (each analyzed video is a clip: its
metrics, transcript and frames). Your job is not to hand back the footage, it's
to cut it into a tight, watchable story per channel across four reels:
**Topics, Hooks, Hidden Insights, Formats.**

Tool map (what replaced each Sandcastles tool):

| Sandcastles tool | Replacement here |
|---|---|
| `add_channels_to_watchlist` | nothing to register; optionally `scripts/watchlist.py add` to keep the channel on the local watchlist |
| `channel_recap` (recent videos + views + outlier) | `scripts/fetch_channel.py` (free: YouTube, TikTok) or a paid Apify actor (Instagram; TikTok fallback), then `scripts/outlier_score.py` |
| `analyze_video` (deep payload, 1 credit) | `scripts/prep_video.py` (download, transcript, hook frames, contact sheet; free, ~10-25 s per short on the box CPU) + YOU fill the labels in `analysis.json` |
| `get_video_details` | already in the scraped row (views, likes, comments, caption) + `transcript.txt` |
| `top_topics` / `top_hooks` / `top_formats` | no equivalent (they were watchlist-wide). Cluster the channel's own labels instead |
| `current_org_usage` (credits) | no credits. For Apify: re-read pricing with `fetch-actor-details` and show the bill |

Sources, prices and limits: `references/data-sources.md`.

---

## The golden rule: never spend money the user didn't approve

YouTube and TikTok pulls, downloads and transcription are **free** (they only
cost box time). Instagram has **no free path**: it needs the paid Apify actor
`apify/instagram-reel-scraper` (US$0.0026 per reel + US$0.001 per run at
FREE-tier prices on 2026-10-29). The TikTok paid fallback is
`clockworks/tiktok-scraper` (US$0.0037 per video + US$0.001 per run).

So the flow does all the free work first (gather and rank candidates), then
shows the user the exact bill for any paid scrape and the time estimate for the
local analysis, then proceeds only on an explicit "go". If the user ever seems
unsure, stop and confirm. A surprise charge is the worst possible outcome of
this skill.

---

## Step 1 — Intake (ask before doing anything that costs)

You need four things. If the user already gave some in their message, don't
re-ask; just confirm what's missing.

1. **Which channels?** Accept handles (`@mkbhd`), URLs, or names, across YouTube /
   TikTok / Instagram. List them back so the user can confirm spelling, and say
   up front which ones are free (YouTube, TikTok) and which need a paid scrape
   (Instagram).

2. **How many videos per channel?** Ask: *"How many recent videos should I look at
   per channel?"* If they don't know, **recommend 30**: enough to see real
   patterns without hours of processing.

3. **Top performers or most recent?** Ask which set of videos to analyze, and
   **recommend top performers**: *"I'd suggest the top-performing videos in a date
   range rather than just the most recent: you want to learn what wins, not what's
   average. But I can do either."*
   - **Top performers** → pull the channel's recent videos, rank by outlier score
     (then views), take the top N within the date range.
   - **Most recent** → take the last N videos posted within the date range.

4. **What date range?** Ask how far back to look. If they don't know, **suggest the
   last 90 days**: recent enough to reflect what's working now, wide enough to have
   a real pool to rank from.

---

## Step 2 — Gather candidates (free) and price the job

Work in `/workspace/exports/bot-video/work/diagnostics/<date>-<channels>/`.

1. **Pull recent videos.** Pull generously: at least 2-3× `N`, and enough to
   cover the date range **plus 90 days before it** (the outlier baseline needs
   that history).
   - YouTube: `python3 scripts/fetch_channel.py --platform youtube --handle @x --limit 90 --out yt_x.json`
   - TikTok: `python3 scripts/fetch_channel.py --platform tiktok --handle @x --limit 90 --out tt_x.json`
     (retries 3x; if it still fails, offer the paid fallback with its bill).
   - Instagram: no free path. Prepare the Apify call (input `username`,
     `resultsLimit`, `onlyPostsNewerThan`) and its bill, and hold it for Step 2.4.
2. **Score:** `python3 scripts/outlier_score.py yt_x.json tt_x.json ... --out scored.json`
   Check `baseline` (`fallback_all` = too little history) and `immature` flags.
3. **Rank and select** per the user's choice (top performers vs. most recent),
   within the date range, trim to `N` per channel. Save the selection list.
4. **Show the bill and the time, and get the green light**, e.g.:

   > Here's what I'm about to analyze:
   > • @channelA (TikTok): 30 videos, free, ~10 min of local processing
   > • @channelB (YouTube): 30 videos, free, ~10 min
   > • @channelC (Instagram): needs a paid scrape: 90 reels × US$0.0026 + US$0.001 ≈ **US$0.24**, then 30 videos of local processing
   > Want me to run all three, or just some? You can also lower the per-channel count.

   Let the user drop channels or lower counts. Only proceed on an explicit
   confirmation. For an approved paid run, follow `references/data-sources.md`
   (cap with `maxTotalChargeUsd`, report the real charge afterwards).

---

## Step 3 — Analyze the selected videos (local)

For each approved channel, for each selected video:

```
python3 scripts/prep_video.py <platform_url> --dir analyses/<channel>/<video_id> --lang <en|es> --meta <video-row.json>
```

(For Instagram, pass the reel's `videoUrl` from the Apify row instead of the
page URL, because instagram.com is behind login. `videoUrl` links expire, so
process them soon after the scrape.)

Then **read the transcript and look at the hook frames and the contact sheet**
and fill the `labels` in that video's `analysis.json`: topic, idea seed, why it's
interesting, unique angle, spoken hook (verbatim) + hook category + madlib,
visual hook, on-screen text hook, hook alignment, storytelling format + why it
works, contrast mechanism, story structure (timestamps from `words.json`), CTA
type + placement, visual layout, production notes. For more frames, use the
`/watch` skill at `/workspace/tools/claude-video/skills/watch`.

Practical notes:
- Work **one channel at a time** so a failure doesn't strand the user mid-run.
- If a video fails (removed, private, download blocked), skip it, note it, keep going.
- Give progress updates on long runs ("video 12 of 30").
- If a video has no speech (`non_verbal: true`), analyze the visual and on-screen hook instead.
- Keep each channel's analyses together. That bundle *is* the evidence you
  synthesize the four sections from. Do not analyze across channels into one
  pile: this report is **strictly per-channel**.
- Never fill a label you can't support from the transcript, frames or metrics.

---

## Step 4 — Synthesize the four sections, per channel

For each channel, read across that channel's analyses and write the four reels.
**Synthesize, do not dump.** A list of 30 videos is footage, not a story.
Cluster, rank, name the pattern, and cite 2–3 real examples (with their platform
links and thumbnails) as proof.

The four sections, every channel, in this order:

1. **Top Performing Topics**: what subjects consistently overperform. Cluster the
   videos by topic/idea seed, rank clusters by performance, name each cluster
   specifically ("Clawbot setups", not "AI").

2. **Top Performing Hooks**: what opening moves work. Group by hook category, then
   surface the actual spoken-hook template/madlib underneath (the reusable
   "Most people think X, but actually Y" shape), so the viewer can copy the pattern.

3. **Hidden Insights**: the non-obvious stuff. This is the highest-value reel: the
   patterns a casual viewer scrolling the channel would miss. Cadence, hook↔topic
   pairings, production tricks, structural habits, contrarian angles, length, CTA
   placement. Say *why* it matters, not just *what* it is.

4. **Top Performing Formats (+ other patterns)**: what structural styles win
   (Tutorial, Breakdown, Hot Take, Framework, etc.) and *why they work* for this
   channel, plus any other repeatable pattern you spotted that doesn't fit the
   first three buckets.

Read **`references/synthesis-guide.md`** before writing: it has the detailed
method for each section, how to rank, what makes an insight "non-obvious," and the
citation rules. There is no watchlist-wide aggregate here; your per-channel truth
comes from that channel's own analyses.

---

## Step 5 — Build the interactive HTML report

Build the report from **`assets/report-template.html`**. It's a complete, styled,
self-contained page (DM Sans, the blue→indigo palette, clean white cards on light
gray) with one fully-populated example channel block and `<!-- CLONE PER CHANNEL -->`
and `<!-- CLONE PER VIDEO -->` markers.

1. Read the template.
2. Duplicate the channel block once per channel and fill in real data.
3. Within each channel, duplicate the video card markup for each cited example and
   fill in the real thumbnail, title, metrics, and the **platform link** (every
   video reference must be clickable through to the video). Platform thumbnail
   URLs can expire; for a durable report embed the local `hook_0s.jpg` as base64.
4. Remove leftover example/placeholder content so only real data ships.
5. In the header line, state: N videos per channel · date range · selection basis ·
   "outlier = views ÷ the channel's trailing 90-day average from scraped data".
6. Save as `/workspace/exports/bot-video/work/diagnostics/channel-diagnostic-<channels>-<date>.html`
   and present it to the user.

Keep it strictly per-channel. Do **not** add a cross-channel comparison section:
each channel stands alone as its own diagnostic.

---

## Tone with the user

The people running this are creators and marketers, not engineers. Talk in plain
terms, be explicit about any money and about how long the local processing will
take, and make the hand-off feel like a finished briefing they can act on, not a
data dump. When you deliver the report, say one or two sentences on the single
biggest takeaway per channel, then point them to the file.

## Known gaps vs. the original
- Outlier scores come from our own scrape (approximation of Sandcastles').
- No vendor "production score" or pre-labelled analysis: labels are the agent's
  reading of transcript and frames, and the report says so in its footer.
- No watchlist-wide `top_topics` / `top_hooks` / `top_formats` cross-check.
- Instagram needs a paid scrape; free TikTok views are rounded and lack follower counts.
