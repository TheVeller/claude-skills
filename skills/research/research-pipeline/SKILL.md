---
name: research-pipeline
description: YouTube search + NotebookLM analysis super-skill — searches YouTube, sends videos to NotebookLM for server-side deep analysis, optionally generates a deliverable (infographic, podcast, slides), saves to the vault. Zero Claude tokens for analysis. Use when researching a topic via YouTube or generating research deliverables from video content.
---

# Research Pipeline Skill

A super-skill that combines YouTube search + NotebookLM analysis into a single research workflow. Searches YouTube for videos, sends them to NotebookLM for deep analysis, optionally generates a deliverable (infographic, podcast, slide deck, etc.), and saves everything to the Obsidian vault.

## Token Budget

**This pipeline is designed to use zero Claude tokens for analysis.** NotebookLM processes the corpus server-side (Google's infrastructure). Claude's only job is to orchestrate the pipeline, capture `notebooklm ask` stdout, and write the result to Obsidian. Never re-read large scraped documents in Claude — pass them directly to NotebookLM and let it do the analysis.

## Trigger

Use this skill when the user wants to:
- Research a topic using YouTube as the source
- Analyze trends, gaps, and insights from YouTube videos on a subject
- Generate research deliverables (infographic, podcast, summary) from YouTube content
- Do content research (what's working, view patterns, gaps to exploit)

**Explicit triggers:**
- `/research-pipeline`
- "research [topic] on YouTube"
- "analyze YouTube videos about [topic]"
- "YouTube pipeline for [topic]"
- "find and analyze top videos about [topic]"

## Full Pipeline

### Step 1 — YouTube Search (youtube-search skill)

Search YouTube for the query and collect video URLs + metadata.

```bash
yt-dlp "ytsearch{N}:{QUERY}" --dump-json --no-download --flat-playlist --no-warnings 2>/dev/null
```

Parse results → extract video IDs → build URLs.

**Default**: 10 videos. User can specify (e.g., "top 5", "top 20").

### Step 2 — Create NotebookLM Notebook

Create a dedicated notebook for this research session:

```bash
notebooklm create "{QUERY} Research - {DATE}"
```

Save the notebook ID from output.

### Step 3 — Add YouTube Sources

Add each video URL as a source to the notebook (up to 50):

```bash
notebooklm source add "https://www.youtube.com/watch?v={ID}"
```

Add all videos in sequence. NotebookLM will process the transcripts automatically.

### Step 4 — Wait for Processing

Sources take 30-60 seconds to process. Check status before querying:

```bash
notebooklm source list | grep -E "pending|processing"
# If all rows show "ready", proceed. Otherwise wait 30s and recheck.
```

### Step 5 — Generate Analysis via NotebookLM (zero Claude tokens)

**IMPORTANT: Capture the output — do NOT read it into Claude context.** Pipe stdout directly to a temp file, then write it into the Obsidian note.

```bash
# Run analysis and capture to temp file (NotebookLM processes server-side)
notebooklm ask "Analyze these YouTube videos and provide:
1. KEY THEMES: What are the main topics covered across all videos?
2. TOP INSIGHTS: What are the most important insights or takeaways?
3. CREATOR PERSPECTIVES: How do different creators approach the same topics?
4. GAPS & OPPORTUNITIES: What topics are NOT covered well? What's missing?
5. OUTLIERS: Any surprising or counterintuitive findings?
6. ACTIONABLE TAKEAWAYS: What can someone do with this information?" > /tmp/notebooklm_analysis.txt 2>&1

echo "Analysis captured: $(wc -c < /tmp/notebooklm_analysis.txt) chars"
```

### Step 6 — Generate Deliverable (if requested)

If user requested a specific deliverable, run in parallel with or after Step 5:

| Deliverable | Command |
|-------------|---------|
| Infographic | `notebooklm generate infographic --wait` |
| Podcast | `notebooklm generate audio "deep dive conversation" --wait` |
| Slide deck | `notebooklm generate slide-deck --wait` |
| Mind map | `notebooklm generate mind-map --wait` |
| Flashcards | `notebooklm generate flashcards --wait` |

Download to Research folder:
```bash
RESEARCH_DIR="04_Resources/Research"
notebooklm download infographic "${RESEARCH_DIR}/{QUERY}-{DATE}-infographic.png"
notebooklm download audio "${RESEARCH_DIR}/{QUERY}-{DATE}-podcast.mp3"
```

### Step 7 — Save to Obsidian Vault

**Write the final note by reading from the temp file — never re-read the full corpus in Claude.**

Save to: `04_Resources/Research/{QUERY}-{DATE}.md`

```bash
RESEARCH_DIR="04_Resources/Research"
OUTPUT="${RESEARCH_DIR}/{QUERY}-{DATE}.md"
ANALYSIS=$(cat /tmp/notebooklm_analysis.txt)

cat > "${OUTPUT}" << EOF
---
title: Research — {QUERY}
date: {DATE}
tags: [research, youtube, {topic-tags}]
source: youtube
videos_analyzed: {N}
notebooklm_notebook: {NOTEBOOK_ID}
---

# Research: {QUERY}

## Videos Analyzed

| # | Title | Channel | URL |
|---|-------|---------|-----|
{TABLE}

## Analysis

${ANALYSIS}

## Deliverables

{DELIVERABLE_LINKS_IF_ANY}
EOF

echo "Saved: ${OUTPUT}"
rm /tmp/notebooklm_analysis.txt
```

## Parameters

- `query` — Research topic (required)
- `limit` — Number of videos to analyze (default: 10)
- `deliverable` — Optional: `infographic`, `podcast`, `slides`, `mindmap`, `flashcards`
- `save_to` — Output path in vault (default: `04_Resources/Research/`)

## Example Prompts

```
/research-pipeline Claude Code MCP servers

Research the top 10 YouTube videos about AI agents and give me an infographic

YouTube pipeline: find 5 videos about Obsidian workflows, analyze gaps
```

## Notes

- `notebooklm` CLI must be authenticated: run `notebooklm login` in terminal first
- Deliverables can take 5-15 minutes (NotebookLM processes async)
- Use `--wait` flag to block until deliverable is ready
- Save deliverable files to `04_Resources/Meetings/Research/` alongside the markdown note
- The NotebookLM analysis is done server-side by Google — no Claude tokens used for that step
- yt-dlp installed at: `/opt/homebrew/bin/yt-dlp`

## Adapting to Other Sources

This pipeline isn't just for YouTube. Swap Step 1 for any source:
- PDFs: `notebooklm source add "./file.pdf"`
- Web articles: `notebooklm source add "https://article-url.com"`
- Text: `notebooklm source add --text "paste content here"`
- Drive files: `notebooklm source add "https://drive.google.com/..."`
