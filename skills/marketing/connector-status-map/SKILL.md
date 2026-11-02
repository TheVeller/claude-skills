---
name: connector-status-map
description: >-
  Use before proposing a publish or turning a connector live; read the Content
  OS map and CAPABILITIES.md.
---
# Connector status from the notion-publisher map

Before proposing a publish or installing a connector, read the Mapa notion-publisher page in Content OS and the repo CAPABILITIES.md.

States to use:
- Live with dry-run gate: code ready; webhooks still dry-run until the owner enables the live gate and sets WEBHOOK_TOKEN.
- Live dry-run: code on main; needs API keys or *_PUBLISH_LIVE flags (Typefully, Postiz, Eventbrite via Composio).
- Dry-run only, discover, stub, or read-only scraper: do not publish through them.
Never call a connector live without SWE confirmation and the owner's explicit yes. Never invent webhooks. Never print secrets.
