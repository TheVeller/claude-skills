# Data sources (replaces the Sandcastles MCP)

Checked 2026-10-29. Prices are Apify FREE-tier list prices read with
`fetch-actor-details` (output.pricing) on that date; higher Apify plans are
cheaper. **Re-read the pricing before every paid run** and show the bill.

| Platform | Free path (default) | What the free path gives | Paid fallback (ask first) |
|---|---|---|---|
| YouTube Shorts | `scripts/fetch_channel.py --platform youtube` (yt-dlp: flat list of the /shorts tab, then one `yt-dlp -j` per video) | exact views, likes, comments, publish timestamp, duration, full title+description, channel subscriber count. Tested on @mkbhd: 4 videos in 6 s. | `streamers/youtube-shorts-scraper` (input `channels`, `maxResultsShorts`, `oldestPostDate`, `sortChannelShortsBy`), US$0.004 per short (+US$0.0013 per short with a date filter) |
| TikTok | `scripts/fetch_channel.py --platform tiktok` (yt-dlp profile grid; needs `curl_cffi`, can fail at random, the script retries 3x) | views/likes/comments/timestamp/caption per video. Tested on @mkbhd: 12 videos in 11 s. **Views are rounded** on the grid (e.g. 1,300,000), **no follower count**, no pinned/sponsored flag. | `clockworks/tiktok-scraper` (input `profiles`, `resultsPerPage`, `profileSorting`, optional paid date filter `oldestPostDateUnified`). US$0.0037 per video + US$0.001 per run (+US$0.0013 per video with the date filter). Gives exact `playCount`, `diggCount`, `commentCount`, `shareCount`, `collectCount`, `authorMeta.fans`, `isPinned`, `isSponsored`/`isAd`. |
| Instagram Reels | **none**: instagram.com redirects yt-dlp to the login page, and we never use cookies or log in to scrape | nothing | `apify/instagram-reel-scraper` (input `username` [array], `resultsLimit`, `onlyPostsNewerThan`, `skipPinnedPosts`). US$0.0026 per reel + US$0.001 per run. Gives `videoPlayCount`, `likesCount`, `commentsCount`, `caption`, `timestamp`, `url`, `videoDuration`, `videoUrl`, `isPinned`, `paidPartnership`. Do NOT tick the paid add-ons (`includeSharesCount`, `includeTranscript` US$0.048/min, `includeDownloadedVideo`): transcribe locally instead. Followers: `apify/instagram-profile-scraper` `followersCount`, US$0.0026 per profile. |
| X / Twitter | `x` namespace public reads (read the x-api-mcp-guide skill first) | posts and metrics of X accounts | n/a |

## Running a paid Apify actor (only after an explicit yes)
1. `fetch-actor-details` with `output: {pricing: true}`: confirm the price is unchanged.
2. Show the bill: `channels x videos x price + runs x start fee`, e.g. 3 IG channels x 60 reels x 0.0026 + 3 x 0.001 = US$0.47.
3. `call-actor` with the input above, `callOptions.maxTotalChargeUsd` set to the approved amount, `waitSecs: 45`; poll with `get-actor-run`.
4. `get-dataset-items` with `write_to_file: true` (CallDynamicTool) and `limit` >= the item count, then copy the item array into a JSON file and run
   `scripts/normalize.py --source apify-ig-reels|apify-tiktok|apify-yt-shorts <file> --out norm.json`.
5. Report what was actually charged (from `get-actor-run` stats) next to the estimate.

## Helpers (all in scripts/, pure Python + yt-dlp/ffmpeg; tested 2026-10-29)
- `fetch_channel.py`: free pull (YouTube, TikTok) -> normalized JSON.
- `normalize.py`: yt-dlp and the 3 Apify actors -> one schema (`uuid, platform, handle, title (full caption), published_at, view_count, like_count, comment_count, share_count, engagement_rate, platform_url, duration_s, thumbnail, follower_count, is_pinned, paid_partnership`).
- `outlier_score.py`: outlier score = views / mean views of the same channel's videos posted in the 90 days before it (video excluded). Flags `baseline: fallback_all` (fewer than 3 prior videos: uses all other scraped videos) and `immature` (< 2 days old).
- `watchlist.py`: the local watchlist (`/workspace/exports/bot-video/watchlist.json`) plus `pull` and `report`.
- `prep_video.py`: download + audio + local transcription (`stt_words.py`, faster-whisper in `/workspace/tools/venv`) + hook frames (0/0.5/1/2/3 s) + 4x3 contact sheet + an `analysis.json` with empty label fields for the agent.
- `merge_labels.py`: copies filled labels back into the scored file.
- Denser viewing: the `/watch` skill from claude-video at `/workspace/tools/claude-video/skills/watch` (frames with timestamps).

## What we can NOT replicate (say so in reports)
- Sandcastles' exact outlier formula and its full-history baseline: ours is computed from what we scraped, so it is an approximation.
- Sandcastles' `production score` and its pre-labelled analysis fields: here the agent writes the labels itself from the transcript and frames, and they must be marked as the agent's judgment.
- The watchlist-wide aggregates `top_topics` / `top_hooks` / `top_formats` across Sandcastles' index: we only aggregate our own analyzed videos.
- Sandcastles video pages (`sandcastles_url`): links go to the platform URL instead.
- Instagram for free, TikTok follower counts and exact TikTok views for free.
