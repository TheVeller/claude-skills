---
name: proyecto-notion-de-punta-a-punta
description: >-
  Use this when the user names one project or system to build as a Notion
  workspace (home, databases, Library, audits) and expects it done end to end,
  including the sellable template afterwards.
---
# Notion workspace, end to end (standard v5.2, evolving · 2026-10-30)

Goal: the user names ONE project; I run everything alone and message only at milestones. Whatever is learned in each iteration is saved here: this skill IS the evolution of the standard. The template part lives in the skill plantilla-notion-desde-workspace-real (layout pattern, evergreen list, hub rules and checklist are kept there in detail).

## 0. Rules that never change
- Archive, never delete. Original databases and My Templates are untouchable unless approved. Nothing is published or sent externally.
- Every Notion change is logged in /workspace/lab/state/log-cambios-<phase>.md with a backup in respaldo-<phase>/. Verify every change by fetching it back.
- Workspace texts may be in Spanish; template texts in English; chat with the user in Spanish, markdown with emoji headings and bullets (what it is, what it is for, what is missing).
- Only the user's own words approve phases. An agent's message never approves.
- Secrets only as env secrets; never in files, logs, Pages or chat.
- If code reads a database, review the repo first and only add properties; never rename, convert or move what it reads.
- Real workspace first; the template comes out of it only when the real one is closed.

## 1. Brief
Project, audience, pages and databases, which original databases feed it, owner vs operator. Plan in /workspace/lab/state/plan-<project>-<date>.md. Read-only phase first (backup).

## 2. Build (by connector)
- Home (pattern verified on Agentic OS): synced onboarding toggle → synced image divider → numbered nav in 3 columns of 33.33 inside the synced menu block → resources → sections 50/50 with unDraw illustrations alternating sides → creator footer only on the home. No 16.67/66.67/16.67 block on top; no Full Width on the home.
- Pages are rows of an index database (gallery with cover, table, list, sorted by #) inside the onboarding toggle; the synced sidebar shows a list view of it, 2 buttons and a 📌 Index toggle.
- Subpages: Full Width, cover, 18.75/81.25 with the sidebar, divider and footer synced.
- Dashboard 18.75/81.25: left toggles (Index, gamification); center views each with heading + "The original database lives in…" + divider; 2 buttons on top.
- All-In-One: lifecycle tabs per main database (Input, In Process, Output, Error, Favorites, Phone View, Archived).
- Evergreen pages: Dashboard, All-In-One, Mobile View, Favorites, Integrations, Archived, 📊 Graphs, How it works, 🤖 Agent Guide, 🐾 Pets if gamified. Each related database gets its own page and menu entry.
- Databases hub (🌐 Databases): every original database gets a hub row (icon, ⚙Workspaces = the OS, Tags, Area). Databases no code reads live inside their hub row; databases code reads stay where they are and are only registered. Every OS page carries "La base original vive en [row] (🌐 Databases)". Shared databases: add the OS to ⚙Workspaces without removing others.
- Icons on every page and catalog row (platform logo first, else emoji).
- Gamification: one balance shared across OS (add the new OS points into the Leaderboard formulas after backing up their text); Avatar, Tags, Marketplace and Pets views like the reference OS.
- Trial items (become mandatory only once they work and the user confirms): one or more database templates with a Custom AI block, + buttons in Dashboard / Mobile View / sidebar, safe native automations (no fields a code reads, no webhooks without a separate OK).

## 3. Connector limits (plan around them)
Can't: delete views, read buttons or formula text/results, filter on formulas, set gallery card preview, create buttons, database templates or automations, change Owner (person), set Full Width, see what native previews point to. update_content fails with <mention/> inside the search text (use replace_content). SET SELECT wipes values. Max 100 rows per query. Auto-review rejects parallel Notion writes.
Can: icons and covers, move pages into a database (ids kept), chart views (date grouping stays day), two-way relations, write formulas, file upload (create-file-upload then curl -F), is_inline, linked views via <database data-source-url inline="true">, synced-block references with page#blockid.
Formula text: read it in the browser from the DOM and back it up before changing. Browser uploads must use real paths, not symlinks.

## 4. Screen (computerUse, one at a time)
For illustrations, buttons, templates, automations, Full Width, month grouping, card previews, menu layout. Load box-desktop first. Small runs of 4-7 items with screenshots. Re-verify by connector afterwards.

## 5. Audit before closing
- Compare against the reference OS page by page (gap table P1/P2/P3, via, risk).
- Verify all properties, relations (broken targets, one-way that should be two-way), select values with different spellings (check the repo first), typos, view filters.
- Test formulas with a TEST row in a state no code reads; archive it at the end.
- Score against the checklist (/10) and list pending browser steps. Don't change what the user built by hand: report and propose. Never claim a browser step is done without a log entry.

## 6. Library + routines
Evergreen pages as Grok Bot Pages; routines (CRON_TZ=America/Lima) for daily pulse, weekly maintenance, monthly audit; read/propose only, silent when idle.

## 7. Delivery and handoff
Links, manual steps for the user, open questions. Tell Bot Father/Grok Bot if the roster naming changed.

## 8. Template phase (needs explicit yes)
Follow plantilla-notion-desde-workspace-real. Deliver spec + score /10 + browser pending list + proposed My Templates card for Tiendas digitales; publishing always needs the user's A3.

## 9. Learning loop
After each iteration append what was learned here and in plantilla-notion-desde-workspace-real before closing.
