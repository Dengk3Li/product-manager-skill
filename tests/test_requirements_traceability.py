from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "skills/product-requirements/scripts/check_requirements_traceability.py"


def valid_model() -> dict:
    return {
        "product": "Checkout",
        "baseline": {
            "id": "checkout-v1",
            "status": "APPROVED",
            "requirement_ids": ["BO-001", "PR-001", "EN-001"],
            "approval_evidence": [
                {"type": "HUMAN_APPROVAL", "ref": "product-review-2026-09-03"}
            ],
        },
        "release_acceptance": {
            "status": "PENDING",
            "evidence": [],
        },
        "requirements": [
            {
                "id": "BO-001",
                "type": "business_outcome",
                "title": "Increase completed purchases",
                "parent_id": None,
                "supports": [],
                "materiality": "MATERIAL",
                "decision_required": False,
                "acceptance_required": True,
                "delivery_status": "IN_PROGRESS",
                "verification_status": "NOT_VERIFIED",
                "acceptance_criteria": ["Completion rate is measured"],
                "evidence": [],
            },
            {
                "id": "PR-001",
                "type": "product_requirement",
                "title": "Support guest checkout",
                "parent_id": "BO-001",
                "supports": ["BO-001"],
                "materiality": "MATERIAL",
                "decision_required": False,
                "acceptance_required": True,
                "delivery_status": "IMPLEMENTED",
                "verification_status": "PASS",
                "acceptance_criteria": ["A guest can place an order"],
                "architecture_refs": ["checkout"],
                "evidence": [
                    {"type": "TEST_RESULT", "ref": "tests/guest-checkout"}
                ],
            },
            {
                "id": "EN-001",
                "type": "enabler",
                "title": "Persist guest cart identity",
                "parent_id": "PR-001",
                "supports": ["PR-001"],
                "materiality": "SUPPORTING",
                "decision_required": False,
                "acceptance_required": False,
                "delivery_status": "NOT_STARTED",
                "verification_status": "NOT_VERIFIED",
                "evidence": [],
            },
        ],
    }


class RequirementsTraceabilityTest(unittest.TestCase):
    def run_checker(self, payload: dict, phase: str = "report") -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            model = Path(temp_dir) / "requirements.json"
            model.write_text(json.dumps(payload), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(CHECKER), str(model), "--phase", phase],
                text=True,
                capture_output=True,
                check=False,
            )

    def test_approved_baseline_covers_requirements_with_one_human_decision(self) -> None:
        result = self.run_checker(valid_model(), "align")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS phase=align requirements=3 blockers=0", result.stdout)

    def test_enabler_must_support_another_requirement(self) -> None:
        payload = valid_model()
        payload["requirements"][2]["supports"] = []
        result = self.run_checker(payload)
        self.assertEqual(result.returncode, 2)
        self.assertIn("enabler must support", result.stderr)

    def test_requirement_hierarchy_must_be_cycle_free(self) -> None:
        payload = valid_model()
        payload["requirements"][0]["parent_id"] = "PR-001"
        result = self.run_checker(payload)
        self.assertEqual(result.returncode, 2)
        self.assertIn("cycle", result.stderr)

    def test_support_relationships_must_be_cycle_free(self) -> None:
        payload = valid_model()
        payload["requirements"][1]["supports"] = ["EN-001"]
        result = self.run_checker(payload)
        self.assertEqual(result.returncode, 2)
        self.assertIn("support relationships contain a cycle", result.stderr)

    def test_ai_proposal_cannot_approve_the_baseline(self) -> None:
        payload = valid_model()
        payload["baseline"]["approval_evidence"] = [
            {"type": "AI_PROPOSAL", "ref": "generated PRD"}
        ]
        result = self.run_checker(payload, "align")
        self.assertEqual(result.returncode, 2)
        self.assertIn("baseline approval requires one human decision", result.stderr)

    def test_unresolved_explicit_human_decision_blocks_alignment(self) -> None:
        payload = valid_model()
        payload["requirements"][1]["decision_required"] = True
        payload["requirements"][1]["decision_status"] = "OPEN"
        result = self.run_checker(payload, "align")
        self.assertEqual(result.returncode, 2)
        self.assertIn("required product decision is still open", result.stderr)

    def test_missing_implementation_evidence_warns_without_blocking_delivery(self) -> None:
        payload = valid_model()
        payload["requirements"][1]["evidence"] = [
            {"type": "AI_PROPOSAL", "ref": "generated implementation summary"}
        ]
        result = self.run_checker(payload, "delivery")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN: PR-001: implemented requirement lacks primary implementation evidence", result.stdout)

    def test_incomplete_blocker_warns_without_stopping_other_work(self) -> None:
        payload = valid_model()
        payload["requirements"][2]["delivery_status"] = "BLOCKED"
        result = self.run_checker(payload, "delivery")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN: EN-001: blocker lacks reason, owner, or next_action", result.stdout)

    def test_acceptance_blocks_only_unverified_required_outcomes(self) -> None:
        payload = valid_model()
        payload["requirements"][0]["verification_status"] = "PASS"
        payload["requirements"][0]["evidence"] = [
            {"type": "RUNTIME_OBSERVATION", "ref": "checkout-metric-dashboard"}
        ]
        payload["release_acceptance"] = {
            "status": "ACCEPTED",
            "evidence": [{"type": "HUMAN_ACCEPTANCE", "ref": "release-review"}],
        }
        result = self.run_checker(payload, "acceptance")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("accepted=1", result.stdout)

    def test_acceptance_does_not_require_human_review_for_each_enabler(self) -> None:
        payload = valid_model()
        payload["requirements"][0]["verification_status"] = "PASS"
        payload["requirements"][0]["evidence"] = [
            {"type": "RUNTIME_OBSERVATION", "ref": "checkout-metric-dashboard"}
        ]
        payload["release_acceptance"] = {
            "status": "ACCEPTED",
            "evidence": [{"type": "HUMAN_ACCEPTANCE", "ref": "release-review"}],
        }
        result = self.run_checker(payload, "acceptance")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("EN-001", result.stderr)

    def test_acceptance_requires_one_human_release_decision(self) -> None:
        payload = valid_model()
        payload["requirements"][0]["verification_status"] = "PASS"
        payload["requirements"][0]["evidence"] = [
            {"type": "RUNTIME_OBSERVATION", "ref": "checkout-metric-dashboard"}
        ]
        payload["release_acceptance"] = {"status": "ACCEPTED", "evidence": []}
        result = self.run_checker(payload, "acceptance")
        self.assertEqual(result.returncode, 2)
        self.assertIn("release acceptance requires one human decision", result.stderr)


if __name__ == "__main__":
    unittest.main()
