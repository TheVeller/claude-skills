---
name: handoff-local-hermes
description: >-
  Usar cuando Grok necesite que Hermes ejecute algo local (vault, ADK, script,
  ledger Notion) y no deba hacerlo un scout.
---
# Handoff local

Canal: Telegram Hermesto (`web.telegram.org/a/#7381252761`, @theveller_n8n_bot). Composio bot API no ve chat_id 93372553. No uses GET_UPDATES (Hermes ya hace poll).

```text
FROM (Forja|Grok Bot) → Hermes
CAPACIDAD local pedida (skill/script/ledger)
INPUT IDs / links
OUTPUT esperado en Notion o vault
GATE A0–A4
```

Reglas:
- Ejecución local siempre vía Hermes, nunca desde un scout.
- A3 externo y A4 irreversible = Ignacio.
- Un handoff por encargo. No reenvíes el mismo paquete en el mismo sprint.
