# Design system

One architecture, a palette per subject. The structure below stays constant across dashboards; the accent hue, the neutral bias and the typographic voice come from the subject at hand. Load the `artifact-design` skill for the aesthetic call and `dataviz` before writing chart code.

## Tokens and the three-state theme

The viewer has three states, not two: explicit light, explicit dark, and system (no attribute stamped). Define the full light palette on bare `:root`, redefine only the tokens under `@media (prefers-color-scheme: dark)` guarded as `:root:not([data-theme="light"])`, then again under `:root[data-theme="dark"]`. Style everything through the tokens — a color declared only inside a media block never applies in the un-stamped state, which is how a page ends up with one theme's text on the other theme's ground.

```css
:root {
  --bg: …; --card: …; --border: …;      /* surfaces */
  --ink: …; --ink-2: …; --muted: …;      /* text, in descending weight */
  --accent: …; --accent-soft: …;         /* the subject's signal color */
  --warn: …;                             /* the one alert hue, never the accent */
  --track: …; --gridline: …;             /* chart furniture */
}
```

`body` must paint an explicit token background; a transparent body borrows the host's ground. Keep `--warn` semantically separate from `--accent`: the accent means "this is the signal", the warn means "this needs attention", and a page that conflates them cannot show a problem.

## Structural conventions

- **Squared geometry** — `--radius: 0` throughout, or a single deliberate radius; mixing is what makes a dashboard look assembled rather than designed
- **Mono for metadata** — labels, stamps, axis ticks, provenance tags in monospace, uppercase, ~10px, letter-spacing ~0.08em. Sans for prose and for the big numbers
- **`font-variant-numeric: tabular-nums`** everywhere digits stack
- **Tiles** in a fixed grid (5×2 or 4×2). If a cell is left over, fill it with something that carries information — a period label, a state — never a decorative void
- **Sticky section nav** that wraps and centers (`flex-wrap: wrap; justify-content: center`). A nowrap nav inside a max-width container overflows silently the moment a section is added
- **Wide content scrolls inside its own container** (`overflow-x: auto` on the table/chart wrapper), so the page body never scrolls sideways

## Provenance tags

```css
.src { font: 10px ui-monospace; text-transform: uppercase; padding: 1px 4px; border: 1px solid; }
.src.observed  { color: var(--accent); border-color: var(--accent); }
.src.benchmark { color: var(--ink-2);  border-color: var(--border); }
.src.assumed   { color: var(--warn);   border-color: var(--warn); }
```

Render them inline next to the figure they qualify, in tables and in cards alike.

## Charts

Inline SVG only — the Artifact CSP blocks external libraries. Shared specs:

- Thin marks, recessive grid, axis text in `--muted`
- Direct labels on the marks that matter (endpoint, peak, threshold crossing); never a number on every point
- A threshold line (cost, target, break-even) gets a label at the end of the line, anchored so it cannot collide with the first mark
- Stacked bars need a legend; a legend row of small squares plus text costs 20px and saves the reader every time
- Hover tooltip on every plotted series — an HTML/SVG chart is interactive by default
- Stagger end labels when several lines converge: sort by y, push each one below the previous if closer than ~13px

## Interaction

Filter and scenario controls are square buttons (`.fbtn`) in a row above the thing they change, with the active one filled in the accent. A range slider gets its own full-width row — sharing a flex row with a variable-width label changes the track width mid-drag and makes the thumb jump. Give the slider a month ruler with ticks aligned to the thumb's travel (`left/right: half-thumb`), and echo the current position in a label with period, week and index.

## Bilingual from the start

Mark every user-visible string `data-key="section.item"` and keep two dictionaries (`en`, `es`) plus a selector that re-walks the DOM. Adding i18n after the fact means touching every line again — build it in from the first section. Strings composed in JavaScript need the same treatment: read them from the active dictionary rather than concatenating literals.

## Diagram embedding

Rendered PNGs go in as `data:` URIs (external assets are blocked). Render at scale 2 and a width around 1400 for legibility without bloating the page; the whole artifact must stay under 16MB.
