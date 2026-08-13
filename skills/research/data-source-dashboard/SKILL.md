---
name: data-source-dashboard
description: Turn any raw data source (CSV export, API pull, hand-entered numbers) into a decision-ready interactive dashboard published as an Artifact — 12-section taxonomy, aggregates-only privacy, observed/benchmark/assumed provenance on every number, ES/EN + dark/light, interactive scenarios, and one mechanism diagram via excalidraw-diagram. Use when the user hands over a data export and wants analysis they can act on, or says "hazme un dashboard de estos datos", "analiza este export", "qué me dice esta data", "dashboard de métricas", "build a dashboard from this CSV", "turn this into a dashboard".
---

# Data source → decision dashboard

Distilled from a real build: an 18k-member community export turned into growth, funnel, forecast and a monetization ladder, iterated with its owner until it changed decisions. This is that pipeline, generalized.

## Sources

- [references/section-taxonomy.md](references/section-taxonomy.md) — the 12 sections, what each answers, minimum inputs, chart type
- [references/design-system.md](references/design-system.md) — tokens, 3-state theme, chart specs, i18n, nav, provenance tags
- [references/doctrine.md](references/doctrine.md) — privacy boundary + the rules learned the hard way. Read before writing numbers.
- `templates/analyze.template.mjs` · `templates/dashboard.template.html` — the scaffold `new-dashboard.sh` copies
- Diagrams (optional dependency): the [`excalidraw-diagram`](https://github.com/coleam00/excalidraw-diagram-skill) skill. Install it alongside this one, or skip step 6.

## When / When not

**Use** when there is a real data source and a decision behind the question ("should I pay for this tier", "where is growth coming from", "what do I do next").

**Do not** use for a one-off number the user just wants answered in chat, for dashboards over live production DBs (this pipeline is snapshot-based), or to publish anything containing personal data — see doctrine.

## Workflows

### 1. Scope the source and the decision

Ask what decision the dashboard has to serve, then inventory the source: columns, row count, date range, what is measured vs hand-entered. Name the sections the data actually supports — an empty section is worse than a missing one.

### 2. Scaffold

```bash
bash <skill-dir>/scripts/new-dashboard.sh <dest-dir> "<Dashboard Title>"
```

Put `<dest-dir>` where the user keeps projects. When no home is obvious, scaffold in the session scratchpad and ask before writing into their tree.

### 3. Aggregate — raw stays home

Edit `analyze.mjs` (it ships with CSV parsing, daily/weekly/monthly series, cohorts, funnel, spikes, channel velocity, forecast scenarios, age). It reads the raw file **in place** (Downloads, a gitignored dir) and writes `metrics.json` with **aggregates only**.

```bash
node analyze.mjs "<path-to-raw-export>"
```

### 4. Audit the aggregates

Recompute the headline numbers a second way before anything is rendered. Every disagreement is a bug in `analyze.mjs` until proven otherwise.

```bash
node <skill-dir>/scripts/audit.mjs <project-dir>
```

### 5. Build the dashboard

Fill the template's sections following `references/section-taxonomy.md` and `references/design-system.md`. Every number carries a provenance tag; every assumption is a toggle; every section closes with a computed sentence.

```bash
node <skill-dir>/scripts/build.mjs <project-dir>
```

### 6. Diagram the mechanism

One diagram per dashboard: the loop, ladder or attribution flow the charts cannot show. Never restate numbers already on a chart. Follow the `excalidraw-diagram` SKILL.md — its palette, its render-and-look loop:

```bash
cd <excalidraw-skill-dir>/references
uv run python render_excalidraw.py <project-dir>/visuals/<name>.excalidraw
```

Read the rendered PNG with the Read tool, fix, re-render. Source `.excalidraw` stays in `<project-dir>/visuals/`; `build.mjs` inlines the PNG as a `data:` URI wherever the template has `__DIAGRAM_<NAME>__` (the Artifact CSP blocks external assets).

### 7. Verify in a browser, then publish

```bash
cd <project-dir> && python3 -m http.server 8791   # then drive it with Playwright
```

Check: no horizontal scroll at 1200/900/390, console clean, toggles recompute the charts, light and dark both legible, ES and EN both complete. Then publish `dashboard.html` with the Artifact tool. Republishing the **same file path** keeps the same URL — always iterate in place.

### 8. Refresh with a new export

`README.md` in the project records the exact refresh commands. Re-run steps 3→7; the artifact URL does not change.

## Rules

1. Aggregates only in the published page. The audit script is the gate, not a formality.
2. Tag every number `observed` / `benchmark` / `assumed`, and render the tag.
3. Never replace a measured line with a modeled one. Measured data survives redesigns.
4. Assumptions are toggles, never hardcoded constants buried in prose.
5. One number, one source: define it once, reference it everywhere, so sections cannot contradict each other.
6. A chart nobody can read is a bug — legend, direct labels, and a "how to read this" line.
7. Sections end in a sentence that states what the data means, not in a number.
8. Recompute staleness and projections from the viewer's clock, so a snapshot ages honestly.

## Failure modes

- `new-dashboard.sh` exit 2 = missing arguments · exit 3 = destination exists (never clobbers)
- `audit.mjs` exit 1 = a gate failed (PII, credentials, or sums that do not reconcile). Fix the data, not the gate.
- Raw export sits in a synced folder (Drive, Dropbox): read it in place, never copy it into the repo.
- Diagram renderer needs one-time setup: `uv sync && uv run playwright install chromium`.
- Publishing as an Artifact is a Claude Code feature; without it, `dashboard.html` is a standalone file that opens in any browser.

## Report

- Where the project lives and where the raw source stayed
- Which sections were built and which were skipped for lack of data
- The audit result and the anti-PII / anti-credential gate result
- The artifact URL, plus the two or three findings that would change what the user does next
