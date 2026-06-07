#!/usr/bin/env python3
"""Prepare a raw Markdown file as a Sphere fragment."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import sphere_build_discovery
import sphere_validate


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "untitled"


def infer_title(markdown: str, fallback: str) -> str:
    for pattern in (r"^#\s+(.+)$", r"^##\s+(.+)$"):
        match = re.search(pattern, markdown, flags=re.MULTILINE)
        if match:
            return match.group(1).strip()
    return fallback


def normalize_markdown(markdown: str, title: str) -> str:
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    normalized: list[str] = []
    skipped_title = False

    for line in lines:
        h1 = re.match(r"^#\s+(.+)$", line)
        if h1:
            heading = h1.group(1).strip()
            if not skipped_title and heading == title:
                skipped_title = True
                continue
            normalized.append(f"## {heading}")
            continue
        normalized.append(line)

    text = "\n".join(normalized).strip()
    if not re.search(r"^##\s+", text, flags=re.MULTILINE):
        text = f"## Summary\n\n{text}"
    return text + "\n"


def build_manifest(
    *,
    fragment_id: str,
    title: str,
    source_path: str,
    source_format: str,
    author: str,
    author_url: str | None,
    canonical_url: str | None,
    language: str,
    content_type: str,
    policy: str,
    price: float | None,
    currency: str,
    payment_profile: str,
    payment_method: str,
    payment_endpoint: str,
    license_type: str,
    llm_retrieval: bool,
    llm_training: bool,
    llm_citation_required: bool,
) -> dict[str, object]:
    access: dict[str, object] = {
        "policy": policy,
        "preview_chars": 500,
        "price_per_access": price,
        "currency": currency,
        "sponsor": {
            "name": None,
            "url": None,
            "disclosure": None,
        },
    }
    if policy in {"paid", "metered"}:
        access["payment"] = {
            "profile": payment_profile,
            "method": payment_method,
            "endpoint": payment_endpoint,
        }

    return {
        "sphere_version": sphere_validate.SPEC_VERSION,
        "fragment_id": fragment_id,
        "identity": {
            "title": title,
            "author": {
                "name": author,
                "url": author_url,
            },
            "canonical_url": canonical_url,
            "language": language,
            "type": content_type,
        },
        "hierarchy": {
            "corpus_id": None,
            "series_id": None,
            "constellation_id": None,
            "position": None,
        },
        "sources": [
            {
                "source_id": "source_1",
                "path": source_path,
                "kind": "text",
                "format": source_format,
                "role": "primary",
                "transformation": "converted",
                "included_in_content": True,
            }
        ],
        "relations": [],
        "access": access,
        "content_flags": {
            "nsfw": False,
            "nsfw_categories": [],
            "age_restriction": None,
        },
        "license": {
            "type": license_type,
            "llm_retrieval": llm_retrieval,
            "llm_training": llm_training,
            "llm_citation_required": llm_citation_required,
        },
    }


def prepare_fragment(args: argparse.Namespace) -> Path:
    source = Path(args.source)
    markdown = source.read_text(encoding="utf-8")
    title = args.title or infer_title(markdown, source.stem.replace("-", " ").replace("_", " ").title())
    fragment_date = args.date or date.today().isoformat()
    fragment_id = args.fragment_id or f"{fragment_date}-{slugify(title)}"
    fragment_dir = Path(args.output) / fragment_id
    fragment_dir.mkdir(parents=True, exist_ok=args.force)

    content = normalize_markdown(markdown, title)
    price = args.price
    if args.policy in {"paid", "metered"} and price is None:
        price = 0.003

    manifest = build_manifest(
        fragment_id=fragment_id,
        title=title,
        source_path=str(source),
        source_format=source.suffix.lower().lstrip(".") or "md",
        author=args.author,
        author_url=args.author_url,
        canonical_url=args.canonical_url,
        language=args.language,
        content_type=args.type,
        policy=args.policy,
        price=price,
        currency=args.currency,
        payment_profile=args.payment_profile,
        payment_method=args.payment_method,
        payment_endpoint=args.payment_endpoint,
        license_type=args.license,
        llm_retrieval=not args.no_llm_retrieval,
        llm_training=args.llm_training,
        llm_citation_required=not args.no_citation_required,
    )

    (fragment_dir / "sphere.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (fragment_dir / "content.md").write_text(content, encoding="utf-8")
    sphere_build_discovery.build_discovery(fragment_dir, publisher=args.publisher)

    reporter = sphere_validate.validate_fragment(fragment_dir)
    reporter.print(fragment_dir)
    if reporter.errors:
        raise SystemExit(1)

    print()
    print("Prepared Sphere fragment")
    print(f"  Fragment: {fragment_id}")
    print(f"  Title:   {title}")
    print(f"  Policy:  {args.policy}")
    print(f"  Output:  {fragment_dir}")
    return fragment_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare a raw Markdown file as a Sphere fragment.")
    parser.add_argument("source", help="Path to a raw Markdown file")
    parser.add_argument("--output", default="fragments", help="Output directory for generated fragments")
    parser.add_argument("--title")
    parser.add_argument("--fragment-id")
    parser.add_argument("--date", help="Fragment date prefix, YYYY-MM-DD. Defaults to today.")
    parser.add_argument("--author", default="Unknown Author")
    parser.add_argument("--author-url")
    parser.add_argument("--canonical-url")
    parser.add_argument("--language", default="en")
    parser.add_argument("--type", default="document", choices=sorted(sphere_validate.CONTENT_TYPES))
    parser.add_argument("--publisher", default="demo")
    parser.add_argument("--policy", default="free", choices=sorted(sphere_validate.POLICIES))
    parser.add_argument("--price", type=float)
    parser.add_argument("--currency", default="USD")
    parser.add_argument("--payment-profile", default="mpp-paymentauth", choices=sorted(sphere_validate.PAYMENT_PROFILES))
    parser.add_argument("--payment-method", default="stripe")
    parser.add_argument("--payment-endpoint", default="https://api.sphere.pub/v1/pay")
    parser.add_argument("--license", default="CC-BY-NC", choices=sorted(sphere_validate.LICENSES))
    parser.add_argument("--llm-training", action="store_true")
    parser.add_argument("--no-llm-retrieval", action="store_true")
    parser.add_argument("--no-citation-required", action="store_true")
    parser.add_argument("--force", action="store_true", help="Allow writing into an existing fragment directory")
    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    prepare_fragment(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
