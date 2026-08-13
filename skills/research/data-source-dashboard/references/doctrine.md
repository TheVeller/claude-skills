# Doctrine

Rules paid for in rework. Each one exists because skipping it cost a full iteration.

## The privacy boundary

The raw export holds names, emails and per-person behaviour. **It stays where the user put it** (Downloads, a gitignored folder) and is read in place. Only `metrics.json` — counts, shares, distributions — crosses into the repo and the published page.

- Never copy the raw file into the repo, "temporarily" included
- Never emit a list of individuals. Aggregate to domain, segment or count
- Organisation names may be published only when the user approves them explicitly, and never alongside contact details
- Credentials live in `.claude/secrets.local.json` (gitignored) and are read by fetch scripts. A key never appears in a template, a build output, or a commit
- `audit.mjs` greps the built page for address-shaped strings and key prefixes before publishing. When it fails, fix the pipeline — never relax the gate

## Provenance on every number

Three tags, rendered next to the figure, not hidden in a comment:

| Tag | Meaning |
|---|---|
| `observed` | measured from the user's own data |
| `benchmark` | external standard, source named |
| `assumed` | a decision with no history behind it yet |

A dashboard where measured and invented numbers look identical is worse than no dashboard: it launders assumptions into facts. When a reader cannot tell which is which, they cannot argue with the model, and a model nobody can argue with does not get corrected.

## Measured data outranks modeled data

A single real transaction beats a beautiful projection. When a redesign is tempted to drop the measured line because the modeled one is cleaner, the measured line stays and the model gets rebuilt around it. Real evidence is the only thing in the dashboard that cannot be regenerated.

## Assumptions are controls, not constants

Every assumption a reader might dispute becomes a toggle that recomputes the view: price, conversion, cadence, upgrade rate, cohort size. This converts arguments about the numbers into experiments with the numbers, and it is the difference between a report and a tool.

## One number, one definition

Define each derived figure once and reference it everywhere. Break-even seats, marginal cost, doubling time — when the same concept is recomputed in three sections, they drift, and the reader stops trusting all three. Contradictions between sections are the most damaging bug this dashboard can ship.

## Charts must survive first contact

A chart is finished when someone who has never seen it can state what it says. That requires a legend, direct labels on the marks that matter, and one plain sentence explaining how to read it. Abstract cumulative lines with no annotation get skipped; annotated ones get quoted in meetings.

## Prose closes every section

End each section with a sentence that says what the numbers mean and what changes because of them. Numbers state; sentences decide.

## The snapshot ages

The page is a snapshot, but it is read weeks later. Recompute from the viewer's clock: how old the export is, what each scenario implies today, how many days remain to a milestone. Flag staleness past a month instead of quietly presenting old numbers as current.

## Verify by looking

Render it, open it, look at it — at desktop, at mobile, in light and dark. Overflow, collisions and unreadable contrast are invisible in source and obvious on screen. The validator checks color; only your eyes check layout.

## Iterate in place

Republish the same file path so the artifact keeps its URL. The user shares that link; a new URL each round breaks every reference to it.
