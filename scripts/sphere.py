#!/usr/bin/env python3
"""Sphere reference CLI."""

from __future__ import annotations

import argparse
import sys

import sphere_build_discovery
import sphere_demo_server
import sphere_prepare
import sphere_validate


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="sphere", description="Sphere reference CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate a Sphere fragment")
    validate.add_argument("fragment_dir")

    serve = subparsers.add_parser("serve", help="Run the local demo server")
    serve.add_argument("fragment_dir", nargs="?", default="examples/basic-fragment")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8765)

    build = subparsers.add_parser("build-discovery", help="Generate fragment discovery HTML")
    build.add_argument("fragment_dir")
    build.add_argument("--publisher", default="demo")
    build.add_argument("--output")

    prepare = subparsers.add_parser("prepare", help="Prepare a raw Markdown file as a Sphere fragment")
    prepare.add_argument("source")
    prepare.add_argument("--output", default="fragments")
    prepare.add_argument("--title")
    prepare.add_argument("--fragment-id")
    prepare.add_argument("--date")
    prepare.add_argument("--author", default="Unknown Author")
    prepare.add_argument("--author-url")
    prepare.add_argument("--canonical-url")
    prepare.add_argument("--language", default="en")
    prepare.add_argument("--type", default="document", choices=sorted(sphere_validate.CONTENT_TYPES))
    prepare.add_argument("--publisher", default="demo")
    prepare.add_argument("--policy", default="free", choices=sorted(sphere_validate.POLICIES))
    prepare.add_argument("--price", type=float)
    prepare.add_argument("--currency", default="USD")
    prepare.add_argument("--payment-profile", default="mpp-paymentauth", choices=sorted(sphere_validate.PAYMENT_PROFILES))
    prepare.add_argument("--payment-method", default="stripe")
    prepare.add_argument("--payment-endpoint", default="https://api.sphere.pub/v1/pay")
    prepare.add_argument("--license", default="CC-BY-NC", choices=sorted(sphere_validate.LICENSES))
    prepare.add_argument("--llm-training", action="store_true")
    prepare.add_argument("--no-llm-retrieval", action="store_true")
    prepare.add_argument("--no-citation-required", action="store_true")
    prepare.add_argument("--force", action="store_true")

    args = parser.parse_args(argv)

    if args.command == "validate":
        return sphere_validate.main([args.fragment_dir])
    if args.command == "serve":
        return sphere_demo_server.main(["--fragment-dir", args.fragment_dir, "--host", args.host, "--port", str(args.port)])
    if args.command == "build-discovery":
        build_args = [args.fragment_dir, "--publisher", args.publisher]
        if args.output:
            build_args.extend(["--output", args.output])
        return sphere_build_discovery.main(build_args)
    if args.command == "prepare":
        prepare_args = [args.source, "--output", args.output, "--author", args.author, "--language", args.language]
        for option in (
            "title",
            "fragment_id",
            "date",
            "author_url",
            "canonical_url",
            "publisher",
            "policy",
            "currency",
            "payment_profile",
            "payment_method",
            "payment_endpoint",
            "license",
        ):
            value = getattr(args, option)
            if value is not None:
                prepare_args.extend([f"--{option.replace('_', '-')}", str(value)])
        prepare_args.extend(["--type", args.type])
        if args.price is not None:
            prepare_args.extend(["--price", str(args.price)])
        if args.llm_training:
            prepare_args.append("--llm-training")
        if args.no_llm_retrieval:
            prepare_args.append("--no-llm-retrieval")
        if args.no_citation_required:
            prepare_args.append("--no-citation-required")
        if args.force:
            prepare_args.append("--force")
        return sphere_prepare.main(prepare_args)

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
