---
title: Roadmap
description: What shipped in v1 and the direction beyond it.
summary: What ships today, what was deliberately left out, and where it could go.
status: vision
order: 10
note: The "Shipped in v1" section is current and real. Everything under "Direction beyond v1" is possible direction, not committed functionality or a timeline.
---

# Roadmap

> Where Sphere is now, what was intentionally left out, and where it could go next.

---

## You are here: v1 shipped (June 2026)

Sphere v1 is a bounded, self-hostable release. It is infrastructure you run, not a
service anyone operates for you.

**Shipped in v1**

- The fragment contract: the stable format and its canonical schema, which live in
  the `sphere-node` repository under `spec/`.
- A self-hostable Sphere Node on Cloudflare Workers: discovery, free content, a
  dormant `402` paid seam, and an event ledger. Deployable into your own Cloudflare
  account with the Deploy to Cloudflare button. The deployer owns the data.
- A local Claude plugin (an MCPB desktop extension): Fragment Intelligence
  (`analyze_fragment_readiness`, `generate_fragment_report`) and authoring
  (`prepare_fragment`, `validate_fragment`) that run on local files with no backend,
  plus owner-side monitoring tools (`get_publisher_summary`, `get_fragment_usage`,
  `get_payment_status`) that read your own Node.
- A public site and published documentation.

**Deliberately out of v1 (decisions, not omissions)**

- No managed or hosted Sphere service. Single-tenant, owner-deployed, by design.
- No private sandbox product. Preparation and validation happen locally in the
  plugin; there is no hosted sandbox.
- Payments are a dormant seam: the `402` challenge is present, verification is not
  wired, and no payment provider is integrated.
- The rights-and-risk detection tool is not included yet.
- No registry, marketplace, or revenue-attribution service.

---

## Principle

Prove **Fragment Intelligence** before live monetization. The first value is
preparing, validating, and understanding agent-readable fragments. Payment, payout,
and revenue follow evidence that publishers want to transform and inspect their
corpus, not before.

---

## Direction beyond v1 (vision, not committed)

These are possible directions, evidence-led and unscheduled. None of this exists today.

**Protocol depth.** More relation and fragment examples, richer validation messages,
versioned format migration notes.

**Live payment.** Replace the dormant seam with real verification and signed receipts;
reconcile paid access with a revenue ledger; prepare publisher payout. Only after
Fragment Intelligence proves useful.

**Rights and risk.** A rights-and-risk surface for fragments, pending the right
review and separation from prior obligations.

**Publisher governance.** Accounts, corpus and series management, attribution
declarations, license presets, statements, takedown and `410 Gone` behavior.

**Quality and discovery.** Particles derived from fragments (claims, citations,
definitions, evidence), quality signals, constellation-level discovery pages, and
ranking for agent consumers.

**Broader client access.** Keep the tools usable across MCP-capable clients, not a
single vendor.

---

## Near-term, concrete

The honest next decisions, not a backlog:

1. Harden and document the v1 Node and plugin from real use.
2. Decide whether and when to submit the plugin to the Connectors Directory.
3. Decide if and when live payment is worth wiring, driven by publisher evidence.
