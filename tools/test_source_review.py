from __future__ import annotations

import unittest

from scripts.source_review import diff_institutions, render_markdown_report


class SourceReviewTest(unittest.TestCase):
    def test_reports_added_removed_and_changed_institutions(self) -> None:
        current = [
            {"code": "00001", "rawCode": "0001", "nameOfficial": "One"},
            {"code": "00002", "rawCode": "0002", "nameOfficial": "Two"},
        ]
        candidate = [
            {"code": "00002", "rawCode": "0002", "nameOfficial": "Two Updated"},
            {"code": "00003", "rawCode": "0003", "nameOfficial": "Three"},
        ]

        changes = diff_institutions(current, candidate)

        self.assertEqual([item["code"] for item in changes["added"]], ["00003"])
        self.assertEqual([item["code"] for item in changes["removed"]], ["00001"])
        self.assertEqual([item["code"] for item in changes["changed"]], ["00002"])
        self.assertEqual(changes["changed"][0]["before"]["nameOfficial"], "Two")
        self.assertEqual(changes["changed"][0]["after"]["nameOfficial"], "Two Updated")

    def test_markdown_report_requires_human_review(self) -> None:
        report = {
            "checkedAt": "2026-07-31",
            "requiresHumanReview": True,
            "sourceChanges": [{"id": "source", "status": "changed"}],
            "institutionChanges": {
                "added": [{"code": "00003", "rawCode": "0003", "nameOfficial": "Three"}],
                "removed": [],
                "changed": [],
            },
            "errors": [],
        }

        markdown = render_markdown_report(report)

        self.assertIn("Human review required", markdown)
        self.assertIn("00003", markdown)
        self.assertIn("No data or release files were changed", markdown)


if __name__ == "__main__":
    unittest.main()
