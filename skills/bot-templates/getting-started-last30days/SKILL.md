---
name: getting-started-last30days
description: >-
  Use this on the first conversation of a freshly imported last30days bot, to
  install the skill and walk the new owner through setup.
---
# Getting started with last30days

I research what people actually say about any topic in the last 30 days, across Reddit, X, YouTube, TikTok, Hacker News, Polymarket, GitHub and the web, and write a grounded brief.

## Steps
1. Install the skill: `npx skills add mvanhorn/last30days-skill -g` (into ~/.agents/skills/last30days). If it fails with ENOENT, `mkdir -p ~/.local/lib ~/.local/bin` and retry. Register it as a skill (symlink into the skills folder). Never install it as a Cursor plugin. It needs Python 3.12+ (use python3.13 if the default is older).
2. Run the engine's welcome and setup (`--welcome`, then `setup`). Export `LAST30DAYS_HOST=grok-bot`. Never overwrite ~/.config/last30days/.env: append missing keys only, chmod 600, never print secrets.
3. Ask the owner, one at a time:
   - X: use the built-in X connector if present (set `LAST30DAYS_X_HOST_LANE=1`). Otherwise offer signing into x.com on this computer, an xAI key, or skipping X. Never silently read browser cookies.
   - TikTok and Instagram: offer ScrapeCreators through GitHub device sign-in (`setup --github-start`, then `--github-poll`; the owner enters the code at https://github.com/login/device). It gives far more free credits than the web form. Save keys only with `setup --store-key`.
   - Which language and topics they care about most.
4. Create the monthly routine that checks GitHub for a newer skill version and reinstalls if one exists.
5. Write memories with their answers, then ask for the first research topic.
