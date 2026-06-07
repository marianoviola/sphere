#!/usr/bin/env python3
"""Validate a Sphere fragment folder.

This validator intentionally uses only the Python standard library so the
reference implementation can run before Sphere has packaging or dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SPEC_VERSION = "0.4.0"
POLICIES = {"free", "metered", "paid", "sponsored"}
CONTENT_TYPES = {"post", "episode", "document", "dataset"}
LICENSES = {"CC-BY", "CC-BY-NC", "CC-BY-NC-ND", "proprietary"}
PAYMENT_PROFILES = {"mpp-paymentauth", "sphere-token", "x402"}
SOURCE_KINDS = {"text", "data", "image", "audio", "video", "mixed", "external"}
SOURCE_ROLES = {"primary", "supporting", "evidence", "media", "standalone"}
TRANSFORMATIONS = {"extracted", "converted", "summarized", "transcribed", "described", "preserved"}
RELATION_TYPES = {
    "cites",
    "extends",
    "responds_to",
    "updates",
    "contradicts",
    "supports",
    "part_of",
    "derived_from",
    "translation_of",
    "same_as",
}
FRAGMENT_ID_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")
LANG_RE = re.compile(r"^[a-z]{2}$")
MEDIA_RE = re.compile(r"!\[[^\]]*]\((media/[^)\s]+)\)")


class Reporter:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def print(self, fragment_dir: Path) -> None:
        print(f"Sphere fragment validation: {fragment_dir}")
        for message in self.errors:
            print(f"ERROR: {message}")
        for message in self.warnings:
            print(f"WARN: {message}")
        if self.errors:
            print(f"Result: invalid ({len(self.errors)} error(s), {len(self.warnings)} warning(s))")
        else:
            print(f"Result: valid ({len(self.warnings)} warning(s))")


def load_json(path: Path, reporter: Reporter) -> dict[str, Any] | None:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        reporter.error("missing sphere.json")
        return None
    except json.JSONDecodeError as exc:
        reporter.error(f"sphere.json is not valid JSON: line {exc.lineno}, column {exc.colno}")
        return None

    if not isinstance(data, dict):
        reporter.error("sphere.json root must be an object")
        return None
    return data


def require_object(data: dict[str, Any], key: str, reporter: Reporter) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        reporter.error(f"`{key}` must be an object")
        return {}
    return value


def require_string(data: dict[str, Any], key: str, reporter: Reporter, *, allow_null: bool = False) -> str | None:
    value = data.get(key)
    if value is None and allow_null:
        return None
    if not isinstance(value, str) or not value.strip():
        reporter.error(f"`{key}` must be a non-empty string")
        return None
    return value


def require_bool(data: dict[str, Any], key: str, reporter: Reporter) -> bool | None:
    value = data.get(key)
    if not isinstance(value, bool):
        reporter.error(f"`{key}` must be a boolean")
        return None
    return value


def validate_manifest(manifest: dict[str, Any], reporter: Reporter) -> None:
    version = require_string(manifest, "sphere_version", reporter)
    if version and version != SPEC_VERSION:
        reporter.warn(f"`sphere_version` is {version}, expected {SPEC_VERSION}")

    fragment_id = require_string(manifest, "fragment_id", reporter)
    if fragment_id and not FRAGMENT_ID_RE.match(fragment_id):
        reporter.error("`fragment_id` must match yyyy-mm-dd-title-slug")

    identity = require_object(manifest, "identity", reporter)
    title = require_string(identity, "title", reporter)
    if title and len(title) > 180:
        reporter.warn("`identity.title` is long; consider a shorter fragment title")

    author = require_object(identity, "author", reporter)
    require_string(author, "name", reporter)
    require_string(author, "url", reporter, allow_null=True)
    require_string(identity, "canonical_url", reporter, allow_null=True)

    language = require_string(identity, "language", reporter)
    if language and not LANG_RE.match(language):
        reporter.error("`identity.language` must be ISO 639-1 lowercase, e.g. `en` or `it`")

    content_type = require_string(identity, "type", reporter)
    if content_type and content_type not in CONTENT_TYPES:
        reporter.error(f"`identity.type` must be one of: {', '.join(sorted(CONTENT_TYPES))}")

    hierarchy = require_object(manifest, "hierarchy", reporter)
    require_string(hierarchy, "corpus_id", reporter, allow_null=True)
    require_string(hierarchy, "series_id", reporter, allow_null=True)
    require_string(hierarchy, "constellation_id", reporter, allow_null=True)
    position = hierarchy.get("position")
    if position is not None and not isinstance(position, int):
        reporter.error("`hierarchy.position` must be an integer or null")

    validate_sources(manifest.get("sources"), reporter)
    validate_relations(manifest.get("relations"), reporter)

    access = require_object(manifest, "access", reporter)
    policy = require_string(access, "policy", reporter)
    if policy and policy not in POLICIES:
        reporter.error(f"`access.policy` must be one of: {', '.join(sorted(POLICIES))}")

    preview_chars = access.get("preview_chars")
    if not isinstance(preview_chars, int) or preview_chars < 0:
        reporter.error("`access.preview_chars` must be a non-negative integer")

    price = access.get("price_per_access")
    if policy in {"paid", "metered"}:
        if not isinstance(price, (int, float)) or price <= 0:
            reporter.error("paid or metered fragments require positive `access.price_per_access`")
    elif price is not None:
        reporter.warn("`access.price_per_access` is ignored for free or sponsored fragments")

    currency = require_string(access, "currency", reporter)
    if currency and len(currency) != 3:
        reporter.error("`access.currency` must be a 3-letter currency code")

    payment = access.get("payment")
    if policy in {"paid", "metered"}:
        if not isinstance(payment, dict):
            reporter.error("paid or metered fragments require `access.payment` metadata")
        else:
            profile = require_string(payment, "profile", reporter)
            if profile and profile not in PAYMENT_PROFILES:
                reporter.error(f"`access.payment.profile` must be one of: {', '.join(sorted(PAYMENT_PROFILES))}")
            require_string(payment, "method", reporter)
            require_string(payment, "endpoint", reporter)

    sponsor = require_object(access, "sponsor", reporter)
    require_string(sponsor, "name", reporter, allow_null=True)
    require_string(sponsor, "url", reporter, allow_null=True)
    require_string(sponsor, "disclosure", reporter, allow_null=True)

    flags = require_object(manifest, "content_flags", reporter)
    nsfw = require_bool(flags, "nsfw", reporter)
    categories = flags.get("nsfw_categories")
    if not isinstance(categories, list):
        reporter.error("`content_flags.nsfw_categories` must be an array")
    if nsfw is False and categories:
        reporter.warn("`content_flags.nsfw_categories` is set while `nsfw` is false")

    license_data = require_object(manifest, "license", reporter)
    license_type = require_string(license_data, "type", reporter)
    if license_type and license_type not in LICENSES:
        reporter.error(f"`license.type` must be one of: {', '.join(sorted(LICENSES))}")
    require_bool(license_data, "llm_retrieval", reporter)
    require_bool(license_data, "llm_training", reporter)
    require_bool(license_data, "llm_citation_required", reporter)


def validate_sources(value: Any, reporter: Reporter) -> None:
    if value is None:
        return
    if not isinstance(value, list):
        reporter.error("`sources` must be an array when present")
        return
    for index, source in enumerate(value):
        if not isinstance(source, dict):
            reporter.error(f"`sources[{index}]` must be an object")
            continue
        source_id = require_string(source, "source_id", reporter)
        require_string(source, "path", reporter)
        kind = require_string(source, "kind", reporter)
        if kind and kind not in SOURCE_KINDS:
            reporter.error(f"`sources[{index}].kind` must be one of: {', '.join(sorted(SOURCE_KINDS))}")
        require_string(source, "format", reporter)
        role = require_string(source, "role", reporter)
        if role and role not in SOURCE_ROLES:
            reporter.error(f"`sources[{index}].role` must be one of: {', '.join(sorted(SOURCE_ROLES))}")
        transformation = require_string(source, "transformation", reporter)
        if transformation and transformation not in TRANSFORMATIONS:
            reporter.error(
                f"`sources[{index}].transformation` must be one of: {', '.join(sorted(TRANSFORMATIONS))}"
            )
        included = source.get("included_in_content")
        if not isinstance(included, bool):
            reporter.error(f"`sources[{index}].included_in_content` must be a boolean")
        if source_id and not re.match(r"^[a-zA-Z0-9_-]+$", source_id):
            reporter.error(f"`sources[{index}].source_id` must contain only letters, numbers, `_`, or `-`")


def validate_relations(value: Any, reporter: Reporter) -> None:
    if value is None:
        return
    if not isinstance(value, list):
        reporter.error("`relations` must be an array when present")
        return
    for index, relation in enumerate(value):
        if not isinstance(relation, dict):
            reporter.error(f"`relations[{index}]` must be an object")
            continue
        relation_type = require_string(relation, "type", reporter)
        if relation_type and relation_type not in RELATION_TYPES:
            reporter.error(f"`relations[{index}].type` must be one of: {', '.join(sorted(RELATION_TYPES))}")
        require_string(relation, "target", reporter)
        require_string(relation, "description", reporter, allow_null=True)


def declared_source_paths(manifest: dict[str, Any] | None) -> set[str]:
    if not manifest:
        return set()
    sources = manifest.get("sources")
    if not isinstance(sources, list):
        return set()
    return {source.get("path") for source in sources if isinstance(source, dict) and isinstance(source.get("path"), str)}


def validate_content(fragment_dir: Path, reporter: Reporter, manifest: dict[str, Any] | None = None) -> None:
    content_path = fragment_dir / "content.md"
    if not content_path.exists():
        reporter.error("missing content.md")
        return

    text = content_path.read_text(encoding="utf-8")
    if not text.strip():
        reporter.error("content.md must not be empty")
        return

    if re.search(r"<[a-zA-Z][^>]*>", text):
        reporter.error("content.md must be pure Markdown, not HTML")

    if re.search(r"^# ", text, flags=re.MULTILINE):
        reporter.error("content.md headings must start at `##`; H1 is reserved for manifest title")

    if not re.search(r"^## ", text, flags=re.MULTILINE):
        reporter.warn("content.md has no `##` headings")

    for media_ref in MEDIA_RE.findall(text):
        media_path = fragment_dir / media_ref
        if not media_path.exists():
            reporter.error(f"referenced media file does not exist: {media_ref}")

    media_dir = fragment_dir / "media"
    if media_dir.exists() and media_dir.is_dir():
        referenced = set(MEDIA_RE.findall(text))
        declared = declared_source_paths(manifest)
        for media_file in media_dir.iterdir():
            if media_file.is_file():
                rel = f"media/{media_file.name}"
                if rel not in referenced and rel not in declared:
                    reporter.warn(f"media file is not referenced from content.md or declared in sources: {rel}")


def validate_fragment(fragment_dir: Path) -> Reporter:
    reporter = Reporter()
    if not fragment_dir.exists():
        reporter.error("fragment path does not exist")
        return reporter
    if not fragment_dir.is_dir():
        reporter.error("fragment path must be a directory")
        return reporter

    manifest = load_json(fragment_dir / "sphere.json", reporter)
    if manifest is not None:
        validate_manifest(manifest, reporter)
    validate_content(fragment_dir, reporter, manifest)
    return reporter


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate a Sphere fragment folder.")
    parser.add_argument("fragment_dir", type=Path, help="Path to a folder containing sphere.json and content.md")
    args = parser.parse_args(argv)

    reporter = validate_fragment(args.fragment_dir)
    reporter.print(args.fragment_dir)
    return 1 if reporter.errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
