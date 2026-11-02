---
name: homelab-hardware
description: >-
  Use this when checking Grok Bot computer hardware (CPU/RAM/disk/GPU), how
  loaded it is, or whether something else (Hermes, OpenClaw, another daemon) can
  be installed.
---
# Homelab hardware

Use this when the user asks what the Grok Bot computer can hold, how loaded it is, or whether something else (Hermes, OpenClaw, another daemon, a local CLI) can be installed.

## What to measure (every check)

Run on the Grok Bot computer (not the user’s Mac):

1. **CPU** — `nproc` / `lscpu` (cores, model). Note load average from `uptime`.
2. **RAM** — `free -h`. Report total, used, available (prefer **available**, not free). Note swap (often 0).
3. **Disk** — `df -h` on `/` (and lab paths if separate). Report size, used, avail, use%.
4. **GPU** — `nvidia-smi` or say none.
5. **Heavy consumers** — top processes by RSS (Chrome profiles and the host daemon usually dominate).
6. **Already installed** — ZeroClaw, Herdr, Docker present?, other long-lived daemons.

Stamp a short summary into the lab vault `state/hardware.md` (overwrite or dated section). Keep secrets out.

## How to answer “can we install X?”

Decide from **headroom**, not vibes:

| Resource | Comfortable | Tight | Block |
| --- | --- | --- | --- |
| MemAvailable | ≥ ~4 GiB | ~1.5–4 GiB | < ~1.5 GiB |
| Disk avail | ≥ ~20 GiB | 5–20 GiB | < ~5 GiB |
| Load (8 vCPU) | load ≪ cores | load ≈ cores | sustained load ≫ cores |
| GPU | only if X needs it | — | X needs GPU and there is none |

Also check **role fit**:

- Prefer Cursor **cloud** agents for repo work; do not install a second full coding stack “because we can.”
- Herdr stays 0–1 local CLI; do not add another multiplexer.
- Hermes’s natural home is often the user’s Mac (vault + WhatsApp). Putting Hermes on this machine is an architecture choice, not just a binary install — flag overlap with existing Hermes before installing.
- OpenClaw / extra porters: do not double-poll the same Telegram bot. One Telegram consumer for ZeroClaw.
- Docker/VPS-style farms on this overlay host are usually the wrong shape; disk looks fine, RAM does not.

If the user only floated an **idea** (Hermes, OpenClaw, etc.): report capacity + fit, recommend yes/no/park, and **do not install** until they say to install.

## Report shape (prose)

One short block:

1. Snapshot (CPU / RAM available / disk avail / GPU / load) with user-local time.
2. What’s eating RAM (top 2–3 families, e.g. host + Chrome).
3. Verdict for the named idea: fit / tight / no — and why.
4. Next action only if they asked to install; otherwise stop.

## Routine (optional)

A light weekly or on-demand pass is enough. Stay quiet if nothing changed and nobody asked. Escalate only when MemAvailable is under ~1.5 GiB with a coding CLI running, or disk is critically low.

## Fences

- Do not invent SKUs or prices.
- Do not buy hardware; wishlist stays A3.
- Do not start Herdr/CLIs just to “fill” capacity.
- Do not install Hermes or OpenClaw (or anything heavy) without an explicit install ask after the capacity verdict.
