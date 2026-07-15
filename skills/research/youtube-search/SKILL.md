---
name: youtube-search
description: Search YouTube for videos via yt-dlp and return structured results (title, channel, views, duration, description) for analysis. Use when the user wants to search YouTube, find top videos on a topic, or pull video metadata.
---

# YouTube Search Skill

Search YouTube for videos and return structured results using yt-dlp.

## Trigger

Use this skill when the user wants to:
- Search YouTube for videos on a topic
- Find top YouTube videos about a query
- Research what's popular on YouTube about a subject
- Get video metadata (views, channel, duration, description) for analysis

## How to Use

When triggered, call the Bash tool to run yt-dlp with the search query.

### Basic Search

```bash
yt-dlp "ytsearch10:{QUERY}" \
  --dump-json \
  --no-download \
  --flat-playlist \
  --no-warnings \
  2>/dev/null
```

Each line of output is a JSON object. Parse and return structured results.

### Result Fields to Extract

From each JSON object, extract:
- `id` → YouTube video ID
- `title` → Video title
- `url` → Full URL: `https://www.youtube.com/watch?v={id}`
- `view_count` → Number of views (may be null for search results)
- `channel` → Channel name
- `channel_url` → Channel URL
- `duration` → Duration in seconds (convert to MM:SS)
- `description` → First 300 chars of description
- `upload_date` → Date in YYYYMMDD format
- `like_count` → Likes (may be null)

### Output Format

Return results as a structured markdown list:

```markdown
## YouTube Search Results: "{query}"

Found {N} videos

| # | Title | Channel | Views | Duration |
|---|-------|---------|-------|----------|
| 1 | [Title](URL) | Channel Name | 1.2M | 12:34 |
...

### Full Details

**1. [Video Title](URL)**
- Channel: Channel Name
- Views: 1,234,567
- Duration: 12:34
- Published: 2024-03-15
- Description: First 300 chars...
```

## Parameters

- `query` — Search query string (required)
- `limit` — Number of results (default: 10, max: 50)
- `sort_by` — Sort preference: `relevance` (default), `views`, `date`

## Notes

- yt-dlp is installed at `/opt/homebrew/bin/yt-dlp`
- Search results may not include view counts (YouTube API limitation with yt-dlp search)
- For view counts, a second pass fetching individual video metadata may be needed
- If view counts are needed: `yt-dlp --dump-json "https://www.youtube.com/watch?v={id}"`

## Example Usage

User: "Search YouTube for the top 5 videos about Claude Code MCP servers"

```bash
yt-dlp "ytsearch5:Claude Code MCP servers" --dump-json --no-download --flat-playlist --no-warnings 2>/dev/null
```

Parse JSON output → return structured table + details.
