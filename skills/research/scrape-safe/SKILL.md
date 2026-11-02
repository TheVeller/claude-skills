---
name: scrape-safe
description: >-
  Use this before scraping any public web source into a dataset: legality
  checklist, cheapest-tool order, and the per-run deliverable.
---
# scrape-safe

Turn one public web source into a clean dataset where every row carries its source URL and capture date, using the cheapest allowed tool.

## 1. Pre-flight checklist (stop if any fails)
- The source is public: no login, no someone else's session, no paywall bypass.
- Read robots.txt and the site's Terms of Service; quote the relevant lines in the run sheet. If they forbid automated access to the target paths, stop and report.
- No evasion: no rotating proxies, no captcha solving, no disguises to get past a block. If blocked, stop and report.
- Social networks: only public X posts (via FxTwitter) and public YouTube subtitles are in scope. Instagram, TikTok, LinkedIn and Facebook are out: use the official API or hand off.
- No personal data: drop emails, phone numbers, and individual people's profiles from the output.
- Out of scope: enrichment, building directories, interpretation, publishing, purchasing. Hand those off.

## 2. Tool order (cheapest first)
1. Official API or open dataset.
2. Plain HTTP fetch (curl or WebFetch) + Python, free. Respect rate limits (about 1 request per second).
3. Scrapling (Fetcher and parser only) for static pages, or agent-browser + defuddle for JS pages, only if robots and ToS allow it.
4. X public posts via FxTwitter, YouTube via subtitles, OCR for screenshots, ElevenLabs Scribe for audio.
5. Exa, Tavily or Firecrawl to find or extract pages.
6. Apify actor with a low item count and an explicit spend cap. Any paid run needs the owner's explicit yes first, with the estimated cost stated.

## 2b. Installed kit on this machine
- Static pages: curl + Python; Scrapling (`/home/box/.venvs/scrapling`, Fetcher and parser only, never StealthyFetcher).
- JS pages: `agent-browser open <url>` then `agent-browser get text` / snapshot; clean text with `defuddle parse <url|file> --markdown`.
- X public posts: `curl https://api.fxtwitter.com/<user>/status/<id>` (JSON).
- YouTube: `yt-dlp --skip-download --write-auto-subs --sub-langs es,en <url>`.
- Screenshots/images: RapidOCR (`/home/box/.venvs/ocr/bin/python`, `from rapidocr_onnxruntime import RapidOCR`).
- Audio: ElevenLabs Scribe (speech-to-text) via the ElevenLabs connector.
- Discovery/extraction: Exa, Tavily, Firecrawl; Apify with low count and spend cap.
- Instagram/TikTok/LinkedIn/Facebook stay out of scope.

## 3. Build the dataset
- One row per record, normalized columns, plus source_url and fetched_at (ISO date) on every row.
- Deduplicate; keep raw values; never invent or fill missing data.

## 4. Deliverable per run
A run sheet with source, tool used, robots/ToS check (quoted), row count, cost, date, and known limits. Plus a CSV or JSON file and a 5-row sample in the reply. No request, no run.
