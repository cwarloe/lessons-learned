# Spec-Driven Development (SDD)

A lightweight version of the workflow AWS Kiro uses: before building a feature,
agree on **what** (requirements), then **how** (design), then **in what order**
(tasks). Then the code gets written against those three documents.

It is backwards design for software: define success and the acceptance evidence
first, then build toward them.

## When to write a spec

Write one when a change meets **any** of these:

- It will take more than one sitting (an agent or future-you must resume it).
- It touches several files or more than one part of the app.
- It has behavior you could write a test for.

Skip it when the change is a one-sitting tweak, copy edit, styling fix, or bug
with an obvious cause. Don't retrofit specs for features that already exist;
start with the next real feature.

## Which repos use it

| Tier | Repos | What they get |
|---|---|---|
| Full | subscription-manager, deckbench, sideline-rugby, 5bx-video-game, record-your-story, Bible-Reader | A `specs/` folder; one spec per qualifying feature |
| Lite | 5BX, classic-games-portal, pptx-slides-to-markdown, mynetworkmaps, dnp3-training, daily-bible-reading, Colonial-News | A short steering section in `CLAUDE.md` only; no specs |
| Already covered | mr-life-manager, learning-narrative-kit, novel-builder, stewardship-curriculum, network-analyst-development-framework | Nothing new; their decision logs and agent files already do this job |
| Skip | content, concept, and stub repos | Nothing |

Revisit a repo's tier if it grows (a Lite repo that starts getting multi-day
features moves to Full).

## Workflow

1. **Requirements** (`specs/<feature>/requirements.md`). User stories plus
   acceptance criteria in EARS form. Charles approves before design starts.
2. **Design** (`design.md`). Components, data, flow, error handling, and how
   each requirement will be tested. Approve before tasks.
3. **Tasks** (`tasks.md`). Small checkbox steps, each tied to requirement IDs.
   One task at a time; check it off in the same commit that completes it.
4. **Verify**. Every acceptance criterion maps to a passing test or a named
   manual check. Mark the spec `Status: Done`.

If a requirement changes mid-build, edit `requirements.md` first, then update
design and tasks to match. The spec stays the source of truth.

## EARS cheat sheet

EARS (Easy Approach to Requirements Syntax) keeps criteria testable:

| Pattern | Form |
|---|---|
| Always | THE SYSTEM SHALL `<response>` |
| Event | WHEN `<trigger>` THE SYSTEM SHALL `<response>` |
| State | WHILE `<state>` THE SYSTEM SHALL `<response>` |
| Unwanted | IF `<condition>` THEN THE SYSTEM SHALL `<response>` |
| Optional | WHERE `<feature is enabled>` THE SYSTEM SHALL `<response>` |

Test for a good criterion: could someone who has never seen the app tell
whether it passed?

## Setting up a Full-tier repo

1. Copy `templates/spec/` to `specs/_template/` in the repo.
2. Add the section in `templates/steering/CLAUDE-spec-section.md` to the repo's
   `CLAUDE.md` (or `AGENTS.md` if that is the repo's agent file).
3. For a feature: copy `specs/_template/` to `specs/<feature-slug>/` and start
   with requirements.

Folder note: Kiro itself uses `.kiro/specs/`. These repos use a visible
`specs/` folder so the files are easy to find on GitHub mobile. Rename the
folder if you ever adopt Kiro.
