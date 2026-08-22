---
name: reporte-gm
description: >-
  Rollup GM → sala GMs → Orquestador. Use when Forja, Levy, Brandy,
  Inti or Oppy deliver the department digest. Grok workflow: reporte-gm.
  Not for raw scout noise.
user-invocable: true
---

# Reporte GM

El scout manda `hallazgo`. El GM manda este bloque a sala GMs → Orquestador. Silencio si no hay nada material. No GM → Ignacio.

```text
GM
PERÍODO
TOP 1–3 (una línea + link + score)
DESCARTADOS (conteo, no lista)
PEDIDO A SCOUTS (próximo barrido)
PROPUESTA BOT (opcional, 1 máx, a Orquestador — no crear)
A3 (sí/no — solo si hay que gastar/publicar/cerrar)
```

## Rules

- Silence if nothing material.
- Newest-on-top on the existing dept ledger (`Ledger-{Forja,Levy,Brandy,Inti,Oppy}.md`). Same fields, no extras, no invented numbers.
- Headings + the fenced block. One line per TOP item.
- DESCARTADOS = count, not a list.
- Forja = revenue 07:35. Levy = life 07:25. Brandy = brand 07:40. Inti = intelligence 07:45. Oppy = ops 07:50. Cadencia 07:25–07:50. Forja 08:44 is stale.
- Mid-session: vault. Session close: paste into the existing Notion page-ledger if a URL exists (do not create a new DB or page). Else stay vault and say `ledger missing`.
