---
name: saves-library-sync
description: Use when pushing an archive of saved links into a content-library app that extracts data with a credit-based scraper, or when retrying items that came back empty or in error.
---
# Sync saves into a content library

1. Load the saves store (one row per save: platform, url, author, date if any, short text). Deduplicate by URL.
2. Capture in batches with the library's capture tool. Log every result (url, item id, status, error) to a dated sync JSON next to the store. Never print the API key.
3. After each batch, check real item status. Treat empty data as an error even if the app says ready.
4. Do not re-capture a URL already in the library (it returns duplicate). Reprocess the item id instead; if the connector bridge lacks reprocess, call the server HTTP API with the same key.
5. Retry the platform with most errors first. Stop the run on a 402 (scraper out of credits) and write remaining ids to a retry-targets file.
6. Recharging credits is a payment: ask the owner, never pay.
7. Report counts per platform and the queue file path. Stay silent if nothing new.
