---
name: personal-gateway
description: >-
  Use this when standing up or explaining the Personal Gateway: Telegram agent
  group, ZeroClaw and optional NullClaw porters, Hermes Telegram↔WhatsApp, and
  how Grok Bot posts with an authorship prefix.
---
# Personal Gateway

Bidirectional bridge between agent surfaces. Not an extra brain. Not a mini-Grok Bot.

**Hermes is interoperability, not the center.** Homelab Porter / Grok Bot owns the agent-computer layer.

## Layers it joins

1. **Hermes** — Mac vault, skills, WhatsApp Hermes, Hermes Telegram identity.
2. **Grok Bot / Homelab Porter** — HITL + map + homelab. Grok 1:1. Not a Telegram bot.
3. **ZeroClaw (Klawz)** — primary porter: Telegram + optional WhatsApp (own number). Personal Gateway daily / agentz primary.
4. **NullClaw** — second porter (lab): own Telegram bot; optional WhatsApp only with a **different** number. Does not own agentz unless reassigned.
5. **Personal Gateway** — mixed Telegram group (commonly `agentz`) + documented WA mirrors.

## Who writes where

| Who | How | Rule |
| --- | --- | --- |
| Human owner | their Telegram user | yes |
| ZeroClaw | primary Telegram bot on Grok PC | yes; groups prefer mention_only |
| NullClaw | second Telegram bot | own allowlist; never ZeroClaw’s token |
| Hermes-Telegram | Hermes on Mac | yes; no reply-loop echo |
| Grok Bot | Telegram Web as the human | every post starts with `soy Grok Bot…` |

## WhatsApp

- **Klawz WA:** Homelab Porter ops (1:1, groups Klawz / Grok Bot open, General mention-only); daily mirror tags Hermesto LID.
- **NullClaw WA:** only after a **new** number is provisioned and bridged; never share Klawz session.
- Hermes owns Hermes WhatsApp ↔ Telegram. Do not conflate with porter WA numbers.

## Caps

- One consumer per Telegram bot token; one WhatsApp session per phone number.
- Do not run `zeroclaw channel doctor` casually (rotates bind codes).
- Composio must not poll the ZeroClaw Telegram bot.
- Keep porters dumb relative to Grok Bot.

## First-run

1. Mixed Telegram group (human + ZeroClaw + Hermes-Telegram).
2. Allowlist ZeroClaw; mention_only in groups.
3. Optional: add NullClaw bot to lab surfaces with its own allowlist.
4. Hermes TG ↔ WA both directions.
5. Grok Bot in group only with `soy Grok Bot…`.
6. Smoke-test ZeroClaw path; separately smoke NullClaw if installed.
