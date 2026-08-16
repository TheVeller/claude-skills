# Agentic OS audit protocol

## Semantic scope

Audit source material under:

- repository root entry points;
- `.claude/`, `.agents/`, `.cursor/`, `.codex/`;
- `.scripts/`, `.config/`;
- `00_Inbox/`, `02_Programs/`, `05_Archive/`, `06_Metadata/`;
- relevant `.obsidian/` configuration;
- nested repositories for architecture, documentation, integration, and repository health.

Validate generated, vendor, cache, output, and binary artifacts mechanically. Do not semantically review them. Deep-review nested-repository code only when observed drift or risk requires it.

## Absolute exclusions

Do not read, search, summarize, index, or quote:

- `01_Journal/`;
- `03_Areas/`;
- `04_Resources/`;
- `.env` files or names containing `secret`, `credential`, `token`, `api-key`, `apikey`, or private-key material;
- credential stores, local auth sessions, keychains, or personal data.

Inspect only the existence or ignore policy of a sensitive path when a security audit requires it; never inspect its contents.

## Evidence record

For every finding, record:

| Field | Meaning |
|---|---|
| `severity` | P0, P1, P2, or P3 |
| `source` | Exact file, command output, Linear URL, or issue |
| `observed` | Factual current state |
| `expected` | Governing contract or invariant |
| `impact` | What becomes unreliable |
| `disposition` | Fix now, backlog, accept, or retire |
| `verification` | Deterministic gate proving closure |

Severity:

- **P0:** workflow blocker, data-loss/security exposure, or canonical source unavailable.
- **P1:** authority contradiction, broken active workflow, or costly duplication.
- **P2:** bounded drift with a clear future fix.
- **P3:** style or low-impact cleanup.

Correct P0/P1 during an approved execution. Create prioritized Linear backlog for P2/P3.

## Phase invariants

Read exact identifiers from `.config/agentic-os-governance.json`. Verify at minimum:

- Phase 0 has the contiguous core sequence defined in config, with amendments distinguished from core deliverables and the declared department count consistent everywhere.
- Phase 2 has one live canonical issue per configured ordinal, no gaps or duplicate ordinals, and exactly one final gate.
- Every retired Phase 2 issue has one manifest row: `historical issue -> canonical issue -> absorbed intent -> evidence -> disposition`.
- Each canonical issue actually contains the absorbed intent and acceptance evidence.
- Historical issues remain Done, detached, searchable, and recoverable unless separately approved for archive.

Do not accept title similarity as proof of absorption. Compare objective, implementation contract, acceptance criteria, dependencies, and evidence one issue at a time.

## Documentation audit

For each document, decide one role only:

1. canonical Linear Document;
2. Linear change record/implementation contract;
3. local generated mirror;
4. local executable or operational projection;
5. Obsidian durable knowledge;
6. derived index/pointer;
7. obsolete and recoverable through Git.

Flag any artifact claiming two authorities, any manual mirror without a check, and any memory entry carrying independent status or a copied canonical body.

## Safe execution gates

Before mutation:

1. Resolve exact targets and preserve unrelated dirty work.
2. Confirm the approved Linear plan and source document.
3. Show bulk-operation grouping and recoverability.
4. Keep remote deletion/archive separate from local cleanup.

After mutation:

1. Run focused tests.
2. Run local coherence check.
3. Run live check when authentication exists.
4. Record factual evidence in Linear.
5. Produce a temporary pointer-based handoff.
