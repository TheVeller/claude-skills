# readme-commit modes

Two modes only. Locked skeleton, emoji H2s, footer, and taste bars stay the same; **how you write** changes.

## Detection

| Condition | Mode |
|---|---|
| No `README.md`, empty file, or placeholder-only (`# Name`, `TODO`, `<project name>`) | `greenfield` |
| README has real H2 / prose / tables usable as baseline | `existing` |
| User says `force-greenfield` | force `greenfield` |
| User says `merge-only` | force `existing` |

Announce the chosen mode + one-line reason before Detect/crawl.

**Hard rule:** never full-overwrite a non-empty README without explicit user OK.

## Posture

| Mode | Posture |
|---|---|
| `greenfield` | Full elegant skeleton from `structure.md`. General meta badges. Features from crawl only. No comparative table (no useful baseline). |
| `existing` | Inventory → comparative table in chat → merge. Preserve keep / keep-extra. Force locked Why/Quick-start titles, **emoji on every H2**, footer, img alt+caption, Requirements inside Tech Stack. |

## Decision vocabulary (existing)

| Decision | Meaning |
|---|---|
| **keep** | Content good; maybe retitle only for emoji-H2 rule |
| **reshape** | Same facts, skill shape (tables, captions, order) |
| **upgrade** | Weak/missing slot filled from crawl evidence |
| **replace** | Only if false, broken, or placeholder |
| **keep-extra** | Non-contract section that adds value; do not delete |
| **drop** | Spam / dupe / invented claims; ask user if unsure |

## Existing path

1. **Inventory** — map every current H2/H3 → contract slots in `structure.md`; list extras outside the skeleton.
2. **Comparative table (chat, before any write)** — required.
3. **Write** — reorder toward skeleton; preserve keep/keep-extra; do not regenerate honest diagrams unless user asks.
4. **Review** — summarize keep / reshape / upgrade / replace / keep-extra / drop counts.

## Sample comparative table

| Section | Today | Skill would do | Decision |
|---|---|---|---|
| Hero | plain H1, no ASCII | graphify-style box + meta badges + logo strip | upgrade |
| Why + Features | bullet list | `## ✨ Why this exists + Features` + Feature \| What you get | reshape |
| Architecture | stale screenshot | keep Mermaid already present | keep |
| Quick start | wrong clone URL | fix remote; rename to `## 🚀 Quick start` | reshape |
| Changelog | dense weekly log | not in skeleton | keep-extra |
| Footer | missing | TheVeller · Núcleo Lab · Crafter Station | upgrade |
| Fake “MIT” badge | no LICENSE file | pending / match real file | replace |
