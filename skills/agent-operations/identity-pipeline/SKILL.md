---
name: identity-pipeline
description: >-
  Use when alta con identidad, auditing identity (incl. Composio fase 1,
  Postly/composio connect fase 3), Chrome profiles per-bot, or updating identity
  inventory.
---
# Identity pipeline (Bot Father)

Factory execution + **identity inventory** for agents/bots. **Grok Bot** = roster SSOT + “alta con identidad”. **Bot Father** = pipeline + identity ledger + CreateAgent when named. **Ignacio** = HITL + structural yes in 1:1.

## Must NOT
- Invent oficios / CreateAgent without Orq naming.
- Start without Orq + Ignacio OK.
- Skip HITL (captcha/SMS/2FA).
- Touch Mac Orca/Herdr (Hermes) or ZeroClaw (Orq) inside this pipeline.
- Duplicate Gmails for the same agent; paste secrets in chat.
- Replace Orq roster SSOT — only own **identity** columns.

## Phases (updated)
**Fase 1 — core (obligatorio antes de CreateAgent serio)**  
VPN → Gmail real → AgentMail → (número/Instinct si Orq pidió) → **cuenta Composio.dev** (por identidad o compartida según Orq) → Bitwarden (títulos en ledger) → Chrome profile dedicado → CreateAgent si aplica.

**Fase 2 — otras cuentas**  
Google Sign-In apps, redes (FB/IG/…), ChatGPT, etc. Solo con Ignacio OK y fase 1 estable.

**Fase 3 — cablear**  
Conectar todo a **Composio** (connectors del agente) + **social scheduler** (Postly LTD, hasta ~200 workspaces / cuentas ilimitadas según plan Ignacio). No crear Postly de nuevo si ya existe LTD; asignar workspace/cuentas.

## Chrome profiles
- Extensiones (Bitwarden, Surfshark, …) son **por perfil**, no globales entre bots.
- Homelab tools (VPN/vault): prefer perfil **Ignacio/Orq**.
- Identidad de agente: `~/.chrome-profiles/<slug>` propio; instalar extensiones ahí si esa identidad las necesita.
- Un alta a la vez; bajo RAM = un Chrome.

## Inventory
`/workspace/lab/state/identity-inventory.md` — no secrets; Bitwarden **title** only. Include composio account + postly workspace columns when known.

## Triggers
`/identity-pipeline`, Orq webhook alta. No Kit OS @mention cron. Fleet healthchecks off until Ignacio enables.

## Related
[alta-identidad](`alta-identidad` skill), [brand-chrome-login](../../agent-operations/brand-chrome-login/SKILL.md), Postly = fase 3 scheduler (Ignacio already has LTD).
