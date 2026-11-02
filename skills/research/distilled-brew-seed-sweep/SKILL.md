---
name: distilled-brew-seed-sweep
description: Use this when a daily content-inspiration sweep reads Distilled Brew (daily top-5 GitHub/Product Hunt/Hacker News digest) to find seeds for a niche, before proposing any item.
---
# Distilled Brew seed sweep

Distilled Brew (https://distilledbrew.com) is a JS-rendered page with no RSS. Read it through its public API instead.

## Steps
1. GET https://gtxjjyyirjenzserckvk.supabase.co/functions/v1/api-digests?limit=3 with curl, no auth. Take the newest digest: number, date and its top-5 items. If the newest number equals the last one already swept, there is no delta: stop.
2. If the API fails or is empty, fall back to the web page. If neither reads, write n/d and stop; never invent items.
3. Niche-filter each item against the niche list the calling bot keeps. Drop anything off-niche.
4. Check the no-re-seed list before seeding: search memory and the vault for the item's name or URL. Skip any item already seeded or parked unless there is a real delta (new release, license change, own demo, big star jump).
5. Verify each surviving repo on GitHub: stars, license (n/d if NOASSERTION or missing), latest release tag and date. Untested claims go "según el README del autor".
6. Score each seed 1-5 stars for fit, link the original item plus the digest number, and use the caller's finding format.
7. Save the raw API response and the picks to the run's vault folder, then record the seeded items in memory as do-not-re-seed.
8. Zero seeds means silence: send nothing.
