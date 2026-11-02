---
name: brand-chrome-login
description: >-
  Use this when creating or using a Chrome brand profile on the Grok Bot
  computer (Ignacio / Núcleo / The Veller), signing into a real Gmail, pausing
  for 2FA/HITL, or doing Sign in with Google on one named service — never for
  identity farms or mass signups.
---
# Brand Chrome login (native Grok Bot desktop)

## When
- Need a **named brand Chrome profile** on the Grok Bot computer.
- Sign into a **real** Gmail for that brand.
- Optionally: **Sign in with Google** on **one** named service the user requested.

## Never
- Identity farms, rotating Gmails, mail→social→mass signup pipelines.
- Extra CLIs (Playwright/Puppeteer/Selenium) unless the user later asks for scripted repetition *and* RAM allows.
- Skipping 2FA / captcha / passkey — those are HITL.
- Inventing emails or passwords in chat; use in-chat forms or box handoff.

## Allowed profiles (default set)
- `Ignacio` — personal
- `Nucleo` — Núcleo Lab
- `Veller` — The Veller

Only create others if the user names a real brand. Cap: few profiles; one active Chrome session when MemAvailable is tight (~&lt;2 GiB prefer one profile at a time).

## Prerequisites (read first)
1. Cursor-managed `box-desktop` before any desktop/browser dispatch.
2. Cursor-managed `in-chat-forms` before any typed login/OTP step.
3. Homelab hardware check if MemAvailable looks under ~1.5 GiB — do not open a second heavy Chrome.

## Recipe
1. **Confirm** with the user (or prior message): profile name, Gmail address, and optional target service URL. One service per run.
2. **Profile dir** on the Grok Bot computer, e.g. `/home/box/.chrome-profiles/<slug>` (slug: `ignacio`, `nucleo`, `veller`). Create dir if missing. Launch Chrome with that `--user-data-dir` via computerUse (not Shell CDP/Playwright).
3. **Open** `https://accounts.google.com/` (or Gmail). Prefer cookie-import path from box-desktop only when appropriate; otherwise fresh login.
4. **Typed gate:** snapshot → `request_user_form` for email/password when fillable; else `request_box_help`. Never ask them to paste secrets in chat.
5. **2FA / passkey / device prompt:** `request_box_help` (or OTP form with `submitAfterFill` when it is a single code field). Wait for handback.
6. **Verify** signed-in Gmail (account chip / mail.google.com) with screenshot or snapshot. Stamp lab state: profile, email (non-secret), date, status.
7. **If a service was named:** open that URL → “Sign in with Google” → pick the brand account → HITL if challenged → confirm landed session. Document service + profile in state. Stop after that one service.
8. **Close or leave** Chrome: leave the profile session warm if the user will continue; otherwise close to free RAM. Mention which.

## State
Update `/workspace/lab/state/chrome-brand-profiles.md` (create if needed): profile, Gmail (address only), services signed in, last_ok, notes. No passwords/tokens.

## Report to user
Short prose: profile ready or not, whether Gmail is in, which service (if any), and what HITL they did. Offer the next single service only if useful.

## Main default Chrome (2026-09-27)
- The **default Chrome profile** on the Grok computer is branded **Ignacio (human main)** — personal Bitwarden + `[REDACTED: email]`.
- Do not treat default Chrome as the synthetic `grokbot.veller` vault profile.
- Brand dirs under `~/.chrome-profiles/` remain for Núcleo / Veller / extras; create new profiles only when Ignacio asks.

## VPN (Surfshark)
- Surfshark Chrome extension is on the Ignacio main profile.
- Use it when creating **new real Gmail** identities (identity stack).
- For Incognito: enable "allow in Incognito" for Surfshark (and Bitwarden only if needed) so VPN works in private windows.
