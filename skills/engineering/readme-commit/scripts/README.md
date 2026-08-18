# readme-commit scripts

Modes (`greenfield` / `existing`) live in skill docs (`../references/modes.md`), not scripts.

| Script | Purpose |
|---|---|
| `fetch-favicon.sh` | Download site favicon/apple-touch-icon into repo assets |
| `resolve-icon-url.py` | Helper: parse HTML → absolute icon URL (used by fetch-favicon) |
| `detect-stack.mjs` | Print stack hints from `package.json` (no network) |
| `sync-github-about.sh` | `gh repo edit` description / homepage / topics (`--dry-run` supported) |
| `check-readme-contract.sh` | Fail-closed: locked H2s, footer, box, cover; Compatible-with channels (stack deny-list); Surfaces matrix; Topics; ship `--repo` About |

Always invoke with **absolute vault paths** when cwd is a nested product repo.

## Screenshots

No shell wrapper. Ordered path in `SKILL.md`:

1. User path → copy to `docs/assets/` or `.github/assets/`
2. Live URL → Playwright MCP `browser_take_screenshot`
3. Skip honestly

Every image needs `alt` + `<em>` caption in the README.
