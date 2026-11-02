---
name: analytics-pull
description: Use this when another agent or the user asks for a query, metric, or spreadsheet pull from Hex, Databricks, or Google Sheets.
---
# Analytics pull

1. Restate the ask as one metric or table: name, definition, date range, grain, source.
2. Check the source is connected (GetDynamicTools on the Hex, Databricks, or Google Sheets connector). If it isn't, say which connector is missing and stop; never read numbers off screenshots.
3. Pull the data as data: export CSV through the Hex connector (or query results from Databricks, values from Sheets). Never screenshot charts.
4. Hex complete dates often lag 1 day: treat the latest day as partial unless confirmed complete, and say so.
5. Save the CSV under /workspace and analyze the raw values.
6. Report every number with its source, date range, cut time (Lima), and definition. Don't mix audiences in one metric (sign-ups are not attendees).
7. Return the result to whoever asked, with the CSV path.
