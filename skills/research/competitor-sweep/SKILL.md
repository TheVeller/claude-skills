---
name: competitor-sweep
description: Use this when running a periodic competitor sweep (DIRECT peers + REFERENCE players) and deciding whether anything is material enough to report.
---
# Competitor sweep

1. Window: since the last sweep (~48h; Monday covers the weekend). Read the last sweep log so nothing is re-reported.
2. For each watched brand, fetch first-party pages of each DIRECT peer: pricing page, store listing (Chrome Web Store version + date, Gumroad price), services page, Luma/event page. Fetch REFERENCE players only for launches or pricing/GTM plays.
3. Diff against the previous sweep notes (save notes per run in a dated folder in the workspace).
4. Material = new product or offer, price change, plan limits changed, new GTM or event format. Not material = version-only bumps, locale diffs, bugfixes, hiring, blog posts without an offer.
5. If material: one block per finding in the finding format (signed with the bot name, DIRECT/REFERENCE tag, one link, score 1-5, next step). Send only to the configured destination.
6. If nothing: send nothing anywhere.
7. Log the sweep in memory: date, window, result (sent finding or NADA_NUEVO), notes folder.
8. If a search tool is out of quota, continue with plain fetches. Repeated source/auth failure: tell the owner once.
9. Never contact anyone, publish, or change product or pricing.
