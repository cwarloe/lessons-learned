"""Regression checks for intentionally small, structural traveler guardrails."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_agent_traveler import validate  # noqa: E402


TEMPLATE = (ROOT / "templates/traveler/traveler.md").read_text(encoding="utf-8")


def realistic(*, state="ready_for_review", owner_required="yes", decision="pending"):
    text = TEMPLATE.replace("| State | template |", f"| State | {state} |")
    text = text.replace("| Owner decision required | no |", f"| Owner decision required | {owner_required} |")
    text = text.replace("| Owner decision | not_required |", f"| Owner decision | {decision} |")
    text = text.replace("| Work ID | REPLACE_ME |", "| Work ID | X-001 |")
    text = text.replace("| Repository | REPLACE_ME |", "| Repository | cwarloe/example |")
    text = text.replace("| Current agent/owner | REPLACE_ME |", "| Current agent/owner | agent-one |")
    text = text.replace("| Start / last update (UTC) | REPLACE_ME |", "| Start / last update (UTC) | 2026-11-26 |")
    text = text.replace("| Scope authorization | REPLACE_ME |", "| Scope authorization | approved wave |")
    text = text.replace("**Inspectable outputs:** REPLACE_ME", "**Inspectable outputs:** [PR](https://github.com/example/pull/1)")
    text = text.replace("| REPLACE_ME | REPLACE_ME | REPLACE_ME | not_assessed |", "| smoke | test | [logs](logs/test.txt) | pass |")
    return text


class TravelerValidationTests(unittest.TestCase):
    def test_template_valid_in_template_mode(self):
        self.assertEqual(validate(TEMPLATE, template=True), [])

    def test_template_cannot_be_operational_record(self):
        self.assertTrue(validate(TEMPLATE))

    def test_ready_record_needs_output_and_evidence(self):
        self.assertEqual(validate(realistic()), [])

    def test_missing_acceptance_evidence_fails(self):
        text = realistic().replace("[logs](logs/test.txt)", "no log")
        self.assertTrue(any("linked evidence" in e for e in validate(text)))

    def test_missing_output_fails(self):
        text = realistic().replace("[PR](https://github.com/example/pull/1)", "unavailable")
        self.assertTrue(any("linked inspectable" in e for e in validate(text)))

    def test_owner_required_does_not_complete_without_decision(self):
        self.assertTrue(any("owner-required" in e for e in validate(realistic(state="complete"))))

    def test_owner_required_can_complete_with_recorded_decision(self):
        text = realistic(state="complete", decision="approved")
        text = text.replace("| Owner decision evidence | not_recorded |", "| Owner decision evidence | [owner record](https://example.com/decision) |")
        self.assertEqual(validate(text), [])

    def test_low_risk_no_owner_decision_can_complete(self):
        text = realistic(state="complete", owner_required="no", decision="not_required")
        self.assertEqual(validate(text), [])

    def test_stop_risk_cannot_reach_review(self):
        text = realistic().replace("| Risk tier | low |", "| Risk tier | stop |")
        self.assertTrue(any("Risk tier 'stop'" in e for e in validate(text)))

    def test_blocked_requires_specific_escalation(self):
        text = realistic(state="blocked")
        self.assertTrue(any("recorded blocker" in e for e in validate(text)))
        text = text.replace("**Blocker / escalation:** none_recorded", "**Blocker / escalation:** [CI timeout](https://example.com/run)")
        self.assertEqual(validate(text), [])

    def test_invalid_status_and_missing_section(self):
        text = realistic(state="succeeded").replace("## Owner decision and closeout", "## Other")
        errors = validate(text)
        self.assertTrue(any("invalid State" in e for e in errors))
        self.assertTrue(any("missing section" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
