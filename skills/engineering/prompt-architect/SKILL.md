---
name: prompt-architect
description: >-
  Use this when the user has an app idea and needs the surface map, one
  reference, mvp-plan.md, design-style-plan.md, prd.md, and the first prompt
  before Lovable or a coding agent. Uses a Refero reference, a Relume sitemap,
  one scroll-stopper component and a local identity palette. Never goes
  straight to Lovable. Use when the user invokes /prompt-architect.
argument-hint: "[app idea]"
category: engineering
---
# prompt-architect

Turn an app idea into a pack a builder can paste into Lovable, Cursor, Bolt, v0, or Replit. The pack is the product of this skill; the builder is a later handoff, never the first move. Mirror the user's language in the docs (ES / EN / PT). Code and the first prompt stay English.

This skill is the standard for every new project. Do not skip a step and do not go straight to Lovable.

> Grok Bot fleet: internal skill of SWE, not a sibling bot. Do not spawn a separate Prompt Architect bot.

## Hard rules

1. **Never go straight to Lovable.** Do not open Lovable, paste a prompt into Lovable, or ask `start-cc+lv` to bootstrap until the four deliverables exist and the user has signed off on the first prompt.
2. **Four deliverables, in order.** `mvp-plan` → `design-style-plan` → `prd` → first prompt. Do not skip ahead to the prompt.
3. **Design locks, required.** Every pack names one reference, one surface map (Relume or hand-built), one scroll-stopper component, and one local identity palette. If any lock is missing, ask once — do not invent a generic SaaS look.
4. **One surface map.** List the screens/surfaces the MVP will actually ship. Everything else is out of scope.
5. **Handoff only.** When the pack is complete, give the user the first prompt and point them at `start-cc+lv` for the session contract. This skill does not build the app.

## Inputs

| Input | Role |
|---|---|
| App idea (one paragraph is enough) | Problem, who it is for, what "done" looks like |
| Optional audience / city / brand | Grounds the local identity palette |
| Optional existing notes, screenshots, competitors | Evidence — cite, do not flatten |

If the idea is only a noun ("a CRM"), ask one clarifying question for the job-to-be-done, then continue. Do not interview the idea to death.

## Before any doc

Do these in order. Do not open with a homepage.

1. **Reference.** One URL of a screen that already works in this niche. Refero, referral.design, Savee, or 21st.dev are the usual places. If the user did not name one, ask once. Do not invent a look. When the user gives a Refero style link (for example `styles.refero.design/style/<id>`), use that link as the design DNA: pull its palette, type and spacing, and say what you took from it. Name the product + screen, not "clean SaaS".
2. **Surfaces before the homepage.** Map every page or app surface first (4–8 surfaces, each with one job; mark the one that holds the scroll-stopper). For a marketing site, use Relume: one paragraph of the product, the reference URL, and the design principles, then the generated sitemap and wireframes. Move sections before export. The homepage is one surface. If the Relume MCP or Composio plugin is connected, use it; otherwise build the sitemap by hand from the same shape (home, about, product, contact, plus whatever the idea needs).
3. **One component (the scroll stopper).** Pick one real component to bring over (21st.dev or the Relume library). Not a moodboard. This is the attention-grabber that stops the scroll in the hero: an interactive search, a live map, a quote or price animation, a video. Name it, say where it lives (usually the hero), and specify the motion, contrast, and the line of copy that does the stopping. If one is not obvious, ask once.
4. **Local identity match.** Take the reference palette and recolor it toward the place or brand the product is for. For a place, use its real materials and landmarks (for Arequipa: sillar white, terracotta, charcoal, the Misti, 🇳🇵). Do not copy the reference site's colors blindly when a local identity exists. Write the final palette (3 to 5 colors with roles) into the design doc.
5. **Mobile is in the first build.** Most traffic is a phone. The first prompt says mobile first, then widen, and a person still clicks every width.
6. **Concrete copy.** Name the specific thing. Prefer the action ("start free") over "get started". No em-dash piles. No line that admits the photos or names are placeholders.
7. **Images and SEO after structure.** Generate a logo or photo only when one is missing. A keyword roadmap does not block the first build.

If the user has no reference or sitemap pick yet, propose **one** candidate for each and wait for a yes. Do not generate three moodboards.

## Sources (read-only, check the link opens before using it)

- **Refero styles** (`styles.refero.design`): design DNA. Take palette, type and spacing from one style link and say what you took.
- **Relume** (`relume.ai`): sitemap and wireframes before any build.
- **21st.dev** and **React Bits** (`reactbits.dev`): the one scroll-stopper component. Name the component and where it goes.
- **Context.dev design.md generator** (`context.dev/free-tools/design-md-generator`): turns an existing site into a `design.md` (colors, type, spacing). Use it to read an existing brand from its live site.
- **GitHub OSS**: for an existing product or brand, read its repo (tailwind config, CSS variables, fonts, logos) before inventing anything.
- **Brand identity owner**: if the brand already has an identity made by the design owner (Musa Designer in Futuraria), use it as the palette and type source and do not redo it. If the design owner has none, the extracted site/repo identity goes to them in a `brand-kit.md` (palette hex, type, logo URL, three literal quotes of tone, mobile and desktop screenshots, source of each item). Extract only after the user says yes.

## Output

Four fenced `md` blocks, this order, no commentary around them. If the user wants files instead, write the same four files where they say (default: repo root or a `docs/` folder they name).

1. **mvp-plan.md** — goal, problem and who feels it, first useful loop, scope and exclusions, stack, weekly timeline, success metrics the user can see without opening DevTools. Includes the surface list from Relume (or the hand-built sitemap).
2. **design-style-plan.md** — the reference URL, the surface map, the one scroll-stopper component, the local identity palette and type (pairing and scale), spacing and radius, the mobile widths, the copy rules above, and one line on what this product must **not** look like.
3. **prd.md** — vision, users and jobs, surfaces → requirements (must / should), empty/error/success states for the first useful loop, data the MVP stores (names, not a schema essay), non-functional specs, non-goals, roadmap, metrics.
4. **first-prompt.md** — the English prompt that restates the idea in two sentences and says: build from this surface map and this reference URL, include this one scroll-stopper component (quote its copy), match the local identity palette (quote the roles), mobile first, concrete copy, no SEO pass yet, what not to build, and implement the MVP from `mvp-plan` + `design-style-plan` + `prd`, not a new product. If a Relume export exists, the prompt says to build from that export plus the reference, not from a vibe.

Show the prompt to the user. **Stop.** Do not paste it into Lovable.

## Defaults

- Web / frontend unless the user asks for backend
- React + Vite + Tailwind unless they name something else
- Infer missing constraints with a lean MVP
- No brand CTAs, no third-party signup blocks

## Done

The pack is done when all four blocks (or files) exist, every design lock has a concrete name, and the user has the first prompt in their hands.

## After delivery

Offer the Lovable batch using these docs as project knowledge, then git and cloud agents (`start-cc+lv`). Do not launch that batch unless they asked.
