---
name: drift-hunt-roster
description: Use when running a daily roster drift hunt - compare live agents and rooms on the box against the fleet inventory docs and report only new deltas to an ops room.
---
# Roster drift hunt

1. Count live dirs in the agents folder on the box. A dir with group.json is a room; any other dir is an agent.
2. Compare against the source-of-truth docs (inventory and roster) and the locked expected count kept in the routine prompt.
3. For each id not in the docs or the closed list, read its profile (name, description, manager) and its creation time with `stat -c %w` (birth time). Never use mtime for creation dates; bulk mtime changes from syncs or restores are not drift.
4. A delta is only: a new live id not listed, a listed id missing from the box, a new rename, or the canon count rewritten without a lock. Items already reported and waiting for a decision are not reposted.
5. If there is a delta, write one finding signed with the bot's name: 🎯 what changed · 🔗 one link or n/d · ⭐ score · ➡️ next owner and action. Dense prose, no code fences. Post it to the ops room only.
6. If there is no delta, stay silent.
7. Never edit the docs, create bots, or message the owner directly. When a lock arrives in the room (the owner's decision relayed by the fleet director), update the routine prompt's expected count and closed list with a full-prompt update, and log it in memory.
8. If a run fails or skips, say so in the next stand-up and re-verify before reposting.
