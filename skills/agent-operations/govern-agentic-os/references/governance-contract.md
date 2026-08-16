# Agentic OS governance contract

## Authority map

| Concern | Authority | Local role |
|---|---|---|
| Project phases, priority, status, implementation contracts, durable decisions | Linear | Short navigation pointers or generated mirrors only when offline/code-adjacent consumption is necessary |
| Durable knowledge and reusable briefs | Obsidian | Canonical knowledge notes, not task-status mirrors |
| `Do Date`, rituals, daily execution ledgers | Notion | Operational data; never project phase/status authority |
| Code, pull requests, commits, executable evidence | Git/GitHub | Implementation truth; never roadmap authority |
| Runtime declarations | `.config` and runtime manifests | Machine-readable operational truth |
| Claude-mem, Graphify, OpenWiki | Derived memory/indexes | Store source URL/ID, commit, checksum, and summaries; never become co-canonical |

Do not synchronize authority bidirectionally. A downstream state may cite its source but must not silently overwrite it.

## Canonical Linear Documents

Maintain four durable documents, addressed through `.config/agentic-os-governance.json`:

1. `architecture`
2. `governance`
3. `tooling`
4. `data`

Keep issue bodies as change records and implementation contracts that link to the relevant document. Do not duplicate a document body in its issue.

## Local-document test

Create or retain a local specification only when both conditions hold:

1. It is reusable beyond one Linear issue.
2. It needs offline or code-adjacent consumption.

Otherwise place it in a Linear Document or issue body. A permitted local mirror must declare its source and generated state and must have an explicit pull/check path. An operational registry may remain local when software consumes or validates it directly; link its policy document instead of copying it.

## Memory policy

Index canonical sources by stable identifier and URL. Permit short derived summaries, embeddings, graph edges, timestamps, and checksums. Reject full copied document bodies, independent status fields, and decisions that cannot be traced back to Linear or Git.

## Session ownership

- Start from the Linear Document that owns the concern.
- Use repository checks as evidence, not as a replacement roadmap.
- End mutating work with test evidence consolidated in the Linear issue body.
- Treat comments as non-canonical discussion. Delete only agent-generated comments whose unique substance has been verified in the body; preserve human and system comments.
- Keep handoffs temporary and pointer-based.
- Never auto-pull, auto-fix, or change issue state from a session-start hook.

## Language and future publication

Use Spanish for current narrative and English for technical identifiers. Do not create bilingual duplicates. Before open-source publication, run a dedicated gate for English translation, secrets/PII removal, exclusion of private vault areas, internal-link repair, generated-artifact policy, and licensing.
