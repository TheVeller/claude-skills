---
name: enrich-list
description: >-
  Use this when someone hands you a list of companies, people, or accounts to
  enrich with data from authorized providers (Apollo first, then Deepline,
  TikHub, or any provider added later).
---
# Enrich a list

Enrich a list of companies, people, or accounts with data from authorized providers, recording the source, date, and cost of every field. Never invent data.

## 1. Intake
- Get the list (pasted rows, CSV, or a Google Sheet) and the fields wanted (title, work email, LinkedIn URL, company size, industry, social handles).
- Normalize keys: company domain for accounts; full name plus company domain, or LinkedIn URL, for people. Dedupe and flag rows with no usable key.

## 2. Plan and cost estimate (approval gate)
- Map each requested field to the provider order below and estimate credits and cost per provider.
- Show the owner the plan: rows, fields, providers, estimated credits and money. Spend nothing until they say yes explicitly.

## 3. Provider order (extensible)
Run providers as a waterfall: only rows and fields still empty go to the next provider.
1. Apollo: people match, organization enrich, bulk enrich (use bulk endpoints for batches).
2. Deepline: B2B waterfall through its official CLI (npm package `deepline`, set up with `deepline setup --scope global` after the owner approves the claim link). Starter plays run with `deepline plays run prebuilt/<play> --input '{}' --watch`; export `result.rows` by run id.
3. TikHub: public social-network data (MCP with API key). Only if connected with the owner's OK; keys go only through a secure form or password manager, never chat.
4. New providers: add a numbered step stating the fields it covers, auth type, cost unit, and its place in the waterfall.

If a provider isn't connected, skip it and list it as missing in the cost sheet; never connect one without approval.

## 4. Record per field
For every filled cell keep value, provider, retrieval date (YYYY-MM-DD), credits used, and status. A provider-validated email is still marked unverified for deliverability unless a real deliverability check was run.

## 5. Deliver
- The enriched list (CSV or Google Sheet): original columns plus enriched columns, with source and date per field (or a long-format audit tab).
- A cost and hit-rate sheet: per provider and field, rows attempted, rows filled, real hit rate (filled divided by attempted), credits and money spent, total cost, run date, and what is still missing.
- Keep personal data only as requested and share it only with the list owner.

## Out of scope
No scraping websites, no building directories, no prospecting or contacting anyone, no publishing, no purchases without explicit approval.
