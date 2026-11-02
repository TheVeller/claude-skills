---
name: start-cc+lv
description: >-
  Use when starting or iterating a Lovable-wired app: hybrid Lovable +
  terminal/cloud agents, credit economy, agent-driven GitHub connect right after
  the first prompt, Try to Fix (free on preview errors), tests in builds, git
  sync to main. Also when the user invokes `/start-cc+lv`, says "empezar con
  Lovable", "sync con main para Lovable", or starts work on any repo wired to
  Lovable.
---
# start-cc+lv — Hybrid Lovable + agents

Contract for apps whose UI/Cloud live in **Lovable** and whose cheap iteration is **terminal agents, Cloud Agents, or Origin**, with git on `main`.

## Who does what
- **Lovable**: scaffold + planning nativo, Cloud (auth/DB/edge/storage/payments), secrets, deploy, preview, native integrations. Expensive — use sparingly and in batches.
- **Terminal / Cloud Agents / Origin**: default code edits, refactors, fixes, docs, **tests**. Arrive in Lovable via `git push` to `main`.
- **Orca / Herdr / hermes-dev**: Mac fleet control — Hermes lane, not SWE.

## Golden rule (credits)
- Default = agents + git, not Lovable chat.
- Lovable chat/MCP only for: the first build prompt, Cloud enable, secrets, deploys, native integrations, schema/RLS via its tooling, preview-only debugging, or explicit user ask.
- Never use Lovable `send_message` for edits a local/cloud agent can do via git.
- Batch Lovable messages; fine-tune locally.
- **Git-sync does NOT deploy edge functions.** Write functions locally in a batch; deploy once in Lovable at the end (Try to Fix after reproducing the fetch, or minimal `deploy <fn> as-is`).
- **Try to Fix is free** when the Lovable preview error detector fires. Prefer it over paid `send_message` for build/preview failures; escalate to Cloud Agent / paid chat only if it fails.

## Connect GitHub — ALWAYS, right after the first prompt
Every new Lovable project gets GitHub connected immediately after the first build prompt finishes, so every later change is born on GitHub. No exceptions, no waiting until code work is needed, never handed to the user.
1. First prompt completes (Lovable reports the build done).
2. Check `get_project` / editor GitHub panel for an existing repo.
3. If none: browser subagent opens the project editor (signed-in Lovable account that owns the workspace) → GitHub / Connect → pick the org for that product (default the user's usual org; e.g. crafter-station for community projects, TheVeller for personal) → create repo → confirm the repo URL. One browser at a time; close it after.
4. If GitHub OAuth/authorize or org-install needs the user's own sign-in or 2FA, hand off only that step, then resume.
5. Record the repo URL in notes/memory. From here, all code work = Cloud Agent pushing to `main`.

## Tests in the loop (mandatory)
- Every coding route grows automated checks: smoke, unit/integration where cheap, typecheck, CI on `main` when available.
- Cloud Agent done-when includes the relevant test scripts, not only `npm run build`.

## Lifecycle
1. **Prompt pack first** (Prompt Architect): mvp-plan + design-style-plan + prd → Lovable project knowledge.
2. **First prompt** in Lovable (one batch).
3. **Connect GitHub immediately** (section above).
4. **Cloud Agent-first** afterwards: push to `main`; Lovable redeploys app code; edge functions need an explicit Lovable deploy step.

## Session rules (editing main)
1. **Sync to `origin/main` before work.** Run `git status`.
   - Clean and on `main`: `git fetch origin` then `git reset --hard origin/main`.
   - Dirty or on another branch: STOP and ask (commit + push, stash, or discard). Never `reset --hard` over a dirty tree without asking. Do not auto-checkout `main`.
   - Report the resulting HEAD sha and subject in one line so the user can confirm Lovable is on the same commit.
2. **Single branch `main`, direct push, no PRs.** Lovable watches `main`.
3. **Small commits; specific files only.** Pattern:
   ```bash
   git pull --rebase origin main   # pick up edits made in Lovable directly
   git add <specific files>        # never -A / . — avoid pulling secrets or junk
   git commit -m "<short imperative subject>"
   git push origin main
   ```
4. **`pull --rebase` if Lovable edited remote; never force-push `main`.** No `--force` / `--force-with-lease`, no `--no-verify`. If a hook fails, fix the root cause and make a new commit (no `--amend` once pushed). On conflicts with Lovable edits: rebase, resolve, push; never discard remote changes.
5. **After push: report sha**; if edge fns changed, close with Try to Fix / minimal deploy. At session end, confirm `git status` is clean and `git log @{u}..` is empty.

## The agent does NOT
- Ask the user to wire GitHub↔Lovable (only a sign-in/2FA step goes to them).
- Command Orca/Herdr (Hermes).
- Spend Lovable credits when Try to Fix or a Cloud Agent + git would do.
- Publish without the user's OK.
