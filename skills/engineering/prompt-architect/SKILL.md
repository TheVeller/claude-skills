---
name: prompt-architect
description: >
  Turns an app idea into mvp-plan, design-style-plan, prd and a first Lovable prompt,
  using a Refero reference, a Relume sitemap, one scroll-stopper component and a local
  identity palette. Never goes straight to Lovable. Use when the user invokes
  /prompt-architect, has an app idea to pack for Lovable, or asks for a surface map,
  Refero, Relume, scroll stopper, and local identity before building.
argument-hint: "[app idea]"
category: engineering
---

# prompt-architect

Turn an **app idea** into a Lovable-ready pack. The pack is the product of this skill.
Lovable is a later handoff, never the first move.

**Language:** skill docs English. Conversation may stay Spanish.

**Skill dir:** `$SKILL_DIR` = directory containing this `SKILL.md`.

## Hard rules

1. **Never go straight to Lovable.** Do not open Lovable, paste a prompt into Lovable, or ask `start-cc+lv` to bootstrap until the four deliverables below exist and the user has signed off on the first Lovable prompt.
2. **Four deliverables, in order.** `mvp-plan` → `design-style-plan` → `prd` → first Lovable prompt. Do not skip ahead to the prompt.
3. **Four design locks, required.** Every pack names exactly one Refero reference, one Relume sitemap, one scroll-stopper component, and one local identity palette. If any lock is missing, stop and ask — do not invent a generic SaaS look.
4. **One surface map.** List the screens/surfaces the MVP will actually ship. Everything else is out of scope.
5. **Handoff only.** When the pack is complete, give the user the first Lovable prompt and point them at `start-cc+lv` for the session contract. This skill does not build the app.

## Inputs

| Input | Role |
|---|---|
| App idea (one paragraph is enough) | Problem, who it is for, what "done" looks like |
| Optional audience / city / brand | Grounds the local identity palette |
| Optional existing notes, screenshots, competitors | Evidence — cite, do not flatten |

If the idea is only a noun ("a CRM"), ask one clarifying question for the job-to-be-done, then continue. Do not interview the idea to death.

## Design locks

Resolve these before writing the PRD. Write them into `design-style-plan`.

| Lock | What "done" means |
|---|---|
| **Refero reference** | One real UI from [Refero](https://refero.design) (or a captured Refero-style shot) that sets hierarchy, density, and component rhythm. Name the product + screen, not "clean SaaS". |
| **Relume sitemap** | One sitemap shaped with [Relume](https://www.relume.io) page/section vocabulary. Pages and sections only — no wireframe essay. |
| **Scroll-stopper** | Exactly one component (hero, first fold, or key empty state) that must stop the scroll. Specify the motion, contrast, and the line of copy that does the stopping. |
| **Local identity palette** | Colors, type, and two texture/material notes grounded in a real place, brand, or cultural identity the user owns — not a generic AI gradient. 5–7 colors max, with roles (bg, fg, accent, danger, mute). |

If the user has no Refero or Relume pick yet, propose **one** candidate for each and wait for a yes. Do not generate three moodboards.

## Workflow

### 1. Surface map

Write the MVP as a short surface map: 4–8 surfaces, each with one job. Mark the surface that holds the scroll-stopper. Drop anything that is not needed for the first useful loop.

### 2. `mvp-plan`

A markdown plan, not a manifesto:

- Problem and who feels it
- First useful loop (the one path that must work)
- Surface map
- In / out of scope
- Success check the user can see without opening DevTools

### 3. `design-style-plan`

Lock the four design items above, then:

- Type pairing and scale
- Spacing and radius
- What the scroll-stopper looks like in one paragraph
- What this product must **not** look like (one line)

### 4. `prd`

Product requirements for the MVP only:

- Users and jobs
- Surfaces → requirements (must / should)
- Empty, error, and success states for the first useful loop
- Data the MVP stores (names, not a schema essay)
- Non-goals

### 5. First Lovable prompt

One prompt. It must:

- Restate the idea in two sentences
- Point at the four design locks by name
- List the surface map
- Quote the scroll-stopper copy and the palette roles
- Say what not to build
- Tell Lovable to implement the MVP from `mvp-plan` + `design-style-plan` + `prd`, not to invent a new product

Show the prompt to the user. **Stop.** Do not paste it into Lovable.

## Outputs

Write four files next to the idea (ask where; default to the current repo root or a `docs/` folder the user names):

| File | Content |
|---|---|
| `mvp-plan.md` | Step 2 |
| `design-style-plan.md` | Step 3 + the four locks |
| `prd.md` | Step 4 |
| `lovable-prompt.md` | Step 5 |

If the user wants them inline instead of files, print the same four headings in that order.

## Done

The pack is done when all four files (or headings) exist, every design lock has a concrete name, and the user has the first Lovable prompt in their hands. Next session, if they want to build: `start-cc+lv`.
