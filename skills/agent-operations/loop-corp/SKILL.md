---
name: loop-corp
description: >-
  Orquestador + GMs corren el loop corp (9h / standing). Use when
  dispatching the daily or standing corporate cycle. Not raw scout
  noise — see hallazgo / reporte-gm.
user-invocable: true
---

# Loop Corp

Ignacio → Orquestador → GMs → staff. Orquestador no DM a scouts.

## Comm

No spam a canales existentes. Rooms GM = one-to-many. Forja split Core / ROI (cap 6).

```
Ignacio 1:1 (HITL) → Orquestador   results, A3, decisions
Orquestador → sala GMs+Orquestador   orders, not 1:1 GM ops
GMs → their staff rooms
Bot ↔ bot 1:1 OK
Scout → GM hallazgo
GM → sala GMs → Orquestador → Ignacio 1:1 (reporte-gm / corte)
```

## Factory

GM propone. Orquestador crea. Ignacio si estructural o A3. Frozen: Closer / Ventas / Partnerships / caja-bot. No crear bots desde este skill.

## Loop

intent → GMs en paralelo → staff `hallazgo` → GM audita + 1 mejora → `reporte-gm` → Orquestador resume a Ignacio.

## Ritual clock (America/Lima)

Scouts 05:15–06:20. Hermes 06:30/06:45/07:00. Pulso Día 07:10. GMs 07:25–07:50. Orquestador digest to Ignacio 09:00. Close 21:00.

Sprint: aggregators, not executors. NotebookLM = Hermes.

## Formato

Exact `hallazgo` and `reporte-gm`. Do not invent a third.

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
PROPUESTA BOT (opcional, 1 máx, a Orquestador — no crear)
A3 (sí/no — solo si hay que gastar/publicar/cerrar)
```

- Newest-on-top into existing `Ledger-{Forja,Levy,Brandy,Inti,Oppy}.md`
- Headings + fenced field block. No prose soup.
- One line per TOP: offer + link + score.
- DESCARTADOS = count, not a list.
- No invented fields/numbers.
- YAML: single frontmatter, no duplicated `---`
- Gold paste: Ledger-Inti
- Mid-session = vault. Session close = same Notion pages if URL exists; else stay vault and say `ledger missing`. Do not create DBs or pages.

## Vault

Vault-first. Drafts off-vault ok. Docs en vault = pensados, no dumps. Migrar a Notion al cerrar sesión (Hermes). No tocar Notion durante el loop.

Skills: `hallazgo` (scout → GM) · `reporte-gm` (GM → sala GMs → Orquestador).
