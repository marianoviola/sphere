# Publisher Intelligence

> How publishers understand fragment readiness, simulated agent use, future usage, revenue, attribution, and payouts through ChatGPT, other LLMs, MCP tools, and APIs.

---

## Purpose

Sphere should let a publisher ask:

- Are my fragments ready for agent consumption?
- Which fragments have weak provenance, licensing, or media descriptions?
- How would an agent discover, preview, cite, and retrieve these fragments?
- Which fragments look valuable before live monetization exists?
- Which fragments were used this week?
- How much did each fragment earn?
- Which corpus, series, or constellation is growing fastest?
- Which fragments get many previews but few paid unlocks?
- Which contributors generated the most attributed revenue?
- Which media or data sources are preserved but rarely retrieved?
- What should I publish or repackage next?

The interface can be a dashboard, but the deeper goal is agent-readable business intelligence. In v0 this should focus on **Fragment Intelligence**: readiness, risk, simulation, and estimated value. Live usage, revenue, attribution, and payout reporting can follow as the market for paid agent access matures.

A publisher should be able to query Sphere through ChatGPT, Claude, Codex, custom agents, MCP clients, API clients, or scheduled reports without becoming dependent on a single LLM vendor.

---

## v0 Focus — Fragment Intelligence

Sphere v0 should answer:

> Are these fragments ready for AI agents, and what would make them more valuable?

Initial intelligence dimensions:

| Dimension | Questions |
|---|---|
| Readiness | Is the fragment valid, structured, and agent-readable? |
| Provenance | Are sources, canonical URLs, authors, and transformations declared? |
| Rights | Is the license explicit? Is LLM retrieval/training allowed or restricted? |
| Media | Are images, audio, and video described or transcribed? |
| Data | Are datasets preserved with schema, caveats, and row/context notes? |
| Relations | Does the fragment cite, support, extend, or belong to a constellation? |
| Access | Is the policy clear: free, metered, paid, or sponsored? |
| Value | What demand or price scenario would make this fragment worth publishing? |

These reports can be generated before any live payment network exists.

---

## Principle

Sphere should distinguish observed access, simulated access, estimated value, and inferred use.

| Signal | Meaning | Certainty |
|---|---|---|
| `ready` | Fragment passes readiness checks | Deterministic validation plus heuristic review |
| `simulated_discovery` | A test agent or local server simulated discovery | Synthetic |
| `estimated_value` | Revenue scenario based on price and assumed demand | Estimated |
| `discovered` | A discovery page or manifest was requested | Certain |
| `previewed` | A free preview was served | Certain |
| `challenged` | A paid access returned `402 Payment Required` | Certain |
| `unlocked` | Full content was served after a valid credential or token | Certain |
| `paid` | Money or prepaid credit was captured | Certain |
| `receipted` | A payment receipt was issued | Certain |
| `cited` | A consumer declared that the fragment was cited | Certain only with a consumer citation receipt |
| `influenced_answer` | The fragment likely influenced an answer | Estimated, not guaranteed |

Sphere can prove that content was requested, unlocked, and paid for once live serving exists. Before that, it can simulate flows and estimate value. It cannot prove that an external LLM used the content in its final answer unless the consumer sends a usage receipt, citation receipt, or callback.

---

## Event Ledger

Sphere should record append-only events for every meaningful interaction.

Recommended event types:

| Event | Description |
|---|---|
| `fragment_discovered` | Discovery HTML or manifest accessed |
| `preview_served` | Free preview served |
| `payment_challenged` | `402 Payment Required` returned |
| `payment_authorized` | Payment credential or fallback token accepted |
| `content_unlocked` | Full fragment served |
| `payment_receipted` | Receipt emitted after payment verification |
| `revenue_attributed` | Net revenue allocated to publisher/contributors |
| `payout_scheduled` | Revenue included in a payout batch |
| `payout_paid` | Payout completed |
| `citation_declared` | Consumer declared downstream citation or use |

Minimal event shape:

```json
{
  "event_id": "evt_...",
  "created_at": "2026-06-07T10:30:00Z",
  "publisher_id": "pub_...",
  "consumer_id": "con_...",
  "fragment_id": "2026-06-07-agent-readable-public-sphere",
  "event_type": "content_unlocked",
  "payment_profile": "mpp-paymentauth",
  "amount": 0.003,
  "currency": "USD",
  "receipt_id": "payrec_...",
  "request_id": "req_...",
  "metadata": {
    "user_agent_family": "agent",
    "source": "api"
  }
}
```

The ledger should avoid storing prompts, private end-user identities, or raw consumer content unless a publisher has a separate explicit agreement.

---

## Revenue Ledger

Usage events explain what happened. Revenue entries explain who earned what.

Recommended revenue entry:

```json
{
  "entry_id": "rev_...",
  "event_id": "evt_...",
  "fragment_id": "2026-06-07-agent-readable-public-sphere",
  "gross_amount": 0.003,
  "currency": "USD",
  "sphere_fee": 0.0006,
  "publisher_net": 0.0024,
  "contributors": [
    {
      "contributor_id": "user_123",
      "share": 1.0,
      "amount": 0.0024
    }
  ],
  "status": "settled"
}
```

This makes publisher statements auditable: each payout can be traced back to fragment access, payment receipts, and attribution rules.

---

## Publisher Analytics API

The API should expose aggregate, drill-down, and export endpoints.

Initial endpoints:

```text
GET /v1/publishers/{publisher_id}/summary
GET /v1/publishers/{publisher_id}/fragments
GET /v1/publishers/{publisher_id}/fragments/{fragment_id}/usage
GET /v1/publishers/{publisher_id}/revenue
GET /v1/publishers/{publisher_id}/payouts
GET /v1/publishers/{publisher_id}/constellations/{constellation_id}/analytics
GET /v1/publishers/{publisher_id}/reports/monthly
```

Example summary response:

```json
{
  "period": {
    "from": "2026-06-01",
    "to": "2026-06-07"
  },
  "usage": {
    "discovered": 1847,
    "previewed": 512,
    "payment_challenged": 344,
    "content_unlocked": 267
  },
  "revenue": {
    "gross": 60.7,
    "sphere_fee": 15.18,
    "publisher_net": 45.52,
    "currency": "USD"
  },
  "top_fragments": [
    {
      "fragment_id": "2026-06-07-agent-readable-public-sphere",
      "title": "Agent-readable public sphere",
      "content_unlocked": 312,
      "publisher_net": 8.4
    }
  ],
  "warnings": [
    {
      "type": "high_preview_low_unlock",
      "fragment_id": "2026-06-07-agent-readable-public-sphere"
    }
  ]
}
```

---

## MCP Tools for LLMs

Sphere should expose the same analytics through MCP tools so ChatGPT and other LLMs can answer publisher questions conversationally.

Initial tool set:

| Tool | Purpose |
|---|---|
| `analyze_fragment_readiness` | Inspect structure, provenance, license, media, data, and relations |
| `find_fragment_risks` | Identify copyright, moderation, rights, or retrieval weaknesses |
| `simulate_agent_access` | Simulate discovery, preview, unlock, and citation behavior |
| `estimate_fragment_value` | Estimate revenue scenarios without live payment data |
| `generate_fragment_report` | Produce a narrative readiness and value report |
| `get_publisher_summary` | Period-level usage and revenue summary |
| `get_fragment_usage` | Drill down into one fragment |
| `get_revenue_breakdown` | Gross, fees, net, contributor attribution |
| `get_top_fragments` | Rank fragments by access, revenue, citations, or conversion |
| `get_payout_statement` | Explain pending and completed payouts |
| `get_usage_anomalies` | Find unusual spikes, low conversion, or under-described media |
| `compare_periods` | Compare week/month/quarter performance |
| `generate_publisher_report` | Produce a narrative report with tables |

Example questions:

```text
Are these fragments ready to be consumed by AI agents?
Which fragments have copyright or licensing risk?
Simulate how an agent would discover and retrieve this fragment.
Estimate the value of this corpus under metered access.
How much did my fragments earn this month?
Which constellation generated the most paid access?
Show fragments with high discovery but low paid unlocks.
Create a monthly payout report grouped by contributor.
Which media-only fragments need better descriptions?
```

The MCP server is a portability layer. A ChatGPT App can use it, but so can Claude, Codex, local agents, or publisher automation.

---

## ChatGPT Experience

In ChatGPT, Sphere can become a publisher assistant:

1. The user asks a natural-language question.
2. ChatGPT calls Sphere MCP tools.
3. Sphere returns structured analytics.
4. ChatGPT explains trends, anomalies, and next actions.
5. A widget can show charts, tables, and drill-down controls.

The widget is useful, but optional. The canonical product surface remains the API/MCP layer, not a single chat UI.

---

## Privacy and Governance

Publisher intelligence should be useful without becoming surveillance.

Required constraints:

- Store aggregate consumer identity by default.
- Do not store prompts unless explicitly agreed.
- Do not expose private consumer details in publisher reports.
- Use signed receipts for paid access and declared citation events.
- Keep usage and revenue ledgers append-only.
- Make payout statements exportable.
- Mark inferred metrics clearly as estimates.

---

## Initial Implementation

The local prototype should add:

1. Fragment readiness checks.
2. Risk and missing-metadata reports.
3. Simulated discovery, preview, 402 challenge, paid unlock, citation, and receipt events.
4. Estimated revenue scenarios for demo fragments.
5. `GET /publisher/summary` in the demo server.
6. Future MCP tools mapping to the same readiness and summary data.

This gives Sphere a credible first answer to:

> Are my fragments ready for agents, what risks do they carry, and what could they be worth?
