# Sphere

> Infrastructure for an agent-readable public sphere: structured Markdown fragments, explicit licensing, HTTP-native access control, and revenue attribution for contributors.

---

## What is Sphere

Sphere is a **headless publishing and access layer** for publishers who want to make their content legible, licensed, and economically accountable to agent consumers — RAG pipelines, AI agents, research tools — without inventing the protocol and infrastructure from scratch.

The name and domain, `sphere.pub`, refer to the public sphere: a shared space where information can circulate, be scrutinised, cited, and compensated. Sphere translates that idea into infrastructure for machine-mediated access.

It sits between a content corpus and the AI systems that want to consume it:

```
Publisher corpus  →  [Sphere]  →  LLM / RAG pipeline / AI agent
                                           ↓
                                     Revenue → Publisher
```

The publisher defines what is free, what is paid, and what is sponsored. Sphere prepares and validates the fragment, exposes clear access semantics, and can later coordinate payment and revenue distribution. The agent consumer gets clean, structured Markdown with explicit licensing metadata.

The first product focus is **Fragment Intelligence**: helping publishers transform content into agent-readable fragments, inspect readiness, surface rights and provenance risks, simulate agent access, and estimate potential value before live monetization is required.

Sphere starts with a **private sandbox for draft preparation** and **publisher-owned Sphere Nodes for real publication**. A publisher can use the sandbox to prepare, validate, review, and test fragments, then publish them to a node it controls. `sphere.pub` can provide optional ancillary services such as registry, payment coordination, analytics, trust signals, MCP tools, and ChatGPT access. Managed public hosting may remain out of scope or become a later product mode, but the protocol should not depend on it.

**Sphere is not:**
- A CMS or publishing platform
- A human-facing product (all consumers are automated systems)
- A replacement for Cloudflare Pay Per Crawl (it complements it)
- A single-vendor workflow tied to Claude, ChatGPT, or any one agent runtime
- A centralized CMS

---

## Why It Exists

LLM crawlers and agentic systems already consume web content at scale. Most publishers have no way to:
- Know which LLM systems are accessing their content
- Gate access by content quality or tier
- Charge for high-value, structured content
- Attribute revenue back to individual content contributors

Sphere solves all four at once, using HTTP primitives — including the 402 status code — plus machine-readable licensing and attribution metadata.

---

## Core Concepts

### Fragment

The atomic unit. A folder containing a manifest (`sphere.json`) and a Markdown file (`content.md`). Optionally includes original sources, data files, and media.

A fragment is a bounded, agent-readable unit of public knowledge. It is intentionally named after the fragmentary logic of montage and constellation: fragments become meaningful through citation, relation, and arrangement, not by pretending to be self-contained wholes.

One product, article, dataset note, media object, document, or bounded multi-source synthesis = one fragment.

### Relations and Constellations

Fragments can cite, extend, update, contradict, support, translate, or derive from other fragments or external sources. A constellation is a curated semantic arrangement of fragments around a question, theme, controversy, or public problem.

### Fragment Authoring Skill

An Agent Skills-compatible workflow that transforms user content into Sphere fragments. It can prepare and validate fragments without publishing, then publish through Sphere API/MCP/CLI only after explicit user approval. It is designed to be portable across compatible environments such as ChatGPT, Codex, API-based agents, and other Agent Skills runtimes.

### Access Policy

Every fragment has one of four policies:

| Policy | Behaviour |
|---|---|
| `free` | 200 immediately, no auth |
| `metered` | Preview free (N chars), full content requires payment |
| `paid` | Full content requires payment |
| `sponsored` | Free, but includes sponsor disclosure metadata |

### Discovery Layer

A machine-readable HTML tree, always publicly accessible, always 200. Agent consumers read this to build an index of what exists, what it costs, and how to pay — before spending any money.

### Payment Flow

HTTP-native. Sphere does not invent its own payment protocol: paid access should use MPP / PaymentAuth-style 402 challenges by default, with `WWW-Authenticate: Payment` and payment credentials or receipts carried through standard HTTP authentication headers. Sphere can still offer a simple prepaid-token fallback for publisher accounting and early integrations.

### Revenue Attribution

Revenue is attributed to the content that generated it. In corpus-based systems (like Considerum), individual contributors whose content is consumed earn proportionally more.

### Fragment Intelligence

Before live payments, Sphere can still help a publisher understand whether a fragment is useful and safe for agents: valid format, clear sources, explicit license, described media, preserved data, meaningful relations, access policy, and estimated value.

---

## Quick Start

Validate the reference fragment:

```bash
python3 scripts/sphere.py validate examples/basic-fragment
```

Expected result:

```text
Result: valid (0 warning(s))
```

The example fragment includes:

- `sphere.json` manifest with access, license, and MPP / PaymentAuth metadata
- `content.md` clean Markdown body
- `index.html` machine-readable discovery descriptor
- optional `sources`, `relations`, `data`, and `media` metadata for provenance and recomposition

Prepare a fragment from raw Markdown:

```bash
python3 scripts/sphere.py prepare examples/raw-content/agent-readable-notes.md \
  --output fragments \
  --date 2026-06-07 \
  --author "Sphere Project" \
  --policy metered \
  --price 0.003
```

Run the local demo server:

```bash
python3 scripts/sphere.py serve examples/basic-fragment
```

Default endpoints:

- `http://127.0.0.1:8765/fragments/2026-06-07-agent-readable-public-sphere/`
- `http://127.0.0.1:8765/content/paid/2026-06-07-agent-readable-public-sphere.md`

Paid content returns `402 Payment Required` until the request includes the mock MPP / PaymentAuth credential printed by the server.

Regenerate discovery HTML from `sphere.json` and `content.md`:

```bash
python3 scripts/sphere.py build-discovery examples/basic-fragment --publisher demo
```

Run tests:

```bash
python3 -m unittest discover -s tests
```

Package the ChatGPT-compatible Agent Skill:

```bash
python3 -m zipfile -c sphere-fragment-authoring.zip skills/sphere-fragment-authoring
```

---

## Document Index

| Document | Description |
|---|---|
| [concept.md](docs/concept.md) | Problem, positioning, and strategic rationale |
| [format.md](docs/format.md) | Fragment format — manifest schema, content conventions |
| [http-layer.md](docs/http-layer.md) | HTTP exposure — discovery HTML, endpoints, status codes |
| [payment-flow.md](docs/payment-flow.md) | MPP / PaymentAuth flow, fallback tokens, payment accounting |
| [monetization.md](docs/monetization.md) | Revenue model, pricing tiers, contributor attribution |
| [publisher-intelligence.md](docs/publisher-intelligence.md) | Usage analytics, revenue ledger, LLM/MCP reporting |
| [governance-and-deployment.md](docs/governance-and-deployment.md) | Sandbox, self-hosted nodes, auth, permissions, quotas, responsibility |
| [product-page.md](docs/product-page.md) | Public page positioning, sections, repo and Cloudflare plan |
| [infrastructure.md](docs/infrastructure.md) | Stack, Cloudflare components, deployment |
| [roadmap.md](docs/roadmap.md) | Project phases, near-term backlog, publishable path |
| [skill-spec.md](docs/skill-spec.md) | Extended operating spec for the Sphere Fragment Authoring workflow |

## Implementation

| Path | Description |
|---|---|
| [examples/basic-fragment](examples/basic-fragment) | Minimal valid Sphere fragment |
| [scripts/sphere.py](scripts/sphere.py) | Reference CLI for validate, serve, and build-discovery |
| [scripts/sphere_prepare.py](scripts/sphere_prepare.py) | Prepare raw Markdown as a Sphere fragment |
| [scripts/sphere_validate.py](scripts/sphere_validate.py) | Dependency-free fragment validator |
| [scripts/sphere_build_discovery.py](scripts/sphere_build_discovery.py) | Dependency-free discovery HTML generator |
| [scripts/sphere_demo_server.py](scripts/sphere_demo_server.py) | Dependency-free local demo server with mock MPP / PaymentAuth flow |
| [skills/sphere-fragment-authoring](skills/sphere-fragment-authoring) | Installable Agent Skill for ChatGPT/Codex/API fragment authoring |

---

## Version

Spec version: `0.4.0`
Last updated: 2026-06-07
