---
name: no-dev
description: Explain technical things to a non-developer — purpose first, plain language, short. Use when the user says "explica para no dev", "/no-dev", "explain simply", "wtf", "explica más simple", "no entiendo", or when a previous explanation drowned them in implementation detail.
---

# No-Dev

Explain the thing so someone who does not write code can decide what to do about it.

## The failure this fixes

A technical explanation defaults to **how**: files, functions, layers, response shapes. That is
the right level for another engineer and the wrong level for the person paying for the outcome.

They do not need to follow the mechanism. They need to answer one of three questions:

- Should I approve this?
- Should I worry about this?
- What do I get when it is done?

If your explanation does not help with one of those, it was decoration.

## The shape

Four beats, in this order. Usually under 150 words total.

**1 · Purpose — what this thing is FOR.** Not what it is. What job it does in their life.
> *"Your vault has little programs that fetch your email, calendar and contacts."*

**2 · What actually happened.** The event, in cause-and-effect. Include the human consequence,
not the error message.
> *"The middleman they called shut down in July. Nobody told the programs, so they've been
> calling a dead number for 26 days."*

**3 · What you're going to do.** Numbered, 2-4 items, each one a visible outcome.

**4 · Risk and result.** What could go wrong, and what they'll notice when it works.
> *"Low risk. Tomorrow at 7am your daily sync stops failing and starts bringing real data."*

Then the decision: *"Shall I go ahead?"*

## Rules

**Analogy from ordinary life, not from computing.** A phone number, a mailbox, a spare key,
a middleman. Never "it's basically a hash map."

**One analogy per explanation.** Two is where it starts lying.

**If you must name a tool, cash it out immediately.** `Composio` → "the service that actually
talks to Gmail." Never leave a proper noun standing alone as if it explained itself.

**Show a real value if you have one.** People trust a timestamp they can read more than a
sentence about timestamps. One short block, not a dump.

**Delete every number that does not change the decision.** "3 files" matters if you're asking
permission to touch 3 files. "745 lines" almost never matters.

**Lead with the conclusion.** They can stop reading after the first line and still be right.

## Do not

| Don't | Because |
|---|---|
| Explain the mechanism to justify the effort | It reads as asking for credit, not for a decision |
| Apologise for simplifying | Simplifying *is* the job |
| Say "basically" or "essentially" | Filler that signals you're about to be vague |
| Keep the internal names of things | `requestViaRube` means nothing; "where it calls out" does |
| Hedge every claim | If it's uncertain, say so once, plainly |
| Write more when they asked for less | Being asked twice to shorten means you already failed once |

## Calibrate to what they asked

| They said | Give them |
|---|---|
| "explica para no dev" | The four beats |
| "wtf" / "explica breve" | Purpose + what happened + the ask. Skip the rest |
| "explica más" *after* a simple version | They want depth on ONE part — ask which, or pick the part that changes their decision |

## When plain language is not the right call

Say so, briefly, then simplify anyway:

- **Irreversible or destructive actions.** Name the specific thing being destroyed. "Deletes
  your notes from March" beats "cleans up old data."
- **Security and money.** Do not soften. Exact scope, exact exposure.
- **When they will have to maintain it themselves.** They need the real names then, or they
  cannot search for help later.

## Example

> Your vault has little programs that go fetch your email, calendar and contacts.
>
> To do it, they called a middleman called **Rube**. Rube shut down on July 4th. Nobody told
> the programs, so they've spent 26 days calling a disconnected number — and since nothing was
> running on a schedule, nobody noticed.
>
> **What I found:** Rube wasn't doing the work, it was passing the message to **Composio** —
> which is still running, already connected to your accounts, and speaks the exact same
> language back.
>
> So nothing needs rewriting. They just need a new number to call.
>
> **What I'll do:** ① a small new file that knows how to talk to Composio ② change the one
> line in each of the 3 broken programs ③ make failures say *what* broke — right now they just
> say "error", which is why this went unnoticed for a month.
>
> **Risk:** low. I'm touching who they call, not what they do with the answer.
> **Result:** tomorrow at 7am your daily sync stops failing.
>
> Shall I go?

Note what is absent: no file paths, no function names, no response formats, no line counts.
The one number that survived — 3 programs — is there because it sizes the permission being asked for.
