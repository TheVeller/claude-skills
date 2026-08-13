# Section taxonomy

Twelve sections in reading order: what happened → why → what is coming → what it costs → what to do. Build only the ones the data supports; skipping is free, an empty section is not.

Order matters. Actuals before projections, projections before money, money before plan, plan before summary. The summary is last because it is the only section that may reference every other one.

| # | Section | The question it answers | Minimum input | Form |
|---|---|---|---|---|
| 01 | growth | How fast, and is it speeding up or slowing down? | one timestamp per record | cumulative area + periodic bars + rate bars (±) |
| 02 | acquisition mix | Where do they come from? | any origin field (domain, channel, referrer, city) | composition rows + top-N index rows |
| 03 | engagement | How many did anything at all? | any action count per record | funnel rows + distribution |
| 04 | cohorts | Which segments exist and how big? | tags/labels (multi-valued ok) | ranked index rows |
| 05 | engine | What caused the spikes, and which channel is accelerating? | timestamps + segment | spike attribution table + velocity index (recent share ÷ lifetime share) |
| 06 | activity | What did we actually do, and how did it land? | an event/action log, ideally with quality scores | upcoming list + per-period bars + satisfaction rows |
| 07 | forecast | Where does this land if nothing changes, and if it does? | 01 + a rate | scenario lines to a horizon + ETA table + "what it takes" per scenario |
| 08 | monetization | What does reach cost and what pays for it? | a cost structure + at least one real price point | tier/cost table + product ladder + break-even |
| 09 | ladder | How does the entry product feed the expensive one over time? | 08 + a conversion assumption | monthly stacked bars + accumulating pool line + cohort markers |
| 10 | pipeline | Who is already close enough to say yes? | any counterpart field (hosts, orgs, domains) | ranked prospect rows by warmth |
| 11 | plan | What do we do, in what order? | everything above | tracks, each item with owner · when · expected effect · metric to watch |
| 12 | executive summary | If I read one section, what do I do Monday? | everything above | state paragraph · what works (3) · what's at risk (3) · bottom line |

## Per-section rules

**01 growth** — Ship an as-of slider (reference date) and recompute the rolling tiles from it; static "last 7 days" numbers rot the moment the export ages. Show the rate of change, not just the volume: a growing list with a falling rate is a different story than the total tells.

**02 acquisition mix** — Classify origins into 3–4 buckets *and* show the long tail. Whoever appears repeatedly with a corporate identity is a prospect, not a row.

**03 engagement** — Always express as a funnel with the drop-off visible. The interesting number is usually the one that never converted.

**05 engine** — Velocity index = recent share ÷ lifetime share. Above 1.15 is accelerating, below 0.85 is fading, 0.00 means a segment has stopped entirely — that last one is the most actionable signal on the page.

**07 forecast** — Linear scenarios, labeled as such. Pair every scenario with **what fulfilling it actually takes** in operational terms, or it reads as a promise. Mark scenarios that only differ by cadence, not by luck.

**08 monetization** — Separate **marginal** cost from absolute: what the next step costs from where the user already is. Put the measured price point first and the modeled ones after, each with its tag.

**09 ladder** — This is a cohort-accumulation model, not a monthly multiplication: buyers accumulate into a pool, and the expensive product launches when the pool crosses a threshold. The output the user cares about is *when* the first cohort becomes possible and *how many runs it takes to get there*.

**11 plan** — Group into tracks that could each have one owner. An item without a number attached is an opinion.

**12 executive summary** — Do not restate the plan; point to it. Repetition between 11 and 12 is the most common coherence bug.
