---
name: loop-corp
description: >-
  Use when running the Grok corp: HITL 1:1 with Ignacio, team work in rooms,
  ritual clock, vault-first, two-layer reports. During a timed sprint, run
  Sprint Parallel first. Not raw scout noise — see hallazgo / reporte-gm.
user-invocable: true
---
# Loop Corp (Grok Bot)

Use this when running Ignacio’s Grok corp: 9h sprints, GM cycles, new bots, or any “how does the company talk?” question.

**If the sprint has a defined reset/cut time, run [Sprint Parallel](../sprint-parallel/SKILL.md) first.** That skill turns on dual-channel (1:1 GMs + rooms) and max parallelization until the cut. This file is the standing corp OS.

## Comm

```
Ignacio 1:1 (HITL) → Grok Bot   results, A3, decisions
Grok Bot → sala GMs+Orquestador   orders
GMs → their staff rooms
Bot ↔ bot 1:1 OK
Scout → GM hallazgo
GM → sala GMs → Grok Bot
Grok Bot → Ignacio 1:1 weekday 09:00:
  1) 5 reporte-gm (Forja, Levy, Brandy, Inti, Oppy) — lo importante
  2) corte Grok Bot — lo más más (máx 3 TOPs)
```

No spam a canales existentes. Rooms GM = one-to-many.

Ignacio’s personal chats are HITL: he looks at results. Do not dump wiring there. GMs never write Ignacio. Scouts never.

Outside a timed sprint, command GMs from the GM room and do not 1:1 them for ops. **During a timed sprint, also 1:1 each GM in the same beat** (see Sprint Parallel). Never DM scouts. Forja is split Core / ROI (cap 6).

## Factory

GM proposes. Grok Bot creates. Ignacio if structural or A3. Frozen: Closer, Ventas, Partnerships, caja-bot, Skool/WhatsApp, publishers, identity farm. No crear bots desde este skill.

## Loop

intent → GMs en paralelo → staff `hallazgo` → GM audita + 1 mejora → `reporte-gm` → Grok Bot resume a Ignacio.

## Ritual clock (America/Lima)

Scouts 05:15–06:20. Hermes 06:30/06:45/07:00. Pulso Día 07:10. GMs 07:25–07:50. Grok Bot HITL pack 09:00 (5 GM + corte). Close 21:00. Sunday ritual. Monthly caja, no A4.

Sprint: aggregators, not executors. NotebookLM = Hermes.

## Formato

Exact [hallazgo](../hallazgo/SKILL.md) and [reporte-gm](../reporte-gm/SKILL.md). **Do not invent a third.**

Hallazgo:

```text
SCOUT
OFERTA / SEÑAL (1 frase)
LINKS
SCORE ROI o urgencia (1–5)
FIT (1–5) — vs Memory Setup / perfil (obligatorio si scout = Programas & Perks)
TAG (opcional): embajador | beca | hackathon
NEXT STEP sugerido (no ejecutar A3)
```

Reporte GM:

```text
GM
PERÍODO
TOP 1–3 (una línea + link + score)
DESCARTADOS (conteo, no lista)
PEDIDO A SCOUTS (próximo barrido)
PROPUESTA BOT (opcional, 1 máx, a Grok Bot — no crear)
A3 (sí/no — solo si hay que gastar/publicar/cerrar)
```

- Newest-on-top into existing `Ledger-{Forja,Levy,Brandy,Inti,Oppy}.md`.
- Headings + fenced field block. No prose soup.
- One line per TOP: offer + link + score.
- DESCARTADOS = count, not a list. No invented fields or numbers.
- YAML: single frontmatter, no duplicated `---`.
- Gold paste: Ledger-Inti.
- Mid-session = vault. Session close = same Notion page if a URL exists. Else stay vault and say `ledger missing`. Do not create DBs or pages.
- All Tasks / Finance OS / Comms stay their own schemas. GM reports do not become those rows.
- Flojo (sin link/score, DESCARTADOS-lista, cifra inventada) = Grok Bot lo devuelve al GM. Ignacio ve `n/d` en ese hueco.

## Procesos (sprint)

Idle / solo-ack is a bug. Each GM owns ONE end-to-end flow mapped to vault skills, not a random hallazgo. Run them **in parallel** (Sprint Parallel).

| GM | Flujo | Skills |
|---|---|---|
| Forja | corte ventas | Pulso Revenue → hallazgo → reporte-gm |
| Levy | ritual AM | Renovaciones + Pulso Día (assemble-day) → reporte-gm; caja = Hermes |
| Brandy | lote editorial | Eventos/Calendario/Comunidad/Inspiración → Borrador A1 (sim) → reporte-gm |
| Inti | learning | research-pipeline → Inbox/Ingesta → Síntesis → NotebookLM (Hermes) |
| Oppy | mapa OS | verifica que los 4 flujos existen en vault; 1 gap |

Workspace rooms (Núcleo, GPT-Chain, Veller, Crafter) map their own 4 boxes when those brands are the ROI north star.

Sala GMs = loop. Each cycle: trigger → skill → output → owner. No invented numbers.

## Vault

Vault-first. Drafts off-vault ok. Docs en vault = pensados, no dumps. Migrar a Notion al cerrar sesión (Hermes). No tocar Notion durante el loop.

Skills: `hallazgo` (scout → GM) · `reporte-gm` (GM → sala GMs → Grok Bot).
