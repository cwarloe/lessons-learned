# A lightweight production line for agent work

This is a **pattern library**, not a mandatory platform or a new project-management
system. Start with one meaningful unit of work and a [one-page traveler](templates/traveler/README.md).
The same principles apply to a software fix, a customer-validation experiment, a
training lesson, or an instructional video, but each project chooses its own
acceptance evidence.

## Standard work: six stages

| Stage | Produce | Gate | Avoid |
| --- | --- | --- | --- |
| Sort | One outcome and a bounded unit of work | Duplicate/obsolete work removed from scope | A second backlog |
| Set in order | Input provenance, an owner, existing instructions and dependencies | Exact source and constraints identified | Untraceable copies |
| Shine | A quick failure-mode scan and a small, reproducible check | Known blockers and unsafe assumptions visible | Waiting for defects to recur |
| Standardize | Acceptance criteria, a traveler and a reproducible test | Another agent can repeat the check | One-off chat instructions |
| Sustain | Defects, countermeasures, rework and result recorded | Corrective action checked in the next run | Forgotten lessons |
| Safety | Explicit authority, privacy, cost and external-effect boundaries | Stop the line on material uncertainty | Treating a green build as approval |

The six rows are a practical 6S adaptation; they need not become six meetings.
Keep **at most two active items per agent** unless the repo documents a different
limit. Move an item to `blocked` when an external condition truly prevents
progress; continue other non-conflicting items within the approved scope.

## Authority: keep work moving without manufacturing approvals

| Work class | Agent may do autonomously under an approved workstream | Owner decision still needed |
| --- | --- | --- |
| Reversible internal engineering | Diagnose, change, test, document, open and merge a green low-risk PR when authorized | Unexpected cost, broad deletion, a protected branch, material security changes |
| Research and experiments | Collect sources, plan tests, document assumptions and unsuccessful attempts | Spending, external outreach, disclosure of confidential material, choosing a business direction |
| Training, creative and instructional content | Draft variants, run structural checks, prepare review artifacts | Publish consequential content, certify effectiveness, accept final media or theological claims |
| Live customer/participant workflows | Use synthetic data and propose measured improvements | Access to real private data, consent terms, communications or public launch |

Specific repository instructions, existing PR hold statements and the user's
current directions take precedence over this guide. A preapproved workstream
can authorize routine work without a fresh sign-off for every subtask. It never
creates consent for a separate high-impact action. A tool requiring human
approval is a stop condition, not a reason to bypass protection.

### Stop-the-line / Andon triggers

- Source instructions, owner decisions or quality references conflict.
- A test proves the result is unsafe, materially wrong, or unreproducible.
- A privacy, identity, security, legal, financial or theological judgment is
  needed beyond the delegated scope.
- Paid calls would cross a cap, rates are unknown, or credentials are missing.
- An agent has only its *own assertion* of human review or quality approval.
- A PR touches another worker's branch or a protected workflow unexpectedly.

Record the blocker, evidence and the **specific decision** needed. Do not mark
the work `complete`, work around access controls or ask the owner to perform
routine technical steps that an authorized agent can finish.

## Traveler and measurable feedback

The [template](templates/traveler/traveler.md) is one human-readable page. It
links **outputs first**, then high-resolution/reference artifacts, acceptance
checks, observed defects and the owner decision if required. The
[defect record](templates/traveler/defect.md) captures the failure *and* the
preventive control; after the same defect recurs twice, escalate the control
method rather than blindly retrying the same prompt or build.

Suggested measures, never fabricated: first-pass acceptance, attempts to pass,
rework time, lead time, paid credits, actual dollar cost, and repeated defect
rate. Keep `unknown`, `not_measured`, `not_applicable` and `0` distinct. A
single successful test is not evidence of statistical process capability.

## Verification and continuous improvement

1. Start with the existing test command and standard work; don't add a new CI
   workflow when an existing one can safely host the check.
2. Record a baseline before claiming an improvement. Compare comparable
   inputs, versions, quality rubrics and denominators.
3. Pair automated checks (links, data schema, provenance, repeatability) with
   explicitly independent human judgment where form, meaning, theology or
   customer value cannot be proven by code.
4. Ship small changes with their test evidence. Keep rejected attempts and
   hypotheses separate from validated causes.
5. Review recurring failures before introducing more automation or ceremony.

This is intentionally smaller than a Scrum program. The goal is trustworthy
throughput, not more meetings or paperwork.
