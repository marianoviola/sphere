# Governance and Deployment

> Sphere starts with a private sandbox for preparation and testing, plus publisher-owned Sphere Nodes for real publication. The sandbox may remain private-only or evolve later, but it is not the default public hosting model.

---

## Deployment Principle

Sphere should separate the protocol from ancillary services.

```text
Sphere Protocol
  -> Private Sphere Sandbox for drafts and testing
  -> Sphere Node self-hosted by the publisher for publication
  -> Optional sphere.pub ancillary services
  -> ChatGPT, MCP clients, agents, and API consumers
```

The publisher can prepare fragments in a private sandbox, validate them, review rights and risk metadata, and then publish them to a Sphere Node it controls.

`sphere.pub` may help with sandbox preparation, discovery, payment coordination, analytics, trust signals, and LLM interfaces. Public production hosting should remain node-based by default, while any future managed hosting option should be treated as an explicit product evolution rather than an assumption baked into the protocol.

---

## Private Sandbox

The private sandbox is a controlled environment for preparing and testing fragments before publication.

Allowed sandbox uses:

- Convert source materials into draft fragments.
- Validate `sphere.json`, `content.md`, sources, data, media, and relations.
- Run copyright-risk and moderation-risk checks.
- Preview discovery metadata.
- Test paid-access flows with mock or test credentials.
- Query draft analytics and publisher-intelligence flows with synthetic data.

Sandbox constraints:

- Draft fragments are private by default.
- Draft fragments are not listed in the public registry.
- Draft fragments are not monetized.
- Draft fragments should have low storage and ingestion quotas.
- Draft fragments should be deletable without archival guarantees.
- A sandbox fragment must not be treated as publicly published content.

This gives Sphere a low-friction onboarding path without forcing every early user to deploy infrastructure before understanding the value.

---

## Publisher Nodes

Publisher-owned Sphere Nodes remain the default publication model because:

- Publishers retain control over their corpus, storage, access rules, logs, and takedown process.
- Sphere avoids becoming a centralized moderation and copyright liability bottleneck.
- The protocol remains portable across Cloudflare, other serverless platforms, private infrastructure, or future hosting models.
- Agent consumers can still discover and pay for content through standard HTTP semantics.
- `sphere.pub` can remain an enabling coordination layer rather than a gatekeeping platform.

This is more faithful to the public sphere metaphor: many publisher-controlled nodes, connected by shared protocol semantics.

---

## Roles

Sphere should distinguish authorship, publication, maintenance, rights, and review.

| Role | Meaning |
|---|---|
| Author | Person or entity that created the original content |
| Publisher | Entity that publishes the fragment through a Sphere Node |
| Maintainer | User or automation that prepared or updated the fragment |
| Rights holder | Entity claiming ownership, license, or publication rights |
| Reviewer | Person or system that reviewed rights, quality, or risk |
| Consumer | Agent, RAG pipeline, research tool, or LLM client accessing fragments |

Authorship is descriptive. Publication is operational. Rights declaration is legal. Review is procedural. These should not collapse into one field.

---

## Publisher Responsibility

The publisher is responsible for:

- Declaring authorship and provenance.
- Declaring the basis for publication rights.
- Choosing the fragment license.
- Choosing the access policy and price.
- Reviewing copyright and moderation risk.
- Responding to takedown requests.
- Managing users, API keys, quotas, and publication permissions.

In the sandbox, responsibility starts earlier: the user or publisher who uploads source material is responsible for having the right to process it. Sandbox checks can assist but do not transfer responsibility to Sphere or to an LLM.

LLMs can assist review, summarization, copyright-risk detection, and metadata extraction, but they should not be treated as final legal authorities.

---

## Authentication and Permissions

A Sphere Node should support human users, automation keys, and scoped service credentials.

Recommended roles:

| Role | Permissions |
|---|---|
| `owner` | Manage node, billing, domains, users, keys, quotas |
| `admin` | Manage corpus, series, policies, reviewers |
| `editor` | Create and edit fragments |
| `reviewer` | Approve, reject, or request changes |
| `publisher` | Publish approved fragments |
| `analyst` | Read usage, revenue, and payout data |
| `consumer` | Access fragments according to policy |

Recommended scopes:

| Scope | Meaning |
|---|---|
| `fragment:read` | Read fragment metadata and content according to policy |
| `fragment:write` | Create or update draft fragments |
| `fragment:review` | Review rights, risk, and quality metadata |
| `fragment:publish` | Publish or unpublish fragments |
| `analytics:read` | Read usage and revenue analytics |
| `billing:read` | Read payouts, fees, and statements |
| `billing:write` | Configure payment and payout settings |
| `node:admin` | Manage users, domains, keys, and quotas |

ChatGPT Apps, MCP clients, CLI tools, and publisher automations should receive the narrowest scope needed for the task.

---

## Rights and Review Metadata

Fragments should carry explicit rights and review declarations.

Example:

```json
{
  "rights": {
    "declared_by": "publisher",
    "basis": "owned | licensed | public_domain | fair_use_claim | unknown",
    "rights_holder": {
      "name": "Publisher Name",
      "url": "https://publisher.example"
    },
    "source_license": "string | null",
    "copyright_risk": "low | medium | high | unknown"
  },
  "review": {
    "status": "draft | needs_review | approved | rejected | withdrawn",
    "reviewed_by": "automated | human | publisher",
    "moderation_risk": "low | medium | high | unknown",
    "notes": []
  }
}
```

These fields do not guarantee legality or truth. They make responsibility, review status, and risk explicit for publishers and consumers.

---

## Quotas

Quota enforcement exists at two levels: sandbox quotas and node quotas.

Sandbox quotas should be conservative because the sandbox is for preparation, not permanent hosting.

Recommended sandbox quotas:

| Quota | Purpose |
|---|---|
| Draft fragment count | Prevent the sandbox from becoming shadow hosting |
| Storage | Control source files, media, and datasets |
| Monthly conversions | Bound parsing, extraction, and LLM review cost |
| Review checks | Bound copyright and moderation checks |
| Retention | Delete stale drafts automatically unless exported |

Node quotas belong primarily to the publisher-controlled Sphere Node.

Recommended quota dimensions:

| Quota | Purpose |
|---|---|
| Fragment count | Prevent spam and accidental over-publication |
| Storage | Control media, dataset, and source-file growth |
| Monthly ingestions | Control conversion and review workload |
| Monthly agent requests | Control serving cost and abuse |
| Paid unlocks | Control payment and accounting volume |
| API calls | Protect MCP/API endpoints |
| Review queue | Keep human review operationally bounded |

Example:

```json
{
  "quotas": {
    "fragment_limit": 1000,
    "storage_gb": 50,
    "monthly_ingestions": 5000,
    "monthly_agent_requests": 1000000,
    "monthly_api_calls": 250000
  }
}
```

`sphere.pub` ancillary services may also have quotas for registry entries, analytics retention, payment volume, MCP calls, trust checks, and sandbox drafts.

---

## Optional sphere.pub Services

`sphere.pub` can provide useful network services around sandbox drafts and publisher-owned nodes.

Possible ancillary services:

| Service | Purpose |
|---|---|
| Private sandbox | Prepare, validate, review, and test draft fragments before publication |
| Registry | Let agent consumers discover publisher Sphere Nodes |
| Payment coordination | Coordinate MPP / PaymentAuth profiles, fallback tokens, receipts, and settlement |
| Analytics aggregation | Aggregate usage and revenue across nodes when publishers opt in |
| Trust signals | Publish verified publisher status, rights declarations, risk metadata, and reliability signals |
| MCP gateway | Provide LLM tools for analytics, registry lookup, and report generation |
| ChatGPT App | Offer a conversational interface over publisher-owned nodes |
| Schema registry | Host versioned specs, JSON Schemas, examples, and compatibility tests |
| Payout support | Coordinate statements and payout metadata when payment flows use Sphere services |

These services are optional except when a user chooses the hosted private sandbox. A publisher should still be able to operate a Sphere Node without using `sphere.pub`.

---

## Future Managed Hosting

The sandbox may remain only a private preparation environment. It may also evolve into a managed hosting product if the market proves that publishers need it.

If Sphere ever adds managed public hosting, it should be introduced as a separate deployment mode with explicit responsibilities:

- Clear publisher terms and rights declarations.
- Strict quotas and review workflows.
- Takedown and dispute processes.
- Separate labels for sandbox, managed, and publisher-hosted fragments.
- No change to the protocol requirement that publisher-owned nodes remain supported.

The protocol should not assume managed hosting. It should only require that fragments are discoverable, access-controlled, licensed, and accountable through standard Sphere semantics.

---

## Non-Goals

Sphere should not become:

- A centralized CMS.
- A universal moderation authority.
- A copyright court.
- A single-vendor ChatGPT-only workflow.
- The owner of publisher content or publisher relationships.

Sphere should define interoperable infrastructure for accountable agent-readable publishing. Managed hosting, if it ever exists, should be one implementation path rather than the identity of the project.
