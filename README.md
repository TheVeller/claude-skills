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

## Beyond my own skills

This repo holds **only skills I authored**. My day-to-day agent setup stands on a much larger ecosystem — here's where the rest comes from, and where you can find your own.

### Primary source — [skills.sh](https://skills.sh)

Most skills in my stack are discovered and installed with the [`skills`](https://skills.sh) CLI:

```bash
npx skills add <owner>/<repo> -s <skill>   # single skill (recommended)
npx skills add <owner>/<repo>              # whole repo — careful, some ship hundreds
```

> **Tip:** always pin `-s <skill>`. Some community repos bundle 1000+ skills and a bare `add` installs every one of them.

### Third-party skills I use — credit to their authors

I run these but did **not** write them; they live in their upstream repos, not here:

| Source | Skills / focus |
|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | systematic-debugging, brainstorming, git-worktrees, TDD, writing-plans |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | design-taste-frontend (frontend design taste) |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | ui-ux-pro-max, design, design-system, banner-design |
| [opusgamelabs/game-creator](https://github.com/opusgamelabs) | game-designer — basis for my [`game-designer-ue`](./skills/engineering/game-designer-ue) |
| [dstn2000/claude-unreal-engine-skill](https://github.com/dstn2000/claude-unreal-engine-skill) | unreal-engine |
| [roble3/cc-blender-skill](https://github.com/roble3/cc-blender-skill) | blender-modeling |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | deploy-to-vercel, vercel-* |
| [googleworkspace/cli](https://github.com/googleworkspace/cli) | gws-* (Gmail, Calendar, Drive, Sheets…) |
| [stripe/docs](https://docs.stripe.com) | stripe-best-practices, stripe-projects |
| [mattpocock/skills](https://github.com/mattpocock/skills) · [slavingia/skills](https://github.com/slavingia/skills) · [crafter-station/skills](https://github.com/crafter-station/skills) | assorted engineering / business / second-brain skills |
| [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) | large community mega-pack — install **selectively** |

Business / second-brain skills I use but didn't author (meeting-notes, invoice-extractor, lead-scraper, cold-email-campaigns, follow-up-nurture, …) come from the packs above and are intentionally kept out of this repo.

## License

MIT © [Ignacio Alberto Velásquez Franco (@TheVeller)](https://github.com/TheVeller)
