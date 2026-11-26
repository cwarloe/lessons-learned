#!/usr/bin/env python3
"""Structural guardrails for a single Markdown agent traveler (stdlib only).

These checks intentionally cannot attest that a link or reviewer claim is true.
Project-specific evidence validation and independent review remain mandatory.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SECTIONS = (
    "Outputs and reference artifacts",
    "Work order and provenance",
    "Acceptance criteria and verification evidence",
    "Execution, defects and countermeasures",
    "Owner decision and closeout",
)
FIELDS = (
    "Work ID",
    "Repository",
    "Current agent/owner",
    "State",
    "Risk tier",
    "Owner decision required",
    "Owner decision",
    "Owner decision evidence",
    "Start / last update (UTC)",
    "Scope authorization",
    "Cost (actual USD / credits)",
)
STATES = {"template", "planned", "in_progress", "blocked", "ready_for_review", "complete"}
RISKS = {"low", "review_required", "stop"}
DECISIONS = {"pending", "not_required", "approved", "rejected"}
LINK = re.compile(r"\[[^\]\n]+\]\(([^)]+)\)")


def _field_rows(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        match = re.fullmatch(r"\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", line)
        if match:
            fields[match.group(1).strip()] = match.group(2).strip()
    return fields


def _section(text: str, heading: str) -> str:
    pattern = rf"(?m)^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, re.DOTALL | re.MULTILINE)
    return match.group(1) if match else ""


def _real_link(value: str) -> bool:
    return any(
        target.strip() and "REPLACE_ME" not in target and not target.startswith("#")
        for target in LINK.findall(value)
    )


def validate(text: str, *, template: bool = False) -> list[str]:
    errors: list[str] = []
    fields = _field_rows(text)
    for heading in SECTIONS:
        if not re.search(rf"(?m)^## {re.escape(heading)}\s*$", text):
            errors.append(f"missing section: {heading}")
    for name in FIELDS:
        if not fields.get(name):
            errors.append(f"missing field: {name}")

    state = fields.get("State", "")
    risk = fields.get("Risk tier", "")
    owner_required = fields.get("Owner decision required", "")
    decision = fields.get("Owner decision", "")
    if state not in STATES:
        errors.append(f"invalid State: {state!r}")
    if risk not in RISKS:
        errors.append(f"invalid Risk tier: {risk!r}")
    if owner_required not in {"yes", "no"}:
        errors.append(f"invalid Owner decision required: {owner_required!r}")
    if decision not in DECISIONS:
        errors.append(f"invalid Owner decision: {decision!r}")

    if template:
        if state != "template":
            errors.append("--template expects State 'template'")
        return errors
    if state == "template":
        errors.append("operational traveler cannot remain in template state")

    for name in (
        "Work ID", "Repository", "Current agent/owner", "Start / last update (UTC)",
        "Scope authorization",
    ):
        if not fields.get(name) or "REPLACE_ME" in fields[name]:
            errors.append(f"replace placeholder in {name}")
    if risk == "stop" and state not in {"planned", "blocked"}:
        errors.append("Risk tier 'stop' cannot advance until a new authorized risk assessment")
    if state == "blocked":
        log = _section(text, "Execution, defects and countermeasures")
        item = re.search(r"(?m)^- \*\*Blocker / escalation:\*\* (.+)$", log)
        if not item or item.group(1).strip() in {"none_recorded", "REPLACE_ME", ""}:
            errors.append("blocked state requires a recorded blocker/escalation")
    if state in {"ready_for_review", "complete"}:
        outputs = _section(text, "Outputs and reference artifacts")
        checks = _section(text, "Acceptance criteria and verification evidence")
        if not _real_link(outputs):
            errors.append("ready/complete requires a linked inspectable output")
        if not _real_link(checks) or "REPLACE_ME" in checks:
            errors.append("ready/complete requires filled acceptance checks and linked evidence")
        if "| pass |" not in checks.lower():
            errors.append("ready/complete requires at least one recorded passing acceptance check")
    if state == "complete":
        if owner_required == "yes":
            if decision != "approved" or not _real_link(fields.get("Owner decision evidence", "")):
                errors.append("owner-required completion needs approved verdict and independent decision evidence")
        elif owner_required == "no" and decision != "not_required":
            errors.append("non-owner completion requires Owner decision 'not_required'")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", action="store_true", help="validate reusable template only")
    parser.add_argument("paths", type=Path, nargs="+")
    args = parser.parse_args(argv)
    has_errors = False
    for path in args.paths:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            print(f"{path}: cannot read: {exc}", file=sys.stderr)
            has_errors = True
            continue
        errors = validate(text, template=args.template)
        if errors:
            has_errors = True
            for error in errors:
                print(f"{path}: {error}", file=sys.stderr)
        else:
            print(f"{path}: structural check passed (not substantive review)")
    return 1 if has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
