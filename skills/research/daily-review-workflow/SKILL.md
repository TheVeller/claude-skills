---
name: daily-review-workflow
description: Complete workflow for conducting daily reviews with data aggregation. Use when executing daily-review command, syncing external data sources (Linear, Notion, Calendar, etc.) before generating review reports, or understanding the daily review process flow. Triggers on requests like "run daily review", "sync data for daily note", "conduct end-of-day review", or when user mentions daily-review command.
---

# Daily Review Workflow

Complete workflow for conducting end-of-day reviews with automatic data aggregation from external systems.

## Overview

The daily review process follows a **Sync → Analyze → Report** flow:

1. **Data Aggregation**: Sync all external data sources to populate today's daily note
2. **Analysis**: Review today's activity, progress, and insights
3. **Report Generation**: Create structured review in daily note

## Workflow

### Step 0: Data Aggregation (CRITICAL - Execute First)

**MUST execute** `node .scripts/daily-pull.js` before analyzing the vault.

This script orchestrates syncs from multiple sources:

1. **Fathom** - Meeting recordings (new ones since today)
2. **Linear** - Issues from Crafter Station workspace
3. **Notion** - Tasks from multiple databases:
   - Personal tablero
   - Goals-OS database
   - GPT Chain database
   - Teams tablero
4. **Google Calendar** - Events for today
5. **Cal.com** - Bookings for today
6. **Gmail** - Important emails, daily summary, follow-ups
7. **Apollo CRM** - Contacts (if configured)

**Execution:**
```bash
node .scripts/daily-pull.js
```

**Options:**
- `--skip-linear` - Skip Linear sync
- `--skip-notion` - Skip Notion sync
- `--skip-calendar` - Skip Calendar sync
- `--skip-fathom` - Skip Fathom sync
- `--skip-calcom` - Skip Cal.com sync
- `--skip-email` - Skip Gmail sync
- `--skip-apollo` - Skip Apollo CRM sync
- `--dry-run` - Show what would be synced without updating files

**Error Handling:**
- If a sync fails, the script continues with other syncs
- Failed syncs are logged but don't stop the process
- The daily review should proceed even if some syncs fail

**Output:**
- Populates today's daily note at `01_Journal/YYYY/1-Daily/YYYY-MM-DD.md`
- Updates sections: Tasks, Calendar, Meetings, Email Follow-ups
- Counts pending items in inbox

### Step 1: Today's Activity Analysis

After syncs complete, analyze:

- **Notes modified today** - Find all `.md` files modified today
- **New notes created** - Identify newly created files
- **Project work** - Review progress across active projects
- **Synced tasks** - Review tasks from Linear and Notion (now in daily note)
- **Synced events** - Review calendar events and Cal.com bookings
- **Synced meetings** - Review Fathom recordings and action items

### Step 2: Progress Assessment

Evaluate:
- What was accomplished?
- What got stuck or blocked?
- What unexpected discoveries emerged?
- Review completed tasks from synced sources

### Step 3: Capture Insights

Document:
- Key learnings from today
- New connections discovered
- Questions that arose

### Step 4: Tomorrow's Setup

Plan:
- Top 3 priorities
- Open loops to close
- Questions to explore
- Review pending tasks from synced sources

### Step 5: Generate Report

Create structured review in daily note with:
- Accomplished items
- Progress made by project/area
- Insights and learnings
- Blocked/stuck items
- Discovered questions
- Tomorrow's focus (top 3 priorities)
- Open loops

## Daily Note Structure

The daily note template includes sections that get populated by syncs:

```markdown
## Calendar
### Today's Events
<!-- Updated by calendar-sync.js -->
- [Events appear here]

### From Cal.com
<!-- Updated by calcom-sync.js -->
- [Cal.com bookings appear here]

### Meetings Recorded (Fathom)
<!-- Links to Fathom recordings from today -->
- [Meetings appear here]

## Tasks
### From Linear (Crafter Station)
<!-- Updated by linear-sync.js -->
- [ ] [Issues appear here]

### From Notion (Personal)
<!-- Updated by notion-sync-personal.js -->
- [ ] [Tasks appear here]

### From Notion (Goals-OS)
<!-- Updated by notion-sync-goals-os.js -->
- [ ] [Tasks appear here]

### From Notion (GPT Chain)
<!-- Updated by notion-sync-gpt-chain.js -->
- [ ] [Tasks appear here]

### From Notion (Teams)
<!-- Updated by notion-sync-teams.js -->
- [ ] [Tasks appear here]

### From Gmail
<!-- Updated by email-sync.js -->
*No emails synced yet*

### Email Follow-ups
<!-- Updated by email-sync.js -->
*No pending follow-ups*

### From Fathom (Action Items)
<!-- Action items extracted from today's meetings -->
- [ ] [Action items appear here]
```

## Sync Order

Syncs execute in this order:

1. Fathom (meetings first - may inform other syncs)
2. Linear (task management)
3. Notion Personal
4. Notion Goals-OS
5. Notion GPT Chain
6. Notion Teams
7. Calendar (events)
8. Cal.com (bookings)
9. Gmail (emails)
10. Apollo CRM (contacts)

This order ensures dependencies are handled correctly (e.g., meetings before calendar events).

## Error Handling

**Individual Sync Failures:**
- Each sync is wrapped in try/catch
- Failed syncs are logged but don't stop others
- Errors are collected and reported at the end

**Complete Failure:**
- If daily-pull.js fails completely, daily review should still proceed
- Note in report which syncs failed
- User can manually sync later if needed

## Integration with Daily Review Command

The `/daily-review` command (`.claude/commands/daily-review.md`) uses this workflow:

1. Executes `daily-pull.js` first (Step 0)
2. Waits for syncs to complete
3. Reads updated daily note
4. Performs analysis (Steps 1-4)
5. Generates report (Step 5)

## References

- **Sync Orchestration**: `.scripts/daily-pull.js` - Main sync orchestrator
- **Individual Sync Scripts**: See `references/sync-sources.md` for details on each sync
- **Daily Review Command**: `.claude/commands/daily-review.md` - Command implementation
- **Error Handling**: `references/error-handling.md` - Detailed error handling patterns

## Common Issues

**Syncs taking too long:**
- Some syncs (especially Notion with multiple databases) can take 10-30 seconds
- This is normal - wait for completion before proceeding

**Daily note not found:**
- Script creates daily note if it doesn't exist
- If creation fails, daily review can still proceed with manual note creation

**Missing API keys:**
- Check `.claude/secrets.local.json` for required keys
- Syncs requiring missing keys will fail gracefully
- See individual sync scripts for required keys

**High pending count:**
- If pending items > 10, consider running `/classify` command
- Daily pull reports this automatically
