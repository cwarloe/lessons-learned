# One-page agent traveler

Copy [`traveler.md`](traveler.md) into the relevant repository as one record
per meaningful unit of work. Put the real outputs and reference links at the
top of the page so an owner can inspect them on a phone. Use the companion
[`defect.md`](defect.md) only for substantive failures, not every iteration.

Suggested location: `docs/travelers/<work-id>.md`, unless the repository already
has a QA, release or experiment record. **Extend an existing authoritative
record rather than creating a duplicate tracker.**

The traveler captures state, provenance, scope, acceptance criteria, evidence,
defects, rework, cost and owner authority. It does not assume that every work
item needs approval, nor does an agent's assertion count as owner approval.

Validate the untouched template:

```sh
python3 scripts/check_agent_traveler.py --template templates/traveler/traveler.md
```

Validate an operational copy after replacing every `REPLACE_ME`:

```sh
python3 scripts/check_agent_traveler.py path/to/traveler.md
```

The validator checks only **structure and declared transitions**. It cannot
verify whether a link, cost, reviewer signature or claimed test result is
authentic. Project-specific CI and independent review own those facts.

States: `planned` → `in_progress` → (`blocked` or `ready_for_review`) →
`complete`, with loops to `in_progress` when checks fail. A low-risk task that
requires no owner decision can reach `complete` after verified evidence. A
task that needs an owner decision cannot reach `complete` based on an agent's
own review.

Keep one record even when several agents contribute. The work ID and current
owner identify responsibility; the evidence and failure history survive
handoffs and tool changes.
