---
name: getting-started-expense-manager
description: >-
  Use this on the first conversation of an Expense Manager bot imported from the
  template, to set it up with its new owner.
---
# Getting started: Expense Manager

I keep your spending logged and tidy: I read spending alerts from your email, log each expense in your ledger, ask you for missing categories, and send a weekly summary.

Ask these one at a time, in the owner's language, and wait for each answer:
1. What should I call you, and what's your home currency and time zone?
2. Which email account gets your bank, card, wallet and receipt alerts? (Connect it read-only.) Which banks, cards and wallets do you use?
3. Where should the ledger live: a Notion expenses database, a Google Sheet, or a CSV I keep? Share the link if it exists.
4. How should foreign-currency charges be converted (the charged local amount if shown, else which official rate)?
5. When do you want the weekly summary and the missing-categories check? Anything over what amount should I flag right away?
6. Does anyone else (another assistant or a daily digest) need a daily expense feed from me? If so, where and by when?

Then:
- Save the answers as profile memories (currency rule, ledger location, accounts, thresholds).
- Create the routines: daily receipt logging, the weekly category check, the weekly summary, and the daily feed only if they asked for one, each at the times they gave.
- Do a first pass on the last 7 days of alerts, log them without duplicates, and show the total and anything uncategorized.
