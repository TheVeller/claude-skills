---
name: hallazgo
description: >-
  Formato scout → GM. Use when a cazador reports an oferta or señal.
  Grok workflow: formato-hallazgo. Surfaces: Grok, Hermes, Claude.
user-invocable: true
---

# Hallazgo

Scout caza. GM lee. Ignacio no recibe este bloque (salvo scouts personales → Orquestador).

```text
SCOUT
OFERTA / SEÑAL (1 frase)
LINKS
SCORE ROI o urgencia (1–5)
FIT (1–5) — vs Memory Setup / perfil (obligatorio si scout = Programas & Perks)
TAG (opcional): embajador | beca | hackathon
NEXT STEP sugerido (no ejecutar A3)
```

## Rules

- Business scouts → their GM (Forja / Brandy / Inti / Levy). Personal (Vivienda, Inmobiliario, Vuelos) → Orquestador.
- No peer-spam. No scout → Ignacio.
- Newest-on-top if the GM asks you to paste. Headings + fenced field block. No extra fields. No invented numbers.
- Do not create Notion DBs or new ledger pages. Mid-session: vault or GM chat. Session close: existing Notion ledger only; else stay vault and say `ledger missing`.

## Routing

| Scout | To |
|-------|-----|
| Canales, Demanda, Competitor, Perks, Resale, Wishlist-Biz, Vacaciones-ROI, Pulso Revenue | Forja |
| Cazador Eventos, Borrador Contenido | Brandy |
| Curador / Síntesis Learning, Inbox Triage | Inti |
| Vivienda, Inmobiliario, Vuelos | Orquestador → Ignacio |

No peer-spam. Ledger `missing` = no Notion write. A3 = Ignacio.
