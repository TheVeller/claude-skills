```text
 _____ _          __     __   _ _            ____  _    _ _ _
|_   _| |__   ___ \ \   / /__| | | ___ _ __/ ___|| | _(_) | |___
  | | | '_ \ / _ \ \ \ / / _ \ | |/ _ \ '__\___ \| |/ / | | / __|
  | | | | | |  __/  \ V /  __/ | |  __/ |   ___) |   <| | | \__ \
  |_| |_| |_|\___|   \_/ \___|_|_|\___|_|  |____/|_|\_\_|_|_|___/
```

Portable agent workflows for research, engineering, handoffs, and Obsidian operations. Built from real projects, packaged as self-contained `SKILL.md` directories.

[![GitHub stars](https://img.shields.io/github/stars/TheVeller/claude-skills?style=flat&logo=github&label=stars)](https://github.com/TheVeller/claude-skills/stargazers)
[![License: MIT](https://img.shields.io/badge/license-MIT-black.svg)](./LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/TheVeller/claude-skills)](https://github.com/TheVeller/claude-skills/commits/main)
[![Agent Skills](https://img.shields.io/badge/format-Agent%20Skills-2563eb)](https://skills.sh)

Use these skills when a repeatable workflow needs more than a prompt: deterministic scripts, references, safety rules, and a clear definition of done. The collection contains skills authored or materially adapted by [@TheVeller](https://github.com/TheVeller); upstream work is credited explicitly.

## Start here

| Goal | Skill |
|---|---|
| Turn a data export into a dashboard that changes a decision | [`data-source-dashboard`](./skills/research/data-source-dashboard) |
| Turn long-form sources into reusable research | [`research-pipeline`](./skills/research/research-pipeline) |
| Sync a local repository without losing work | [`repo-sync`](./skills/engineering/repo-sync) |
| Improve a GitHub README and ship the change | [`readme-commit`](./skills/engineering/readme-commit) |
| Transfer work into a fresh Orca agent terminal | [`orca-handoff`](./skills/agent-operations/orca-handoff) |
| Explain a technical decision to a non-developer | [`no-dev`](./skills/agent-operations/no-dev) |
| Keep an Obsidian vault committed continuously | [`autocommit`](./skills/obsidian-vault/autocommit) |
| Audit a whole repository for drift, broken links, and leaked secrets | [`repo-audit`](./skills/obsidian-vault/repo-audit) |

## Install

Install one skill globally with the [`skills`](https://skills.sh) CLI:

```bash
npx skills add TheVeller/claude-skills --skill repo-sync -g
```

Install several skills into the current project:

```bash
npx skills add TheVeller/claude-skills \
  --skill research-pipeline readme-commit orca-handoff
```

Or clone and copy a directory directly:

```bash
git clone https://github.com/TheVeller/claude-skills.git
cp -R claude-skills/skills/engineering/repo-sync ~/.claude/skills/
```

The repository groups skills by category for browsing. Install or copy the individual skill directory, not its category directory.

## Catalog

### Research

| Skill | What it does |
|---|---|
| [`data-source-dashboard`](./skills/research/data-source-dashboard) | Turns a raw export into an interactive dashboard: aggregates-only privacy, provenance on every number, scenario toggles, ES/EN and dark/light. |
| [`research-pipeline`](./skills/research/research-pipeline) | Sends sources through NotebookLM and returns grounded notes, with optional infographic, podcast, or slides. |
| [`youtube-search`](./skills/research/youtube-search) | Searches YouTube through `yt-dlp` and collects URLs plus metadata for research pipelines. |
| [`daily-review-workflow`](./skills/research/daily-review-workflow) | Pulls synced sources, handles failures, and writes an end-of-day review note. |

### Engineering

| Skill | What it does |
|---|---|
| [`readme-commit`](./skills/engineering/readme-commit) | Audits or creates a useful GitHub README, verifies it against the repository, then commits it. |
| [`repo-sync`](./skills/engineering/repo-sync) | Detects ahead, behind, and diverged states; fast-forwards safely and backs up before destructive syncs. |
| [`intent-layer`](./skills/engineering/intent-layer) | Captures intent and structural constraints before implementation. |
| [`clone-software-repo`](./skills/engineering/clone-software-repo) | Clones an external repository into a managed software workspace. |
| [`start-cc+lv`](./skills/engineering/start-cc+lv) | Starts a Claude Code workflow connected to Lovable and a GitHub-based deployment path. |
| [`game-designer-ue`](./skills/engineering/game-designer-ue) | Adapts game-feel analysis and design methods to Unreal Engine 5 systems. |
| [`wayfinder-sequential`](./skills/engineering/wayfinder-sequential) | Cautious variant of [`/wayfinder`](https://github.com/mattpocock/skills): one ticket per session, no parallel research, map re-evaluated after every resolution, prototype decisions stay with the user. Requires the upstream `wayfinder` skill. |
| [`wavespeed`](./skills/engineering/wavespeed) | Generates or edits image, video, audio, and 3D assets through the `wavespeed` CLI, where every model is one explicit `run <id>` call. |

### Agent Operations

| Skill | What it does |
|---|---|
| [`orca-handoff`](./skills/agent-operations/orca-handoff) | Writes a redacted handoff, opens the correct Orca terminal or worktree, waits for TUI readiness, and delivers the prompt. |
| [`no-dev`](./skills/agent-operations/no-dev) | Converts technical explanations into purpose, consequence, action, risk, and result. |
| [`govern-agentic-os`](./skills/agent-operations/govern-agentic-os) | Keeps a repository and its issue tracker from becoming two sources of truth: audit, plan, execute, check, and hand off governance work under one authority model. |

### Obsidian Vault

| Skill | What it does |
|---|---|
| [`obsidianizer`](./skills/obsidian-vault/obsidianizer) | Turns raw material into vault-ready notes with frontmatter, wikilinks, and PARA placement. |
| [`autocommit`](./skills/obsidian-vault/autocommit) | Operates and diagnoses an `fswatch`-based auto-commit daemon for a vault. |
| [`repo-audit`](./skills/obsidian-vault/repo-audit) | Runs a queue of audit units in one autonomous pass — coherence, broken symlinks, leaked secrets, PARA placement, scripts, doc condensation — read-only except its own report artifacts. |

### Marketing

| Skill | What it does |
|---|---|
| [`promo-webinar`](./skills/marketing/promo-webinar) | Turns a short webinar brief into a 9-asset multichannel promo kit plus a publish calendar. |
| [`sundai-campana-hack`](./skills/marketing/sundai-campana-hack) | Generates the full before/during/after content plan for a Sundai Latam hack campaign. |

## Repository layout

```text
skills/
|-- agent-operations/  # handoffs and human-agent communication
|-- engineering/       # repository and implementation workflows
|-- marketing/         # campaign copy and event promotion
|-- obsidian-vault/    # knowledge-system operations
`-- research/          # source discovery and synthesis
```

Each leaf directory includes a `SKILL.md` and may include scripts, references, templates, or assets. Dependencies and setup steps live beside the skill that needs them.

## Compatibility

The format works with agents that support Agent Skills, including Claude Code, Cursor, and Codex through the `skills` CLI. Individual workflows may require tools such as `git`, `gh`, `fswatch`, `yt-dlp`, NotebookLM, or Orca; check the target skill before installing.

## Attribution

This repository does not mirror the full third-party stack used in TheVeller's workspace. Those skills stay in their upstream repositories:

| Source | Skills or focus |
|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | Debugging, planning, worktrees, and TDD |
| [mattpocock/skills](https://github.com/mattpocock/skills) | Domain modeling, grilling, handoffs, implementation, teaching, and the `wayfinder` planning chain (`wayfinder-sequential` here builds on it) |
| [coleam00/excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill) | Research-backed Excalidraw workflow diagrams |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Design critique and frontend refinement |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | Frontend design judgment |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | UI/UX design workflows |
| [opusgamelabs/game-creator](https://github.com/opusgamelabs) | Basis for the adapted `game-designer-ue` skill |
| [dstn2000/claude-unreal-engine-skill](https://github.com/dstn2000/claude-unreal-engine-skill) | Unreal Engine workflows |
| [roble3/cc-blender-skill](https://github.com/roble3/cc-blender-skill) | Blender modeling |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | Vercel deployment workflows |
| [googleworkspace/cli](https://github.com/googleworkspace/cli) | Google Workspace service skills |
| [Composio](https://composio.dev) | `composio-cli`, installed with `composio --install-skill` and generated from the CLI's own source |
| [diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute) | The `omniroute-*` gateway skills, generated by the product's own skill generator |

Install community skills selectively and keep their original license and attribution.

## Contributing

Issues and pull requests are welcome. A useful contribution should keep one workflow per skill, document external dependencies, avoid secrets and machine-specific data, and include a runnable check for non-trivial scripts.

## License

MIT (c) [Ignacio Alberto Velasquez Franco (@TheVeller)](https://github.com/TheVeller)
