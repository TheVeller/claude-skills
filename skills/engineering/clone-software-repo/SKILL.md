---
name: clone-software-repo
description: Clone a GitHub repo into 02_Programs/3-Software/ ready for terminal-agent work — SSH-rewritten (HTTPS auth is broken in this env), with Google-Drive-safe defaults (core.fileMode false + post-clone fsck). Use when the user pastes a GitHub URL and wants it cloned locally, or says "clona este repo", "trae este repo a local", "clónalo a 3-software", "clone this repo", "setup this repo locally", "bájate este proyecto", or hands over a github.com link to work on from the terminal.
---

# Clone Software Repo → 3-Software

Single-shot skill: take a GitHub link, clone it into `02_Programs/3-Software/<repo>` with the defenses this vault needs (it lives inside Google Drive, and HTTPS git auth is broken here). Output is a tight "what landed + how to run it" summary.

## When to use

User pastes a GitHub URL (or `owner/repo`) and wants it on local disk to work with terminal agents. NOT for: re-cloning the GPT Chain `_initiatives-software` repos (that's `[[gpt-chain-refresh]]`), or creating a brand-new project from scratch (that's a Lovable/scaffold flow).

## Environment facts (must honor)

- **HTTPS auth is broken** → always clone over SSH. The script rewrites `https://github.com/OWNER/REPO` → `git@github.com:OWNER/REPO.git` automatically. See `[[reference-github-https-broken-use-ssh]]`.
- **Vault is inside Google Drive** → Drive flips permission bits and can corrupt `.git` over time. The script sets `git config core.fileMode false` and runs `git fsck` right after clone. See `[[project-code-repos-under-gdrive-corrupt]]`.
- **Target is always** `02_Programs/3-Software/<name>`. Existing repos there (e.g. `distilledbrew`, `preview-canvas-studio`) are cloned as plain subfolders — no companion vault page is required.

## Workflow

### Step 1 — Run the clone script

```bash
bash .claude/skills/clone-software-repo/scripts/clone-to-software.sh <url|owner/repo> [target-name]
```

- Accepts `https://github.com/OWNER/REPO[.git]`, `git@github.com:OWNER/REPO.git`, bare `OWNER/REPO`, or a `…/tree/BRANCH` link (branch is honored).
- `[target-name]` is optional — defaults to the repo name. Use it to avoid a name clash or rename on disk.
- Add `--dry-run` to print the parsed owner/repo/target without cloning (use it if the URL looks unusual before committing).
- The script refuses to overwrite an existing folder (exit 3) — never clobber.

The script prints a final block: `path`, `branch`, `latest commit`, `stack/install`, whether `.env` and agent docs (`AGENTS.md`/`CLAUDE.md`) are present.

### Step 2 — Report to the user

Relay a tight summary:

| Field | Value |
|---|---|
| Repo | `owner/repo` |
| Landed at | `02_Programs/3-Software/<name>` |
| Branch · latest | `main` · `sha "msg"` |
| Install | e.g. `bun install` |
| Has `.env` / agent docs | yes/no |

Then the obvious next step: `cd "02_Programs/3-Software/<name>" && <install>`, and (if no `.env` but an `.env.example` exists) note they'll need to fill secrets. If the repo has no `AGENTS.md`/`CLAUDE.md`, offer to scaffold one so terminal agents have context (don't auto-create).

## Failure modes

- **Bad/unparseable URL** (exit 2): show what was passed; ask for a clean `owner/repo` or full github.com link.
- **Target exists** (exit 3): don't overwrite. Offer a different `[target-name]`, or confirm before removing the old one.
- **Clone failed** (exit 4): almost always SSH key / access (private repo, wrong org). Confirm `ssh -T git@github.com` works and the user has access; HTTPS is NOT a fallback here.
- **fsck corrupt right after clone** (exit 5): Drive interfered mid-clone. Remove the partial dir and retry; if it recurs, clone OUTSIDE Drive and symlink, or mark the folder available-offline first.

## Notes

- No commits, installs, or dev servers are run by this skill — it clones + configures + reports. The user runs install/dev themselves (or asks next).
- Multiple repos: invoke once per URL (keeps each clone's output clean). For a batch, loop the script over the list in one Bash call.

## Related

- `[[reference-github-https-broken-use-ssh]]` · `[[project-code-repos-under-gdrive-corrupt]]`
- `02_Programs/3-Software/SETUP_MAPPING.md` — optional richer per-project vault structure if a repo graduates to a tracked project
- Sibling: `[[gpt-chain-refresh]]` (refresh existing cloned repos)
