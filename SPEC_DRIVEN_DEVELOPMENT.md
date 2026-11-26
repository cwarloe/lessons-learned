# Spec-Driven Development (SDD)

A lightweight version of the workflow AWS Kiro uses: before building a feature,
agree on **what** (requirements), then **how** (design), then **in what order**
(tasks). Then the code gets written against those three documents.

It is backwards design for software: define success and the acceptance evidence
first, then build toward them.

## When to write a spec

Write a full three-part spec when the extra coordination prevents real rework,
for example when **any** of these applies:

- It spans multiple sessions or agents and the next worker needs an explicit
  shared design rather than the PR description.
- It changes a substantial interface, data model, cross-component behavior,
  or a consequential user-facing workflow.
- The cost or risk of misunderstanding is high enough that a written design
  and traceable acceptance evidence materially reduce rework.

For small, reversible, preauthorized fixes, a clear PR description and
reproducible tests are sufficient even when several files change or the code
has behavior that can be tested. Skip a full spec for one-sitting tweaks, copy
edits, styling fixes, and obvious bugs. Don't retrofit specs for features that
already exist; start with the next real feature that benefits from one.

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
   acceptance criteria in EARS form. For a new consequential product decision,
   Charles approves before design starts. For a previously approved workstream,
   agents may continue routine implementation without repeated approvals as
   long as they stay inside its explicit authority and risk boundaries.
2. **Design** (`design.md`). Components, data, flow, error handling, and how
   each requirement will be tested. Obtain owner approval when the design
   changes a consequential decision or exceeds the approved scope; for
   preauthorized low-risk work, independent agent review and tests can verify
   the design without another owner approval ceremony.
3. **Tasks** (`tasks.md`). Small checkbox steps, each tied to requirement IDs.
   Parallel agents may work independent tasks at once when file ownership and
   integration are clear. Check each task off with the commit that completes it.
4. **Verify**. Every acceptance criterion maps to a passing test or a named
   manual check. Mark the spec `Status: Done`.

If a requirement changes mid-build, edit `requirements.md` first, then update
design and tasks to match. The spec stays the source of truth.

For work crossing several agents or sessions, the optional
[agent traveler](templates/traveler/README.md) can link the acceptance evidence,
defects and decision status. Do not duplicate an existing repo QA record.
`ready_for_review` is not `complete`: a passing CI check cannot replace a
required owner decision.

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
