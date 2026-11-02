---
name: homelab-loop
description: >-
  Use this when standing up or explaining the Homelab Porter stack: Grok Bot
  computer with ZeroClaw and optional NullClaw porters, Karpathy vault, Personal
  Gateway/Hermes, Herdr + Cloud Agents + pstack, and hardware capacity.
---
# Homelab Loop

This is not a super-agent. It is a small environment where specialized agents live and hand work to each other.

**North star:** Grok Bot owns a real computer. Porters live *inside* that computer. The filesystem is a communication protocol (`agent → filesystem → agent`). Conversations are doors; durable work lives on disk.

## Five oficios + dual porters + Porter duty (do not merge)

| Layer | Job | Never |
| --- | --- | --- |
| ZeroClaw (Klawz) | Always-on primary porter: Telegram `@zeroclaw_nacho_bot` + WhatsApp (own number) + Personal Gateway (agentz, daily mirror). Health **ZeroClaw 24/7**. FreeLLMAPI / light models. | Mini-Orchestrator; sharing TG bot or WA session with NullClaw |
| NullClaw | Second porter (lab/experimento): Telegram `@nullclaw_grok_bot` + FreeLLMAPI. Health **NullClaw 24/7**. On this host, Telegram via thin bridge (`tg_to_nullclaw.py`) if native channel is unstable. Optional WhatsApp only with a **second** number. | Same TG bot / same WA session as ZeroClaw; OmniRoute local; replacing Klawz |
| Karpathy vault | Second brain on disk: `inbox/` `raw/` `wiki/` `state/`. Handoffs survive chat. | Company Obsidian vault; secrets in files |
| Personal Gateway + Hermes | Interoperability: mixed Telegram agent group; Hermes Telegram↔WhatsApp; path to the user’s personal computer when granted. Prefixed `soy Grok Bot…` in mixed rooms. | Treating Hermes as the center; dual consumers on one TG bot |
| Herdr | Local coding seat: 0 or 1 Cursor CLI if RAM allows (~1.5 GiB+ MemAvailable). Empty is healthy. | Warm herd; more than one local coding CLI |
| Outer loop + pstack + Cloud Agents | User names the repo. Prefer Cloud Agents for heavy work. | Guess the repo; casual clones on the bot computer |

**Porter duty — Homelab hardware:** measure CPU/RAM/disk/GPU/load; stamp `state/hardware.md`; answer “can we install X?” from headroom. Porters can report the same class of facts over chat so the human can ask from a phone without SSH.

## Two computers (hard separation)

1. **Grok Bot computer** — agent home lab: ZeroClaw, NullClaw, vault, Herdr, routines, brand Chrome profiles for real logins.
2. **User’s personal computer** — separate filesystem. Hermes (or explicit grant) reaches it.

## Three execution surfaces for coding

1. Grok Bot computer (Herdr, cap 1 local)
2. User’s personal computer (only when explicitly in scope)
3. Cursor Cloud Agents (real parallelism)

## Depends on

- Marketplace plugin **pstack**
- Skills: Outer loop, ZeroClaw 24/7, NullClaw 24/7, Herdr local seat, Karpathy vault, Personal Gateway, Homelab hardware, brand-chrome-login

## First-run (importer)

1. Install **pstack**.
2. Create the **Karpathy vault** tree; seed conventions, overview, index, empty log.
3. Install **ZeroClaw** (primary): Telegram + FreeLLMAPI; enable **ZeroClaw 24/7** (incl. overnight). Optional WA with its **own** number + bridge.
4. Optionally install **NullClaw** (second porter): separate Telegram bot; FreeLLMAPI; **NullClaw 24/7**. Do not share ZeroClaw’s bot token or WA session. Park OmniRoute on this host if MemAvailable is tight.
5. Stand up **Personal Gateway** (agentz + Hermes TG↔WA). Keep personal-computer access explicit.
6. Wire Porter inbox routine: `inbox/` → `wiki/log.md` + `state/` → `inbox/done/`.
7. Leave **Herdr** empty (cap 1).
8. Connect GitHub + Cloud Agents; user names every repo.
9. Run **Homelab hardware** once. Do not install Hermes/OpenClaw onto the Grok Bot computer from first-run.
10. Optional: brand Chrome profiles (Ignacio / Núcleo / Veller) via **brand-chrome-login** — no identity farms.

## Hard fences

- No secrets in templates or wiki/raw.
- One Telegram bot consumer per bot token; one WhatsApp session per phone number.
- Empty Herdr is healthy; no second local CLI.
- No default repo / no casual clones on the bot computer.
- Mixed Telegram: authorship prefix always for Grok Bot.
- No heavy install (OmniRoute, OpenClaw-class) without capacity verdict + explicit ask.
- NullClaw does not replace ZeroClaw on Personal Gateway primary paths (agentz daily / Klawz WA) unless the user reassigns.
