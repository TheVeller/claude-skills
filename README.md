# TheVeller · Claude Skills

> A curated monorepo of **my own** Claude Code / agent skills — organized by category. Each skill is a self-contained `SKILL.md` (plus any scripts/references it needs) that drops into any agent's skills directory.

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](./LICENSE)
[![Skills](https://img.shields.io/badge/skills-11-blue.svg)](#catalog)
[![Author](https://img.shields.io/badge/by-@TheVeller-6e5494.svg)](https://github.com/TheVeller)

These are skills I authored or adapted for my own Obsidian + agent workflow. Third-party / installed skills are intentionally **not** here — only my work.

## Catalog

### 🔬 research
| Skill | What it does |
|---|---|
| [`research-pipeline`](./skills/research/research-pipeline) | YouTube → NotebookLM → notes. Server-side analysis at **zero LLM tokens**. Optional infographic/podcast/slides. |
| [`youtube-search`](./skills/research/youtube-search) | Search YouTube via `yt-dlp`, collect video URLs + metadata. Feeds `research-pipeline`. |
| [`daily-review-workflow`](./skills/research/daily-review-workflow) | End-of-day review routine — pulls synced sources, handles errors, writes the daily note. |

### 🛠️ engineering
| Skill | What it does |
|---|---|
| [`game-designer-ue`](./skills/engineering/game-designer-ue) | Game-feel / juice audit + design methodology mapped to Unreal Engine 5 (Niagara, UMG, Camera Shake, Sequencer). For TBS/tactical. |
| [`readme-commit`](./skills/engineering/readme-commit) | Verify/optimize a star-worthy README, then commit with Conventional Commits. |
| [`repo-sync`](./skills/engineering/repo-sync) | Sync a working repo to remote with a safe, scripted flow. |
| [`intent-layer`](./skills/engineering/intent-layer) | Capture intent + structure analysis before implementation (state detection, token estimation, templates). |
| [`start-cc+lv`](./skills/engineering/start-cc+lv) | Bootstrap a Claude Code session wired to Lovable + Cloud Native + Render via GitHub `main`. |
| [`clone-software-repo`](./skills/engineering/clone-software-repo) | Clone an external repo into a managed software workspace. |

### 📓 obsidian-vault
| Skill | What it does |
|---|---|
| [`obsidianizer`](./skills/obsidian-vault/obsidianizer) | Turn raw content into vault-ready Obsidian notes (frontmatter, wikilinks, PARA). |
| [`autocommit`](./skills/obsidian-vault/autocommit) | Operate a local `fswatch` auto-commit daemon for a vault (start/stop/status/debug). |

## Install a skill

Each skill folder is self-contained. Copy the one you want:

```bash
git clone https://github.com/TheVeller/claude-skills.git
cp -R claude-skills/skills/research/research-pipeline ~/.claude/skills/
```

> **Note on layout:** skills are grouped into category folders for browsing. Claude Code discovers skills at `~/.claude/skills/<name>/SKILL.md` (flat) — so copy the individual skill folder up one level as shown, not the category folder.

## Prerequisites

Some skills call external CLIs (documented in each `SKILL.md`): `notebooklm` + `yt-dlp` (research), `fswatch` (autocommit), `git`/`gh` (engineering).

## Attribution

- `game-designer-ue` is my Unreal Engine 5 adaptation of the browser-based [`game-designer`](https://github.com/OpusGameLabs) methodology (MIT). Original patterns credited; UE mappings and TBS reframing are mine.

## License

MIT © [Ignacio Alberto Velásquez Franco (@TheVeller)](https://github.com/TheVeller)
