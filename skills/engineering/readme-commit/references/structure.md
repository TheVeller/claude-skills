# README structure (readme-commit)

Exact skeleton. Omit empty sections. English body.

**Modes:** `greenfield` / `existing` via `modes.md`.

**Canons:** notion-publisher (matrix + 28px strip), graphify (box), distilledbrew (Tech Stack).

**Ship:** `sync-github-about.sh` + gate `--repo owner/repo`.

## Three layers

1. **Hero badges** — tech/runtime/org shields (not Compatible-with)
2. **Compatible with** — channels + sources/destinations only; logos `docs/assets/logos/` `height="28"`
3. **Surfaces / App tools** — app capabilities matrix (MCP, bots, REST, consoles); cell `width="20"`

Stack (React, Vite, Bun, Clerk, Supabase, TanStack, Tailwind, TypeScript) = badges + Tech Stack. Never Compatible-with.

## Hero

`<div align="center">` + `<pre>` Template A (`╔`). Then:

1. `# Title`
2. Bold one-liner
3. Meta badges + **stack shields**
4. Links
5. `### Compatible with` — ≥2 channel/source logos **or** `<!-- logos: pending -->`
6. Cover `width="900"` **or** honest skip

## Body (every H2 emoji-prefixed)

1. `## ✨ Why this exists + Features` — exact
2. `## 🧩 Surfaces / App tools` — logo | Name | Role | Status; or `<!-- surfaces: pending -->`
3. `## 🚫 What it is not` — omit if empty
4. `## 🏗️ How it works / Architecture`
5. `## 🔗 Upstream / Integrations` — omit if empty
6. `## 📊 Status` — omit if empty
7. `## 🚀 Quick start` — exact
8. `## 📡 API` — omit if none
9. `## 🛠️ Tech Stack` — for-the-badge + Layer + Requirements
10. `## 📚 Documentation`
11. `## 🏷️ Topics / search keywords` — ≥3, mirror About
12. `## 🤝 Contributing`
13. `## 📄 License`

## Footer

Visible: `with 🖤 by TheVeller · Núcleo Lab · Crafter Station` (linked as in skill).

## Separators

Blank lines between blocks. Single `---` before footer only.
