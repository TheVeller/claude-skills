---
name: herdr-local-seat
description: >-
  Use this when configuring Herdr as the 0–1 local Cursor CLI seat on the Grok
  Bot computer, or when a routine should enforce the coding-cap and RAM policy.
---
# Herdr local seat

Herdr is a lightweight multiplexer for local Cursor CLI panes on the Grok Bot computer. It sits. It does not think.

## Policy

- Empty by default. A stopped server or missing socket with an empty herd is **healthy**.
- Cap: **0 or 1** coding agent pane.
- Start the daemon only on demand when the outer-loop bot (or the user) needs a local seat **and** MemAvailable is above about 1.5 GiB.
- Chrome + the CLI eat RAM, not Herdr itself. Under ~1.5 GiB free, do not start a coding CLI.
- If Herdr shows more than one coding agent, stop the extras.

## Who thinks

The outer-loop bot writes pstack-quality prompts and prefers Cursor **cloud** agents. Herdr is only for work that must be local (fixtures, files cloud cannot see). Never clone repos onto this computer as the default path.

## Routine shape

- Light daytime check is enough (for example once in the morning).
- Stay quiet when empty/healthy and there is no coding work.
- Escalate only for HITL (spend, stuck agent) or when the cap/RAM rule was enforced.

## Fences

- Do not keep a warm herd “just in case.”
- Do not launch coding work from the Herdr routine; route repo tasks to the outer-loop bot.
- Do not treat empty Herdr as a blocker in inbox or porter loops.
