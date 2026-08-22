# Property map pointer

**SSOT for Notion Publisher props lives in the notion-publisher repo**, not in this skill.

| Repo | Path |
|---|---|
| Local vault workspace | `02_Programs/1-Workspaces/GPT Chain/_initiatives-software/gumroad-published/docs/notion-property-map.md` |
| GitHub | [Nucleo-Lab/notion-publisher](https://github.com/Nucleo-Lab/notion-publisher) → `docs/notion-property-map.md` |

Before mapping sections → props, skim that file (Gumroad / Postly / Luma / GitHub / Composio tables).

Live ingest runner (creates Not-started rows):

```bash
# from notion-publisher checkout
npm run to-cms -- --package="/abs/path/package.md"
```

This skill must not fork or duplicate the full property tables.
