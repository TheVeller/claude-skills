---
name: obsidianizer
description: Analyze a specific folder in this Obsidian vault and standardize it into the Agentic OS pattern. Use when the user wants to improve a folder's structure, create or fix a Base, add or rename a Dashboard, add an explanatory Canvas, normalize naming, or make a section feel more coherent and navigable in Obsidian.
---

# Obsidianizer

Turn one vault section into a clean, usable Obsidian surface.

This skill is for folder-level standardization in this workspace, especially when the user wants the same pattern we have been applying across Inbox, Journal, Programs, Workspaces, Areas, Resources, Archive, or workspace subfolders.

## Use This Skill For

- A folder that needs a proper Base + Dashboard + Canvas pattern
- A folder that already has notes but lacks a usable command surface
- Fixing broken or incomplete Bases
- Cleaning up naming like `Dashboard.md`, duplicate dashboards, ugly `README` labels, or legacy wrappers
- Standardizing a folder so it works better in Obsidian explorer and Bases

Do not use this skill for generic note writing or for isolated markdown edits. For those, use `obsidian-markdown`. When editing `.base` syntax, use `obsidian-bases`.

## Core Outcome

Given one designated folder, produce the smallest coherent system that fits its real contents:

1. Inspect the folder deeply enough to understand its information model
2. Decide whether it needs a Base
3. Create or fix the Dashboard naming and content
4. Create a Canvas that explains the flow visually when that adds value
5. Normalize naming and remove UX confusion
6. Update links so the surface is actually usable

## Standard Pattern

Aim for this shape, adapted to the folder's purpose:

```text
<Folder>/
├── _<Name>_Dashboard.md        # main command surface for section-level folders
├── <Name>.base                # optional; only if the folder has enough structured notes
├── <Name> Workflow.canvas     # optional but preferred when process/structure benefits from visual explanation
├── README.md                  # guide/reference, if the folder benefits from one
└── content...
```

For workspace-local folders inside `02_Programs/1-Workspaces/<Workspace>/`, use:

```text
<Workspace>/
├── <Workspace>_Dashboard.md
├── README.md
├── <Workspace>_Context.md     # if that workspace already uses context maps
└── content...
```

## Naming Rules

Apply these defaults unless the folder already has a stronger local convention:

- Section-level folders: `_Inbox_Dashboard.md`, `_Journal_Dashboard.md`, `_Programs_Dashboard.md`, `_Areas_Dashboard.md`, `_Resources_Dashboard.md`, `_Archive_Dashboard.md`, `_Skills_Dashboard.md`
- Workspace-level dashboards: `<Workspace>_Dashboard.md`
- Main guide file: `README.md`
- Legacy aliases like `*_README.md` should become compatibility shims, not the main entrypoint
- Avoid leaving duplicate dashboard files that represent the same surface

## Decision Rules

### When to Create a Base

Create or fix a Base if the folder has enough structured items that benefit from filtering, grouping, or summary views.

Good signals:
- Many homogeneous notes
- Repeated frontmatter fields
- Natural views like active/archive/status/year/type
- The user expects “database-like” navigation

Avoid creating a Base when:
- The folder is tiny
- The content is mostly one-off docs
- A curated dashboard is enough

### When to Create a Canvas

Create a Canvas when the folder benefits from visual explanation:
- workflow
- hierarchy
- lifecycle
- relationship map
- operating model

Do not create a decorative canvas. It should clarify how the folder works.

## Workflow

### 1. Inspect the Designated Folder

Read:
- folder structure
- representative notes
- existing dashboard/base/canvas/readme files
- frontmatter patterns
- naming inconsistencies

Look for:
- duplicate entrypoints
- broken formulas
- missing properties needed by Bases
- ugly explorer naming
- dashboards that are wrappers instead of real surfaces
- legacy files still acting as primary entrypoints

### 2. Infer the Folder Model

Figure out:
- what entities live there
- which properties are stable
- which views matter operationally
- whether the folder is process-centric, catalog-centric, or guide-centric

### 3. Propose the Minimal Coherent Surface

Usually this means:
- one main dashboard
- zero or one main base
- zero or one canvas
- one main README only if useful

Prefer fewer strong surfaces over many weak ones.

### 4. Implement

Typical work:
- create/fix the Base
- rename dashboard files to standard names
- turn wrapper files into real entrypoints
- demote legacy files into aliases if needed
- add embeds and quick links
- create a canvas note or canvas file for the visual flow
- update links in nearby notes/docs

### 5. Verify

Check:
- the Base does not use unsupported formula patterns
- properties referenced in views/formulas actually exist or degrade gracefully
- there is only one main dashboard per logical surface
- explorer naming is understandable
- embeds and wikilinks point to real files

## Dashboard Expectations

A good dashboard should usually include:
- purpose or quick orientation
- embeds or links to the primary Base(s)
- links to important notes/subfolders
- the visual canvas if relevant
- the minimum context someone needs to operate the folder

Do not make the dashboard a wrapper that only embeds another wrapper.

## Base Expectations

When creating or fixing a Base:
- filter by stable signals such as `type`, folder, date presence, or explicit properties
- avoid brittle year-specific or hardcoded-folder logic unless the folder model truly requires it
- prefer formulas that degrade safely
- if Obsidian Bases syntax is involved, follow the `obsidian-bases` skill

## Canvas Expectations

The canvas should explain the actual operating model of the folder, not a generic hierarchy.

Examples:
- Inbox: capture → pending streams → classify → destinations
- Journal: daily notes → reviews → cadence
- Workspaces: dashboard ↔ context ↔ ops/planning/evergreen

If a previous “Visual” note exists but the real need is a Canvas, migrate the concept and leave a clear pointer if needed.

## Output Style

When reporting back:
- say what surface was standardized
- explain whether a Base was created, fixed, or intentionally skipped
- note naming changes
- mention any Obsidian limitations that are structural rather than repo-fixable

## This Vault Conventions

- Use shared vault skills from `.claude/skills/`
- Workspace-specific skills belong under `02_Programs/1-Workspaces/*/.claude/skills/`
- Prefer `README.md` as the human guide and a properly named dashboard as the operational entrypoint
- Preserve existing patterns when they are already coherent; standardize only what improves UX
