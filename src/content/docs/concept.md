---
title: Concept
description: Why Sphere exists, the public sphere problem, fragments as relational units, and the revenue-model vision.
status: vision
order: 1
note: This document describes the concept and direction behind Sphere, including a future revenue model. It is not a description of shipped v1 features.
---

# Concept

> Why Sphere exists and what problem it solves.

---

## The Problem

LLM systems — RAG pipelines, AI agents, research tools — consume web content at scale. Most of this consumption is invisible to publishers:

- No visibility into which systems are accessing their content
- No way to gate access based on quality or value
- No mechanism to charge for structured, high-value content
- No revenue attribution to the contributors who created the content

Existing solutions are partial:

| Solution | What it does | What it misses |
|---|---|---|
| Cloudflare Pay Per Crawl | Charges at the CDN edge | No content structure, no quality tiers, no attribution |
| `robots.txt` / `llms.txt` | Signals intent | Not enforceable |
| Paywalls | Gates access | Not designed for machine consumers |
| Training data licensing | B2B contracts | Not real-time, not per-item |

---

## The Insight

HTTP already has everything needed to solve this:

- **200** — here is the content
- **402** — payment required before I give you the content
- **HTTP authentication** — payment challenges and credentials in standard headers
- **HTML meta tags** — machine-readable metadata at the discovery layer

The 402 status code was defined in RFC 2616 (1999) as "Payment Required" and reserved for future use. MPP / PaymentAuth gives that status code practical semantics through a `Payment` HTTP authentication scheme: the server challenges, the agent pays or authorizes payment, then retries with a payment credential or receipt.

Sphere is not the payment protocol. Sphere is a structured content/access layer that can use MPP / PaymentAuth for payment, then add the content semantics that generic payment protocols do not provide: fragments, provenance, licensing, quality signals, and contributor attribution.

---

## The Public Sphere

Sphere is named after the public sphere: the shared civic space where information circulates, is evaluated, cited, challenged, and turned into collective knowledge.

As AI agents become intermediaries between people and published knowledge, that public sphere needs machine-readable infrastructure. Sphere treats content as something more than crawlable text: it is a fragment with provenance, policy, price, licensing, and attribution.

The goal is not to hide knowledge behind opaque paywalls. The goal is to make access explicit: what exists, who made it, how it may be used, what it costs, and who should be credited or paid when it is consumed.

Sphere uses "fragment" deliberately. In Walter Benjamin's method of montage and constellation, fragments do not become meaningful by pretending to be total; they become meaningful through arrangement, citation, juxtaposition, and relation. Sphere borrows that intuition for machine-readable public knowledge: a fragment is bounded enough to be accessed, licensed, paid for, cited, and audited, but open enough to connect to other fragments.

Fragments are therefore not isolated content packages. They are particles of public knowledge that can form constellations.

---

## Fragments and Constellations

Sphere distinguishes editorial structure from semantic structure:

**Corpus** is administrative: the publisher-owned body of fragments.

**Series** is editorial: a sequence, often chronological.

**Fragment** is atomic: the publishable unit with content, provenance, license, access policy, and payment metadata.

**Relation** is semantic: a typed edge such as `cites`, `extends`, `responds_to`, `updates`, `contradicts`, or `supports`.

**Constellation** is interpretive: a meaningful arrangement of fragments around a question, theme, controversy, or public problem.

This keeps Sphere faithful to the idea of a public sphere: knowledge is not just stored, but made available for relation, contestation, and recomposition.

---

## Positioning

**Not a CMS.** Sphere does not help publishers write or manage content. It assumes content already exists and adds a monetisation and distribution layer on top.

**Not a CDN.** Sphere does not serve content to humans. It serves Markdown to machines.

**Not a replacement for Cloudflare Pay Per Crawl.** CF Pay Per Crawl operates at the edge, charges per HTTP request regardless of content, and requires no code changes. Sphere operates at the content layer, charges per logical content unit, and provides structured access with licensing metadata. The two are complementary.

**Not a single-vendor agent workflow.** Sphere can be operated through MCP tools, CLI, API clients, ChatGPT, Claude, custom agents, or publisher automation. No agent vendor is part of the core protocol.

**Sandbox first, node-based for publication.** Sphere can provide a private sandbox for preparing, validating, reviewing, and testing fragments. Real publication should work through publisher-owned Sphere Nodes by default. `sphere.pub` can provide ancillary services such as registry, payment coordination, analytics, trust signals, MCP tools, and ChatGPT access. Managed public hosting may evolve later, but it should not define the core protocol.

**A broker, not a platform.** Sphere does not own content. It manages access, meters consumption, and distributes revenue. The content and the publisher relationship remain independent.

---

## The Market

Three types of agent consumers are willing to pay for structured, licensed content:

**RAG pipeline builders** need fresh, verified, structured content from specific domains. Unstructured HTML is expensive to clean. Licensed Markdown is ready to chunk and embed.

**AI agents doing product research** need aggregated signals, not individual pages. A fragment with REIM scores, reliability tiers, and phase-organised reviews is worth more than the sum of individual review pages.

**Enterprise AI teams** building vertical assistants need content with explicit licensing. Training on content with `llm_training: false` is a legal risk. Sphere surfaces this metadata before access.

---

## The Revenue Model

```
Agent consumer pays  →  Sphere takes fee (20–30%)
                   →  Remainder attributed to content contributors
                   →  Contributors paid monthly
```

Attribution is content-quality-weighted: higher-quality content (higher Reliability Score, more verified, more cited) earns a proportionally larger share.

---

## Strategic Bets

1. **Machine payment protocols will become standard** as LLM agents become economically autonomous. Sphere should ride that standardisation instead of competing with it, using MPP / PaymentAuth as the primary HTTP payment layer and mapping to x402-compatible flows where useful.

2. **Structured, licensed content will command a premium** over commodity web content. Publishers who structure their content early will capture disproportionate value.

3. **Agent consumers will prefer verified data** over unverified web content as AI systems compete on factual accuracy. Reliability tiers become a pricing signal.
