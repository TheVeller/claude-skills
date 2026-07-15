# Sync Sources Reference

Detailed information about each data source synced during daily pull.

## Linear Sync

**Script:** `.scripts/linear-sync.js`

**Purpose:** Sync assigned issues from Linear workspace "Crafter Station"

**What it syncs:**
- Issues assigned to current user
- Issues with status != Done
- Issues due today or overdue

**Output location:** Daily note → Tasks → From Linear (Crafter Station)

**Required:**
- Linear MCP server configured
- Workspace: "Crafter Station" (team: MakerPunks, key: MAK)

**Error handling:** If Linear MCP unavailable, skips sync and continues

## Notion Syncs

### Personal Tablero

**Script:** `.scripts/notion-sync-personal.js`

**Purpose:** Sync tasks from Personal workspace database

**What it syncs:**
- Tasks due today or overdue
- Tasks with status != Done

**Output location:** Daily note → Tasks → From Notion (Personal)

**Required:**
- `NOTION_API_KEY` in secrets
- Database ID configured in script

### Goals-OS Database

**Script:** `.scripts/notion-sync-goals-os.js`

**Purpose:** Sync tasks from Goals-OS database

**What it syncs:**
- Tasks due today or overdue
- Tasks with status != Done

**Output location:** Daily note → Tasks → From Notion (Goals-OS)

**Required:**
- `NOTION_API_KEY` in secrets
- Goals-OS database ID configured

### GPT Chain Database

**Script:** `.scripts/notion-sync-gpt-chain.js`

**Purpose:** Sync tasks from GPT Chain database

**What it syncs:**
- Tasks due today or overdue
- Tasks with status != Done

**Output location:** Daily note → Tasks → From Notion (GPT Chain)

**Required:**
- `NOTION_API_KEY` in secrets
- GPT Chain database ID configured

### Teams Tablero

**Script:** `.scripts/notion-sync-teams.js`

**Purpose:** Sync tasks from Teams workspace database

**What it syncs:**
- Tasks due today or overdue
- Tasks with status != Done

**Output location:** Daily note → Tasks → From Notion (Teams)

**Required:**
- `NOTION_API_KEY` in secrets
- Teams database ID configured

**Note:** All Notion syncs use the same API key but different database IDs.

## Calendar Sync

**Script:** `.scripts/calendar-sync.js`

**Purpose:** Sync Google Calendar events for today

**What it syncs:**
- Events scheduled for today
- Links Fathom recordings to calendar events when available

**Output location:** Daily note → Calendar → Today's Events

**Required:**
- Google Calendar OAuth setup
- Calendar API access

**Integration:** Works with Fathom sync to link recordings to events

## Fathom Sync

**Script:** `.scripts/fathom-sync.js`

**Purpose:** Sync meeting recordings from Fathom

**What it syncs:**
- Recordings from today
- Meeting metadata (title, participants, duration)
- Transcripts
- Summaries
- Action items (extracted using meeting-notes skill)

**Output location:** 
- Daily note → Meetings Recorded (Fathom)
- `04_Resources/Meetings/Fathom/` - Full meeting notes

**Required:**
- `FATHOM_API_KEY` in secrets

**Integration:** Links to calendar events when available

## Cal.com Sync

**Script:** `.scripts/calcom-sync.js`

**Purpose:** Sync bookings from Cal.com

**What it syncs:**
- Bookings scheduled for today
- Booking details (attendees, duration, description)
- Generates pre-meeting briefs

**Output location:** 
- Daily note → Calendar → From Cal.com
- `00_Inbox/Pending/Meetings/` (`type: meeting-brief`) - Pre-meeting briefs

**Required:**
- `CALCOM_API_KEY` in secrets (for scripts)
- Rube MCP also provides Cal.com access (OAuth)

## Gmail Sync

**Script:** `.scripts/email-sync.js`

**Purpose:** Sync important emails and generate daily summary

**What it syncs:**
- Important emails (personalized, human-written) → Inbox capture
- Daily email summary → Daily note
- Follow-up tracking → Daily note

**Output location:**
- `00_Inbox/Pending/` - Important email captures
- Daily note → From Gmail
- Daily note → Email Follow-ups

**Required:**
- Gmail OAuth setup
- Scopes: `gmail.readonly`, `gmail.modify`

**Features:**
- AI classification of important emails
- Daily summary generation
- Follow-up tracking

## Apollo CRM Sync

**Script:** `.scripts/apollo-sync.js`

**Purpose:** Import contacts from Apollo CRM

**What it syncs:**
- Contacts to import
- Contact details

**Output location:** `04_Resources/People/`

**Required:**
- `APOLLO_API_KEY` in secrets (if configured)

**Note:** This sync is optional and may not be configured for all users.

## Sync Dependencies

**Fathom → Calendar:**
- Fathom sync runs first
- Calendar sync links recordings to events

**Calendar → Cal.com:**
- Both populate calendar section
- Cal.com provides booking details

**All → Daily Note:**
- All syncs update the same daily note
- Order matters to avoid conflicts

## Rate Limiting

**Notion:**
- Rate limit: ~3 requests/second
- Scripts include delays between requests
- Multiple databases = multiple requests

**Linear:**
- Rate limit: Varies by plan
- MCP handles rate limiting automatically

**Gmail:**
- Rate limit: 250 quota units/second
- Scripts batch operations when possible

**Fathom:**
- Rate limit: Varies by plan
- Scripts include delays

## Error Patterns

**Common failures:**
- Missing API keys → Skip sync, log error
- Network timeout → Retry once, then skip
- Invalid database ID → Skip sync, log error
- OAuth expired → Skip sync, prompt user to re-authenticate

**Recovery:**
- Failed syncs don't block others
- User can manually re-run specific syncs
- Daily review proceeds with available data
