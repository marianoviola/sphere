from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import sphere_validate  # noqa: E402


class ValidateFragmentTest(unittest.TestCase):
    def test_example_fragment_is_valid(self) -> None:
        reporter = sphere_validate.validate_fragment(ROOT / "examples/basic-fragment")
        self.assertEqual([], reporter.errors)
        self.assertEqual([], reporter.warnings)

    def test_missing_required_files_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            reporter = sphere_validate.validate_fragment(Path(tmp))
        self.assertIn("missing sphere.json", reporter.errors)
        self.assertIn("missing content.md", reporter.errors)

    def test_paid_fragment_requires_payment_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fragment_dir = Path(tmp) / "fragment"
            shutil.copytree(ROOT / "examples/basic-fragment", fragment_dir)
            manifest_path = fragment_dir / "sphere.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            del manifest["access"]["payment"]
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            reporter = sphere_validate.validate_fragment(fragment_dir)

        self.assertIn("paid or metered fragments require `access.payment` metadata", reporter.errors)

    def test_h1_heading_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fragment_dir = Path(tmp) / "fragment"
            shutil.copytree(ROOT / "examples/basic-fragment", fragment_dir)
            (fragment_dir / "content.md").write_text("# Wrong heading\n\nBody", encoding="utf-8")

            reporter = sphere_validate.validate_fragment(fragment_dir)

        self.assertIn("content.md headings must start at `##`; H1 is reserved for manifest title", reporter.errors)

    def test_invalid_relation_type_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fragment_dir = Path(tmp) / "fragment"
            shutil.copytree(ROOT / "examples/basic-fragment", fragment_dir)
            manifest_path = fragment_dir / "sphere.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["relations"] = [{"type": "vibes_with", "target": "2026-01-01-other"}]
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            reporter = sphere_validate.validate_fragment(fragment_dir)

        self.assertTrue(any("relations[0].type" in error for error in reporter.errors))

    def test_declared_standalone_media_does_not_warn(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fragment_dir = Path(tmp) / "fragment"
            shutil.copytree(ROOT / "examples/basic-fragment", fragment_dir)
            media_dir = fragment_dir / "media"
            media_dir.mkdir()
            (media_dir / "image.jpg").write_bytes(b"fake-image")
            manifest_path = fragment_dir / "sphere.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["sources"].append(
                {
                    "source_id": "image_1",
                    "path": "media/image.jpg",
                    "kind": "image",
                    "format": "jpg",
                    "role": "standalone",
                    "transformation": "described",
                    "included_in_content": False,
                }
            )
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            reporter = sphere_validate.validate_fragment(fragment_dir)

        self.assertEqual([], reporter.errors)
        self.assertEqual([], reporter.warnings)


if __name__ == "__main__":
    unittest.main()
