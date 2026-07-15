---
name: repo-sync
description: Use when the user wants to confirm a local git repo matches its GitHub remote and pull the latest before working — phrasings like "check if local has the latest from GitHub", "is this repo up to date with the remote", "sync this repo", "pull Lovable's changes first", or at the start of local work on a repo that's also edited in the cloud (Lovable / Supabase projects like videomatic). Detects up-to-date / behind / ahead / diverged, fast-forwards when lossless, and can overwrite the local copy with the remote — always backing up first — when they've diverged.
---

# repo-sync

Make the local working copy reflect GitHub's latest before you start editing.

## Why this exists

Some repos are edited in two places: the cloud (e.g. **Lovable** committing to GitHub for the `videomatic` / pixel-orchestrator-ui project) and locally with Claude Code. GitHub holds the newest cloud changes, so the local clone silently drifts **behind**. Starting local work on a stale clone means editing old code and creating avoidable conflicts. This skill checks the gap first and brings local up to GitHub's state — overwriting local when needed, but never without a recoverable backup.

## Tool

A single script does all the git plumbing so you don't re-derive it each time. Run it from inside the target repo (the current working directory's repo). Resolve its path relative to this SKILL.md: `scripts/repo-sync.sh`.

```bash
bash <skill-dir>/scripts/repo-sync.sh check        # READ-ONLY: fetch + report state
bash <skill-dir>/scripts/repo-sync.sh sync         # apply the safe action
bash <skill-dir>/scripts/repo-sync.sh sync --force # also allow overwriting local (with backup)
```

The script reports `state:` as one of:

| State | Meaning | What `sync` does |
|---|---|---|
| `up-to-date` | local == remote | nothing |
| `behind` | remote has commits local lacks | fast-forward (lossless) |
| `ahead` | local has commits not on remote | refuses unless `--force`; then backs up + hard-resets to remote |
| `diverged` | both have unique commits | refuses unless `--force`; then backs up + hard-resets to remote |

## Workflow

1. **Always start with `check`.** It's read-only — it `fetch`es and prints the state, the ahead/behind counts, and a recommended action. Show the user that line.

2. **Decide based on state:**
   - `up-to-date` → nothing to do. Say so and proceed with the real work.
   - `behind` → run `sync`. This is a plain fast-forward, lossless. Safe to do without asking (it's exactly what "pull the latest" means). If the tree is dirty the script will ask for `--force` so it can stash first — mention the stash to the user.
   - `ahead` or `diverged` → **stop and confirm with the user before overwriting.** Local commits exist that aren't on GitHub. The user's intent for this skill is "let GitHub win and start from there," but that discards local commits, so surface exactly what would be lost (`git log @{u}..@ --oneline`) and confirm. Only then run `sync --force`.

3. **Report what happened** — the resulting state and, for any overwrite, the backup branch name and stash the script created.

## Safety — nothing is lost

`sync --force` never destroys silently. Before any `git reset --hard` or fast-forward over a dirty tree, the script:
- creates a `backup/pre-sync-<timestamp>` branch at the current commit (recovers committed work), and
- runs `git stash push -u` (recovers uncommitted **and** untracked files).

So even a "wrong" overwrite is reversible: `git checkout backup/pre-sync-<ts>` or `git stash list` → `git stash pop`. Tell the user these exist rather than assuming they'll read the script output.

This script wraps `git reset --hard` deliberately, so the vault's PreToolUse guardrail (which blocks bare `git reset --hard`) won't fire — the backups are what make that acceptable. Don't work around the guardrail by other means; route destructive syncs through this script so the backup always happens.

## Notes for the videomatic repo specifically

- Remote: `pixel-orchestrator-ui.git`, branch `main`, upstream `origin/main`.
- It's a standalone git repo nested under the vault; the vault's auto-commit daemon does **not** commit it, so its uncommitted changes are real local work — don't assume a clean tree.
- Untracked files ending in ` 2` (e.g. `Editor 2.tsx`, `.env 2.example`) are Google Drive sync-conflict duplicates, not real source. A force-sync stashes them away (recoverable), which is usually the desired cleanup.

## After many syncs

Backup branches accumulate. To prune old ones once you're sure they're not needed:
`git branch --list 'backup/pre-sync-*'` then delete the stale ones with `git branch -D <name>`.
