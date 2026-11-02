---
name: exportar-bot
description: >-
  Usar al migrar, exportar o respaldar Grok Bots (un bot, un departamento o la
  cuenta): cada export produce siempre 3 variantes en orden: 1) plantilla nativa
  de Grok Bot (CreateBotShareJson, la corre el propio bot), 2) .tgz (paquete
  neutral + tenant OpenBot) y 3) prompt .md para pegar en Notion Agent u otras
  plataformas (Instinct, Open Bot, Cue).
---
# Exportar bot

## 🧭 Cuándo usar y quién decide
- Se acabaron los slots de Grok Bot y hay que liberar uno, o se quiere un respaldo portable antes de archivar un bot.
- Destino por defecto, en este orden: **Instinct** → **Open Bot** → **Cue**. Si el usuario nombra otro, usa el mapeo genérico (paquete neutral) y la sección más parecida.
- Grok Bot sigue siendo dueño del roster: avísale antes de empezar (qué bot, a dónde, por qué).
- El usuario decide cuál bot sale y aprueba el borrado. Nunca se borra el bot Grok hasta que el nuevo esté verificado.
- Todo lo que sea publicar, enviar o crear cuenta en la plataforma nueva es acción del usuario o necesita su OK explícito.


## 🧱 Las 3 variantes (siempre, en este orden)
1. **Plantilla nativa de Grok Bot.**
   - El bot que se exporta corre **CreateBotShareJson** él mismo, siguiendo la skill administrada por Cursor `export-bot-template`.
   - Si exportas **otro** bot, no lo empaquetas tú: le mandas un **SendToAgent con priority: true**:
     "Ignacio pidió exportar tu plantilla. Sigue la skill export-bot-template y corre CreateBotShareJson ahora: memorias generalizadas, tus skills y routines, sin datos personales. Responde con el link o archivo."
   - La tarjeta con el link le aparece al usuario en el chat de ese bot.
2. **.tgz:** paquete neutral (Paso 2) y, si aplica, el tenant OpenBot (Paso 2b) → `/workspace/exports/<bot-slug>.tgz`.
3. **Prompt .md para pegar:**
   - `NOTION-AGENT-PROMPT.md` (ver "Formato Notion Agent prompt") y, para otras plataformas, `INSTINCT-ONBOARDING.md`.
   - Ambos van dentro de la carpeta y se re-empaqueta el .tgz.

## 🎯 Paso 0 · Alcance (lo elige el usuario)
| Alcance | Qué entra | Cuándo |
|---|---|---|
| **Bot** | Un bot | Liberar un slot o respaldar uno antes de archivarlo. |
| **Departamento** | Un GM, sus bots y su sala (p. ej. Forja + Forja Core) | Mover un área entera sin romper la cadena de reporte. |
| **Cuenta** | Todos los bots (40+) y todas las salas | Salida completa de Grok o respaldo total. |
- **Pertenencia a un departamento:** sale de `profile.json` → `description` ("bajo X", "Hallazgo → X", "Reporta a X") y de `group.json` (`memberIds`) de la sala del GM. Mapa vigente: `/workspace/exports/departamentos.md`.
- **Ambiguos** (en la sala del GM pero su descripción reporta a otro, p. ej. Cazador Gangas → Forja): **no entran** salvo que el usuario lo diga.
- Ignacio aprueba el alcance y la lista final de bots **antes** de armar nada. Grok Bot recibe el aviso (qué bots, a dónde, por qué).
- Con 40+ bots: un departamento a la vez. No hacer fan-out a todos los bots sin el OK del usuario.

## 📦 Paso 1 · Inventario del bot (solo lectura)
Ruta base: `/home/box/agent-data/agents/<id>/`. No modifiques nada.
- **Persona y oficio:** `profile.json` → `name`, `description`. Completa con la sección de instrucciones del bot (oficio, anti-oficios, escritura) y su home/Evergreen en Notion.
- **Memoria portable:** `memory/profile.md` y `memory/log/AAAA-MM.md`. Copia hechos de trabajo y convenciones. Salta líneas `[episode]` y `[note]`. No leas `user-memory` ni shards de proyecto.
- **Routines:** `automations/<slug>/automation.json` → `name`, `prompt`, `schedule` (cron, hora Lima), `enabled`. Lee el job, no copies el JSON tal cual. `runs.json` solo sirve para ver si corría.
- **Skills:** las skills de usuario están en `/home/box/agent-data/workflows/<slug>/SKILL.md` y son compartidas. Exporta solo las que el bot nombra en sus routines, memoria o instrucciones.
- **Conectores/MCP:** anota qué servicios usa (Notion, Gmail, Sheets, Composio, etc.) según routines y skills. Solo nombres y para qué; nunca tokens.
- **Identidad y canales:** inbox propio, salas o grupos donde habla, a quién reporta. Datos de Notion: links al home, Evergreen y fila del Inventario.
- **Secretos:** nunca abras `box-secrets.json`, `host-secrets.json`, `connector-secrets/` ni cookies. Las credenciales viajan por el gestor de contraseñas; en el paquete solo va el título de la entrada.

## 🧠 Paso 1b · Volcado de memoria (antes de armar)
- **El executor no tiene RecallMemory.** Solo ve `memory/profile.md` y `memory/log/*.md` en disco. Lo que cada bot recuerda por RecallMemory no está en el disco.
- **Propuesta** (pide el OK del usuario antes de mandar los mensajes, uno por bot o por departamento):
  - El dueño del export (Bot Father o el agente principal) manda un SendToAgent a cada bot:
    ```
    Vamos a exportar tu oficio a OpenBot. Usa RecallMemory (scope agent) con consultas amplias sobre tu oficio, tus reglas, tus fuentes, tus routines y tus skills, y escribe tus hechos PORTABLES en /workspace/exports/<depto>/<id-del-bot>/memory.md: una línea por hecho, en español. Sin líneas [episode] ni [note], sin contraseñas, tokens ni datos personales de terceros. No inventes nada. No cambies tus routines. Responde solo "listo" con el número de hechos.
    ```
  - Luego re-corre el builder: toma `/workspace/exports/<depto>/<id>/memory.md` y `/workspace/exports/memory-dumps/<id>.md` si existen.
- **Sin volcado**, el bot sale solo con la memoria del disco. Anótalo en `MIGRATION.md`.

## 🗂️ Paso 2 · Paquete neutral
Arma `/workspace/exports/<bot-slug>/` (Markdown plano, sin secretos):
```
<bot-slug>/
├── AGENT.md        # persona + oficio + anti-oficios + escritura
├── memory.md       # hechos y convenciones portables
├── skills/<slug>.md
├── routines.md     # cron Lima + prompt
├── connectors.md   # servicios y permisos, sin tokens
├── identity.md     # canales, mail, a quién reporta (sin secretos)
└── MIGRATION.md    # checklist de este traslado
```
**AGENT.md**
```
# <Nombre del bot>
## Oficio (una línea)
## Qué hace (bullets)
## Anti-oficios: qué NO hace y a quién se lo deja
## Reglas fijas (aprobaciones, datos permitidos, cadencia)
## Escritura (idioma, tono, formato de reportes)
## A quién reporta y cómo
```
**routines.md** (una por bloque)
```
## <nombre>
- Cron: `47 22 * * *` (America/Lima) · en palabras: todos los días 22:47
- Tope: <tiempo/criterio de parada>
- Prompt: <texto del job, sin nombres privados>
- Entrega: <canal/persona> · solo si hubo avance: sí/no
```
**connectors.md**: `servicio · para qué · permiso mínimo (leer/escribir) · entrada del gestor de contraseñas (solo título)`.
**identity.md**: `mail del bot · canales · grupos · reporta a` (sin contraseñas ni códigos).
**MIGRATION.md**: copia el checklist de los pasos 3–5 y marca cada ítem.
Comprime con `tar czf <bot-slug>.tgz <bot-slug>/` para guardarlo en Drive/Notion si el usuario lo pide.

## 🧰 Paso 2b · Paquete de tenant OpenBot (bot, departamento o cuenta)
**Formato real** (verificado en github.com/CopilotKit/openbot, `docs/configuration.md` § Tenant package y `server/src/tenant-package.ts`):
- **No hay import por zip.** El servidor lee una carpeta que nombra `TENANT_PACKAGE_DIR` (por defecto `examples/fintech`) y la valida al arrancar. El `.zip` es solo transporte: se descomprime y se apunta la variable a `tenant/`.
- **Archivos requeridos:** `brand.yaml`, `agents.yaml`, `channels.yaml`, `model.yaml` y `knowledge.yaml`.
- **Opcionales:** `skills.yaml`, `theme.css` y `agents/` (un coworker por archivo).

Estructura que arma `/workspace/exports/tools/build_openbot_pkg.py`:
```
<salida>/
├── README.md · MIGRATION.md · ROUTINES.md · routines.json · build-report.json · <alcance>.zip
└── tenant/
    ├── brand.yaml · model.yaml · knowledge.yaml · channels.yaml · agents.yaml (vacío)
    ├── agents/<id>.yaml   # uno por bot: id, name, title, role_description ≤1000, avatar_seed, type: built-in, system_prompt, skills
    ├── skills.yaml        # deduplicadas por slug
    ├── memory/<id>.md     # memoria portable por bot
    └── workspace/<id>/    # solo con --include-workspace-files
```
- **Skills compartidas:**
  - Una sola entrada por slug en `skills.yaml`. Cada bot las nombra en su lista `skills:`.
  - Si un slug falta o se repite, el servidor no arranca.
  - Formato del slug: 2–40 caracteres en minúsculas, dígitos y guiones.
  - `tools` va solo si está verificado. Nombrar un tool no lo otorga: el admin lo otorga por bot.
- **Salas → `channels.yaml`:**
  - Campos: `id`, `name`, `description`, `permitted_agents` y `allowed_groups`.
  - ⚠️ El paquete **no crea membresías** de personas; se agregan a mano.
  - ⚠️ `allowed_groups` no controla nada hoy.
  - La sala de GMs solo entra en el alcance Cuenta.
- **Routines:**
  - El paquete **no puede sembrarlas** (`docs/routines.md` § Scope).
  - Van en `ROUTINES.md` como pedidos para pegar en el chat de cada bot, siempre con **zona America/Lima**: OpenBot usa **UTC** por defecto.
  - Límites: piso de 15 min, máx. 20 activas por persona, y el admin debe otorgar `create_routine`.
  - Las pausadas se marcan y no se crean.
- **Memoria:**
  - El paquete no tiene campo de memoria.
  - Va al final del `system_prompt` (por defecto) y en `memory/<id>.md`.
  - La memoria de CopilotKit Intelligence / Automatic Learning no se siembra desde el paquete.
- **Seguridad del builder:**
  - Nunca lee archivos de secretos, cookies, `store.db` ni Bitwarden.
  - Redacta mails personales de terceros.
  - Si encuentra algo con forma de secreto, para y no arma el zip.
  - `model.yaml` lleva solo `credential_secret_ref` (una referencia, nunca la llave).
- **Uso:**
  - `python3 /workspace/exports/tools/build_openbot_pkg.py --scope bot|dept|account --target <id|GM> [--out DIR] [--include-ambiguous] [--no-memory-in-prompt] [--include-workspace-files] [--no-zip]`
  - Requiere PyYAML: `pip install --user --break-system-packages pyyaml`.

## 🔁 Paso 3 · Mapeo por plataforma
### Instinct (instinct.com) — prioridad 1
- Es un agente personal por mensajería: WhatsApp, iMessage, SMS y un mail propio `@mail.instinct.com`. La web es panel de admin.
- **No hay import ni campo de system prompt visible.** El traslado es conversacional: manda `AGENT.md` y `memory.md` por mail o chat y pídele que lo guarde como memoria de trabajo. Confirma con una pregunta de recall.
- **Memoria:** archivos markdown versionados + datos de conectores indexados + bóveda de credenciales (llena, no revela). Credenciales: vía el link de bóveda que da Instinct, nunca por chat.
- **Routines:** se despierta por reloj o por eventos (mail, calendario, docs, ubicación). Pide cada routine en lenguaje natural con hora Lima explícita.
- **Skills:** no hay formato de skill publicado. Pega el texto de cada skill como instrucción guardada.
- **Conectores:** Google Workspace, Slack, Notion (confirmados). MCP propio: no verificado.
- ⚠️ Es **un agente personal por cuenta** (grupos aparte). Varios bots Grok dentro de Instinct = oficios fusionados; deja los anti-oficios muy claros o usa otra plataforma.
- ⚠️ Invite-only, sin precio publicado; políticas de entrenamiento con datos (opt-out en settings).

### Open Bot (CopilotKit, github.com/CopilotKit/openbot) — prioridad 2
- Plantilla open source (MIT, alpha) auto-hospedada con Docker Compose + PostgreSQL + tu propia API key de modelo. Cada bot tiene su computadora (browser, archivos).
- **Persona:** un archivo por bot en `examples/<tenant>/agents/<id>.yaml` o en `agents.yaml`: `id`, `name`, `title`, `role_description`, `system_prompt`, `skills`. Pega `AGENT.md` en `system_prompt`.
- **Skills:** `skills.yaml` → `slug`, `title`, `summary`, `instructions`, `tools` (`<serverId>/<tool>`). Cada `skills/<slug>.md` = una entrada.
- **Routines:** se crean pidiéndolas en un canal; el admin debe otorgar `create_routine` en `/admin/plugins/routines`. Piso de 15 min, máximo 20 activas por persona, se apagan tras 10 fallos.
- **Conectores:** MCP y catálogo (Google Drive, Notion…) otorgados por bot por un admin. Canales en `channels.yaml`; Slack/Teams vía OpenTag.
- **Memoria:** no hay archivo de memoria declarado; usa archivos en el workspace del bot o métela en `system_prompt`. "Automatic Learning" (CopilotKit Intelligence) aprende de conversaciones.
- ⚠️ Sin WhatsApp ni mail nativo verificados; requiere servidor propio corriendo 24/7 (box, homelab o VPS).
- Alternativa si "Open Bot" significaba **OpenClaw** (docs.openclaw.ai): `SOUL.md` ← persona, `AGENTS.md` ← reglas/anti-oficios, `USER.md` ← preferencias, `MEMORY.md` + `memory/AAAA-MM-DD.md` ← memoria, `openclaw cron` / automations ← routines.

### Cue (Manus, cue.im) — prioridad 3
- App de agentes personales (web, desktop, iOS, Android). Varios agentes por cuenta, cada uno con mail, número, wallet y computadora (según disponibilidad).
- **Persona:** cada agente tiene nickname + descripción ("responsabilidad" + contexto). Pega el oficio en la descripción y el resto de `AGENT.md` como contexto inicial.
- **Memoria:** memoria propia por agente; carga `memory.md` como primer mensaje y pide que lo guarde.
- **Routines:** "Scheduled Automation" se crea describiendo qué y cuándo. Escribe hora Lima explícita.
- **Canales:** iMessage, Telegram, LINE, Slack (Agent Info → Integration → Messenger). WhatsApp no figura.
- **Conectores:** Gmail, Slack, Notion y otros con permiso. API: `open.manus.ai` (`agent.update` cambia nickname/descripción).
- ⚠️ Invite code, gratis en early access, precio futuro y del número no publicados. Formato de skills: no verificado.

## ✅ Paso 4 · Verificación (smoke test)
- Una routine dispara a su hora (o una de prueba a +10 min) y entrega donde debe.
- Un recall de memoria: pregunta un hecho de `memory.md` y compara.
- Un mensaje por su canal **solo al usuario**, nunca a terceros.
- Paridad: oficio ✔ · anti-oficios ✔ · cada routine ✔ · cada skill ✔ · conectores ✔ · canal ✔ · aprobaciones (no publica sin OK) ✔.
- Anota en `MIGRATION.md` lo que no tiene equivalente y el workaround elegido.

## 🧹 Paso 5 · Cierre
1. Actualiza la fila de cada bot migrado en el inventario de agentes: Plataforma = nueva, Estado = migrado, link al paquete.
2. Avisa a Grok Bot por mensaje directo: bot, destino, qué quedó sin paridad.
3. Pausa (no borres) las routines del bot Grok.
4. Pide al usuario que borre el bot Grok cuando confirme el nuevo; nosotros no podemos borrar agentes.
5. Guarda el `.tgz` como respaldo si el usuario lo quiere.

## 🚫 Qué no hacer
- No meter secretos, tokens, códigos 2FA ni contraseñas en el paquete ni en chats.
- No incluir datos personales de terceros ni líneas `[episode]`/`[note]`.
- No borrar ni pausar el bot Grok antes de la verificación y el OK del usuario.
- No crear cuentas, publicar ni enviar mensajes en la plataforma nueva sin aprobación.
- No cambiar el roster sin avisar a Grok Bot.
- No mandar volcados de memoria ni mensajes a varios bots sin el OK del usuario.
- No meter ledgers ni archivos de trabajo (`--include-workspace-files`) sin revisarlos: pueden traer datos de terceros.
- No inventar campos: si un dato de la plataforma no está verificado, márcalo y pregunta.

## 🧩 Formato Notion Agent prompt (.md)
Úsalo cuando el destino sea un **Custom Agent de Notion**. Se escribe como `<bot-slug>/NOTION-AGENT-PROMPT.md` y luego se re-empaqueta el `.tgz`.
- **Antes:** revisa en la web la ayuda vigente (notion.com/help/custom-agents y las guías). Confirma triggers, Tools and access, Web access, Trusted URLs, créditos y límites de largo. Cita las fuentes con fecha.
- **1. Setup:**
  - Nombre.
  - Un trigger Recurring por cada horario de las routines, en zona America/Lima; cada trigger lleva una sola hora.
  - Trigger opcional por @mención.
  - Accesos sugeridos: páginas y DBs con su permiso. No crees DBs; solo propónlas y pide OK.
  - Web access y Trusted URLs.
  - Canal de entrega.
- **Limitaciones → sustitutos (tabla):**
  - Sitios con login (p. ej. FB Marketplace) → página Inbox donde el dueño pega links.
  - SendToAgent → página o comentario con @mención, o Slack.
  - Memoria o archivos → página de referencia y tracker.
  - Créditos por corrida.
- **2. INSTRUCTIONS** (bloque en español, para pegar):
  - Oficio y pasos de cada corrida.
  - La vara, con `<placeholders>`.
  - Regla de silencio y anti-oficios.
  - formato-hallazgo fusionado.
  - Entrega y cadena de reporte.
  - Corridas.
  - Cuenta los caracteres y mantenlo corto.
- **3. Mensaje de prueba:** una corrida acotada, sin publicar, más una pregunta de recall sobre la vara y los anti-oficios.
- Sin secretos. Conserva los placeholders del dueño.

## ✅ Checklist final (las 3 variantes)
- [ ] **1. Plantilla nativa**
  - [ ] El bot corrió CreateBotShareJson (o recibió el SendToAgent con priority: true).
  - [ ] La tarjeta o link llegó al usuario.
  - [ ] Sin datos personales.
- [ ] **2. .tgz**
  - [ ] Tiene AGENT, memory, skills, routines, connectors, identity y MIGRATION.
  - [ ] Sin secretos, cookies ni `[episode]`/`[note]`.
  - [ ] Se listó el contenido con `tar tzf`.
- [ ] **3. Prompt .md**
  - [ ] NOTION-AGENT-PROMPT.md con setup, INSTRUCTIONS (caracteres contados) y mensaje de prueba.
  - [ ] Limitaciones con sustitutos y fuentes fechadas.
  - [ ] INSTINCT-ONBOARDING.md.
  - [ ] Re-empaquetado dentro del .tgz.
- [ ] Al usuario: rutas, tamaño, lo que no se pudo incluir y los pasos de import.
