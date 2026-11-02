---
name: agent-contract
description: >-
  Usar al crear o cambiar un bot Grok, para dejar mandato corto + Must NOT +
  reporta a + aristas, sin duplicar oficio.
---
# Agent Contract

Antes de crear: lee todos los profile.json en /home/box/agent-data/agents. Si alguien ya cubre el oficio, no crees.

Campos:
- runtime: grok | hermes | hybrid
- family: Director | GM | Business Scout | Personal Scout | Closer | otro
- estado: vivo | stub | backlog
- reporta a / manda a
- mandato (1 frase)
- owns
- Must NOT
- ≠ anti-overlap
- cadencia
- output / formato: brief | hallazgo | handoff-local | roster | approve
- ledger state: ready | partial | missing | local-only
- tools / DB IDs reales
- aristas Comm-Graph
- A-gates

Alta: Grok Bot crea. Forja propone. Ignacio aprueba si es estructural o A3. Actualiza roster + comm graph. No GMs stub ni Closer sin cola.
