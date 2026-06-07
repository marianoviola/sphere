from __future__ import annotations

import http.client
import sys
import threading
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import sphere_demo_server  # noqa: E402


class DemoServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fragment_dir = ROOT / "examples/basic-fragment"
        fragment_id, price, currency = sphere_demo_server.load_demo_metadata(fragment_dir)
        cls.server = sphere_demo_server.SphereDemoServer(("127.0.0.1", 0), sphere_demo_server.SphereDemoHandler)
        cls.server.fragment_dir = fragment_dir
        cls.server.fragment_id = fragment_id
        cls.server.price = price
        cls.server.currency = currency
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.host, cls.port = cls.server.server_address

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def request(self, path: str, headers: dict[str, str] | None = None) -> tuple[int, dict[str, str], bytes]:
        conn = http.client.HTTPConnection(self.host, self.port, timeout=5)
        conn.request("GET", path, headers=headers or {})
        response = conn.getresponse()
        body = response.read()
        headers_dict = {key: value for key, value in response.getheaders()}
        conn.close()
        return response.status, headers_dict, body

    def test_discovery_returns_200(self) -> None:
        status, headers, body = self.request(f"/fragments/{self.server.fragment_id}/")
        self.assertEqual(200, status)
        self.assertIn("text/html", headers["Content-Type"])
        self.assertIn(b"sphere:fragment_id", body)

    def test_paid_content_requires_payment(self) -> None:
        status, headers, body = self.request(f"/content/paid/{self.server.fragment_id}.md")
        self.assertEqual(402, status)
        self.assertIn("WWW-Authenticate", headers)
        self.assertIn(b"payment_required", body)

    def test_paid_content_accepts_mock_payment(self) -> None:
        authorization = f'Payment id="demo_{self.server.fragment_id}", credential="demo-paid-access"'
        status, headers, body = self.request(
            f"/content/paid/{self.server.fragment_id}.md",
            headers={"Authorization": authorization},
        )
        self.assertEqual(200, status)
        self.assertIn("Payment-Receipt", headers)
        self.assertIn(b"## Summary", body)


if __name__ == "__main__":
    unittest.main()
