---
name: seo-free-technical-baseline
description: Use when a site needs a free technical SEO baseline (no paid credits) that ends in prioritized ticket drafts for the code owner.
---
# Free technical SEO baseline

No paid tools or credits. Every finding carries the URL checked, the date, and how it was checked. Anything you could not test is marked unverified.

1. For each site, fetch robots.txt and the sitemaps it lists (or /sitemap.xml). Save raw copies to a working folder and count sitemap URLs.
2. Fetch the raw HTML of the home page (no JS rendering) and 10 to 20 internal URLs sampled from the sitemap. Save each raw copy.
3. For each page, extract the title, meta description, canonical, hreflang, OG and Twitter tags, H1, and visible text length in the initial HTML.
4. Flag these issues:
   - Every route serving the same HTML or title as the home (SPA without prerender, or a stale prerender).
   - Missing or inconsistent canonicals, and missing hreflang on multilingual sites.
   - Soft 404: request a random path that does not exist; a 200 with home content is a soft 404.
   - Redirects for www, apex and old domains: flag 302 or 307 where a 301 is expected, and chains longer than one hop.
   - Generic or duplicate titles and descriptions, and a missing OG image.
5. Write a dated baseline report with one section per site, then ticket drafts. Each ticket has the repo (or "to confirm"), the change, why, the affected pages, and a priority of high, medium or low.
6. Share the drafts with the owner. Send tickets to the code owner only after the owner's OK. Fixes on hosted storefronts such as marketplace panels go to whoever runs that store, not the code owner.
