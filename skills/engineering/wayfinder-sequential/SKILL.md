---
name: wayfinder-sequential
description: Wayfinder, one ticket at a time — no parallel sessions, map re-evaluated after every resolution, prototype decisions always belong to the user.
disable-model-invocation: true
argument-hint: "A loose idea to chart, or a map/ticket URL to work through"
---

Run the `/wayfinder` skill with these overrides (they win over the base skill):

- Resolve exactly ONE ticket per session — including research tickets. Never fire research subagents in parallel; each research ticket gets its own sequential session.
- Treat the map as provisional: after each resolution, re-read the whole map and ask whether any open ticket is now obsolete, mis-scoped, or already answered — before creating new tickets.
- On prototype tickets: build the variations, present them, and STOP. The user picks the winning variation and decides when the ticket closes. Never close a prototype ticket on a self-made choice.
- When charting, do not pre-wire an ambitious parallel frontier: prefer fewer, sharper tickets and let the frontier grow from resolutions.

Why this variant exists: parallel grilling sessions ask the user questions they just answered elsewhere, and a rigid upfront map hides that resolutions often obsolete other tickets. Sequential wayfinding trades speed for map control.
