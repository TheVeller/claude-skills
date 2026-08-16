# Executor prompt template (HANDOFF §9.1)

> Plantilla para la **última sección** de `HANDOFF.md`. El auditor **rellena** los placeholders al generar el handoff; el usuario copia el bloque `text` completo a un agente implementador.

## Reglas

- **Siempre** incluir como `## 9. Executor handoff` → `### 9.1 Prompt copy-paste (agente implementador)`.
- **Siempre al final** del HANDOFF, después de References / Out of scope.
- P0 y P1 deben ser **concretos** (copiados del handoff, no genéricos).
- Si hay deep-audit reports (`DEEP-AUDIT-*.md`), mencionarlos en Context.

## Skeleton (rellenar al generar HANDOFF)

````markdown
## 9. Executor handoff

> **Última sección del handoff.** Copia el bloque siguiente en un chat nuevo (Agent / Codex / `implement`).

### 9.1 Prompt copy-paste (agente implementador)

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
````

## Placeholder guide

| Placeholder | Source |
|-------------|--------|
| `{{P0_LIST}}` | Numbered list from HANDOFF § P0 table (issue + path + fix) |
| `{{P1_LIST}}` | Top 5–10 P1 items or "See HANDOFF § P1 — Fixes by area" if too long |
| `{{CONDENSATION_TOP3}}` | Top 3 CONDENSATION-MAP rows by priority, or "None this pass" |
