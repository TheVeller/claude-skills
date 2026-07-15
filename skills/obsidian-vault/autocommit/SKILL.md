---
name: autocommit
description: Operate the local auto-commit daemon for this vault. Use when the user wants to start, stop, restart, inspect, debug, or verify the auto-commit system, or asks about background git automation in this workspace.
---

# Autocommit

Manage the vault's local auto-commit system safely and consistently.

This skill is for the modular daemon behind:

- `.scripts/auto-commit-control.sh`
- `.scripts/auto-commit.sh`
- `.scripts/auto-commit/`

## Use This Skill For

- starting the auto-commit monitor
- stopping it
- restarting it
- checking status
- reading recent logs
- understanding why it is not committing or not staying alive

Do not use this skill for normal manual git workflows. This is specifically for the background daemon.

## Core Commands

Run from repo root:

```bash
bash .scripts/auto-commit-control.sh start
bash .scripts/auto-commit-control.sh stop
bash .scripts/auto-commit-control.sh status
bash .scripts/auto-commit-control.sh logs
bash .scripts/auto-commit-control.sh restart
```

## Standard Workflow

### 1. Check Status First

Always start with:

```bash
bash .scripts/auto-commit-control.sh status
```

If running, report:
- running/not running
- whether the user actually wants a change

### 2. If Starting

Before starting, verify:
- `fswatch` exists
- there is no obvious git operation in progress

Then run:

```bash
bash .scripts/auto-commit-control.sh start
```

After starting, verify again with `status`.

### 3. If It Fails

Check:

```bash
tail -n 80 .scripts/.auto-commit.log
```

Then inspect:
- `.scripts/auto-commit-control.sh`
- `.scripts/auto-commit.sh`
- `.scripts/auto-commit/core/monitor.sh`
- `.scripts/auto-commit/integrations/obsidian-detector.sh`

Key failure patterns:
- `fswatch` missing
- process starts but dies immediately
- Obsidian Git conflict heuristics skipping too aggressively
- commit generation failing
- push failing while commit succeeds

### 4. If Reviewing Behavior

Useful references:
- `06_Metadata/Tools/Misc/Auto-Commit-System.md`
- `.scripts/auto-commit/README.md`

## Reporting Back

When done, report:
- current daemon state
- what command was run
- whether it is now healthy
- if not healthy, the most likely reason

## Safety

- Do not restart blindly if the user is in the middle of sensitive git operations.
- Do not hide when the daemon is flaky; say whether it truly stayed running.
- Treat nested repos and unrelated git states carefully.
