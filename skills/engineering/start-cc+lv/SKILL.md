---
name: start-cc+lv
description: Bootstrap a Claude Code session for projects connected to Lovable + Cloud Native + Render via GitHub main branch. Syncs local repo to origin/main and locks in a "commit and push to main after every change" contract for the rest of the session so the user can preview changes live in Lovable and roll back via git history. Use when the user invokes `/start-cc+lv`, says "empezar con Lovable", "setup proyecto Lovable+Render", "sync con main para Lovable", "trabajar con Cloud Native", or starts work on any repo wired to Lovable.
---

# start-cc+lv — Claude Code + Lovable session contract

Activate this workflow at the start of any session where the project's deploy target is **Lovable + Cloud Native + Render** and the user previews live from `origin/main`.

## Step 1 — Sync local to `origin/main`

Before any work, align the local working tree with the remote:

```bash
git status
```

- **If working tree is clean and on `main`**:
  ```bash
  git fetch origin
  git reset --hard origin/main
  ```
- **If working tree is dirty or on another branch**: STOP. Ask the user what to do (commit + push, stash, or discard) — never `reset --hard` over their work without explicit confirmation. See "Executing actions with care" in the root CLAUDE.md.
- **If not on `main`**: ask the user — do not auto-checkout; they may have intentional state.

Report the resulting HEAD sha and commit subject in one line so the user can confirm Lovable is on the same commit.

## Step 2 — Session contract (active until session ends)

Once synced, follow these rules for **every** change made during the session:

1. **Single branch: `main`.** Never create feature branches. Lovable watches `main`.
2. **Commit + push after every meaningful change.** Pattern:
   ```bash
   git pull --rebase origin main   # pick up edits made in Lovable directly
   git add <specific files>        # never `-A` / `.` — avoid pulling secrets or junk
   git commit -m "<short imperative subject>"
   git push origin main
   ```
3. **Small commits.** The user rolls back via git history when something breaks — granular commits make rollback cheap.
4. **No destructive shortcuts** without explicit user confirmation:
   - No `--force` / `--force-with-lease` push to `main`.
   - No `--no-verify` to skip hooks. If a hook fails, fix the root cause.
   - No `git reset --hard` mid-session.
5. **Hook failures = fix the code, not bypass the hook.** Re-stage and commit again (new commit, not `--amend` if the original was already pushed).
6. **Conflicts with Lovable edits**: rebase, resolve, push. Do not discard remote changes — Lovable may have edited from the UI side.

## Step 3 — Routine reminders to surface

- After each push, mention briefly: "Pushed `<sha>` — Lovable / Render should pick this up on next deploy."
- If push fails because remote is ahead → `git pull --rebase origin main` then retry. Do not force.
- At end of session, confirm `git status` clean and `git log @{u}..` empty.

## What this skill does NOT do

- Does not configure Render / Cloud Native / Lovable themselves — that wiring already exists at the GitHub repo level.
- Does not run tests or builds automatically — the user wants speed; let CI on the deploy target catch issues.
- Does not write to CLAUDE.md or memory — the skill is the source of truth for this workflow.
