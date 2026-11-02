---
name: nullclaw-24-7
description: >-
  Use this when installing NullClaw as a second porter on the Grok Bot computer,
  or when creating/running the 24/7 health routine that keeps its Telegram
  bridge up day and night.
---
# NullClaw 24/7

NullClaw is the **second** porter on the Grok Bot computer (lab/experimento). It is not ZeroClaw/Klawz and not Grok Bot.

## Standing duty

Keep the NullClaw Telegram path healthy 24/7. If it dies, restart it. Ping the user only if it stays down after restart.

## Health check (this host’s shape)

1. Prefer the thin Telegram bridge: pidfile `/home/box/.nullclaw/tg-bridge.pid` whose cmdline contains `tg_to_nullclaw.py` (native `nullclaw gateway` + Telegram may segfault — do not force it).
2. If healthy: stamp `last_ok` (user-local time) into `state/nullclaw.md`. Send nothing.
3. If unhealthy: run `bash /home/box/.nullclaw/start-daemon.sh`, wait, re-check.
4. If recovered: one short line that NullClaw was down and restarted.
5. If still down: ping with the last ~20 lines of `/home/box/.nullclaw/logs/tg-bridge.log`.

## Identity fences

- Telegram bot must be **separate** from ZeroClaw’s bot.
- WhatsApp (if any) needs a **second** phone number / session — never Klawz’s WA.
- FreeLLMAPI (or equivalent light path) for intelligence; no local heavy LLM.

## Routine shape

- Every 15 minutes including overnight (availability).
- Scope: health + restart only. No inbox processing, no Herdr, no chat replies from this routine.

## Fences

- Do not expand into coding or map work.
- Do not spam when healthy.
- Do not start OmniRoute on this machine from this routine.
