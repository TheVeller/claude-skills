---
name: creator-breakdown
description: >-
  Use when someone wants a newsletter-style teardown of how a creator grew and
  monetizes (viral clusters vs durable steps, collab vs solo, comment/DM funnel,
  CTA coverage, themes) from scraped history and local outlier math; no
  Sandcastles.
metadata:
  origin: external-adapted
  source: "content.game (Kallaway / Content Dept.)"
  credit: "Adapted from content.game material by Kallaway / Content Dept.; rebuilt by TheVeller to run without Sandcastles."
  upstream_license: "sin dato (upstream terms not confirmed)"
---

> Source: adapted from content.game (Kallaway / Content Dept.) "Creator Breakdown" (delivered under the "Creator Breakout Detector" form), claimed 2026-10-29. Rebuilt on 2026-10-29 to run without Sandcastles: yt-dlp / optional Apify for the history, `outlier_score.py` for the score, the original 5 engine scripts unchanged. Original in /workspace/exports/bot-video/work/content-game/creator-breakout-skill/.

# Creator Breakdown

A repeatable teardown that reverse-engineers how a creator broke out **and how
they monetize**: the analysis behind a "Creator Breakdown" newsletter. It
produces: the viral cluster (or sustained step), the eras (pre/spike/post), the
collab-vs-solo lever, the comment/ManyChat funnel proof, the topic timeline, and
a monetization read.

The performance signal is **outlier score** = a video's views ÷ the channel's
trailing 3-month average. It measures content quality independent of audience
size, which is why a <100K-follower creator can still be analyzed rigorously.
Here it is computed locally by `scripts/outlier_score.py` from the scraped
history (90-day window before each video, the video itself excluded), so it is
our approximation of Sandcastles' number.

Tool map (what replaced each Sandcastles tool):

| Sandcastles tool | Replacement here |
|---|---|
| `channel_recap` (resolve channel, followers) | `scripts/fetch_channel.py` (channel row: name, handle, follower count when the platform gives it) |
| `add_channels_to_watchlist` | not needed (optional: `scripts/watchlist.py add`) |
| `search_my_videos` (3 × limit-25 sweep) | one full pull of the profile grid with `fetch_channel.py` (free: YouTube, TikTok) or a paid Apify actor (Instagram; TikTok fallback) |
| `outlier_score` field | `scripts/outlier_score.py` |
| `get_video_details` (likes/comments) | already in the scraped rows |
| `analyze_video` labels (for `lego_bricks.py` / `signature_diff.py`) | `scripts/prep_video.py` + the agent's labels, merged with `scripts/merge_labels.py` |

Sources, prices and limits: `references/data-sources.md`.

## When to use which tool

- **One clean question — "when did X break out?"** → run `scripts/detect_breakout.py`
  alone (sustained step-change). The separate "creator-breakout-detector" skill
  was never delivered by content.game; this script is its engine.
- **Full teardown / newsletter / "how do they make money?"** → use this skill.
  It runs the same engine *and* the spike/collab/funnel layers below.
- **Hooks specifically — "why do their hooks win / write me hooks"** → use the
  `hook-machine` skill (deep-analyzes hooks, builds a rubric, writes & grades).
  A full teardown often ends with a hook pass: once you've found the winning
  videos here, hand their URLs to hook-machine for the hook formula.

## What you need

A single channel: handle (`@callanfaulkner`) or profile URL, plus its platform
(YouTube, TikTok or Instagram).

---

## Configuration

**`LOOKBACK_DAYS = 730`**: the teardown analyzes the trailing 730 days (~2
years) of the creator's history. This is the single knob that bounds the entire
pull. 730 days captures the full arc (rise → spike → current era) of essentially
every short-form creator while keeping data volume low. Treat it as fixed; only
touch it for the rare creator with a materially longer history.

---

## Step 1 — Resolve the channel and price the pull

- Confirm the handle and platform with the user if ambiguous.
- **YouTube / TikTok: free.** Estimate time: YouTube needs one call per video
  (~1-2 s each, so 300 videos ≈ 5-10 min); TikTok returns the grid in one pass.
- **Instagram: paid** (`apify/instagram-reel-scraper`, US$0.0026 per reel +
  US$0.001 per run at FREE-tier prices on 2026-10-29). Estimate the reel count
  for 730 days (posts per week × 104), show the bill, e.g. "≈ 400 reels ≈
  US$1.04", and wait for an explicit yes. Follower count needs
  `apify/instagram-profile-scraper` (US$0.0026, one profile).
- If the free TikTok pull fails 3 times, offer `clockworks/tiktok-scraper`
  (US$0.0037 per video + US$0.001 per run; it also returns exact views, follower
  count, pinned and sponsored flags) with its bill.

## Step 2 — Pull the video history (bounded)

Pull everything posted in the trailing **`LOOKBACK_DAYS` (730)**, with no view,
engagement or outlier filter. Work in
`/workspace/exports/bot-video/work/breakdowns/<handle>-<date>/`.

- YouTube: `python3 scripts/fetch_channel.py --platform youtube --handle @x --limit 400 --out page_yt.json`
  (raise `--limit` until the oldest video is older than 730 days; drop older rows
  only after scoring, because the oldest in-window videos need their 90-day baseline).
- TikTok: `python3 scripts/fetch_channel.py --platform tiktok --handle @x --limit 400 --out page_tt.json`
- Instagram (approved): `call-actor` `apify/instagram-reel-scraper` with
  `{"username": ["x"], "resultsLimit": <est>, "onlyPostsNewerThan": "<today − 820 days>"}`
  (730 + 90 for the baseline), `callOptions.maxTotalChargeUsd` = the approved
  amount; save the dataset items and run
  `python3 scripts/normalize.py --source apify-ig-reels items.json --out page_ig.json`.

Unlike the Sandcastles version there is no 25-item cap and no cursor timeout:
the full grid comes back in one pull, so the old 3-window sweep is not needed.
Caveats to state in the report:
- If the platform hid part of the grid (deleted/private videos, a pull that
  stopped early), the baseline can be biased. Report the pulled count and date span.
- Free TikTok views are rounded (e.g. 1.3M), so small outlier differences are noise.
- Views are a snapshot taken today: the newest videos (< 2 days, flagged
  `immature`) are still growing.

**Keep the full caption** (normalize.py stores title + description / the full
TikTok and Instagram caption in `title`): do not abridge it, or the
CTA-coverage detector will miss real CTAs.

## Step 3 — Score and combine into one file

```
python3 scripts/outlier_score.py page_*.json --out /tmp/cb_videos.json
```

Each video then has `published_at` and `outlier_score` (null when views or date
are missing; never invented), plus `view_count`, `engagement_rate` ((likes +
comments + shares) ÷ views; shares are missing on YouTube and on free
Instagram), `title`, `platform_url`. The engine scripts read exactly these
names. Rows flagged `baseline: fallback_all` (start of history, fewer than 3
prior videos in 90 days) are less reliable; mention it if they matter.

## Step 4 — Run the engines

```
python3 scripts/detect_breakout.py    /tmp/cb_videos.json --out /tmp/cb_step.json
python3 scripts/breakdown_analyze.py  /tmp/cb_videos.json --out /tmp/cb_spike.json
python3 scripts/funnel_consistency.py /tmp/cb_videos.json --top-k 10 \
        --offer-keywords "academy,program,bootcamp,course,coaching,workshop,masterclass" \
        --out /tmp/cb_funnel.json
```

- **detect_breakout.py** → is there a *sustained* upward step? (`status: ok`
  with a trigger video, or `no_upward_inflection`).
- **breakdown_analyze.py** → the *spike cluster*, the pre/spike/post eras, a
  `verdict` of `transient_spike_reverted` / `transient_spike` /
  `possible_durable_step`, `collab_vs_solo`, `top_by_outlier`, and
  `vanity_virality` flags.
- **funnel_consistency.py** → **consistency vs spike-reliance** (view CV,
  max/median ratio, core-band share, cadence), **CTA coverage** (% of all and
  of top-K posts carrying a CTA), and the **offer vs non-offer mix** of top
  videos + how many CTAs ride non-offer content. Tune `--offer-keywords` to the
  creator's actual product. **Requires FULL captions** — make sure Step 2/3 kept
  the complete `title`/`description` text, not an abridged title, or CTA
  detection will under-count.

> **Optional `--since YYYY-MM-DD`** on `detect_breakout.py` and
> `breakdown_analyze.py` hard-scopes the analysis to videos on/after that date
> and auto-prints a clipped-data note. Because `LOOKBACK_DAYS` already bounds the
> pull, you rarely need it — use it only to re-scope an existing JSON without
> re-pulling.

These cross-check each other: a creator the detector calls
`no_upward_inflection` and the funnel script calls **tight/consistent** (low CV,
low max/median) is the *Shelby pattern* — deliberately never-viral, winning on
funnel, not spikes. A `transient_spike_reverted` + **spike-reliant** combo is
the *launch-spike* pattern.

**Read both.** The interesting case (and the common one for "anti-viral,
stacking-singles" creators) is `no_upward_inflection` from the detector +
`transient_spike_reverted` from the analyzer: that means the creator did **not**
durably level up — they fired a **launch spike** that mean-reverted. Say that
plainly; it's usually the real story.

## Step 5 — Verify the monetization funnel (free)

Take the **top 3–4 spike/outlier videos** from `cb_videos.json` (the scrape
already carries `like_count` and `comment_count`; if a row lacks them, re-read
that one video with `yt-dlp -j --skip-download <url>`). Compare
`comment_count` vs `like_count`:

- **comments ≫ likes** = a ManyChat/comment-to-DM trigger firing (the lead
  engine). Quote the numbers — they're the proof the funnel works.
- **high view_count + tiny comment_count + low `engagement_rate` (≤1.5%)** =
  *vanity virality*: reach without lead capture. Flag it even when it's one of
  their "biggest" videos — it's the counter-example to content×audience×product
  fit, and it's often hiding inside the "breakout."

Also read the CTA in each caption (e.g. "Comment BOOTCAMP") to name the funnel
entry point.

## Step 6 — Map the topic timeline to the offer

Skim titles oldest→newest and note when the creator's framing shifts (tool →
"hire AI" → "AI team/architect" → "AI agent workflows"). Tie the spike's topic
to the product they were selling at that moment (look for launch/CTA language
near the spike dates). The thesis to test: **content × audience × product fit** —
does the content attract exactly the buyer for the offer?

## Step 6b — Theme-pillar the top videos (the "viral ≠ offer" check)

Read the captions of the **top ~10 by outlier** and cluster them into 2–4
content **pillars**. The non-obvious finding is usually that *most of the top
videos are NOT about the offer*. Typical pillars:

- **Magnet / lifestyle** — aspirational, low-production, pulls cold audience
  (the pink-Porsche / Miami / "day in the life" posts).
- **Filter / polarizing belief** — a hyper-specific worldview that *repels* the
  wrong audience and bonds the right one ("men won't provide for you"). High
  comment volume, strong saves, low-to-mid views — it does the sorting work.
- **Offer / CTA** — the posts actually about the product (the bootcamp/academy).
  Usually the *minority* of top performers.
- **Proof / authority** — results, testimonials, credentials, behind-the-scenes
  that make the offer believable.

Name the split explicitly (e.g. "7 of the top 10 are Magnet/Filter, only 2 are
Offer"). That ratio is the headline insight: the audience is built by content
that is **not** the offer, and the offer is monetized by the funnel that rides
on top of every post.

## Step 7 — Build the report (make it as visual as possible)

The output is a newsletter-style teardown. **Visualize every part of the report
that can be visualized — render it as visually as possible wherever it's
relevant.** Default to a chart, timeline, or diagram over a paragraph or table
whenever the underlying data supports one. Use the visualization widget (or an
inline chart/SVG) and pair each visual with a one-to-two-line plain-language
read so the takeaway is never buried.

Visualize at minimum, wherever the data exists:

- **Outlier-score timeline** — every video plotted by `published_at` (x) vs
  `outlier_score` (y), with the inflection date and the spike cluster marked.
  This is the spine of the whole story; always include it.
- **Era comparison** — pre / spike / post median outlier and median views as a
  grouped bar chart, so the step-vs-spike verdict is obvious at a glance.
- **Collab vs solo** — side-by-side bars of mean outlier.
- **Consistency** — view distribution (histogram or box plot) showing the core
  band vs the spike, with the max/median ratio called out.
- **CTA coverage** — % of all posts and of the top-K carrying a CTA (gauge or
  bar), plus the offer vs non-offer split of top performers (stacked bar / donut).
- **Content pillars** — the top ~10 videos colored by pillar (Magnet / Filter /
  Offer / Proof), so "most winners aren't the offer" is *shown*, not just stated.
- **Funnel proof** — comments-vs-likes for the top 3–4 videos as paired bars, to
  show the ManyChat trigger firing.

If a section genuinely has no visual angle, write it as tight prose — but the
default is: show it, don't just tell it.


## Optional — LEGO bricks and signature diff (needs labels)

`scripts/lego_bricks.py` (what the top-K hold constant vs. vary) and
`scripts/signature_diff.py` (what changed at the inflection) read label fields
(`topic`, `*_category`, `*hook*`, `format_category`, `story_structure`).
Sandcastles filled those via `analyze_video`; here:

1. For the top ~10 by outlier (and, for signature_diff, ~8 before and ~8 after
   the inflection), run
   `python3 scripts/prep_video.py <url> --dir analyses/<id> --lang <en|es> --meta <row.json>`
   (free, ~10-25 s per short).
2. Read each transcript and the hook frames / contact sheet, fill `labels` in
   `analysis.json` (only what the evidence shows).
3. `python3 scripts/merge_labels.py /tmp/cb_videos.json analyses/ --out /tmp/cb_analyzed.json`
4. `python3 scripts/lego_bricks.py /tmp/cb_analyzed.json --top-k 10` and
   `python3 scripts/signature_diff.py /tmp/cb_analyzed.json --inflection <YYYY-MM-DD>`

Say in the report that these labels are the analyst's reading.

## Known gaps vs. the original
- Outlier score is our approximation from the scraped history, not Sandcastles' index.
- Instagram history is paid; free TikTok views are rounded and lack follower counts.
- Video labels are written by the agent, not pre-computed.
