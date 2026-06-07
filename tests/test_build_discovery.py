from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import sphere_build_discovery  # noqa: E402


class BuildDiscoveryTest(unittest.TestCase):
    def test_generate_discovery_contains_core_metadata(self) -> None:
        html = sphere_build_discovery.generate_discovery_html(ROOT / "examples/basic-fragment", publisher="demo")

        self.assertIn('meta name="sphere:fragment_id"', html)
        self.assertIn('meta name="sphere:payment:profile" content="mpp-paymentauth"', html)
        self.assertIn('link rel="sphere:content"', html)
        self.assertIn('class="preview"', html)

    def test_build_discovery_writes_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "index.html"
            result = sphere_build_discovery.build_discovery(
                ROOT / "examples/basic-fragment",
                publisher="demo",
                output=output,
            )

            self.assertEqual(output, result)
            self.assertTrue(output.exists())
            self.assertIn("Agent-Readable Public Sphere", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
