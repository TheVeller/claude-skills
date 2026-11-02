---
name: karpathy-vault
description: >-
  Use this when creating or explaining the Karpathy-style markdown vault on the
  Grok Bot computer (inbox/raw/wiki/state) as the homelab second brain.
---
# Karpathy vault (second brain)

The Grok Bot computer holds a small markdown vault (Karpathy-inspired LLM personal knowledge base). It is a second brain for the remote homelab, not the company Obsidian vault on the user’s personal computer.

**Protocol:** `agent → filesystem → agent`. ZeroClaw (or another agent) writes inbox/state/raw today; Homelab Porter / Grok Bot reads later, runs a routine, continues the work, writes new state. They do not need one giant shared conversation to hand off work. The computer itself is part of memory.

## Layout

```text
lab/
  AGENTS.md      # porter rules for ZeroClaw (who writes what)
  USER.md        # optional short user note
  inbox/         # Telegram recados (status: new)
  inbox/done/    # after the map bot processes them
  raw/           # sources the user drops (links, notes, pdf). Do not rewrite.
  wiki/          # curated pages the map bot owns
  wiki/log.md    # append-only activity log
  wiki/index.md  # index of wiki pages
  wiki/conventions.md
  wiki/overview.md
  state/         # live ops stamps (zeroclaw, herdr, ram)
  sync_inbox.py  # optional: materialize Telegram logs into inbox/*.md
```

Symlink or root path may be `/workspace/lab` on the Grok Bot computer. Name the root clearly in memory after import.

## Roles (who writes)

| Path | Writer | Reader |
| --- | --- | --- |
| `inbox/` | ZeroClaw (and sync script) | Map / Homelab Porter bot |
| `raw/` | User only | Map bot integrates into wiki |
| `wiki/` (except log) | Map bot | User reads; user does not edit |
| `wiki/log.md` + `state/` | ZeroClaw (lab ops) and map bot | Everyone |
| Company roster / GM canon | Stays in the user’s main vault (e.g. Hermes/Obsidian). Do not clone it into this lab. |

## Flow

1. User messages the Telegram porter.
2. Porter writes `inbox/YYYY-MM-DD-HHMMSS.md` with date (user timezone), sender, id, full text, `status: new`.
3. Map bot routine reads `status: new`, does the minimum, appends `wiki/log.md`, updates `state/`, moves file to `inbox/done/`.
4. User drops sources in `raw/`. Map bot integrates into `wiki/`; never edits `raw/` in place as canon.

## Second-brain rules

- Prefer short markdown pages over databases.
- Index everything from `wiki/index.md`.
- Append to `log.md`; do not rewrite history.
- `state/` is ephemeral truth (health stamps), not essays.
- Coding still goes to Cursor cloud agents; do not turn this vault into a git checkout farm.

## First-run

1. Create the folder tree above on the Grok Bot computer.
2. Seed `wiki/conventions.md`, `wiki/overview.md`, `wiki/index.md`, empty `wiki/log.md`, `raw/README.md`, `AGENTS.md`.
3. Point ZeroClaw’s workspace (or a symlink) at this root.
4. Wire the map bot’s inbox routine to this path.
5. Tell the user: read wiki, drop sources in raw, do not hand-edit wiki.

## Fences

- Do not merge this lab vault with the company Obsidian vault.
- Do not let the porter own curated wiki pages (only log + state + inbox).
- Do not store secrets in wiki or raw.
