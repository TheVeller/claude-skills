---
name: channel-triage-canales
description: >-
  Use when triaging scout CSV candidates into the channels database owned by
  Publisher.
---
# Channel triage into Canales

Owner of the channels database decides what enters.

1. Read new CSV files from the scout inbox that are not yet in the triage log.
2. Enter a row only if it is a destination where notion-publisher publishes or could publish on a recurring basis: social network, newsletter, blog or forum with API, community where you post, or marketplace product listing. Deduplicate by name and domain. Create in discover status; fill only properties that have a source; otherwise write no data.
3. Hand schedulers and aggregators to the directories owner. Hand one-shot directories and launchboards to their owners. Hand stores to the store owner. Do not create them in Canales.
4. Save triage-YYYY-MM-DD.csv with name, source, decision and reason.
5. Report to the owner only when something entered. Do not create databases, delete rows, publish, or open secrets.
