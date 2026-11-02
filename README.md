```text
 _____ _          __     __   _ _            ____  _    _ _ _
|_   _| |__   ___ \ \   / /__| | | ___ _ __/ ___|| | _(_) | |___
  | | | '_ \ / _ \ \ \ / / _ \ | |/ _ \ '__\___ \| |/ / | | / __|
  | | | | | |  __/  \ V /  __/ | |  __/ |   ___) |   <| | | \__ \
  |_| |_| |_|\___|   \_/ \___|_|_|\___|_|  |____/|_|\_\_|_|_|___/
```

Portable agent workflows for research, engineering, handoffs, and Obsidian operations. Built from real projects, packaged as self-contained `SKILL.md` directories.

[![GitHub stars](https://img.shields.io/github/stars/TheVeller/claude-skills?style=flat&logo=github&label=stars)](https://github.com/TheVeller/claude-skills/stargazers)
[![License: MIT](https://img.shields.io/badge/license-MIT-black.svg)](./LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/TheVeller/claude-skills)](https://github.com/TheVeller/claude-skills/commits/main)
[![Agent Skills](https://img.shields.io/badge/format-Agent%20Skills-2563eb)](https://skills.sh)

Use these skills when a repeatable workflow needs more than a prompt: deterministic scripts, references, safety rules, and a clear definition of done. The collection contains skills authored or materially adapted by [@TheVeller](https://github.com/TheVeller); upstream work is credited explicitly.

## Start here

| Goal | Skill |
|---|---|
| Turn a data export into a dashboard that changes a decision | [`data-source-dashboard`](./skills/research/data-source-dashboard) |
| Turn long-form sources into reusable research | [`research-pipeline`](./skills/research/research-pipeline) |
| Sync a local repository without losing work | [`repo-sync`](./skills/engineering/repo-sync) |
| Improve a GitHub README and ship the change | [`readme-commit`](./skills/engineering/readme-commit) |
| Ingest a package into Notion Publisher CMS | [`to-cms`](./skills/engineering/to-cms) |
| Turn an app idea into a Lovable-ready pack (surface map, Refero, Relume, scroll stopper, local identity) | [`prompt-architect`](./skills/engineering/prompt-architect) |
| Format scout findings / GM rollups for the corp loop | [`hallazgo`](./skills/agent-operations/hallazgo) · [`reporte-gm`](./skills/agent-operations/reporte-gm) |
| Prepare a whole repo and ship it as public open source | [`ship-oss`](./skills/engineering/ship-oss) |
| Transfer work into a fresh Orca agent terminal | [`orca-handoff`](./skills/agent-operations/orca-handoff) |
| Explain a technical decision to a non-developer | [`no-dev`](./skills/agent-operations/no-dev) |
| Keep an Obsidian vault committed continuously | [`autocommit`](./skills/obsidian-vault/autocommit) |
| Audit a whole repository for drift, broken links, and leaked secrets | [`repo-audit`](./skills/obsidian-vault/repo-audit) |

## Install

Install one skill globally with the [`skills`](https://skills.sh) CLI:

```bash
npx skills add TheVeller/claude-skills --skill repo-sync -g
```

Install several skills into the current project:

```bash
npx skills add TheVeller/claude-skills \
  --skill research-pipeline readme-commit orca-handoff
```

Or clone and copy a directory directly:

```bash
git clone https://github.com/TheVeller/claude-skills.git
cp -R claude-skills/skills/engineering/repo-sync ~/.claude/skills/
```

The repository groups skills by category for browsing. Install or copy the individual skill directory, not its category directory.

## Catalog

### Research

| Skill | What it does |
|---|---|
| [`data-source-dashboard`](./skills/research/data-source-dashboard) | Turns a raw export into an interactive dashboard: aggregates-only privacy, provenance on every number, scenario toggles, ES/EN and dark/light. |
| [`research-pipeline`](./skills/research/research-pipeline) | Sends sources through NotebookLM and returns grounded notes, with optional infographic, podcast, or slides. |
| [`youtube-search`](./skills/research/youtube-search) | Searches YouTube through `yt-dlp` and collects URLs plus metadata for research pipelines. |
| [`daily-review-workflow`](./skills/research/daily-review-workflow) | Pulls synced sources, handles failures, and writes an end-of-day review note. |
| [`analytics-pull`](./skills/research/analytics-pull) | Use this when another agent or the user asks for a query, metric, or spreadsheet pull from Hex, Databricks, or Google Sheets. |
| [`caza-demanda-nucleo`](./skills/research/caza-demanda-nucleo) | Use this when running the daily demand hunt for an automation services brand (Make/n8n, WhatsApp/IG agents, CRM+WhatsApp, training) on freelance marketplaces with lightweight fetch, no browser. |
| [`competitor-sweep`](./skills/research/competitor-sweep) | Use this when running a periodic competitor sweep (DIRECT peers + REFERENCE players) and deciding whether anything is material enough to report. |
| [`creator-breakdown`](./skills/research/creator-breakdown) | Use when someone wants a newsletter-style teardown of how a creator grew and monetizes (viral clusters vs durable steps, collab vs solo, comment/DM funnel, CTA coverage, themes) from scraped history and local outlier math; no Sandcastles. *(adapted from content.game, see Attribution)* |
| [`distilled-brew-seed-sweep`](./skills/research/distilled-brew-seed-sweep) | Use this when a daily content-inspiration sweep reads Distilled Brew (daily top-5 GitHub/Product Hunt/Hacker News digest) to find seeds for a niche, before proposing any item. |
| [`enrich-list`](./skills/research/enrich-list) | Use this when someone hands you a list of companies, people, or accounts to enrich with data from authorized providers (Apollo first, then Deepline, TikHub, or any provider added later). |
| [`sandcastles-channel-diagnostic`](./skills/research/sandcastles-channel-diagnostic) | Use when someone wants to deep dive, analyze or reverse-engineer one or more creator channels (top topics, hooks, hidden insights, formats) as an HTML report, built from scraped metrics, local transcripts and frames; no Sandcastles. *(adapted from content.game, see Attribution)* |
| [`sandcastles-watchlist-all-recent`](./skills/research/sandcastles-watchlist-all-recent) | Use when the user wants every video the local watchlist channels posted in the last 7 days, newest first with links and no performance filter; free for YouTube/TikTok, no Sandcastles. *(adapted from content.game, see Attribution)* |
| [`sandcastles-watchlist-outliers`](./skills/research/sandcastles-watchlist-outliers) | Use when the user wants only the outlier videos (1.0x+ of the channel's own 3-month average) posted in the last 7 days by the channels on the local watchlist, ranked with links; free for YouTube/TikTok, no Sandcastles. *(adapted from content.game, see Attribution)* |
| [`scrape-safe`](./skills/research/scrape-safe) | Use this before scraping any public web source into a dataset: legality checklist, cheapest-tool order, and the per-run deliverable. |
| [`startup-outreach-draft`](./skills/research/startup-outreach-draft) | Use this when someone likes a shortlisted startup and wants help reaching a founder/HM — interest kit with reach path, personalization angles, and outreach draft. |
| [`startup-shortlist`](./skills/research/startup-shortlist) | Use this when someone wants an on-demand shortlist of under-the-radar startups to join (not only the weekday morning digest). |
| [`startup-watchlist`](./skills/research/startup-watchlist) | Use this when someone wants to pin, review, update, or clear startups on their join-a-startup watchlist. |

### Engineering

| Skill | What it does |
|---|---|
| [`readme-commit`](./skills/engineering/readme-commit) | Ships a GitHub README with channel Compatible-with (not stack), Surfaces/App-tools matrix, stack badges, native About sync, and a fail-closed `--repo` gate. |
| [`ship-oss`](./skills/engineering/ship-oss) | Sweeps a whole repository for secrets and internal references, verifies LICENSE and `.gitignore`, then flips GitHub visibility to public. Delegates README polish to `readme-commit`. |
| [`repo-sync`](./skills/engineering/repo-sync) | Detects ahead, behind, and diverged states; fast-forwards safely and backs up before destructive syncs. |
| [`clone-software-repo`](./skills/engineering/clone-software-repo) | Clones an external repository into a managed software workspace. |
| [`start-cc+lv`](./skills/engineering/start-cc+lv) | Starts a Claude Code workflow connected to Lovable and a GitHub-based deployment path. |
| [`prompt-architect`](./skills/engineering/prompt-architect) | Turns an app idea into mvp-plan, design-style-plan, prd and a first Lovable prompt, using a Refero reference, a Relume sitemap, one scroll-stopper component and a local identity palette. Never goes straight to Lovable. |
| [`game-designer-ue`](./skills/engineering/game-designer-ue) | Adapts game-feel analysis and design methods to Unreal Engine 5 systems. |
| [`wayfinder-sequential`](./skills/engineering/wayfinder-sequential) | Cautious variant of [`/wayfinder`](https://github.com/mattpocock/skills): one ticket per session, no parallel research, map re-evaluated after every resolution, prototype decisions stay with the user. Requires the upstream `wayfinder` skill. |
| [`wavespeed`](./skills/engineering/wavespeed) | Generates or edits image, video, audio, and 3D assets through the `wavespeed` CLI, where every model is one explicit `run <id>` call. |
| [`to-cms`](./skills/engineering/to-cms) | Ingest a content package into Notion Publisher CMS rows (Not started) with channel auto-detect; never calls publish webhooks. Invocable as `/to-cms`. |
| [`obsidian-plugin-release`](./skills/engineering/obsidian-plugin-release) | Bumps and ships an Obsidian community plugin release: manifest/package/versions, build, signed tag, and GitHub release path. |
| [`herdr-local-seat`](./skills/engineering/herdr-local-seat) | Use this when configuring Herdr as the 0–1 local Cursor CLI seat on the Grok Bot computer, or when a routine should enforce the coding-cap and RAM policy. |
| [`homelab-hardware`](./skills/engineering/homelab-hardware) | Use this when checking Grok Bot computer hardware (CPU/RAM/disk/GPU), how loaded it is, or whether something else (Hermes, OpenClaw, another daemon) can be installed. |
| [`homelab-loop`](./skills/engineering/homelab-loop) | Use this when standing up or explaining the Homelab Porter stack: Grok Bot computer with ZeroClaw and optional NullClaw porters, Karpathy vault, Personal Gateway/Hermes, Herdr + Cloud Agents + pstack, and hardware capacity. |
| [`make-bot-ui`](./skills/engineering/make-bot-ui) | Use when building a custom UI (page, dashboard, buttons) that should wake a Grok Bot over a webhook, when the user must provide a webhook sender key, or when exposing that UI on Tailscale. |
| [`nullclaw-24-7`](./skills/engineering/nullclaw-24-7) | Use this when installing NullClaw as a second porter on the Grok Bot computer, or when creating/running the 24/7 health routine that keeps its Telegram bridge up day and night. |
| [`outer-loop`](./skills/engineering/outer-loop) | Use when standing up this outer-loop bot, starting a coding-agent task, writing a cloud-agent prompt, or babysitting a PR. |
| [`personal-gateway`](./skills/engineering/personal-gateway) | Use this when standing up or explaining the Personal Gateway: Telegram agent group, ZeroClaw and optional NullClaw porters, Hermes Telegram↔WhatsApp, and how Grok Bot posts with an authorship prefix. |

### Agent Operations

| Skill | What it does |
|---|---|
| [`orca-handoff`](./skills/agent-operations/orca-handoff) | Writes a redacted handoff, opens the correct Orca terminal or worktree, waits for TUI readiness, and delivers the prompt. |
| [`no-dev`](./skills/agent-operations/no-dev) | Converts technical explanations into purpose, consequence, action, risk, and result. |
| [`govern-agentic-os`](./skills/agent-operations/govern-agentic-os) | Keeps a repository and its issue tracker from becoming two sources of truth: audit, plan, execute, check, and hand off governance work under one authority model. |
| [`hallazgo`](./skills/agent-operations/hallazgo) | Formats a scout → GM finding block (oferta/señal, links, ROI, fit) for the corporate loop. |
| [`loop-corp`](./skills/agent-operations/loop-corp) | Runs the Orquestador + GMs corporate loop (daily / standing), without dumping raw scout noise. |
| [`reporte-gm`](./skills/agent-operations/reporte-gm) | Formats the GM rollup to the GMs room → Orquestador (Forja, Levy, Brandy, Inti, Oppy). |
| [`agent-contract`](./skills/agent-operations/agent-contract) | Usar al crear o cambiar un bot Grok, para dejar mandato corto + Must NOT + reporta a + aristas, sin duplicar oficio. |
| [`brand-chrome-login`](./skills/agent-operations/brand-chrome-login) | Use this when creating or using a Chrome brand profile on the Grok Bot computer (Ignacio / Núcleo / The Veller), signing into a real Gmail, pausing for 2FA/HITL, or doing Sign in with Google on one named service — never for identity farms or mass signups. |
| [`contexto-aristas`](./skills/agent-operations/contexto-aristas) | Use this when briefing Hermes/Instinct by AgentMail: deep map + where to verify (Drive vault vs Mac-only vs Grok-only), not a short role list or carry dump. |
| [`crear-bot-nico`](./skills/agent-operations/crear-bot-nico) | Usar al crear un Grok Bot nuevo o al auditar bots vivos: oficio sin overlap, escritura UX, workspace Notion a nivel vendible estilo Sales OS (icon x.ai/bot en roster, originales/vistas/dashboard/All-in-One, ilustraciones unDraw obligatorias, My Templates por vistas enlazadas, favicon tienda + foto real en ítems). |
| [`daily-standup`](./skills/agent-operations/daily-standup) | Use this when kicking off a daily standup in a team room — yesterday, today, blockers — short, no status theater. |
| [`design-a-grok-bot`](./skills/agent-operations/design-a-grok-bot) | Use this when designing or creating a new Grok Bot. |
| [`drift-hunt-roster`](./skills/agent-operations/drift-hunt-roster) | Use when running a daily roster drift hunt - compare live agents and rooms on the box against the fleet inventory docs and report only new deltas to an ops room. |
| [`explain-grokbot`](./skills/agent-operations/explain-grokbot) | Use this when the user asks /explain-grokbot, or wants a plain Spanish summary of what this bot is, what it can do, how it reads the current setup, and what should happen next. |
| [`exportar-bot`](./skills/agent-operations/exportar-bot) | Usar al migrar, exportar o respaldar Grok Bots (un bot, un departamento o la cuenta): cada export produce siempre 3 variantes en orden: 1) plantilla nativa de Grok Bot (CreateBotShareJson, la corre el propio bot), 2) .tgz (paquete neutral + tenant OpenBot) y 3) prompt .md para pegar en Notion Agent u otras plataformas (Instinct, Open Bot, Cue). |
| [`grok-bot-project-ops`](./skills/agent-operations/grok-bot-project-ops) | Use this when creating or running a Grok Bot project: Notion Projects and Tasks, staffing, sidebar Projects placement, bots claiming work, and pinging the user when blocked. |
| [`handoff-local-hermes`](./skills/agent-operations/handoff-local-hermes) | Usar cuando Grok necesite que Hermes ejecute algo local (vault, ADK, script, ledger Notion) y no deba hacerlo un scout. |
| [`identity-pipeline`](./skills/agent-operations/identity-pipeline) | Use when alta con identidad, auditing identity (incl. |
| [`panorama-de-flujo`](./skills/agent-operations/panorama-de-flujo) | Usar cuando el usuario pide la visión completa de un flujo o sistema que se está construyendo (contenido, ventas, distribución, un OS): flujograma, owners, tooling, links, estado y decisiones pendientes, antes de que alguien lo tome y lo ejecute. |
| [`routine-healthcheck`](./skills/agent-operations/routine-healthcheck) | Use when auditing Grok Bot routines for token waste, offering a fleet checkup after template import, deciding cadence, or running the standing routine-healthcheck wake. |
| [`sprint-parallel`](./skills/agent-operations/sprint-parallel) | Use whenever a sprint has a defined reset or cut time: maximize parallelization (1:1 GMs + dedicated rooms same beat), map value processes, fill high-quality gaps. |
| [`transcript-healthcheck`](./skills/agent-operations/transcript-healthcheck) | Use when auditing Grok Bot fleet transcripts for user friction, proposing new skills/bots/routines from repeated corrections, or running the standing transcript-healthcheck routine. |

### Obsidian Vault

| Skill | What it does |
|---|---|
| [`obsidianizer`](./skills/obsidian-vault/obsidianizer) | Turns raw material into vault-ready notes with frontmatter, wikilinks, and PARA placement. |
| [`autocommit`](./skills/obsidian-vault/autocommit) | Operates and diagnoses an `fswatch`-based auto-commit daemon for a vault. |
| [`repo-audit`](./skills/obsidian-vault/repo-audit) | Runs a queue of audit units in one autonomous pass — coherence, broken symlinks, leaked secrets, PARA placement, scripts, doc condensation — read-only except its own report artifacts. |
| [`karpathy-vault`](./skills/obsidian-vault/karpathy-vault) | Use this when creating or explaining the Karpathy-style markdown vault on the Grok Bot computer (inbox/raw/wiki/state) as the homelab second brain. |

### Marketing

| Skill | What it does |
|---|---|
| [`promo-webinar`](./skills/marketing/promo-webinar) | Turns a short webinar brief into a 9-asset multichannel promo kit plus a publish calendar. |
| [`sundai-campana-hack`](./skills/marketing/sundai-campana-hack) | Generates the full before/during/after content plan for a Sundai Latam hack campaign. |
| [`hackathon-promo`](./skills/marketing/hackathon-promo) | Builds the multichannel promo kit for an in-person/hybrid hackathon (Luma, blasts, accept/waitlist/reject). |
| [`audience-bullseye-builder`](./skills/marketing/audience-bullseye-builder) | Use this when defining who a channel's content is for: ICP/ideal viewer, how niche to go, why videos reach the wrong people, a 5-ring audience bullseye, a 3/1/1 content mix, or who to study for inspiration (Kallaway, content.game). *(adapted from content.game, see Attribution)* |
| [`campaign-publish-checklist`](./skills/marketing/campaign-publish-checklist) | Use when checking a Notion Publisher campaign row is ready to publish or when proposing a publish calendar. |
| [`channel-triage-canales`](./skills/marketing/channel-triage-canales) | Use when triaging scout CSV candidates into the channels database owned by Publisher. |
| [`connector-status-map`](./skills/marketing/connector-status-map) | Use before proposing a publish or turning a connector live; read the Content OS map and CAPABILITIES.md. |
| [`estandar-directorios`](./skills/marketing/estandar-directorios) | Usar al crear, empaquetar, auditar o mantener un directorio/dataset vendible (Notion + GitHub + web + SEO + newsletter + MCP/API + Gumroad + portales de datasets), incluso en modo autónomo nocturno. |
| [`futuraria-brand-kit-v3`](./skills/marketing/futuraria-brand-kit-v3) | Use when building or updating a brand design system in Futuraria (Musa): modules 01-06, the ordered unified file, brandbook tokens, and official 1:1 logos. |
| [`hook-machine`](./skills/marketing/hook-machine) | Use when researching, writing, grading (A–F) or rewriting short-form video hooks from the best videos of reference channels (Instagram, TikTok, YouTube Shorts), with free scraping and local transcription; no Sandcastles. *(adapted from content.game, see Attribution)* |
| [`lanzar-producto-gumroad`](./skills/marketing/lanzar-producto-gumroad) | Usar cuando llega un producto digital nuevo (por ejemplo una plantilla de Notion terminada) para listarlo en Gumroad de punta a punta sin pedir indicaciones paso a paso. |
| [`marketing-campaign-pm`](./skills/marketing/marketing-campaign-pm) | Use when running a marketing campaign or launch to a date - one plan with goal and date, five fronts (research, positioning, landing, ads, analytics) with owner, due date, dependency and approval, plus screenshot-backed reviews. |
| [`playbook-por-plataforma`](./skills/marketing/playbook-por-plataforma) | Use when drafting or preparing a listing submit for a distribution platform (directories, launchboards, RankInPublic-style, ListingBott-style) and you need per-platform rules, daily limits, ToS pacing, and a pre-submit checklist — never auto-submit. |
| [`product-hunt-launch`](./skills/marketing/product-hunt-launch) | Use this when planning, prepping, running or reviewing a Product Hunt launch: validate build/narrow/kill, launch kit, D-21..D+1 + week-2 countdown, rule-checked CTAs, post-mortem. |
| [`product-mockups-02`](./skills/marketing/product-mockups-02) | Use when building a product's store gallery, description page pieces, 1:1 GIF thumbnail, OS Cube logo, social carousel and native stories (module 02). |
| [`seo-free-technical-baseline`](./skills/marketing/seo-free-technical-baseline) | Use when a site needs a free technical SEO baseline (no paid credits) that ends in prioritized ticket drafts for the code owner. |
| [`social-carousel-universal`](./skills/marketing/social-carousel-universal) | Use when producing a multi-channel social carousel and native stories for a product or brand, with one master design adapted to size limits. |
| [`video-de-launch-de-producto-borrador`](./skills/marketing/video-de-launch-de-producto-borrador) | Usar cuando se pide planear, construir y criticar un video corto de lanzamiento (20-60 s) de un producto de software en el que el producto hace su acción en pantalla. |

### Content

| Skill | What it does |
|---|---|
| [`anti-slop`](./skills/content/anti-slop) | Write like a person. |
| [`call-notes-to-slides`](./skills/content/call-notes-to-slides) | Use when filling or rewriting a What we heard, Next steps, or Project initiatives slide from a customer call, in Figma or Google Slides, using Granola or Gong notes. |
| [`deck-local-export`](./skills/content/deck-local-export) | Use when a design tool (for example Futuraria) can't export a finished deck to PDF or PPTX and you need shareable files for a call recap. |
| [`talk-simple`](./skills/content/talk-simple) | Always talk to the user in simple everyday English with no skill jargon and no AI writing tells. |
| [`verify-me`](./skills/content/verify-me) | Verify writing against the user's voice and unslop rules after a draft is ready. |
| [`write-as-me`](./skills/content/write-as-me) | Mandatory pipeline for any user-facing writing as the user (LinkedIn, email, Slack, DMs, docs, posts). |

### Workspace automation

| Skill | What it does |
|---|---|
| [`corte-email-pulso`](./skills/workspace-automation/corte-email-pulso) | Use this when compiling a daily pulse from Gmail: paid sales, free downloads, and Luma event registrations. |
| [`expense-manager-daily`](./skills/workspace-automation/expense-manager-daily) | Use when logging a reported expense (from an inbox assistant or a bank/receipt email) into a finance database and ledger, or when preparing the daily expenses input draft. |
| [`luma-event-tagging`](./skills/workspace-automation/luma-event-tagging) | Use this when tagging people in a Luma calendar's People list by the events they attended (Going or checked in), adding only missing tags. |
| [`plantilla-notion-desde-workspace-real`](./skills/workspace-automation/plantilla-notion-desde-workspace-real) | Use this when turning a real Notion workspace or OS into a sellable template (Premium and Free) without copying private data: real workspace first (closed against the reference OS and the evergreen list), then light example databases, duplicate via a second account, bring back to the templates database as one card per product. |
| [`proyecto-notion-de-punta-a-punta`](./skills/workspace-automation/proyecto-notion-de-punta-a-punta) | Use this when the user names one project or system to build as a Notion workspace (home, databases, Library, audits) and expects it done end to end, including the sellable template afterwards. |
| [`saves-library-sync`](./skills/workspace-automation/saves-library-sync) | Use when pushing an archive of saved links into a content-library app that extracts data with a credit-based scraper, or when retrying items that came back empty or in error. |

### Bot templates (Grok Bot first-conversation setup)

| Skill | What it does |
|---|---|
| [`getting-started-brandy`](./skills/bot-templates/getting-started-brandy) | Use this as the first conversation of an imported Brand & Community GM bot with its new owner, to set up brands, staff room, rollup routine and report format. |
| [`getting-started-calendario-contenido`](./skills/bot-templates/getting-started-calendario-contenido) | Use this on the first conversation of a newly imported content-calendar bot, to set up its weekly batch, idea bank and standup. |
| [`getting-started-cazador-de-canales`](./skills/bot-templates/getting-started-cazador-de-canales) | Use this on the first conversation of an imported Channel Hunter (distribution scout) bot with its new owner. |
| [`getting-started-cazador-de-vuelos`](./skills/bot-templates/getting-started-cazador-de-vuelos) | Use this on the first conversation of an imported Cazador de Vuelos bot to set up its cheap-flight hunt with the new owner. |
| [`getting-started-cazador-gangas`](./skills/bot-templates/getting-started-cazador-gangas) | Use this on the first conversation of a new Cazador Gangas bot, to set up its deal-hunting sweep with its new owner. |
| [`getting-started-cazador-inmobiliario`](./skills/bot-templates/getting-started-cazador-inmobiliario) | Use this on the first conversation with a new owner of a real-estate deal-hunter bot (buy-to-invest apartments, small lots, court auctions) to set it up. |
| [`getting-started-cazador-programas`](./skills/bot-templates/getting-started-cazador-programas) | Use this on the first conversation of a newly imported Cazador Programas & Perks bot, to set it up with its new owner. |
| [`getting-started-cazador-sponsors`](./skills/bot-templates/getting-started-cazador-sponsors) | Use this on the first conversation of an imported Sponsor Hunter bot to set up what it hunts and who gets findings. |
| [`getting-started-cazador-vivienda`](./skills/bot-templates/getting-started-cazador-vivienda) | Use this on the first conversation of an imported rental-hunter bot, to collect the owner's search criteria and start the watch. |
| [`getting-started-content-drafter`](./skills/bot-templates/getting-started-content-drafter) | Use this on the first conversation of a newly imported Content Drafter bot to set up its voice sources, delivery room, approver and routines. |
| [`getting-started-data-science`](./skills/bot-templates/getting-started-data-science) | Use this on the first conversation of a data science bot imported from a template, to set it up with its new owner. |
| [`getting-started-demand-hunter`](./skills/bot-templates/getting-started-demand-hunter) | Use this on the first conversation of a newly imported Demand Hunter bot, to set it up with its new owner. |
| [`getting-started-digital-stores`](./skills/bot-templates/getting-started-digital-stores) | Use this on the first conversation of a digital-stores catalog bot with its new owner. |
| [`getting-started-directory-builder`](./skills/bot-templates/getting-started-directory-builder) | Use this on the first conversation of an imported Directory Builder bot, to set up its owner, sources, workspace and nightly run. |
| [`getting-started-enrichment-desk`](./skills/bot-templates/getting-started-enrichment-desk) | Use this on the first conversation of a newly imported Enrichment Desk bot to set it up with its new owner. |
| [`getting-started-event-hunter`](./skills/bot-templates/getting-started-event-hunter) | Use this on the first conversation of an imported Event Hunter bot, to set up which event calendars it watches and where it reports. |
| [`getting-started-expense-manager`](./skills/bot-templates/getting-started-expense-manager) | Use this on the first conversation of an Expense Manager bot imported from the template, to set it up with its new owner. |
| [`getting-started-gm-operaciones`](./skills/bot-templates/getting-started-gm-operaciones) | Use this on the first conversation of an imported Operations GM (Agentic OS + homelab auditor) bot with its new owner. |
| [`getting-started-inbox-manager`](./skills/bot-templates/getting-started-inbox-manager) | Use this on the first conversation of an Inbox Manager bot with its new owner, to connect inboxes and set up triage and routines. |
| [`getting-started-intake-intel`](./skills/bot-templates/getting-started-intake-intel) | Use this on the first conversation of an imported Intake Intel bot, to set up its sources, its lead and its daily triage routine. |
| [`getting-started-intelligence-gm`](./skills/bot-templates/getting-started-intelligence-gm) | Use this on the first conversation of an imported Intelligence GM bot (research intake, learning queue, daily intelligence digest) to set it up with its new owner. |
| [`getting-started-join-a-startup`](./skills/bot-templates/getting-started-join-a-startup) | Use this on the first conversation of an imported Join a Startup bot, to collect the owner's job-hunt prefs and start the daily shortlist. |
| [`getting-started-last30days`](./skills/bot-templates/getting-started-last30days) | Use this on the first conversation of a freshly imported last30days bot, to install the skill and walk the new owner through setup. |
| [`getting-started-life-ops`](./skills/bot-templates/getting-started-life-ops) | Use this on the first conversation of a Life Ops GM bot imported from a template, to set it up with its new owner. |
| [`getting-started-luma-tagging`](./skills/bot-templates/getting-started-luma-tagging) | Use this on the first conversation of a Luma Tagging bot with its new owner, to set up which Luma calendar to tag and the tagging rules. |
| [`getting-started-market-watcher`](./skills/bot-templates/getting-started-market-watcher) | Use this on the first conversation of a Market Watcher bot with its new owner, to set up which brands and competitors to watch and where findings go. |
| [`getting-started-meta-vault`](./skills/bot-templates/getting-started-meta-vault) | Use this on the first conversation of an imported Meta Vault (fleet roster and docs drift auditor) with its new owner. |
| [`getting-started-musa-designer`](./skills/bot-templates/getting-started-musa-designer) | Use this on the first conversation of a newly imported Musa Designer bot, to set up its design workspace, brands and delivery rules with its new owner. |
| [`getting-started-plantillas-notion`](./skills/bot-templates/getting-started-plantillas-notion) | Use this on the first conversation with a new owner to set up the Notion template builder. |
| [`getting-started-product-hunter`](./skills/bot-templates/getting-started-product-hunter) | Use this on the first conversation of a Product Hunt launch operator bot with its new owner. |
| [`getting-started-publisher`](./skills/bot-templates/getting-started-publisher) | Use on the first conversation of a Publisher bot imported from the template to set up Notion CMS, repo, schedulers and approval rules. |
| [`getting-started-pulso-brand`](./skills/bot-templates/getting-started-pulso-brand) | Use this in the first conversation of an imported Pulso Brand bot, to set it up with its new owner. |
| [`getting-started-pulso-dia`](./skills/bot-templates/getting-started-pulso-dia) | Use this on the first conversation of a newly imported Pulso Día bot to set up its daily calendar and Do Date brief. |
| [`getting-started-renewals-hunter`](./skills/bot-templates/getting-started-renewals-hunter) | Use this on the first conversation of a household renewals hunter bot to set it up with its new owner. |
| [`getting-started-saves-archivist`](./skills/bot-templates/getting-started-saves-archivist) | Use this on the first conversation of a Saves Archivist bot imported from a template, to set up which platforms, store and library it should use. |
| [`getting-started-scraping-desk`](./skills/bot-templates/getting-started-scraping-desk) | Use this as the first conversation of a newly imported Scraping Desk bot with its new owner. |
| [`getting-started-seo-desk`](./skills/bot-templates/getting-started-seo-desk) | Use this on the first conversation of an SEO desk bot with its new owner, to set up sites, sources, and handoffs before starting SEO work. |
| [`getting-started-slider`](./skills/bot-templates/getting-started-slider) | Use on the first conversation of a Slider bot: it introduces itself and asks the setup questions for turning customer calls into slides. |
| [`getting-started-swe-outer-loop`](./skills/bot-templates/getting-started-swe-outer-loop) | Use this on the first conversation of an imported SWE outer-loop bot to set it up with its new owner. |
| [`publisher-role`](./skills/bot-templates/publisher-role) | Core role instructions for the Publisher bot: campaign CMS operator under the brand manager, approval rules, connectors, and anti-roles. |
| [`video-studio-getting-started`](./skills/bot-templates/video-studio-getting-started) | Use on the first conversation with a new owner to set up the video bot: brand, voice mode, approved formats and the routine. |

## Favorites (curated, upstream)

Third-party skills TheVeller uses every week. They are **not vendored**: [`favorites.json`](./favorites.json) pins the repo, the reviewed commit, the category, and why each one earns a slot. Install them from upstream:

```bash
scripts/install-favorites.sh            # current project
scripts/install-favorites.sh -g         # global
scripts/install-favorites.sh --dry-run  # print the npx commands
```

| Source | Category | Skills |
|---|---|---|
| [ItsssssJack/SlopMonster](https://github.com/ItsssssJack/SlopMonster) | content | `slopmonster` |
| [ItsssssJack/power-design](https://github.com/ItsssssJack/power-design) | content | `power-design` |
| [morluto/rea](https://github.com/morluto/rea) | engineering | `reverse-engineer-anything` |
| [cursor/plugins · pstack](https://github.com/cursor/plugins/tree/main/pstack) | engineering | `architect`, `interrogate`, `blast-radius`, `figure-it-out`, `swarm`, `arena`, `correct`, `reflect`, `recall`, `unslop`, `how`, `why`, `ketchup`, `show-me-your-work`, `technical-writing`, `create-verification-skill`, `poteto-help` |
| [mattpocock/skills](https://github.com/mattpocock/skills) | engineering | `tdd`, `diagnosing-bugs`, `grill-me`, `grill-with-docs`, `to-spec`, `to-tickets`, `implement-spec`, `codebase-design`, `improve-codebase-architecture`, `handoff`, `wayfinder`, `triage`, `prototype`, `domain-modeling`, `writing-for-agents` |
| [crafter-station/skills](https://github.com/crafter-station/skills) | engineering | `cli-build`, `cli-audit`, `surface-recon`, `surfacer`, `generate-brand-assets`, `obsidian-plugin-release`, `supply-chain-audit`, `skill-gen`, `intent-layer` |
| [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | research | `last30days` |

Favorites follow the same categories as this catalog. The full private library (own + third-party, with real usage stats) lives in TheVeller's Notion Skills Library.

## Repository layout

```text
favorites.json         # curated upstream skills (not vendored)
scripts/install-favorites.sh
skills/
|-- agent-operations/  # handoffs and human-agent communication
|-- bot-templates/     # Grok Bot first-conversation setup skills
|-- content/           # writing voice, decks and slides
|-- engineering/       # repository and implementation workflows
|-- marketing/         # campaign copy and event promotion
|-- obsidian-vault/    # knowledge-system operations
|-- research/          # source discovery and synthesis
`-- workspace-automation/ # Gmail, Notion, Luma and library automations
```

Each leaf directory includes a `SKILL.md` and may include scripts, references, templates, or assets. Dependencies and setup steps live beside the skill that needs them.

## Compatibility

The format works with agents that support Agent Skills, including Claude Code, Cursor, and Codex through the `skills` CLI. Individual workflows may require tools such as `git`, `gh`, `fswatch`, `yt-dlp`, NotebookLM, or Orca; check the target skill before installing.

## Attribution

This repository does not mirror the full third-party stack used in TheVeller's workspace. Those skills stay in their upstream repositories:

| Source | Skills or focus |
|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | Debugging, planning, worktrees, and TDD |
| [mattpocock/skills](https://github.com/mattpocock/skills) | Engineering + productivity: spec → tickets → implementation, TDD, diagnosis, grilling, handoffs, and the `wayfinder` planning chain (`wayfinder-sequential` here builds on it) |
| [coleam00/excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill) | Research-backed Excalidraw workflow diagrams |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Design critique and frontend refinement |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | Frontend design judgment |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | UI/UX design workflows |
| [opusgamelabs/game-creator](https://github.com/opusgamelabs) | Basis for the adapted `game-designer-ue` skill |
| [dstn2000/claude-unreal-engine-skill](https://github.com/dstn2000/claude-unreal-engine-skill) | Unreal Engine workflows |
| [roble3/cc-blender-skill](https://github.com/roble3/cc-blender-skill) | Blender modeling |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | Vercel deployment workflows |
| [googleworkspace/cli](https://github.com/googleworkspace/cli) | Google Workspace service skills |
| [crafter-station/skills](https://github.com/crafter-station/skills) | `cli-build`, `cli-audit`, `surface-recon`, `surfacer`, `generate-brand-assets`, `intent-layer`, `obsidian-plugin-release`, `skill-gen`, `spoti-cli`, `supply-chain-audit` |
| [cursor/plugins · pstack](https://github.com/cursor/plugins/tree/main/pstack) | pstack playbooks and engineering principles |
| [ItsssssJack/SlopMonster](https://github.com/ItsssssJack/SlopMonster) · [ItsssssJack/power-design](https://github.com/ItsssssJack/power-design) | De-slopping copy; on-brand HTML decks and sites |
| [morluto/rea](https://github.com/morluto/rea) | Reverse engineering with REA |
| [Composio](https://composio.dev) | `composio-cli`, installed with `composio --install-skill` and generated from the CLI's own source |
| [diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute) | The `omniroute-*` gateway skills, generated by the product's own skill generator |
| [Imperio Digital](https://www.skool.com/imperio) | Paid Skool prompt pack (503 prompts / 20 categories, 0 `SKILL.md`). Not Agent Skills and not installable via the `skills` CLI. Do not vendor. Cherry-pick locally with credit only if a real domain gap hurts (RRHH, legal, e-commerce, generic email, pricing, Skool page templates). |

These skills are not vendored in this repository — install from upstream. Install community skills selectively and keep their original license and attribution. Proprietary prompt packs stay referenced, never copied.

## Contributing

Issues and pull requests are welcome. A useful contribution should keep one workflow per skill, document external dependencies, avoid secrets and machine-specific data, and include a runnable check for non-trivial scripts.

## License

MIT (c) [Ignacio Alberto Velasquez Franco (@TheVeller)](https://github.com/TheVeller)
| content.game (Kallaway / Content Dept.) | Basis for the adapted `audience-bullseye-builder`, `creator-breakdown`, `hook-machine`, `sandcastles-channel-diagnostic`, `sandcastles-watchlist-all-recent`, `sandcastles-watchlist-outliers`, rebuilt to run without Sandcastles (yt-dlp, optional Apify, local outlier math). Credited in each SKILL.md `metadata`. Upstream license terms: sin dato. |
| [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | `last30days`: 30-day social research. Not vendored; installed via `favorites.json`. |
