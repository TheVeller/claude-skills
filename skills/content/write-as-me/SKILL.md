---
name: write-as-me
description: >-
  Mandatory pipeline for any user-facing writing as the user (LinkedIn, email,
  Slack, DMs, docs, posts). Runs me then verify-me before delivery.
---
Standing rule: every user-facing draft (LinkedIn, email, Slack, DMs, docs, posts, customer messages, anywhere) passes both me and verify-me before delivery.

Exempt: casual in-chat replies to the user inside Grok Bot that are not meant to be copied out or sent.

## Pipeline (do not skip)
1. Draft with me. Read the user's voice style notes, unslop notes, and at least two corpus samples from their my-voice folder. Write in their voice. Unslop on the same pass.
2. Prove with verify-me. Write draft to a verify folder. Doctor then all five features then REPORT. On FAIL: rewrite (max 2 loops) and re-verify.
3. Deliver only the verified body (or Slack/email draft content). No "here's a version in your voice" preamble. Keep REPORT in artifacts.

## Surfaces
LinkedIn posts/comments, email bodies/subjects, Slack messages/threads, WhatsApp/iMessage drafts, Notion/docs meant for others, talk tracks they will speak from if they asked for them in their voice, any "write this as me" ask.

## Conflict
Corpus > unslop > polish. Their spoken quirks beat sterile clean English.
