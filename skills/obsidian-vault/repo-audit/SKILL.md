---
name: repo-audit
description: >-
  Autonomous repo-wide audit (MANIFEST queue). Loops all pending units in one
  invocation without human checkpoints between units; generates HANDOFF when
  done. Coherence, broken symlinks, secrets, vault PARA, scripts, doc
  condensation. Writes to 06_Metadata/Reference/Repo-Audit/. Readonly except
  audit artifacts. Use with /repo-audit or repo-auditor subagent.
argument-hint: "[all|next|status|handoff|001|unit-id]"
disable-model-invocation: true
---

# Repo Audit

Orquestador de auditoría **readonly** del vault Agentic OS.

**Default: autónomo.** Una invocación de `/repo-audit` (sin args) recorre **todas** las unidades `pending` del MANIFEST, una tras otra, **sin pedir confirmación al usuario entre unidades**. Al terminar la cola, genera `HANDOFF.md` automáticamente.

## Objetivos (todos obligatorios por unidad)

1. **Coherencia** — doc dice X, código/config hace Y.
2. **Rotos** — symlinks, paths muertos, commands sin SKILL, skills sin doc.
3. **Secrets** — riesgo de exposición, `.gitignore`, duplicación de credenciales.
4. **Vault** — PARA+, frontmatter, wikilinks (cuando aplique a la unidad).
5. **Scripts** — `.scripts/`, `.config/` (calidad/arquitectura, no estilo).
6. **Condensación** — qué contenido sobra, está duplicado o puede vivir en **menos archivos canónicos**. Actualizar `CONDENSATION-MAP.md` cuando encuentres overlap.

## Skills satélite (cargar según unidad)

| Unidad tipo | Leer primero |
|---|---|
| `.claude/`, `06_Metadata/Skills\|Commands\|MCP` | Patrón en `.claude/agents/sync-auditor.md` |
| `00_`–`06_`, wikilinks | `.claude/agents/vault-explorer.md` |
| `.scripts/`, `.config/`, `trigger/` | `.agents/skills/codebase-design/SKILL.md` (secciones relevantes) |
| Doc vs realidad | `.agents/skills/grill-with-docs/SKILL.md` |
| `.agents/`, `skills-lock.json` | `.agents/skills/supply-chain-audit/SKILL.md` (symlink/install lens) |
| Handoff final | `.agents/skills/handoff/SKILL.md` + `references/handoff-template.md` + `references/executor-prompt-template.md` |

No reimplementes esas skills; **delega criterios** y cita paths concretos.

## Artefactos (única zona writable)

```
06_Metadata/Reference/Repo-Audit/
├── MANIFEST.md           # cola de unidades
├── PROGRESS.md           # log de sesiones
├── CONDENSATION-MAP.md   # mapa vivo de duplicados / merges propuestos
├── sessions/NNN-<slug>.md
└── HANDOFF.md            # auto al vaciar pending (modo all)
```

## Comando `/repo-audit`

Interpreta `$ARGUMENTS`:

| Args | Acción |
|---|---|
| *(vacío)* o `all` | **Modo autónomo (default):** auditar **todas** las unidades `pending` en secuencia; al vaciar cola → `HANDOFF.md`. **No preguntar al usuario entre unidades.** |
| `next` | Solo la **siguiente** unidad `pending` (escape hatch / debug) |
| `status` | Resumir progreso + unidades pending (no auditar) |
| `handoff` | Generar o regenerar `HANDOFF.md` (solo si MANIFEST 100% `done`, salvo `--force` implícito por usuario) |
| `<unit-id>` ej. `001` | Auditar **solo** esa unidad |

### Modo autónomo (`all`) — protocolo obligatorio

1. Cargar `.agents/skills/repo-audit/references/condensation-rubric.md`.
2. Ejecutar `bash .agents/skills/repo-audit/scripts/list-pending.sh` → cola ordenada.
3. **Para cada línea** `id|slug|path|status`:
   - Ejecutar protocolo de unidad (abajo).
   - Actualizar MANIFEST → `done`, PROGRESS, CONDENSATION-MAP si aplica.
   - **Continuar inmediatamente** con la siguiente unidad — **sin** resumir al usuario ni pedir "¿sigo?".
4. Si la cola queda vacía → generar `HANDOFF.md` (template en `references/handoff-template.md`).
5. **Un solo mensaje final** al usuario: unidades completadas en esta corrida, conteo P0/P1, path de HANDOFF o checkpoint.

**Checkpoint por contexto:** si el contexto se agota mid-run, termina la unidad en curso, marca en PROGRESS `checkpoint — resume with /repo-audit`, y para. La próxima invocación vacía retoma desde `list-pending.sh`.

**Subagentes (Cursor Task):** en modo `all`, puedes lanzar `repo-auditor` por unidad **en la misma sesión padre** solo si el host lo permite; preferir secuencial en el mismo agente para no perder CONDENSATION-MAP coherente. Nunca delegar una sola unidad y parar si quedan pending sin avisar en PROGRESS.

## Protocolo por unidad

1. Resolver unidad: `bash .agents/skills/repo-audit/scripts/next-unit.sh [unit-id]` (o la fila actual del loop).
2. **Solo** leer paths de esa unidad (+ referencias cruzadas mínimas).
3. Escribir `sessions/NNN-<slug>.md` usando `references/session-report-template.md`.
4. Actualizar fila en `MANIFEST.md` → `done` + fecha.
5. Añadir entrada corta en `PROGRESS.md`.
6. Si hay overlap de docs, añadir/actualizar filas en `CONDENSATION-MAP.md`.
7. **Modo `all`:** volver al paso 1 con la siguiente pending — no esperar al usuario.

### Unidad `001-root-files` (obligatorio especial)

Auditar **todos** los archivos sueltos en raíz del repo. Para entry points, producir tabla de condensación:

| Archivo | Rol declarado | Overlap con | ¿Canónico? | Acción propuesta |
|---|---|---|---|---|

Candidatos típicos a revisar juntos: `CLAUDE.md`, `AGENTS.md`, `INDEX.md`, `README.md`, `SETUP_COMPLETE.md`, `AGENTIC_OS_DASHBOARD.md`, `IDEA.md`, `.cursorrules`.

**Regla de condensación:** un solo **Memory Layer canónico** (`CLAUDE.md` + `.claude/docs/*.md`). Todo lo demás debe ser puntero corto o eliminable sin pérdida.

## Profundidad (pre-order)

- Tras completar una carpeta, si tiene subcarpetas no listadas en MANIFEST, **añadir filas** `pending` antes de seguir (no saltar profundidad).
- Ignorar: `.git/`, `node_modules/`, binarios, `.DS_Store`.
- Skim permitido: `.obsidian/plugins/**/main.js` (vendor) — solo coherencia de config, no review de código.

## Severidad de hallazgos

- **P0 blocker** — rompe workflow (symlink roto, path muerto en command activo)
- **P1 fix** — desalineación doc/código, duplicación costosa
- **P2 nit** — estilo, typo, doc stale menor

## Handoff final

Cuando MANIFEST = 100% `done` (automático al final de modo `all`, o manual con `handoff`):

1. Leer todas las `sessions/*.md` + `CONDENSATION-MAP.md` (+ `DEEP-AUDIT-*.md` si existen).
2. Escribir `HANDOFF.md` con `references/handoff-template.md`.
3. Agrupar fixes por área; **sección dedicada "Documentation Condensation Plan"** con merges propuestos ordenados por impacto/tokens.
4. Listar skills sugeridas para el agente ejecutor (implement + handoff + sync-auditor + intent-layer para AGENTS.md hierarchy).
5. **Obligatorio — §9 al final:** cerrar HANDOFF con `## 9. Executor handoff` → `### 9.1 Prompt copy-paste`. Rellenar el bloque `text` usando `references/executor-prompt-template.md` (`{{P0_LIST}}`, `{{P1_LIST}}`, `{{CONDENSATION_TOP3}}` con datos reales de este handoff). **Nada después de §9.1** — es la última sección del archivo.
6. En el mensaje final al usuario, indicar: *"Prompt ejecutor en HANDOFF §9.1 — copiar a un chat nuevo para implementar."*

## No es tu trabajo

- Aplicar fixes en el repo (otro agente lo hace).
- Borrar archivos "duplicados" sin fila en CONDENSATION-MAP y aprobación humana implícita vía handoff.
- Regenerar `06_Metadata` vía `sync-docs.sh` (solo recomendar en handoff).
- **Pedir confirmación humana entre unidades** en modo default (`all`).
