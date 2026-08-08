---
name: dev-journey
description: Write an exhaustive, warts-and-all development journey document for a build session — every detail from the user's initial prompt to the finished product, including design decisions, tools, tech stack, architecture, agents used, problems and fixes, near-misses, costs and limits hit, and unfinished work with explanations. Use whenever the user says "development journey", "dev journey", "document this session", "write up how you built this", "session retrospective", "postmortem of this build", or asks to capture how a piece of work happened. ALSO offer it proactively (one line, no nagging) at the natural end of any substantial multi-step build session — a design, a deploy, a pipeline, an investigation — because the session transcript is the only complete source and it will be summarized away.
---

# Development Journey Documents

A journey doc is the story of one build session told twice at once: readable as a
public warts-and-all narrative, and precise enough that a future agent (or the
user in six months) could reproduce, resume, or audit the work. Both audiences
read the same document — never split it in two.

The failures are the product. A journey doc that reads as a victory lap is a
failed journey doc. What makes these documents worth writing is exactly the
material a polished README omits: the dead ends, the wrong conclusions almost
drawn, the rate limit that killed the last feature, the schema mismatch that
cost three retries. Readers learn from the potholes, not the freshly paved road.

## Timing: mine the transcript while it exists

The session conversation is the primary source, and it is perishable — context
gets summarized, scratchpads get wiped, screenshots go stale. Write the doc at
the end of the session that did the work, from the live transcript, not later
from memory. If asked to document a *past* session, say plainly which sections
are reconstructed and from what evidence (git history, memory files, artifacts)
— reconstruction is fine, silent reconstruction is not.

Before writing, sweep the transcript chronologically and collect: every tool
that was called and why, every error message verbatim, every decision point,
every user message. The doc is written from this sweep, not from your summary
memory of the session — summary memory has already dropped the warts.

## Document structure

Use numbered sections. This exact skeleton has worked across real projects;
keep the bones, adapt the flesh to the session:

```markdown
# Development Journey — "<Deliverable Name>" <one-phrase context>

**Date:** YYYY-MM-DD
**Deliverable:** <URL or path — the thing itself, not a description of it>
**Brief:** "<the user's initial prompt, quoted verbatim>"
**Final render/artifact:** <file in repo, if visual>

## 1. The brief — <what was actually being asked>
## 2. <Setup / cold start / reconnection — how the session got to a working state>
## 3. Design decisions
## 4. <The core problem of this session — its own named section>
## 5. Tools and features used  (table: tool → what it did THIS session)
## 6. What went wrong, and the fixes  (numbered; verbatim error text)
## 7. Verification
## 8. Where things stand
```

Sections 4's title should name the session's actual crux ("The texture
problem", "The auth dance", "Getting the stream to resume") — every real
session has one, and finding it is most of the writing work.

## Completeness checklist — including what nobody thinks to ask for

The user's request will name the obvious topics (decisions, tools, problems).
These are the topics that get silently dropped; walk the full list every time
and include every line that applies. It is a checklist, not a table of
contents — most items become a sentence or two inside the sections above.

**Origin**
- The initial prompt, quoted verbatim, plus how you interpreted it and any
  ambiguity you resolved silently (the reader can't see your thinking).
- Invisible constraints that shaped the output: active style modes, house
  style guides loaded (`get_guide`-type content), standing user rules,
  skills invoked. The reader can't know a minimalism mode was on unless told.

**Starting context**
- Environment state at minute zero: what was installed/running/dead, what a
  probe returned, what had to be launched.
- What was *reused* instead of re-derived: memory files, handoff docs, prior
  clients/scripts. Name them — that reuse is a finding about process.

**Decisions**
- For each significant decision: the options considered, the one chosen, and
  *why the others lost*. A decision without its rejected alternatives is a
  fact, not a decision.
- First instincts deliberately overridden, and what rule/reason overrode them.
- Descoped and YAGNI-cut items: what was deliberately NOT built and why.
  Absence reads as oversight unless documented as choice.

**Tech stack and architecture**
- Languages, libraries, protocols, APIs, versions where they mattered.
- The shape of the thing: how the pieces talk (a client → local server →
  canvas pipeline; a generator script → SVG → design nodes). If data flows,
  describe the flow.
- Bundled/generated code: where the load-bearing scripts live now.

**Agents and AI machinery**
- Subagents spawned and what each did; advisor consultations and whether the
  advice changed the plan (say what it changed); model and any relevant
  settings. If none: one line saying the work was done inline.

**Human-in-the-loop moments**
- Every point where the user had to act (auth, approvals, live corrections,
  answers to questions) — these are invisible in the artifact but essential
  to reproduce the session.

**Problems, near-misses, and fragility**
- Every failure with its error text verbatim and the fix that worked.
- Near-misses: wrong conclusions *almost* drawn and what saved you (the
  stale screenshot that nearly "proved" rendering was broken). These teach
  more than clean failures.
- Fragility and luck: things that worked but might not again (timing-
  dependent renders, undocumented behavior, free-tier quirks). Label them.

**Costs and limits**
- Quotas, rate limits, credits, plan ceilings — hit or merely approached.
  Include the reset date if known. Money and limits are exactly the detail a
  future session needs and never has.
- Rough wall-clock where meaningful ("~12s app launch", "2s render lag").

**Verification**
- How each "it works" claim was actually checked — observed effects
  (screenshots, HTTP codes, file listings, live URLs), never a clean exit.
- What was NOT verified and why (couldn't, ran out of quota, didn't matter).

**Unfinished business**
- Every incomplete item with its explanation: what's missing, why it
  stopped, what unblocks it, and whether the deliverable stands without it.
  "The footer never landed; the design stands without it" beats silence.

**Knowledge captured**
- Which durable stores were updated (memory files, HANDOFF, README) and
  what went into each — so the next reader knows where else to look.

**Where things stand**
- Live links to the deliverable. Blocked-until dates. Concrete next steps
  as options, not promises.

## Style

- Full prose, short sentences, active voice. Section headings for
  navigation; tables only for enumerable facts (tool → use).
- Every identifier exact: file paths, URLs, error strings, hex values,
  version numbers, port numbers, tool parameter names. A simplified
  identifier is a wrong identifier.
- Honest register: no self-congratulation, no hedging away failures. Write
  "Wrong conclusion nearly drawn from a lagging screenshot" — not "some
  minor rendering inconsistencies were observed."
- Distill rules learned into quotable one-liners at the point where they
  were learned: "probe the port, do not trust 'the window is visible'";
  "read the tool schema before the first call, not after the error."
- Length follows content: a rich session earns 150+ lines. Do not pad a
  thin session — a short honest doc beats a long inflated one.

## File and repo conventions

- Name docs `DEVELOPMENT-JOURNEY.md`, then `DEVELOPMENT-JOURNEY-2.md`, `-3`…
  — one doc per deliverable/session, never overwrite a predecessor. Follow
  the project's existing convention if one exists.
- Copy final renders/artifacts out of session-transient scratchpads into the
  project folder and reference them from the doc — scratchpads die with the
  session.
- If the project is a git repo, commit the doc (and renders) after writing;
  push if a remote exists. If a HANDOFF or README exists and the doc makes
  it stale, update it in the same commit.

## Proactive offering

At the natural end of a substantial multi-step build session (something was
created, deployed, investigated, or fixed across many tool calls), offer once,
in one line, alongside the final summary: "Want a development journey doc for
this session?" Do not offer for trivial sessions, do not repeat the offer, and
do not write the doc unprompted.
