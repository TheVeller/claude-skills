---
name: caza-demanda-nucleo
description: Use this when running the daily demand hunt for an automation services brand (Make/n8n, WhatsApp/IG agents, CRM+WhatsApp, training) on freelance marketplaces with lightweight fetch, no browser.
---
# Demand hunt (marketplaces, curl only)

1. Make a dated scratch folder (for example /workspace/cazaMMDD) and reuse the last parser (parse.py) and seen.json (ids already reviewed or reported).
2. Workana: curl the public search pages with a browser user agent, one per keyword: whatsapp, chatbot, agente ia, inteligencia artificial, automatizacion, n8n, make, kommo, hubspot, crm, gohighlevel, manychat, instagram, capacitacion. Parse the embedded results JSON: title, slug, country, budget, proposal count, published time, client rating and verified payment.
3. Freelancer in Spanish: last 48 hours to 7 days by skill (whatsapp, chatbot, n8n, make.com, kommo). Keyword search can ignore the keyword and can silently return 0, so treat 0 as a possible failure.
4. 99Freelas only if the brief is in Spanish or the stack is Make/n8n plus the official WhatsApp API. Reddit blocks curl. n8n.io/jobs is 404; the real board is community.n8n.io/c/jobs/13 and is mostly English For Hire posts.
5. Filter: open, published in the last 7 to 14 days, fewer than 10 proposals, a real business buyer, stack fits the services. Skip sales, closer and setter roles, generic content, product-SaaS builds and how-do-I-learn posts.
6. Score 1 to 5: stack fit, budget, client history (rating, verified payment, recurring), brief quality, home-country bonus. Only 4 or 5 goes out.
7. Check seen.json and memory: never resend a reported or saturated lead without a genuinely new angle.
8. If something qualifies, post one block in the agreed room using formato-hallazgo (signed with the bot name; offer, one link, score, next). If nothing qualifies, send nothing.
9. Log one dated journal line: result (NADA_NUEVO or the finding), closest near-misses with proposal counts and why they failed, and the scratch folder. Close all processes.
