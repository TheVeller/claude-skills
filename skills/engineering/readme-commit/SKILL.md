---
name: readme-commit
version: 0.3.0
description: >
  GitHub README (English): graphify box, Compatible-with = channels/sources (not
  stack), Surfaces/App-tools matrix (notion-publisher), stack = hero badges +
  Tech Stack, About via sync-github-about. Ship gate --repo. Triggers: /readme-commit.
argument-hint: "[optional commit message]"
category: engineering
---

# readme-commit

Verify/optimize root `README.md`, sync **native GitHub About**, then commit.

**Language:** README body **English**. Conversation may stay Spanish.

**Skill dir:** resolve the directory that contains this `SKILL.md` (`$SKILL_DIR`). All scripts live under `$SKILL_DIR/scripts/`.

## Three logo layers (do not mix)

| Layer | Content | Where |
|---|---|---|
| Hero badges | Tech / runtime / org | shields.io in hero |
| Compatible with | **Channels + sources/destinations** of the product domain | strip `height="28"` under `docs/assets/logos/` |
| Surfaces / App tools | App surfaces (MCP, bots, REST, consoles) — **not npm** | status matrix table, cell logos `width="20"` |

**Never** put React, Vite, Bun, TanStack, Tailwind, TypeScript, Clerk, or Supabase in Compatible-with. Those = badges + `## Tech Stack`. Product auth/host (e.g. Clerk OAuth, Lovable host, GitHub as commit destination) belong in **Surfaces** and/or Compatible-with only when they are domain destinations/sources — prefer Surfaces for auth/host; Compatible-with for social/content channels.

**Canon refs (MUST skim remotes before write):**

| Ref | Steal |
|---|---|
| [Nucleo-Lab/notion-publisher](https://github.com/Nucleo-Lab/notion-publisher) | 28px integration strip, **Status matrix**, Channel grid |
| [crafter-station/graphify-visualizer](https://github.com/crafter-station/graphify-visualizer) | Double-box hero, cover 900 |
| [TheVeller/distilledbrew](https://github.com/TheVeller/distilledbrew) | Mermaid, API table, for-the-badge Tech Stack |

```bash
gh api repos/Nucleo-Lab/notion-publisher/contents/README.md --jq .content | base64 -d | head -120
gh api repos/crafter-station/graphify-visualizer/contents/README.md --jq .content | base64 -d | head -80
gh api repos/TheVeller/distilledbrew/contents/README.md --jq .content | base64 -d | head -80
```

**Companions:** `references/structure.md`, `references/modes.md`, `references/ascii-heroes.md`, `scripts/`.

## Nested cwd

Target repo = current working directory (or the path the user names). Scripts always run via absolute `$SKILL_DIR/scripts/…` paths so nested product repos do not break discovery.

## Workflow

### 0. Mode

`greenfield` | `existing` per `references/modes.md`. Never wipe non-empty README without user OK.

### 1. Detect

- `owner/repo`, live URLs, LICENSE
- **Channels/sources** (YouTube, Instagram, X, TikTok, LinkedIn, Telegram, …)
- **App surfaces** (MCP tools, bots, REST, setup console, cron, …)
- **Stack** (for badges + Tech Stack only)

### 2. Crawl

- Stack → `detect-stack.mjs`
- Features / MCP / APIs / docs from repo only — no invented claims

### 3. Assets

Outdir for channel/surface marks: **`docs/assets/logos/`** (notion-publisher path). Prefer curated platform logos; `fetch-favicon.sh` fallback once per URL.

1. Channel/source/destination sites → logos into `docs/assets/logos/`
2. Surface icons (Telegram, MCP, GitHub, …) for matrix cells
3. Build Compatible-with strip (`height="28"`) — channels/sources only
4. Zero channel logos after tries → `<!-- logos: pending -->`
5. Cover: Playwright once or honest skip

### 4. Diagram

Mermaid and/or Excalidraw readme-dark.

### 5. Build README

**Hero:** box (`╔`) → H1 → one-liner → **meta + stack shields** → links → Compatible-with (channels) → cover.

**Body (emoji H2s)** — see `structure.md`. After Why/Features (or after Architecture):

- `## 🧩 Surfaces / App tools` — table: logo | Name | Role | Status (≥2 rows with `<img>`), or `<!-- surfaces: pending -->` after crawl found nothing

Locked titles: `## ✨ Why this exists + Features`, `## 🚀 Quick start`, `## 🏷️ Topics / search keywords` (≥3 topics = About topics).

Footer exact: TheVeller · Núcleo Lab · Crafter Station.

### 6. GitHub About (MUST on ship)

```bash
bash "$SKILL_DIR/scripts/sync-github-about.sh" owner/repo \
  --description "…" [--homepage URL] --topic a --topic b --topic c …
```

### 7. Review + gate

Ship: `bash "$SKILL_DIR/scripts/check-readme-contract.sh" README.md --repo owner/repo` — Compatible-with deny-lists stack names; Surfaces H2 or pending; About checks.

### 8. Commit

`docs(readme): …` + assets under `docs/assets/logos/`.
