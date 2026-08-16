# Condensation rubric

Use when auditing markdown entry points and overlapping docs.

## Questions per file pair

1. **Same audience?** (Claude Code vs Cursor vs human vs dashboard)
2. **Same layer?** (Memory ADK vs runbook vs marketing README)
3. **Duplicate facts?** Count overlapping sections (tables, command lists, folder trees).
4. **Stale risk?** More copies = more drift (e.g. "17 commands" in 3 files).
5. **Canonical rule:** one fact → one file. Others link with 1 line.

## Actions

| Action | When |
|--------|------|
| **merge** | Same audience + same layer; keep richer version |
| **cut** | Paragraph duplicated elsewhere; replace with wikilink |
| **link-only** | File becomes 5–15 lines pointing to canonical |
| **archive** | Historical snapshot (SETUP_COMPLETE) → `05_Archive/` or delete after extract |
| **keep** | Unique audience or unique facts |

## Root entry points (always compare in unit 001)

- `CLAUDE.md` — Claude Code memory (canonical ADK pointer)
- `AGENTS.md` — Cursor Cloud delta only
- `README.md` — public / GitHub face
- `INDEX.md` — narrative map (overlap con README?)
- `AGENTIC_OS_DASHBOARD.md` — status dashboard (not second CLAUDE)
- `SETUP_COMPLETE.md` — milestone log (archive candidate)
- `IDEA.md` — scratch (inbox or archive)
- `.cursorrules` — Cursor style (overlap con AGENTS?)

## Record in CONDENSATION-MAP.md

One row per proposed change; do not delete source files during audit.
