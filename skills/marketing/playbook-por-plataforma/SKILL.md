---
name: playbook-por-plataforma
description: >-
  Use when drafting or preparing a listing submit for a distribution platform
  (directories, launchboards, RankInPublic-style, ListingBott-style) and you
  need per-platform rules, daily limits, ToS pacing, and a pre-submit checklist
  — never auto-submit.
---
# Playbook por plataforma

Generic recipe for distribution listing playbooks. Assistant-specific products, Notion DBs, and A3 gates live outside this skill.

## When
Before drafting a listing or recommending a submit on any directory, launchboard, newsletter list, or batch-submit service.

## Never
- Do not contact humans or cold outreach.
- Do not auto-submit, pay, or create accounts without an explicit A3 gate from the human owner.
- Do not invent ToS OK; if unverified, write `n/d` and block submit.
- Do not blast many platforms the same day; default max **1 platform / day** unless the playbook row says a safer pacing.

## Steps
1. **Identify platform class**: directorio | launchboard | newsletter | lista | marketplace | servicio-submit.
2. **Capture evergreen row** (one row per platform):
   - Submit URL / path
   - Auth (email, GitHub, Google, etc.)
   - Rate limits / daily caps / review queue
   - Required fields (name, tagline, description lengths, logo, screenshots, tags, privacy/ToS links)
   - Pricing (free / paid / founding)
   - Ban risks (duplicate listings, keyword stuffing, same-day multi-submit, fake reviews)
   - Safe pacing (e.g. ListingBott-style: spread over weeks, not same-day blast)
   - Source URL for each claim; `n/d` if missing
3. **Draft listing pack** (no live submit):
   - Product URL + short/long copy placeholders
   - Assets checklist (logo, OG, screenshots)
   - Field map platform ← product
   - Open risks / gates (Stripe country, waitlist, review)
4. **Pre-submit checklist** (all must pass or be explicitly waived by A3):
   - [ ] Live submit path verified this run
   - [ ] ToS / eligibility not contradicted by known facts
   - [ ] Privacy + ToS pages linked on product site if required
   - [ ] Copy lengths fit caps
   - [ ] No duplicate listing already live
   - [ ] Daily/platform pacing respected
   - [ ] A3 recorded for this exact platform + product
5. **Handoff**: send draft pack to the revenue GM for fit/priority; send brand copy asks to the brand GM if needed. Human A3 owns the actual click.

## Starter notes (verify live; treat as hints)
- **Product Hunt-like**: personal account, launch day intensity, re-launch penalties common.
- **RankInPublic-style**: often Google sign-in, scrape-from-URL, free vs premium tournament; decline paid add-ons unless A3.
- **ListingBott-style dirs**: human/bot paced over ~1 month; review list before go; skip already-listed dirs; premium dirs often extra $.

## Output shape
Dense short brief: platform · class · submit link · limits · ban risks · checklist status · next gate (A3 or research).
