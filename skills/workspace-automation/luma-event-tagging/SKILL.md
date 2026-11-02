---
name: luma-event-tagging
description: Use this when tagging people in a Luma calendar's People list by the events they attended (Going or checked in), adding only missing tags.
---
# Luma event tagging

Tag each person in a Luma calendar's People list with the tags of every event where they were Going or Checked in. Only add missing tags.

## 1. Map events to tags
- Inventory the calendar's existing tags first.
- For each event: city and country tags only if in-person; a format tag (IRL Workshops, Hacks, Online Hack, Online Workshops); a tool or topic tag (fall back to keywords from the title).
- Keep the event-to-tags map in a plan file. Create a new tag only for a justified new region or tool, and only if the owner allowed it.

## 2. Per event
1. Open the event guest list and save the Going and Checked-in emails to going-EVENT.txt. Ignore Invited, Waitlist and Not Going.
2. Build the pending list with `comm -23` of the going list against the emails already done.
3. In People: clear the search, type the email key by key, open the person, click the existing tags that are missing. Never press Enter in the tag box. Log `email | tagged/already/not found | tags` to res-EVENT.log.
4. Every 20 people or so, check that two known contacts still show up in search.

## 3. Untagged people
Try the full People export first (Luma may email a code). Otherwise go profile by profile: for each qualifying event, apply its tags. If an event is not mapped, decide its tags from the event page, add them to the map and apply. No qualifying event means no tag; log it as "sin evento".

## 4. Imports (only if the owner authorized this route)
Export the event guest CSV, keep only approved guests, and import them into People with the event tags. Test first with a small event that the import keeps tags and sends no emails.

## 5. Limits and closing
- Never remove tags (except undoing your own mis-click), change memberships, edit events, or send anything.
- One window, one tab. When done, quit the browser from your own screen with the menu Exit option; never kill browser processes on a shared computer.
- Report each run: X of Y, what is left, what is blocked. Stay silent if nothing moved.
