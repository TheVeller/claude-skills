# Repo Audit Handoff

> Generado al cerrar todas las unidades del MANIFEST. Input para agente ejecutor (implementación + condensación de docs).

## Executive summary

- Unidades auditadas: N
- P0 blockers: N
- P1 fixes: N
- Docs candidatas a merge/cut: N

## P0 — Blockers (fix first)

| # | Issue | Paths | Suggested fix |
|---|-------|-------|---------------|
| 1 | … | … | … |

## P1 — Fixes by area

### `.claude/` / ADK
…

### `.scripts/` / automation
…

### Vault / PARA
…

### `.agents/` / skills
…

## Documentation Condensation Plan

**Goal:** fewer canonical entry points; eliminate stale duplicate prose.

| Priority | Action | Sources to cut/merge | Canonical target | Est. token savings |
|----------|--------|----------------------|------------------|-------------------|
| 1 | … | CLAUDE.md, AGENTS.md, … | … | … |

### Proposed canonical stack (target state)

| Layer | Single source | Others become |
|-------|---------------|---------------|
| Memory / Claude Code | `CLAUDE.md` + `.claude/docs/` | Short pointers only |
| Cursor Cloud | `AGENTS.md` | Delta vs CLAUDE only |
| Human onboarding | `README.md` or `INDEX.md` (pick one) | Link out |
| Ops dashboard | `AGENTIC_OS_DASHBOARD.md` | Data only, no duplicate ADK rules |

## Session index

| ID | Slug | P0 | P1 | Report |
|----|------|----|----|--------|
| 001 | root-files | … | … | [[sessions/001-root-files]] |

## Suggested skills for executor agent

- `implement` — apply code/config fixes
- `handoff` — if chaining another pass
- `intent-layer` — restructure AGENTS.md / doc hierarchy after cuts
- Patrón `sync-auditor` — post-fix doc sync

## Out of scope for executor

- …

## References

- Full condensation map: [[CONDENSATION-MAP]]
- Progress log: [[PROGRESS]]

---

## 9. Executor handoff

> **Obligatorio — siempre la última sección del HANDOFF.** Copiar §9.1 a un agente implementador.

### 9.1 Prompt copy-paste (agente implementador)

Rellenar usando `.agents/skills/repo-audit/references/executor-prompt-template.md` (placeholders `{{P0_LIST}}`, `{{P1_LIST}}`, `{{CONDENSATION_TOP3}}`).

```text
You are the **executor agent** for the Claudesidian / Agentic OS vault audit handoff.

## Context
- Handoff (read first): 06_Metadata/Reference/Repo-Audit/HANDOFF.md
- Condensation map: 06_Metadata/Reference/Repo-Audit/CONDENSATION-MAP.md
- Session reports: 06_Metadata/Reference/Repo-Audit/sessions/
- Deep audit (if present): DEEP-AUDIT-SUMMARY.md, DEEP-AUDIT-SCRIPTS.md, DEEP-AUDIT-WORKSPACES.md
- Canonical memory: CLAUDE.md + .claude/docs/
- Current stack (2026-07-31+): Orca/Hermes, Composio CLI, gws, Railway (layer 12 cloud hosting) — Rube MCP is RETIRED; OpenClaw is a candidate again; Railway's 2026-07-04 retirement was REVERTED

## Mission
Implement fixes from the handoff in priority order. Do NOT re-run a full repo audit unless verification requires it.

## Execution order
1. P0 blockers (below) — all before P1
2. P1 fixes by area (HANDOFF § P1)
3. Documentation condensation — only rows confirmed in CONDENSATION-MAP or explicitly approved by the user; prefer link-only over delete
4. Post-fix: if you touched .claude/commands|skills or .agents/skills → bash .scripts/sync-adk-agents.sh
5. Post-fix: if you cut docs or indexes → bash 06_Metadata/scripts/sync-docs.sh apply (ask user before destructive apply)

## P0 — fix first
{{P0_LIST}}

## P1 — after P0
{{P1_LIST}}

## Condensation (optional this pass)
{{CONDENSATION_TOP3}}

## Constraints
- Minimal diffs; match existing conventions (AGENTS.md, .cursorrules, naming.conventions.md)
- Never commit secrets; never commit unless the user asks
- User conversation in Spanish; code/commits/frontmatter in English
- Linear: when closing issues, comment what was done (/done MAK-XX per architecture.rules.md)

## Deliver back to user
- What was fixed vs deferred (with paths)
- Remaining P1/P2
- Recommended next step (sync-auditor, supply-chain-audit, deep pass on X, etc.)
```
