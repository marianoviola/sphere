#!/usr/bin/env python3
"""Run a local Sphere demo server.

The server is intentionally dependency-free. It demonstrates discovery,
paid-content 402 challenges, and a mock MPP / PaymentAuth retry flow.
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


DEFAULT_FRAGMENT_ID = "2026-06-07-agent-readable-public-sphere"
MOCK_PAYMENT_CREDENTIAL = "demo-paid-access"


def b64url_json(data: dict[str, object]) -> str:
    raw = json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


class SphereDemoHandler(BaseHTTPRequestHandler):
    server_version = "SphereDemo/0.1"

    def do_GET(self) -> None:  # noqa: N802 - http.server API
        path = urlparse(self.path).path

        if path in {"/", "/index.html"}:
            self.redirect(f"/fragments/{self.server.fragment_id}/")
            return

        if path == f"/fragments/{self.server.fragment_id}/":
            self.serve_file(self.server.fragment_dir / "index.html", "text/html; charset=utf-8")
            return

        if path == f"/manifest/{self.server.fragment_id}.json":
            self.serve_file(self.server.fragment_dir / "sphere.json", "application/json; charset=utf-8")
            return

        if path == f"/content/free/{self.server.fragment_id}.md":
            self.serve_content()
            return

        if path == f"/content/paid/{self.server.fragment_id}.md":
            self.serve_paid_content()
            return

        self.send_error_json(404, {"error": "not_found", "path": path})

    def serve_paid_content(self) -> None:
        authorization = self.headers.get("Authorization", "")
        if not self.valid_payment_credential(authorization):
            self.payment_required()
            return

        self.serve_content(
            extra_headers={
                "Payment-Receipt": f"demo_receipt_{self.server.fragment_id}",
                "Cache-Control": "no-store",
            }
        )

    def serve_content(self, extra_headers: dict[str, str] | None = None) -> None:
        self.serve_file(
            self.server.fragment_dir / "content.md",
            "text/markdown; charset=utf-8",
            extra_headers=extra_headers,
        )

    def payment_required(self) -> None:
        challenge_id = f"demo_{self.server.fragment_id}"
        request_payload = {
            "fragment_id": self.server.fragment_id,
            "amount": self.server.price,
            "currency": self.server.currency,
            "method": "mock",
            "credential_hint": MOCK_PAYMENT_CREDENTIAL,
        }
        challenge = (
            f'Payment id="{challenge_id}", '
            'realm="sphere.pub", '
            'method="mock", '
            'intent="charge", '
            f'request="{b64url_json(request_payload)}"'
        )
        body = {
            "error": "payment_required",
            "fragment_id": self.server.fragment_id,
            "price": self.server.price,
            "currency": self.server.currency,
            "payment_profile": "mpp-paymentauth",
            "demo_authorization": f"Payment id=\"{challenge_id}\", credential=\"{MOCK_PAYMENT_CREDENTIAL}\"",
        }

        self.send_json(
            402,
            body,
            extra_headers={
                "WWW-Authenticate": challenge,
                "Cache-Control": "no-store",
            },
        )

    def valid_payment_credential(self, authorization: str) -> bool:
        if not authorization.startswith("Payment "):
            return False
        return f'credential="{MOCK_PAYMENT_CREDENTIAL}"' in authorization

    def serve_file(
        self,
        path: Path,
        content_type: str | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        if not path.exists() or not path.is_file():
            self.send_error_json(404, {"error": "file_not_found", "path": str(path)})
            return

        body = path.read_bytes()
        resolved_type = content_type or mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", resolved_type)
        self.send_header("Content-Length", str(len(body)))
        if extra_headers:
            for name, value in extra_headers.items():
                self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body)

    def send_json(
        self,
        status: int,
        body: dict[str, object],
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        payload = json.dumps(body, indent=2, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        if extra_headers:
            for name, value in extra_headers.items():
                self.send_header(name, value)
        self.end_headers()
        self.wfile.write(payload)

    def send_error_json(self, status: int, body: dict[str, object]) -> None:
        self.send_json(status, body)

    def redirect(self, location: str) -> None:
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    def log_message(self, fmt: str, *args: object) -> None:
        sys.stderr.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), fmt % args))


class SphereDemoServer(ThreadingHTTPServer):
    fragment_dir: Path
    fragment_id: str
    price: float
    currency: str


def load_demo_metadata(fragment_dir: Path) -> tuple[str, float, str]:
    manifest_path = fragment_dir / "sphere.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    fragment_id = manifest["fragment_id"]
    access = manifest.get("access", {})
    price = float(access.get("price_per_access") or 0)
    currency = access.get("currency") or "USD"
    return fragment_id, price, currency


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run a local Sphere demo server.")
    parser.add_argument(
        "--fragment-dir",
        type=Path,
        default=Path("examples/basic-fragment"),
        help="Path to a Sphere fragment directory",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind")
    parser.add_argument("--port", type=int, default=8765, help="Port to bind")
    args = parser.parse_args(argv)

    fragment_dir = args.fragment_dir.resolve()
    fragment_id, price, currency = load_demo_metadata(fragment_dir)

    server = SphereDemoServer((args.host, args.port), SphereDemoHandler)
    server.fragment_dir = fragment_dir
    server.fragment_id = fragment_id
    server.price = price
    server.currency = currency

    print(f"Sphere demo server: http://{args.host}:{args.port}/")
    print(f"Discovery: http://{args.host}:{args.port}/fragments/{fragment_id}/")
    print(f"Paid content: http://{args.host}:{args.port}/content/paid/{fragment_id}.md")
    print(f'Mock credential: Authorization: Payment id="demo_{fragment_id}", credential="{MOCK_PAYMENT_CREDENTIAL}"')
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
