# Error Handling Patterns

How to handle errors during daily review data aggregation.

## Error Handling Strategy

**Principle:** Failures in individual syncs should not prevent the daily review from completing.

## Error Levels

### Level 1: Individual Sync Failure

**What happens:**
- Sync script catches error
- Logs error message
- Returns error code
- Daily pull continues with next sync

**Example:**
```javascript
try {
  await runScript(linearSyncPath)
  console.log('✅ Linear sync complete')
} catch (error) {
  console.error('❌ Linear sync failed:', error.message)
  errors.push('Linear')
  // Continue with next sync
}
```

**User impact:**
- Missing data from that source
- Daily review proceeds with available data
- Error reported in summary

### Level 2: Complete Daily Pull Failure

**What happens:**
- Daily pull script fails completely
- Returns non-zero exit code
- Daily review command catches error

**Example:**
```javascript
try {
  await dailyPull()
} catch (error) {
  console.error('Daily pull failed:', error)
  // Continue with review anyway
  // Note in report that syncs failed
}
```

**User impact:**
- No synced data in daily note
- Daily review proceeds with manual analysis
- User can manually run syncs later

### Level 3: Daily Review Command Failure

**What happens:**
- Review generation fails
- User sees error message
- Daily note may be partially updated

**User impact:**
- Incomplete review
- User can manually complete or retry

## Common Error Scenarios

### Missing API Key

**Symptom:**
```
❌ Notion sync failed: API key not found
```

**Cause:**
- `NOTION_API_KEY` missing from `.claude/secrets.local.json`
- Environment variable not set

**Handling:**
- Skip that sync
- Log clear error message
- Continue with other syncs

**Recovery:**
- User adds API key to secrets
- Re-runs daily pull or daily review

### Network Timeout

**Symptom:**
```
❌ Linear sync failed: Request timeout
```

**Cause:**
- Network issue
- API server slow/unresponsive

**Handling:**
- Retry once (if implemented)
- Skip sync if retry fails
- Continue with other syncs

**Recovery:**
- Usually resolves on next run
- User can manually retry specific sync

### Invalid Database ID

**Symptom:**
```
❌ Notion Personal sync failed: Database not found
```

**Cause:**
- Database ID incorrect in script
- Database deleted or access revoked

**Handling:**
- Skip that sync
- Log error with database ID
- Continue with other syncs

**Recovery:**
- User updates database ID in script
- Or removes that sync from daily pull

### OAuth Token Expired

**Symptom:**
```
❌ Calendar sync failed: Authentication required
```

**Cause:**
- Google OAuth token expired
- Token needs refresh

**Handling:**
- Skip that sync
- Log clear message about re-authentication
- Continue with other syncs

**Recovery:**
- User runs OAuth flow again
- Or uses Rube MCP for interactive access

### Rate Limit Exceeded

**Symptom:**
```
❌ Notion sync failed: Rate limit exceeded
```

**Cause:**
- Too many requests to Notion API
- Multiple databases syncing simultaneously

**Handling:**
- Skip that sync
- Log rate limit error
- Continue with other syncs

**Recovery:**
- Wait and retry later
- Reduce number of databases synced
- Increase delays between requests

## Error Reporting

### In Daily Pull Script

**Summary format:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  Daily Pull complete with 2 error(s):
   - Linear
   - Notion Personal

   Some syncs may have failed. Check the errors above.
```

**What gets logged:**
- Which syncs failed
- Error messages
- Success count

### In Daily Review Report

**Include in report:**
```markdown
## Sync Status

✅ Synced successfully:
- Notion Goals-OS
- Calendar
- Fathom

❌ Syncs failed:
- Linear: API key missing
- Notion Personal: Database not found

⚠️  Review generated with partial data. Some tasks/events may be missing.
```

## Best Practices

### 1. Always Continue

Never stop the entire process because one sync fails. Other syncs may succeed and provide valuable data.

### 2. Clear Error Messages

Log specific, actionable error messages:
- ❌ Bad: "Error occurred"
- ✅ Good: "Linear sync failed: API key not found in secrets.local.json"

### 3. User-Friendly Summaries

Provide clear summary of what succeeded and what failed, with actionable next steps.

### 4. Graceful Degradation

Daily review should work with partial data. Missing some tasks doesn't mean the review is useless.

### 5. Retry Logic (Optional)

For transient errors (network, rate limits), consider retry logic:
- Retry once after delay
- Skip if retry also fails
- Don't retry for permanent errors (missing keys, invalid IDs)

## Testing Error Scenarios

**To test error handling:**

1. **Missing API key:**
   ```bash
   # Temporarily rename secrets file
   mv .claude/secrets.local.json .claude/secrets.local.json.bak
   node .scripts/daily-pull.js
   # Should skip syncs requiring keys, continue with others
   ```

2. **Invalid database ID:**
   ```bash
   # Edit script to use wrong ID
   # Run sync
   # Should fail gracefully, continue with other syncs
   ```

3. **Network timeout:**
   ```bash
   # Disconnect network
   # Run daily pull
   # Should skip network-dependent syncs, continue with local ones
   ```

## Recovery Actions

**After errors, user can:**

1. **Fix and retry:**
   - Add missing API keys
   - Fix database IDs
   - Re-authenticate OAuth

2. **Manual sync:**
   - Run individual sync scripts
   - Use MCP tools directly (Linear, Rube)

3. **Skip problematic syncs:**
   - Use `--skip-*` flags
   - Remove from daily pull if not needed

4. **Proceed with partial data:**
   - Daily review works with available data
   - Missing data can be added manually
