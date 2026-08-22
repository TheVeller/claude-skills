---
name: to-cms
version: 0.1.0
description: >
  Ingest a content package (markdown/archive) into Notion Publisher CMS rows
  ready for button publish. Auto-detects Layer/Source Tags/Channels from package
  frontmatter, calling producer skill cms: contract, or heuristics. Never calls
  publish webhooks. Triggers: /to-cms, "ingesta al CMS", "manda a Notion Publisher".
argument-hint: "[path to package.md | folder] [--sources=...] [--live]"
category: engineering
cms:
  layer: []
  sources: []
  channels: []
  expand: multi
---

# to-cms

Turn a **content package** into Notion **Publisher** row(s) with `* Publish Status = Not started`. You press the Notion button; this skill does **not** publish.

**Language:** skill docs English. Conversation may stay Spanish.

**Skill dir:** `$SKILL_DIR` = directory containing this `SKILL.md`.

## Hard rules

1. **Write Notion only.** Never call `/webhooks/publish-*`, ngrok, Gumroad/Postly/Luma/Composio publish APIs.
2. **Multi by default.** One package → one page per Layer group (Products / Social / Events / Music).
3. **Refuse unclear packages** without `cms:` frontmatter, producer `cms:` contract, or strong heuristics — tell user to add the contract (see `references/channel-contract.md`).
4. Live writes need **notion-publisher** repo env (`NOTION_TOKEN`, `NOTION_DATABASE_ID` → Publisher).

## Inputs

| Input | Role |
|---|---|
| Path to `.md` or folder with `package.md` | Content package |
| Optional `--sources=Gumroad,Postly` | Force Source Tags (override) |
| Optional `--channels=Reddit` | Force Channels |
| Optional `--live` | Create Notion pages (default = dry-run resolve only) |
| Calling producer skill | Its `cms:` block feeds the resolver |

## Resolver priority (union for targets)

1. User explicit override (`--sources=` / “solo Gumroad”)
2. Package frontmatter `cms:`
3. Calling producer skill `cms:` (frontmatter of that skill)
4. Heuristics on headings/filenames — see `references/channel-contract.md`

## Workflow

### 1. Load

Read the package. Parse YAML frontmatter + `#` sections. If folder: prefer `package.md`, keep sibling asset paths for the checklist.

### 2. Resolve

Run:

```bash
node "$SKILL_DIR/scripts/resolve-channels.mjs" --package="<path>"
# optional: --sources=Gumroad,Postly --channels=Reddit --producer-skill="<path/to/SKILL.md>"
```

Expect JSON: `{ layers, sources, channels, pages[], missing[], buttons[] }`.

If `missing` blocks minimum (`title` + at least one Layer + one Source Tag) → stop and ask for contract/fields.

### 3. Map fields

Map body sections → Publisher props using `references/property-map.md` (pointer to notion-publisher SSOT). Do not invent stub-channel props.

### 4. Dry-run vs live

**Default (no `--live`):** print resolved pages + missing checklist + which Notion buttons apply. Stop.

**`--live`:** from a checkout of **notion-publisher** (Nucleo-Lab / this vault workspace `gumroad-published`):

```bash
npm run to-cms -- --package="<absolute-path>" [--sources=...] [--channels=...]
```

Script creates page(s), prints Notion URLs + button list. Still never publishes.

### 5. Done output

Always return:

1. Notion page URL(s) (or dry-run payload)
2. Checklist of missing recommended fields
3. Buttons to press (`Publish in Gumroad`, `Publish in Social`, `Publish in Composio`, …)
4. Explicit: “publish = Notion button; `/to-cms` does not publish”

## Companions

- `references/channel-contract.md` — producer + package `cms:` schema
- `references/property-map.md` — where the Notion prop SSOT lives
- `scripts/resolve-channels.mjs` — deterministic resolver + fixture check
- `fixtures/sample-package.md` — Products+Social multi sample

## Adoption (producer skills)

Any vault skill that emits Publisher-bound packages must declare a `cms:` block (frontmatter or `## CMS channels`). Document only in this slice — no mass-edit of all F100K skills.
