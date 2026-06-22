---
title: Roadmap
description: Current state and the planned phases beyond v1.
summary: What ships today and the planned phases beyond v1.
status: vision
order: 10
note: Only the earliest items here are shipped (the self-hostable Node and the local plugin). Later phases are planned direction, not current functionality.
---

# Roadmap

> A practical path from the current local prototype to a publishable Sphere service.

---

## Current State

Sphere currently has:

- A coherent concept and vocabulary: public sphere, fragment, constellation, relation, particle.
- A fragment format with manifest, canonical Markdown, sources, data, media, access policy, license, and relations.
- A dependency-free validator.
- A fragment preparation CLI for raw Markdown.
- A discovery HTML generator.
- A local demo server with mock MPP / PaymentAuth-style `402 Payment Required`.
- A ChatGPT/Codex-compatible Sphere Fragment Authoring Skill package.
- Tests for validation, preparation, discovery generation, and paid-access server behavior.

Strategic deployment posture:

- Private sandbox for draft preparation, validation, review, and testing.
- Publisher-owned Sphere Nodes for real publication.
- Optional `sphere.pub` ancillary services for registry, payment coordination, analytics, trust signals, MCP, and ChatGPT access.
- Managed public hosting is a possible future product mode, not a protocol assumption.

Product focus:

- Sphere v0 should prove **Fragment Intelligence**, not live monetization.
- The first user value is preparing, validating, reviewing, simulating, and understanding agent-readable fragments.
- Payment, payout, and live revenue are important, but should follow evidence that publishers want to transform and inspect their corpus.
- Avoid building a full payment marketplace before validating the fragment preparation and intelligence workflow.

North-star v0 statement:

> Transform publisher content into agent-readable fragments, then show how those fragments would be read, licensed, cited, governed, and monetized by AI agents.

---

## Phase 1 — Solidify the Fragment Protocol

Goal: make the fragment format stable enough for early users and agents.

Tasks:

- Finalize `sphere.json` required and optional fields.
- Add examples for text, dataset, media, and multi-source fragments.
- Add relation examples: `cites`, `extends`, `responds_to`, `updates`, `contradicts`, `supports`, `part_of`, `derived_from`.
- Expand validation errors into actionable messages.
- Add schema export, ideally JSON Schema.
- Add versioned migration notes for future format changes.
- Keep the Agent Skill aligned with the canonical format.

Exit criteria:

- A publisher can prepare and validate realistic fragments from common sources without manual interpretation of the spec.

---

## Phase 2 — Fragment Intelligence MVP

Goal: let publishers understand whether their content is ready for agent consumption before deploying real infrastructure or accepting live payments.

Tasks:

- Generate fragment readiness reports from `sphere.json`, `content.md`, sources, data, media, license, access policy, and relations.
- Score or label missing metadata, weak provenance, unclear rights, absent media descriptions, missing relations, and risky licensing.
- Simulate agent discovery, preview, paid unlock, citation, and retrieval behavior without requiring real payments.
- Estimate monetization scenarios from declared price and simulated demand.
- Expose a local `GET /publisher/summary` focused on readiness, simulated usage, and estimated value.
- Add tests for readiness checks, simulated analytics, and summary output.
- Document which metrics are observed, simulated, estimated, or future live-payment metrics.

Exit criteria:

- A publisher can ask: "Are my fragments ready for agents, what risks do they carry, and what value might they have?"

Reference:

- [publisher-intelligence.md](publisher-intelligence.md)

---

## Phase 3 — Private Sandbox

Goal: provide a low-friction private environment for preparing, validating, reviewing, and testing fragments before publication.

Tasks:

- Define sandbox states: `draft`, `validated`, `needs_review`, `approved_for_export`, `published_elsewhere`.
- Add sandbox quotas for draft count, storage, conversions, review checks, and retention.
- Add private draft storage semantics.
- Add export flow from sandbox to a publisher-owned Sphere Node.
- Add clear labels that sandbox fragments are not publicly listed, monetized, or published.
- Add rights and review checks before export.
- Add synthetic payment, citation, usage, and analytics test mode.
- Add a conversational Fragment Intelligence report through MCP/ChatGPT when available.

Exit criteria:

- A user can prepare and test a fragment privately before deploying or publishing to a Sphere Node.

Reference:

- [governance-and-deployment.md](governance-and-deployment.md)

---

## Phase 4 — MCP and ChatGPT Access

Goal: make Sphere analytics and authoring usable through ChatGPT and other LLMs without single-vendor lock-in.

Tasks:

- Define a Sphere MCP server with tools for fragment validation, preparation, sandbox workflows, publishing/export, and analytics.
- Add Fragment Intelligence tools:
  - `analyze_fragment_readiness`
  - `find_fragment_risks`
  - `simulate_agent_access`
  - `estimate_fragment_value`
  - `generate_fragment_report`
- Add publisher analytics tools:
  - `get_publisher_summary`
  - `get_fragment_usage`
  - `get_revenue_breakdown`
  - `get_top_fragments`
  - `get_payout_statement`
  - `generate_publisher_report`
- Add ChatGPT App metadata and optional widget UI.
- Keep all tools usable by non-ChatGPT MCP clients.
- Add explicit auth and permission boundaries for publisher data.

Exit criteria:

- A publisher can use ChatGPT or another MCP-capable client to prepare fragments, inspect readiness, simulate agent access, and query usage or revenue data.

---

## Phase 5 — Cloudflare Node Deployment

Goal: move from local demo to a real self-hosted Sphere Node that a publisher can deploy in its own Cloudflare account.

Tasks:

- Implement Cloudflare Workers for ingestion, paid access, and analytics.
- Store fragments and media in R2.
- Store metadata, events, revenue entries, consumers, and publishers in D1.
- Use Queues for async event processing and payout reconciliation.
- Generate and serve discovery HTML through Pages/R2.
- Add deployment scripts and environment documentation.
- Add staging and production environments.
- Document node ownership, domain setup, quotas, and operational responsibilities.

Exit criteria:

- A real publisher can deploy and operate its own Sphere Node.

Reference:

- [infrastructure.md](infrastructure.md)
- [governance-and-deployment.md](governance-and-deployment.md)

---

## Phase 6 — Payment and Receipts

Goal: replace simulated payment behavior with real payment verification and accounting after Fragment Intelligence proves useful.

Tasks:

- Implement MPP / PaymentAuth-compatible challenge and credential verification.
- Keep Sphere fallback token flow for clients that cannot speak PaymentAuth yet.
- Add signed payment receipts.
- Add idempotency support.
- Reconcile paid access events with revenue ledger entries.
- Prepare Stripe Connect publisher payout flow.
- Document compatibility with x402-style clients where useful.

Exit criteria:

- Paid fragment access can be verified, logged, receipted, and attributed.

Reference:

- [payment-flow.md](payment-flow.md)

---

## Phase 7 — Publisher Onboarding and Governance

Goal: make self-hosted Sphere Nodes usable and trustworthy for real publishers.

Tasks:

- Add publisher accounts and API keys.
- Add corpus and series management.
- Add contributor attribution declarations.
- Add license and policy presets.
- Add exportable monthly statements.
- Add privacy guarantees for analytics.
- Add deletion, takedown, and `410 Gone` behavior.
- Add docs for publisher responsibilities.
- Add rights declaration and review metadata.
- Add role-based access control and scoped service credentials.
- Add node-level quota configuration.

Exit criteria:

- A publisher can onboard, publish, inspect usage, and receive a payout statement.

Reference:

- [governance-and-deployment.md](governance-and-deployment.md)

---

## Phase 8 — Quality, Discovery, and Market Signals

Goal: make fragments more valuable than raw web pages.

Tasks:

- Generate particles from fragments: claims, citations, definitions, evidence, table rows, media annotations.
- Add quality and reliability signals.
- Add constellation-level discovery pages.
- Add ranking signals for agent consumers.
- Add usage-based recommendations for publishers.
- Add citation and usage receipt support from cooperating consumers.

Exit criteria:

- Agent consumers can choose higher-quality, better-structured fragments and publishers can improve content based on demand.

---

## Near-Term Backlog

Recommended next tasks:

1. Add a local Fragment Intelligence report command or endpoint.
2. Implement readiness checks for provenance, license, media descriptions, relations, and access policy.
3. Add sandbox state and export concepts to `sphere.json` or a sandbox metadata wrapper.
4. Implement local simulated usage ledger in `scripts/sphere_demo_server.py`.
5. Add dataset and media fragment examples.
6. Add JSON Schema for `sphere.json`.
7. Draft MCP tool schemas for authoring, sandbox workflows, and publisher intelligence.
8. Create a minimal ChatGPT App plan around the MCP server.
