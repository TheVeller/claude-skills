# Synthesis Guide — turning analyzed videos into the four reels

> Adapted from content.game (Kallaway) for the local, no-Sandcastles pipeline.

You have a bundle of analyzed video payloads for **one channel**. This guide is how
you turn that bundle into the four sections of the report. Apply it per channel,
independently. Never merge channels.

The mindset: a viewer could already scroll this channel and see the videos. Your
value is the **pattern they can't see** by scrolling — the through-line across 30
videos. Every section should make the viewer think "oh, I wouldn't have noticed
that." If a section reads like a caption of one video, you've under-synthesized.

## What each analyzed payload gives you

Each video folder made by `scripts/prep_video.py` holds `analysis.json` with:
the scraped surface metrics (views, likes, comments, engagement rate, outlier
score, posted date, thumbnail, platform URL), the local transcript
(`transcript`, plus `hook_words_first_3s`), the opening frames
(`hook_0s/0.5s/1s/2s/3s.jpg`) and a 4x3 contact sheet (`sheet.jpg`). You fill
its `labels` yourself after reading the transcript and looking at the frames:
video summary, topic, idea seed, why it's interesting, unique angle, spoken
hook + hook category + madlib, visual hook, on-screen text hook, hook
alignment, storytelling format + why it works, contrast mechanism (common
belief vs. contrarian reality), story structure (timestamped from
`words.json`), CTA type + placement, visual layout, production notes.

These labels are YOUR reading, not a vendor's pre-computed analysis. Fill only
what the evidence shows; leave a field null rather than guess. There is no
numeric "production score": describe production in words (`production_notes`).

The **outlier score** (views ÷ the channel's trailing 90-day average, computed by
`scripts/outlier_score.py`) is your performance compass — it's how far a video beat the
channel's own baseline, so it isolates "this overperformed" from "this channel is
just big." Rank by outlier score first, views second.

---

## Section 1 — Top Performing Topics

**Goal:** the 3–5 subject territories that consistently overperform for this channel.

Method:
1. Read every video's `topic` and `idea seed`. Cluster into a handful of specific
   territories. Name them concretely — "Self-hosting home servers," not "Tech."
2. Rank clusters by the performance of their videos (median/peak outlier score).
3. For each top cluster: one line on what the territory is, why it overperforms for
   *this* channel, and 2–3 example videos as proof (thumbnail + title + outlier +
   link).

Avoid: generic buckets ("AI," "money," "fitness"). If two clusters are basically
the same angle, merge them. Better three sharp territories than seven mushy ones.

---

## Section 2 — Top Performing Hooks

**Goal:** the opening moves that earn the watch, in a form the viewer can reuse.

Method:
1. Group videos by `hook category` (curiosity gap, contrarian reframe, personal
   story, stakes/threat, etc.).
2. Under each category, pull the actual **spoken-hook template** — strip the specific
   words down to the reusable shape: "Most people think X, but actually Y," "I tried
   X for N days," "Here's why X is about to Y." The template is the gold; it's what
   they copy.
3. Rank categories by how the videos using them performed. Cite the real hook line
   from 2–3 top examples (quote it), with links.
4. If hook alignment data is present, note when the spoken/visual/text hooks
   reinforce each other — tight alignment is often the real reason a hook lands.

Avoid: just naming categories. "They use curiosity gaps" is worthless without the
template and a real example the viewer can model.

---

## Section 3 — Hidden Insights

**Goal:** the highest-value reel — the non-obvious through-lines a scroll would miss.

This is where the report earns its keep. Look for second-order patterns *across* the
bundle, not facts about any single video:
- **Pairings:** a specific hook type that only wins on a specific topic.
- **Cadence/length:** optimal runtime, or a posting rhythm that correlates with hits.
- **Structure habits:** a repeated story structure, a signature cold-open, a
  recurring mid-video reset.
- **Production tells:** a visual layout or production-score band that tracks with
  outliers.
- **Contrarian engine:** whether their wins lean on a common-belief-vs-reality flip,
  and which beliefs they keep attacking.
- **CTA behavior:** where and how they convert, and whether the winners do it
  differently from the rest.

For each insight: state the pattern, the evidence (how many videos / which ones),
and **why it matters** — what the viewer should *do* with it. An insight without a
"so what" is just trivia. Aim for 3–6 real ones; don't pad.

---

## Section 4 — Top Performing Formats (+ other patterns)

**Goal:** the structural styles that win, and why they work for this channel.

Method:
1. Group by `storytelling format` (Tutorial, Breakdown, Hot Take, Framework,
   Monologue, Listicle, etc.).
2. Rank by performance. For each top format, explain *why it works for this channel
   specifically* (using your `why_format_works` labels), with 2–3 examples.
3. Add a short **"other patterns"** note for anything repeatable that didn't fit
   Topics/Hooks/Insights — a signature edit, a recurring series, a thumbnail style.

---

## Ranking and citation rules (all sections)

- **Rank by outlier score, then views.** Outlier score controls for channel size.
- **Always cite real videos.** Every claim is backed by 2–3 example videos with
  their real thumbnail, title, metrics, and clickable platform link. No invented
  titles or numbers — if it isn't in the scraped data or the transcript, don't state it.
- **Quote real hook lines** where relevant; a paraphrase loses the texture.
- **Honesty over volume.** If a channel only yields two real topic clusters, ship
  two. A padded section reads as noise and erodes trust in the whole report.
- **Per-channel only.** Never let one channel's patterns leak into another's section.
