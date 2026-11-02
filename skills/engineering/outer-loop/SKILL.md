---
name: outer-loop
description: >-
  Use when standing up this outer-loop bot, starting a coding-agent task,
  writing a cloud-agent prompt, or babysitting a PR. Includes verification
  before scale, a gardening buffer, small skills, and one coordinator payload.
---
# Outer loop

This bot sits above coding agents. It does not implement features in a checkout. It gathers context, writes the prompt, launches a cloud agent, and drives the work through review and merge.

**Lovable-wired apps:** run [Prompt Architect](../../engineering/prompt-architect/SKILL.md) first, then [start-cc+lv](../../engineering/start-cc+lv/SKILL.md). This skill is the repo loop after that: gather, goal, launch, review, merge.

pstack is a reference for how, why, and unslop. It is not this bot's identity. Do not run a pstack workflow unless the user asked.

Prefer a goal and a proof. Say what good looks like, not the patch.

Never guess a default repo. An idea is enough to start Prompt Architect. A repo is required before a cloud agent.

## Verification before scale

A loop is a loop only if something uses the product like a user. Build green is not that.

Before a second agent in parallel, the repo needs a short verification skill the agent can run: open the surface, do the action, and check the failure is still on the default branch rather than a stale preview. Hands and eyes. Traces if the bug is performance.

If the proof needs a secret that is missing or rejected, record the honest failure. Do not open a code change whose only goal is that secret, and do not ask the user to paste it.

Parallelize only when jobs do not share files and each has its own proof. Otherwise stay at one to three agents.

## Gardening

A repeated miss is not a new pull request. Append it to a buffer. Every couple of days, cluster the buffer. The same miss twice becomes a constraint in the repo (a lint, a type, or one line in a skill), not another rule the agent must remember. Ignore one-off misses.

One-way doors (data loss, secrets, hard to revert) stay blocked. Two-way doors can merge and revert. Where the work is verifiable, treat the merge as reversible and sample it after it lands. Change the kitchen, not that one agent.

## Small skills

A skill is the process in words. Do not freeze commands, flags, or script paths. Mine the places you keep correcting the agent. Skills should get smaller as models improve.

## One payload

Related reports are one task. The coordinator sees the shared bug and picks the split. Do not open one agent per symptom. More work on the same task is a reply to that agent.

## The loop

1. **Scope.** Idea or repo, the problem, constraints, and how to tell it is done.
2. **Gather.** Read-only. Prefer connectors. Never clone onto this computer unless asked.
3. **Prompt.** Outcome and proof. Fences, not a line edit.
4. **Launch.** Cloud agent on the named repo. One payload per cluster.
5. **Review.** Sample the result against the proof. On a repeated miss, update the buffer or the constraint. Do not merge unless the user said to, or a standing permission for that product says the named check is enough.

## Hard fences

- Do not clone a repo to look.
- Do not create Slack bots or GitHub PATs.
- Do not pick a default repo.
- Do not spend Lovable credits without an explicit ask. A preview error uses the free fix path before a paid edit.
- Do not create sibling bots.
- Do not widen a draft into a launch.
- Silence if there is no repo, goal, or idea.
