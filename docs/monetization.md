# Monetization

> Revenue model, pricing tiers, publisher payouts, and contributor attribution.

---

## Revenue Flow

```
Agent Consumer  →  pays Sphere (Stripe prepaid credits)
                       ↓
               Sphere fee: 20–30%
                       ↓
               Publisher revenue share: 70–80%
                       ↓
               (for corpus-based publishers)
               Attribution to individual contributors
```

Sphere does not handle money directly beyond the initial consumer top-up. Publisher payouts are processed monthly via Stripe.

---

## Pricing Tiers by Access Policy

Pricing is set by the publisher per fragment or inherited from the corpus default.

| Policy | Typical price range | Notes |
|---|---|---|
| `free` | — | No charge |
| `metered` | $0.0005–$0.001 / access | Preview free, full content charged |
| `paid` | $0.001–$0.010 / access | Full content gated |
| `sponsored` | — | Free to consumer, sponsor pays publisher directly |

Price is declared in the manifest. Sphere does not enforce a maximum — publishers set their own rates. The market determines what consumers will pay.

---

## Publisher Payout

Publishers receive their accumulated revenue minus the Sphere fee at the end of each month, provided the balance exceeds the minimum threshold ($10 default, configurable).

```
Monthly payout = sum(paid_accesses × price × (1 - sphere_fee_pct))
                 for all fragments in the period
```

Payout is via Stripe — publisher connects their bank account during onboarding. Sphere uses Stripe Connect Express so it never handles publisher funds directly.

---

## Contributor Attribution

For corpus-based publishers (where multiple contributors created the content), Sphere supports per-contributor revenue attribution. This requires the publisher to declare contributor weights per fragment.

```json
// In sphere.json — optional extension
"contributors": [
  { "contributor_id": "user_123", "weight": 0.6 },
  { "contributor_id": "user_456", "weight": 0.4 }
]
```

Sphere tracks which contributors' content was accessed and allocates the publisher's revenue share proportionally. The publisher is responsible for distributing to contributors — Sphere provides the attribution data, not the payments.

Attribution is quality-weighted when the publisher provides a quality signal (e.g. Reliability Score): higher-quality contributions earn a disproportionally larger share.

---

## Analytics for Publishers

Publishers can query consumption and revenue data via API and, later, through MCP tools used by ChatGPT or other LLM clients. See [publisher-intelligence.md](publisher-intelligence.md) for the full analytics and reporting model.

```
GET /v1/publishers/{id}/analytics?period=2026-03

{
  "period": "2026-03",
  "total_requests": 1847,
  "breakdown": {
    "free": 1240,
    "metered_preview": 340,
    "paid": 267
  },
  "revenue_usd": 60.70,
  "sphere_fee_usd": 15.18,
  "net_payout_usd": 45.52,
  "pending_payout": true,
  "payout_date": "2026-04-01",
  "top_fragments": [
    { "fragment_id": "...", "title": "...", "requests": 312, "revenue": 8.40 }
  ]
}
```

---

## Consumer Pricing Model

Consumers top up a prepaid credit balance. No per-request Stripe charge (too slow). Credits are deducted synchronously at payment time.

| Tier | Credit package | Price |
|---|---|---|
| Starter | $10 | $10 |
| Growth | $50 | $47 (6% discount) |
| Scale | $200 | $180 (10% discount) |
| Enterprise | Custom | Negotiated |

Auto-top-up is available: when balance drops below a threshold, Sphere charges the consumer's card automatically.

---

## NSFW and Restricted Content

Fragments flagged as `nsfw: true` require the consumer to have verified age during registration. Sphere returns 403 (not 402) to consumers who have not completed age verification, with a link to the verification flow.

NSFW content may command higher prices — the reduced consumer pool concentrates demand.
