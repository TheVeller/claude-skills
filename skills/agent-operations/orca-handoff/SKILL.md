---
name: orca-handoff
description: Use when handing work to a fresh agent and you also want the new session opened — writes the handoff document, spawns an Orca terminal with the agent, and delivers the prompt.
argument-hint: "What will the next session focus on?"
disable-model-invocation: true
---

Como `/handoff`, pero no se queda en el archivo: **abre la sesión nueva y le entrega el input**.

Un handoff que solo escribe un `.md` es medio trabajo — obliga al usuario a abrir terminal, arrancar el agente y pegar el contexto a mano.

---

## 1 · Escribir el documento de handoff

Aplica íntegras las reglas de `/handoff`:

- Guardar en el **directorio temporal del SO**, nunca en el workspace. Usa el scratchpad de sesión si existe.
- Incluir una sección **"Suggested skills"**.
- **No duplicar** lo que ya viva en PRDs, planes, ADRs, issues, commits o diffs — referenciarlo por path o URL.
- **Redactar** cualquier secreto: API keys, passwords, PII.
- Si el usuario pasó argumentos, son **el foco de la próxima sesión**: adapta el documento a eso.

Añade además, porque el agente nuevo arranca a ciegas:

- **Gotchas del entorno** que le harían perder tiempo (limitaciones de MCP, bugs de escapado, mounts raros, comandos que no existen en esta plataforma).
- **IDs y rutas literales** que necesitará (UUIDs, handles, paths absolutos) — que no tenga que redescubrirlos.
- **Estado del entorno** al cerrar: daemons corriendo o parados, rama actual, instalaciones recientes.

## 2 · Resolver el binario de Orca

Sigue la skill `orca-cli` para elegir el ejecutable. Resumen: `$ORCA_CLI_COMMAND` si está · `orca-dev` en checkout dev · **`orca-ide` en Linux fuera de terminales Orca** (ahí `orca` es el lector de pantalla de GNOME y arranca voz) · `orca` en el resto.

Comprueba que la app responde:

```bash
orca status --json
```

Si no está corriendo, `orca open --json`. Si el ejecutable elegido falla, **reporta el error exacto y para** — no pruebes otro binario, apuntaría a otra build.

## 3 · Cargar la guía versionada antes de ejecutar

```bash
orca skills get orca-cli
```

**No adivines subcomandos ni flags de memoria** — cambian entre releases de Orca. Es una guía larga; filtra la sección que necesitas (`grep -n -iE "terminal|handoff|worktree create"`) en vez de volcarla entera al contexto.

## 4 · Decidir: terminal en el checkout actual, o worktree nuevo

La decisión que más se equivoca. Regla:

| Situación | Comando |
|---|---|
| **El trabajo no toca código** — editar issues, planificar, investigar, documentar | `terminal create --worktree active` |
| **Toca código y necesita rama aislada** — implementar, refactorizar, trabajo paralelo | `worktree create --no-parent --agent <id> --prompt "..."` |

Un worktree nuevo para trabajo que no toca archivos del repo solo añade fricción y un checkout que limpiar después.

Para trabajo en paralelo con otros agentes, el worktree **sí** es obligatorio: sin aislamiento se pisan. Peor si el repo vive en Google Drive.

## 5 · Abrir la terminal y entregar el prompt

Caso corriente (mismo checkout):

```bash
orca terminal create --worktree active --title "<slug-de-la-tarea>" --command "claude" --json
orca terminal wait --terminal <handle> --for tui-idle --timeout-ms 90000 --json
orca terminal send --terminal <handle> --text "<prompt>" --enter --json
```

Caso worktree aislado:

```bash
orca worktree create --name <slug> --no-parent --agent claude --prompt "<prompt>" --json
```

`--agent` arranca el agente en la primera terminal y `--prompt` le entrega el trabajo; evita el patrón "crear worktree y luego abrir agente", que deja un shell huérfano.

**El `wait --for tui-idle` no es opcional** en el camino de dos pasos: mandar texto antes de que el TUI esté listo lo pierde.

Agentes disponibles como `--agent`: `claude`, `codex`, `omp`, `pi`, `grok`, y otros TUI instalados.

### Qué escribir en el prompt

No repitas el handoff — **apúntale a él**:

1. Ruta absoluta del documento de handoff, y de los artefactos que referencia (plan, PRD).
2. **El foco de la sesión**, en una línea.
3. Los 2-4 problemas concretos que va a encontrar, nombrados.
4. Las reglas de trabajo que no puede deducir (modo de checkpoints, dónde vive la fuente de verdad).
5. Los gotchas que más caro le saldrían.

## 6 · Parar

Un handoff completo **transfiere la propiedad**. Reporta la terminal y el handle creados, y **deja de monitorear**.

No uses `orca orchestration task-create` ni `dispatch --inject` ni `check --wait` — eso es orquestación supervisada, y se pide distinto. Si el usuario quiere supervisar, esperar resultados o coordinar un DAG, esta no es la skill: usa `orchestration`.

---

## Gotchas

| Problema | Qué hacer |
|---|---|
| `timeout` no existe en macOS | No lo uses en Bash; falla silenciosamente y devuelve output vacío. Usa `--timeout-ms` de Orca |
| Handle obsoleto (`terminal_handle_stale`) | Re-listar con `terminal list --worktree <selector> --json`. **Nunca** mandar a la vez al viejo y al nuevo |
| El id de worktree es de dos partes | `<repoId>::<worktreePath>`. Copia el campo `id` completo; el repoId solo no basta |
| Trabajo multi-commit bajo Google Drive | Parar el daemon antes (`.scripts/auto-commit-control.sh stop`) y matar los `fswatch` huérfanos a mano — el script de control los deja vivos |
| Guía de Orca en el contexto | 300+ líneas. Filtra con `grep`, no la vuelques entera |

## Relacionadas

`handoff` (solo documento) · `orca-cli` (guía completa del CLI) · `orchestration` (cuando sí quieres supervisar en vez de transferir)
