# Channel contract (`cms:`)

Required for producer skills that feed Notion Publisher via `/to-cms`. Also allowed on content package frontmatter.

## Schema

```yaml
cms:
  layer: Social | Products | Events | Music   # or list
  sources: [Postly, Composio, Gumroad, Luma, GitHub, Skool]
  channels: [Reddit, Instagram, TikTok, YouTube, Twitter, Eventbrite, ...]
  expand: multi   # default; one page per Layer group
```

## Where it lives

| Place | When |
|---|---|
| Producer `SKILL.md` frontmatter `cms:` | Default targets for everything that skill emits |
| Package frontmatter `cms:` | Per-package override / expansion |
| `/to-cms --sources=` / user text | Hard override (wins) |

## Resolver priority

1. User explicit override
2. Package frontmatter `cms:`
3. Producer skill `cms:`
4. Heuristics (below)

Union Source Tags and Channels across hits. Layer groups determine how many Notion pages to create.

## Heuristics (step 4)

| Signal in package | Adds |
|---|---|
| Heading / section `Landing Page Copy`, `Gumroad Title`, `Template` | Layer `Products`, Source `Gumroad` |
| `GitHub Repo`, `Release Tag`, `Release Notes` | Layer `Products`, Source `GitHub` |
| `Caption`, `POV`, `Instagram Caption`, `Video`/`GIF`/`Image` | Layer `Social`, Source `Postly` |
| `Reddit Title`, `Reddit Body`, `Reddit Subreddit` | Layer `Social`, Source `Composio`, Channel `Reddit` |
| `Luma Title`, `Luma Start`, `Luma Description` | Layer `Events`, Source `Luma` |
| Filename contains `gumroad` / `postly` / `luma` / `reddit` | Matching source |

## Minimum to create a page

- Title (`Name` / `Gumroad Title` / package `title`)
- At least one Layer
- At least one Source Tag

Missing recommended fields → checklist in output; still create if minimum holds.

## Expand / page strategy

Group by Layer (property sets diverge):

| Layer | Typical Source Tags | Status props set to Not started |
|---|---|---|
| Products | Gumroad, GitHub, Skool | `Gumroad Publish Status`, `GitHub Publish Status`, … as tagged |
| Social | Postly, Composio | `Postly Publish Status`, `Composio Publish Status` |
| Events | Luma | `Luma Publish Status` |
| Music | ONCE (stub only if present) | stub status if props exist |

Do **not** call publish webhooks from `/to-cms`.
