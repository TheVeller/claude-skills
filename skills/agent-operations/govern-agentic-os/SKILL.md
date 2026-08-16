---
name: govern-agentic-os
description: Audit, plan, execute, check, and hand off governance work for this Agentic OS/Claudesidian repository. Use when reconciling the repository with Linear Documents, auditing documentation or architecture, validating phase structure or historical-issue absorption, fixing cross-session drift, deciding where documentation belongs, or preparing an Agentic OS handoff.
---

# Govern Agentic OS

Govern the repository without creating a second source of truth. Treat Linear Documents as durable project canon, repository files as executable or offline artifacts, and memory systems as pointer/derived-index layers.

## Select one mode

| Mode | Default authority | Purpose |
|---|---|---|
| `audit` | Read-only | Collect evidence and classify drift. |
| `plan` | Read-only | Propose a gated remediation plan. |
| `execute` | Mutating, explicitly authorized | Apply only an approved plan. |
| `check` | Read-only | Run deterministic coherence checks. |
| `handoff` | Read-only by default | Compact state into links, evidence, and next actions. |

If the user does not select a mode, infer it from the request. Never infer authorization for `execute` from an audit, diagnosis, review, or plan request.

## Load only the needed context

1. Read [governance-contract.md](references/governance-contract.md) for every mode.
2. Read [audit-protocol.md](references/audit-protocol.md) for `audit`, `plan`, or repo-wide `execute` work.
3. Read `.config/agentic-os-governance.json` when it exists. Treat it as the machine-readable map of Linear IDs, permitted mirrors, exclusions, and phase invariants; do not hard-code those IDs elsewhere.
4. Read the relevant Linear Document or issue before judging its local projection.
5. Use memory/Graphify/OpenWiki only to discover pointers. Verify every material claim at its source.

## Apply the safe workflow

### Audit

1. State the scope and exclusions before reading files.
2. Read source files semantically and generated/vendor artifacts mechanically.
3. Inspect nested repositories for architecture, documentation, integration, and repository health; deep-review code only when evidence reveals drift or risk.
4. Record each finding with severity, source, observed state, expected authority, evidence, and proposed disposition.
5. Correct nothing. Publish findings to Linear only when the user explicitly authorizes the write.

Never read `01_Journal/`, `03_Areas/`, `04_Resources/`, secret-like paths, credentials, tokens, or local environment files during this workflow.

### Plan

1. Start from audit evidence, not memory summaries.
2. Preserve the authority split in the governance contract.
3. Group work into small phases with one verifiable gate per phase.
4. Correct P0/P1 findings in execution; route P2/P3 findings to prioritized Linear backlog.
5. Show exact Linear and filesystem mutation targets. Do not apply the plan.

### Execute

1. Require an approved plan and resolve its exact targets.
2. Re-read each target immediately before mutation.
3. Apply the smallest coherent change; never auto-pull or auto-fix unrelated drift.
4. Keep Linear Documents canonical, issues as change records, and local mirrors generated or explicitly code-adjacent.
5. Run proportional tests and `check` before closing work.
6. Consolidate factual evidence in the relevant issue body only after verification. Do not create a parallel implementation log in comments.

### Check

Run the single repository checker:

```bash
npm run agentic-os:check
npm run agentic-os:check -- --live
npm run agentic-os:check -- --json
```

Local mode is the offline default. It validates the governance config, generated-projection checksums, phase metadata, package/script safety, intention invariants, and ADK mirrors without reading secrets or making network calls. `--live` adds read-only Linear Document reachability and requires `LINEAR_API_KEY`; runtime tooling remains an explicit `npm run tooling:check` because it crosses into user-home runtime configuration. Neither mode writes or pulls. Interpret exit codes as:

- `0`: checks passed; warnings may remain.
- `1`: coherence drift.
- `2`: invalid invocation or missing live precondition.

### Handoff

1. Put the handoff in the operating system's temporary directory, not the repository.
2. Reference Linear Documents, issues, commits, diffs, and files instead of copying them.
3. Include scope, verified state, remaining gates, exact next command, and suggested skills.
4. Redact secrets and personal information.
5. Update Linear only with explicit authorization.

## Enforce the session contract

At session start, run local check and report drift without correcting it. Open the applicable Linear Document before planning or editing.

At session close, run local and live checks when authentication is available, update the relevant Linear issue body with implementation evidence, then prepare a pointer-based handoff. Comments are for exceptional human discussion, not canonical status or evidence. Never mark an issue Done while a required live check fails.

After any change to `.claude/commands/`, `.claude/skills/`, or `.agents/skills/`, follow the repository's ADK sync instructions. Do not run sync merely by invoking this skill.

## Keep outputs English-ready

Write current project narrative in Spanish. Use English for filenames, command names, JSON keys, stable identifiers, and contract headings. Do not maintain parallel translations. Defer full English migration, privacy review, link review, and licensing to the explicit open-source publication gate.
