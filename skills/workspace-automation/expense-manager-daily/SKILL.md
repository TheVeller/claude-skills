---
name: expense-manager-daily
description: Use when logging a reported expense (from an inbox assistant or a bank/receipt email) into a finance database and ledger, or when preparing the daily expenses input draft.
---
# Daily expense logging

## 1. Verify the source email
- Never log on another assistant's word. Open the source email yourself (read-only: never send, archive, label or mark).
- Confirm amount, currency, date and local time (convert UTC headers), merchant or recipient, card or account, operation number, and items if it is a receipt.
- Exclude money received and transfers between the owner's own accounts or cards.
- If a receipt looks like a fee for another order but nothing links them (no order number), write "probably same order, unverified" in Description.

## 2. Dedupe
- External ID: `fin:{source}:{id}`; for email-based rows `fin:gmail:{messageId}`.
- Search the finance database for that External ID, and the ledger CSV for the message id, operation number and merchant, before creating anything. If found, skip.

## 3. Home-currency rule
- Amount is always in the home currency.
- If the email shows the home-currency amount actually charged, use it.
- Otherwise convert at the official selling rate for that date; on weekends or holidays use the last published rate.
- Put the original amount, currency, rate, rate date and source in Description.

## 4. Database row fields
- Copy the field shape from a recent good row of the same kind.
- **Month** and **Year**: relation pages for the expense date. If the month page doesn't exist, leave it empty and ask the owner; don't create it.
- **Bank account**: only when the email names an account that has a page.
- **Payment method**: from the email only (wallet/QR payments = transfer, card charges = credit card). If not shown, leave empty; never guess.
- **Category**: only if clear; anything not confirmed by the owner is marked "tentative" in Description. Person-to-person transfers stay uncategorized until the owner says what they were for.
- Also Status, Type, Document type, Provenance (link to the email), Sync state.

## 5. Ledger backup
- Append one CSV line per expense (date, time, amount, currency, merchant_or_recipient, payment_method, category, note, source, home_amount, fx_rate) and a log line to the status file.

## 6. Tell the owner
- One short message per batch: what was logged with links, what is tentative, and any category or missing-page question. Stay silent if nothing new.

## 7. Daily input draft
- Gather new expenses since the last daily (the whole weekend on Mondays) from the ledger.
- Plain-text draft: header line with date, weekday, timezone and bot name; a legend; an Attention section (unusual or unrecognized charges, uncategorized items, bills due within 3 days, each flagged for the owner); a Cash section (each expense with exact amount and currency, local date and time, merchant, payment method, email link). Mark anything unverified with ⚠️. If nothing is new, one "no new expenses" line.
- Save it as a dated draft file. Send it only through a route the owner approved in their own words; otherwise keep it as a draft and tell the owner once that it didn't go out.
