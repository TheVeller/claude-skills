---
name: ship-oss
description: >
  General OSS-readiness pass for a repo before it goes public: sweep the full tree
  (not just README) for secrets and internal/personal references, verify LICENSE and
  .gitignore, run the Crafter secret/owner gate, delegate README polish to readme-commit,
  then flip GitHub visibility to public and push. Use when the user says "prepara este
  repo para open source", "hazlo público", "ship this as OSS", "publica este repo",
  "make this repo public", "ready this for GitHub", or "/ship-oss".
argument-hint: "[owner/repo opcional] [--dry-run|--publish]"
category: engineering
---

# ship-oss

Repo-wide open-sourcing pass. Sibling to `readme-commit` (same commit-at-the-end shape) but
scoped one layer up: **is the whole repo safe and complete to expose**, not just the README.

**Do not reimplement what already exists** — this skill is glue:

| Concern | Owner |
|---|---|
| Secret-pattern scan + owner verification | `gh-org-publish` (`crafter-oss-gate.sh`, `check-origin-owner.sh`) |
| README structure/taste/Excalidraw flow | `readme-commit` |
| Dependency / supply-chain risk | `supply-chain-audit` (third-party, crafter-station) — only if the repo has a package manifest |

## Modes

| Mode | What runs | Visibility flip / push |
|---|---|---|
| **dry-run** (default) | Full sweep below, report findings | never |
| **publish** | Same sweep, fixes applied, gates green | only on explicit user order |

Never flip a repo to public or push as a side effect of "looks done" — this is a
hard-to-reverse, externally-visible action (see global safety rules). Always state the
target `owner/repo` and get explicit confirmation before step 6.

## Workflow

### 1. Scope

Resolve target: `$ARGUMENTS` if given, else current repo's `origin`. Confirm the intended
owner (personal `TheVeller` vs an org) using the alias table in `gh-org-publish` — don't
re-derive it here.

### 2. Sanitization sweep (full tracked tree, not just README)

Scan `git ls-files` output for content that leaks internal/personal context:

- Issue-tracker refs meant to stay internal: `MAK-\d+`, `linear\.app/<workspace>` URLs
- Absolute local paths: `/Users/<name>/`, Google Drive sync paths (`CloudStorage/...`)
- Fixture/example data that is actually real (real journal notes, real emails, real
  transcripts) — PARA folder *names* like `01_Journal/`, `06_Metadata/` are semantic and
  fine to keep; the leak risk is real *content* inside them, not the folder convention
- Vendored/bulk-installed content with unclear provenance — a `license:` frontmatter key,
  an `AUTO-GENERATED` header, or a bulk "add N files" commit (not a dedicated
  `feat: add <thing>` commit) means it's third-party: exclude it or credit it in an
  Attribution section, never claim it as own-authored

Report every hit with file:line before touching anything. Fix by redacting/removing —
never by explaining the leak away.

### 3. LICENSE

- Missing → ask which license (default MIT, matching this org's existing OSS repos) and add it.
- Present → confirm it matches what the README/footer claims.

### 4. `.gitignore`

Confirm it covers: `.env*` (except `.env.example`), `secrets.local.json`,
`credentials.json`, `node_modules/`, build output, OS cruft (`.DS_Store`). Add missing
lines; don't rewrite an already-adequate file.

### 5. Hygiene gate (fail closed)

```bash
bash .agents/skills/gh-org-publish/crafter-oss-gate.sh .
bash .agents/skills/gh-org-publish/check-origin-owner.sh <EXPECTED_OWNER> .
```

Any non-zero exit → stop, report, do not proceed to step 6. This is a tracked-files-only
scan (`git ls-files`) — pair it with the manual sweep in step 2, which catches
internal-context leaks the pattern gate isn't built to see.

If the repo has a dependency manifest (`package.json`, `requirements.txt`, `go.mod`, …),
offer the `supply-chain-audit` skill for a deeper third-party dependency pass — don't run
it silently, it's a separate skill with its own scope.

### 6. README polish

Delegate to `readme-commit` (`.claude/skills/readme-commit/SKILL.md`) for structure, taste
bar, and the Excalidraw flow diagram if the repo needs one. Don't duplicate its checklist.

### 7. Publish (human-confirmed, `--publish` mode only)

1. All of steps 2–5 green, target owner confirmed with the user.
2. Visibility: `gh repo edit <owner>/<repo> --visibility public` (repo must already exist
   on GitHub under that owner — transfer first via `gh-org-publish` if not).
3. Verify: `gh repo view <owner>/<repo> --json visibility,isPrivate`.
4. Push only after visibility is confirmed public and the user has explicitly said to ship.

## Done when

- [ ] Full-tree sanitization sweep run and clean (or fixes applied + re-swept)
- [ ] LICENSE present and correct
- [ ] `.gitignore` covers secrets/env/build noise
- [ ] `crafter-oss-gate.sh` + `check-origin-owner.sh` both exit 0
- [ ] README passed through `readme-commit`
- [ ] Visibility confirmed public via `gh repo view` (publish mode only)
- [ ] Push done **or** dry-run documented — no silent push
