from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import sphere_prepare  # noqa: E402
import sphere_validate  # noqa: E402


class PrepareFragmentTest(unittest.TestCase):
    def test_prepare_generates_valid_fragment(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            args = sphere_prepare.build_parser().parse_args(
                [
                    str(ROOT / "examples/raw-content/agent-readable-notes.md"),
                    "--output",
                    tmp,
                    "--date",
                    "2026-06-07",
                    "--author",
                    "Sphere Project",
                    "--policy",
                    "metered",
                    "--price",
                    "0.003",
                ]
            )

            fragment_dir = sphere_prepare.prepare_fragment(args)
            reporter = sphere_validate.validate_fragment(fragment_dir)

            self.assertEqual([], reporter.errors)
            self.assertTrue((fragment_dir / "sphere.json").exists())
            self.assertTrue((fragment_dir / "content.md").exists())
            self.assertTrue((fragment_dir / "index.html").exists())

    def test_prepare_removes_matching_h1_and_keeps_h2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            args = sphere_prepare.build_parser().parse_args(
                [
                    str(ROOT / "examples/raw-content/agent-readable-notes.md"),
                    "--output",
                    tmp,
                    "--date",
                    "2026-06-07",
                    "--author",
                    "Sphere Project",
                ]
            )

            fragment_dir = sphere_prepare.prepare_fragment(args)
            content = (fragment_dir / "content.md").read_text(encoding="utf-8")

            self.assertNotIn("# Agent-readable notes", content)
            self.assertIn("## Context", content)

    def test_prepare_paid_policy_adds_payment_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            args = sphere_prepare.build_parser().parse_args(
                [
                    str(ROOT / "examples/raw-content/agent-readable-notes.md"),
                    "--output",
                    tmp,
                    "--date",
                    "2026-06-07",
                    "--policy",
                    "paid",
                    "--author",
                    "Sphere Project",
                ]
            )

            fragment_dir = sphere_prepare.prepare_fragment(args)
            manifest = json.loads((fragment_dir / "sphere.json").read_text(encoding="utf-8"))

            self.assertEqual("paid", manifest["access"]["policy"])
            self.assertEqual(0.003, manifest["access"]["price_per_access"])
            self.assertEqual("mpp-paymentauth", manifest["access"]["payment"]["profile"])


if __name__ == "__main__":
    unittest.main()
