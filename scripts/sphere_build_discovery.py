#!/usr/bin/env python3
"""Generate a Sphere discovery index.html for a fragment."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any


def load_manifest(fragment_dir: Path) -> dict[str, Any]:
    return json.loads((fragment_dir / "sphere.json").read_text(encoding="utf-8"))


def plain_preview(markdown: str, length: int) -> str:
    text = re.sub(r"```.*?```", "", markdown, flags=re.DOTALL)
    text = re.sub(r"!\[[^\]]*]\([^)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)]\([^)]+\)", r"\1", text)
    text = re.sub(r"^#{2,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"[*_`>#-]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:length].strip()


def content_href(fragment_id: str, policy: str, publisher: str) -> str:
    lane = "free" if policy == "free" else "paid"
    return f"https://content.{publisher}.sphere.pub/{lane}/{fragment_id}.md"


def generate_discovery_html(fragment_dir: Path, publisher: str = "demo") -> str:
    manifest = load_manifest(fragment_dir)
    content = (fragment_dir / "content.md").read_text(encoding="utf-8")

    identity = manifest["identity"]
    access = manifest["access"]
    license_data = manifest["license"]
    flags = manifest["content_flags"]
    payment = access.get("payment", {})

    fragment_id = manifest["fragment_id"]
    title = identity["title"]
    author_name = identity["author"]["name"]
    canonical_url = identity.get("canonical_url") or f"https://{publisher}.sphere.pub/fragments/{fragment_id}/"
    language = identity["language"]
    policy = access["policy"]
    preview_chars = int(access.get("preview_chars") or 0)
    preview = plain_preview(content, preview_chars)
    is_free = "true" if policy == "free" else "false"

    def esc(value: object) -> str:
        return html.escape("" if value is None else str(value), quote=True)

    payment_meta = ""
    if payment:
        payment_meta = f"""
  <meta name="sphere:payment:profile" content="{esc(payment.get('profile'))}">
  <meta name="sphere:payment:method" content="{esc(payment.get('method'))}">
  <meta name="sphere:payment:endpoint" content="{esc(payment.get('endpoint'))}">"""

    return f"""<!DOCTYPE html>
<html lang="{esc(language)}">
<head>
  <meta charset="UTF-8">
  <title>{esc(title)} - {esc(author_name)}</title>
  <link rel="canonical" href="{esc(canonical_url)}">

  <meta name="sphere:fragment_id" content="{esc(fragment_id)}">
  <meta name="sphere:version" content="{esc(manifest['sphere_version'])}">
  <meta name="sphere:publisher_id" content="{esc(publisher)}">

  <meta name="sphere:access:policy" content="{esc(policy)}">
  <meta name="sphere:access:preview_chars" content="{esc(preview_chars)}">
  <meta name="sphere:access:price" content="{esc(access.get('price_per_access'))}">
  <meta name="sphere:access:currency" content="{esc(access.get('currency'))}">{payment_meta}

  <meta name="sphere:nsfw" content="{str(bool(flags.get('nsfw'))).lower()}">

  <meta name="sphere:license" content="{esc(license_data.get('type'))}">
  <meta name="sphere:llm_retrieval" content="{str(bool(license_data.get('llm_retrieval'))).lower()}">
  <meta name="sphere:llm_training" content="{str(bool(license_data.get('llm_training'))).lower()}">
  <meta name="sphere:llm_citation" content="{str(bool(license_data.get('llm_citation_required'))).lower()}">

  <link rel="sphere:content" type="text/markdown" href="{esc(content_href(fragment_id, policy, publisher))}">
  <link rel="sphere:manifest" type="application/json" href="sphere.json">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": {json.dumps(title)},
    "author": {{ "@type": "Person", "name": {json.dumps(author_name)} }},
    "inLanguage": {json.dumps(language)},
    "isAccessibleForFree": {is_free},
    "license": "https://sphere.pub/license/{esc(license_data.get('type'))}"
  }}
  </script>
</head>
<body>
  <p class="preview">{esc(preview)}</p>
</body>
</html>
"""


def build_discovery(fragment_dir: Path, publisher: str = "demo", output: Path | None = None) -> Path:
    output_path = output or fragment_dir / "index.html"
    output_path.write_text(generate_discovery_html(fragment_dir, publisher=publisher), encoding="utf-8")
    return output_path


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Generate Sphere discovery index.html for a fragment.")
    parser.add_argument("fragment_dir", type=Path)
    parser.add_argument("--publisher", default="demo")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    output = build_discovery(args.fragment_dir, publisher=args.publisher, output=args.output)
    print(f"Generated discovery: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
