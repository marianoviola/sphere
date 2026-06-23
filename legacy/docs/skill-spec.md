---
title: Sphere Fragment Authoring Skill
description: An earlier Agent Skill specification for fragment authoring, validation, and publishing.
summary: An earlier Agent Skill spec, now superseded by the plugin.
status: vision
order: 11
note: This specifies an earlier Agent Skill design, now superseded by the sphere-plugin. Its payment, Stripe, and monetization references are not shipped.
---

# Sphere Fragment Authoring Skill

## What is Sphere

Sphere is a headless publishing and access layer for LLM distribution. Publishers author minimal content packages (fragments). Sphere ingests, transforms, and exposes them via HTTP to agent consumers. (Planned, not in v1: consumers pay per access or via subscription, and publishers receive a revenue share through a payment provider.)

Sphere is agent-vendor-neutral. There does not need to be a dashboard: authoring, validation, publishing, monitoring, analytics, and payments can happen through Agent Skills, MCP tools, CLI, API clients, ChatGPT, Codex, Claude, custom agents, or publisher automation. No single assistant vendor is part of the core protocol.

Sphere is also payment-protocol-neutral at the content layer. Paid fragment access should prefer MPP / PaymentAuth, while Sphere-specific prepaid tokens are a fallback for clients or deployments that need simpler accounting.

This skill follows the Agent Skills pattern: it should be portable across compatible agent environments. Product-specific installation, file access, MCP availability, and publishing permissions may vary, so always degrade gracefully:

- If publishing tools are available, prepare, validate, preview, and publish after confirmation.
- If publishing tools are not available, prepare and validate local fragment files or in-memory artifacts.
- If file access is unavailable, return a structured fragment preview and the exact `sphere.json` / `content.md` content for the user or calling app to persist.

---

## What is a Sphere Fragment

A Sphere fragment is a **minimal authoring unit** — a folder with a manifest and a Markdown file. It is the input to the Sphere pipeline. Sphere produces all downstream artifacts (summary, metadata, llm_hints, translated versions, discovery HTML). The publisher authors only what a human can reasonably write.

```
{fragment_id}/
  sphere.json      ← manifest: identity, access policy, license
  content.md       ← full content in clean Markdown
  media/           ← images, audio (optional)
    cover.jpg
    audio.mp3
```

---

## Core Workflow

Think in three separable operations:

1. **Prepare fragments** — convert source content into `sphere.json`, `content.md`, and optional media references.
2. **Validate fragments** — check schema, IDs, headings, links, media references, access policy, license, and payment metadata.
3. **Publish fragments** — call Sphere API/MCP/CLI only after the user approves the preview.

Preparation and validation are useful even when publishing is unavailable. Do not collapse these stages into one automatic publish action.

---

## Design Constraints

These constraints are fixed and must be respected in every interaction.

**Fragment atomicity.** A fragment is an autonomous unit. It can be published, updated by replacing its files, or removed entirely. It cannot be merged into a parent fragment or aggregated into a super-fragment. The corpus → series → fragment hierarchy is navigation and policy inheritance only — not semantic containment.

**Agent-only consumers.** Sphere content is consumed by LLMs and automated systems. Never design output for human readers. The discovery HTML is machine-readable. The content Markdown is LLM-optimized.

**Agent-neutral operations.** Operations can go through the Sphere API, MCP server, CLI, or local file workflow and can be driven by any compatible agent or automation layer. The user configures credentials once in the chosen client; the client handles the workflow.

**Always preview before write or publish.** Every fragment or corpus generation ends with a human-readable preview for user confirmation. Never publish, update, delete, or mutate existing user content without explicit user approval.

**Preserve source meaning.** Normalize structure and metadata, but do not summarize, rewrite, invent sources, alter claims, or infer rights aggressively. If transformation is needed for machine readability, show what changed.

---

## sphere.json — Input Manifest Schema

```json
{
  "sphere_version": "0.4.0",
  "fragment_id": "string — slug: {yyyy}-{mm}-{dd}-{title-slug}",

  "identity": {
    "title": "string",
    "author": {
      "name": "string",
      "url": "string | null"
    },
    "canonical_url": "string | null",
    "language": "ISO 639-1 — e.g. it, en, fr",
    "type": "post | episode | document | dataset"
  },

  "hierarchy": {
    "series_id": "string | null",
    "position": "integer | null"
  },

  "access": {
    "policy": "free | metered | paid | sponsored",
    "preview_chars": 500,
    "price_per_access": null,
    "currency": "USD",
    "sponsor": {
      "name": "string | null",
      "url": "string | null",
      "disclosure": "string | null"
    }
  },

  "content_flags": {
    "nsfw": false,
    "nsfw_categories": [],
    "age_restriction": null
  },

  "license": {
    "type": "CC-BY | CC-BY-NC | CC-BY-NC-ND | proprietary",
    "llm_retrieval": true,
    "llm_training": false,
    "llm_citation_required": true
  }
}
```

Everything else — summary, metadata, tags, entities, llm_hints, word count, reading time — is generated by Sphere during processing.

---

## content.md — Conventions

- Pure Markdown, no HTML
- Headings start at `##` (H1 reserved for title in manifest)
- Images referenced as `![alt](media/filename.ext)`
- Code blocks with language tag
- No inline styling

---

## Source Structure — Corpus with Series

A publisher can organize content as a corpus with multiple series. Sphere maps folder structure to hierarchy automatically.

```
publisher-root/
  sphere-corpus.json
  series-martech/
    sphere-series.json
    2026-03-27-futuro-martech/
      sphere.json
      content.md
    2026-03-20-altro-post/
      sphere.json
      content.md
  series-premium/
    sphere-series.json
    2026-03-10-analisi/
      sphere.json
      content.md
```

### sphere-corpus.json

```json
{
  "sphere_version": "0.4.0",
  "corpus_id": "string — slug or UUID",
  "publisher": {
    "name": "string",
    "url": "string | null",
    "sphere_publisher_id": "string — assigned by Sphere on registration"
  },
  "default_license": {
    "type": "CC-BY-NC",
    "llm_retrieval": true,
    "llm_training": false,
    "llm_citation_required": true
  },
  "default_access": {
    "policy": "free"
  }
}
```

### sphere-series.json

```json
{
  "sphere_version": "0.4.0",
  "series_id": "string",
  "title": "string",
  "description": "string | null",
  "language": "ISO 639-1",
  "access_override": null
}
```

---

## HTTP Exposure — How Sphere Serves Content

### Two Separate Endpoints

```
https://sphere.publisher.example/   ← discovery layer — HTML only, always 200
https://content.publisher.example/  ← content layer — Markdown, 200 or 402
  free/                             ← static, fully cacheable, no auth
  paid/                             ← token-gated, metered, logged
```

These endpoints belong to a publisher-controlled Sphere Node. A private sandbox may expose temporary test URLs, but sandbox URLs are not public publication endpoints. The discovery layer is fully cacheable and always accessible. A bot reads it to build a complete index of what exists, what it costs, and how to navigate — without paying anything.

The content layer is split by access policy. `/free/` is stateless and can be served directly from R2 or S3 with no application logic. `/paid/` is the only layer that validates tokens, registers consumption events, and generates revenue.

### Fragment index.html — Discovery

```html
<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <title>Il futuro del MarTech — Mariano Viola</title>
  <link rel="canonical" href="https://sphere.publisher.example/series-martech/2026-03-27-futuro-martech/">

  <!-- Sphere identity -->
  <meta name="sphere:fragment_id"    content="2026-03-27-futuro-martech">
  <meta name="sphere:version"      content="0.4.0">
  <meta name="sphere:publisher_id" content="pub_abc123">

  <!-- Access policy -->
  <meta name="sphere:access:policy"        content="metered">
  <meta name="sphere:access:preview_chars" content="500">
  <meta name="sphere:access:price"         content="0.002">
  <meta name="sphere:access:currency"      content="USD">
  <meta name="sphere:payment:profile"      content="mpp-paymentauth">
  <meta name="sphere:payment:method"       content="stripe">
  <meta name="sphere:payment:endpoint"     content="https://api.publisher.example/v1/pay">

  <!-- Content flags -->
  <meta name="sphere:nsfw"                 content="false">

  <!-- License -->
  <meta name="sphere:license"          content="CC-BY-NC">
  <meta name="sphere:llm_retrieval"    content="true">
  <meta name="sphere:llm_training"     content="false">
  <meta name="sphere:llm_citation"     content="true">

  <!-- Content files -->
  <link rel="sphere:content"  type="text/markdown"    href="https://content.publisher.example/paid/series-martech/2026-03-27-futuro-martech.md">
  <link rel="sphere:manifest" type="application/json" href="sphere.json">

  <!-- Navigation -->
  <link rel="up"   href="../index.html" title="Serie: MarTech">
  <link rel="prev" href="../../2026-03-20-altro-post/index.html">
  <link rel="next" href="../../2026-04-01-prossimo-post/index.html">
  <link rel="home" href="../../index.html">

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Il futuro del MarTech",
    "author": { "@type": "Person", "name": "Mariano Viola" },
    "datePublished": "2026-03-27",
    "inLanguage": "it",
    "isAccessibleForFree": false,
    "hasPart": {
      "@type": "WebPageElement",
      "isAccessibleForFree": true,
      "cssSelector": ".preview"
    }
  }
  </script>
</head>
<body>
  <p class="preview">I primi 500 caratteri del contenuto sono disponibili liberamente...</p>
</body>
</html>
```

### Payment Flow

```
1. BOT reads index.html
   → knows: policy, price, payment profile, method, license

2. BOT requests content
   GET https://content.publisher.example/paid/series-martech/2026-03-27-futuro-martech.md

3. SPHERE responds 402
   HTTP/1.1 402 Payment Required
   WWW-Authenticate: Payment id="pay_123",
     realm="publisher.example",
     method="stripe",
     intent="charge",
     request="{base64url-json-payment-request}"

4. BOT pays or authorizes payment using the selected MPP method

5. BOT re-requests with a Payment credential
   GET .../paid/2026-03-27-futuro-martech.md
   Authorization: Payment id="pay_123",
     method="stripe",
     payload="{base64url-json-payment-credential}"

6. SPHERE verifies payment, logs access, and responds 200 — full Markdown content
   Payment-Receipt: {receipt_reference}
```

### HTTP Status Codes

| Status | Meaning |
|---|---|
| `200` | Free content or valid payment credential / fallback token — full content returned |
| `402` | Payment required — `WWW-Authenticate: Payment` carries the payment challenge |
| `401` | Payment credential or fallback token invalid or expired |
| `410` | Fragment deleted — remove from index |
| `404` | Fragment not found |

---

## Sphere Processing Pipeline

After receiving a publish call through any supported interface, Sphere runs internally:

```
1. VALIDATE   → check manifest schema, required fields
2. INHERIT    → merge corpus/series defaults into fragment manifest
3. PARSE      → convert content.md to internal AST
4. ENRICH     → generate summary, extract entities and tags,
                 compute word_count, reading_time, llm_hints,
                 classify nsfw if flagged
5. SPLIT      → route content to /free/ or /paid/ endpoint
6. DISCOVER   → generate index.html for discovery layer
7. INDEX      → update catalog and search index
8. NOTIFY     → return status to the requesting client via MCP/API
```

---

## Interfaces — Tool Reference

Sphere capabilities may be exposed through MCP tools, CLI commands, API clients, or ChatGPT/Codex skill runtimes. Use whatever interface is available in the current environment. The names below describe the logical operations; concrete tool names may vary by client.

### Publishing

```
sphere_publish_fragment(
  manifest: object,       ← sphere.json content
  content: string,        ← content.md text
  media?: file[]          ← optional media files
) → { fragment_id, status, sphere_endpoint, processing_time_ms }

sphere_update_fragment(
  fragment_id: string,
  fields: {
    manifest?: object,    ← partial manifest update
    content?: string,     ← full content replacement
    media?: file[]
  }
) → { fragment_id, status, updated_at }

sphere_delete_fragment(
  fragment_id: string
) → { fragment_id, deleted_at }
  ← Sphere sets status to deleted, returns 410 on all content requests

sphere_get_status(
  fragment_id: string
) → { fragment_id, status, sphere_endpoint, published_at, updated_at }

sphere_list_corpus(
  publisher_id?: string   ← defaults to authenticated publisher
) → { corpus_id, series[], fragment_count, last_updated }
```

### Analytics & Earnings

```
sphere_get_earnings(
  period?: "mtd | ytd | {yyyy-mm}"   ← default: current month
  series_id?: string,
  fragment_id?: string
) → {
    period,
    pay_per_access: number,
    sponsored: number,
    total: number,
    pending_payout: number,
    next_payout_date: string
  }

sphere_get_consumption(
  period?: string,
  series_id?: string,
  fragment_id?: string
) → {
    total_requests: number,
    breakdown: { free, paid, sponsored },
    consumers: { llm_retrieval, aggregators, direct_api }
  }

sphere_get_top_content(
  limit?: number,          ← default: 10
  period?: string,
  metric?: "requests | revenue"
) → [ { fragment_id, title, requests, revenue } ]

sphere_list_transactions(
  limit?: number,
  before?: string          ← ISO datetime for pagination
) → [ { transaction_id, fragment_id, consumer_id, amount, currency, timestamp } ]
```

### Payment Settings — Stripe Connect

```
sphere_connect_stripe()
→ { onboarding_url: string }
  ← Sphere generates a Stripe Connect Express onboarding URL.
     User completes KYC and IBAN on Stripe directly.
     Sphere never handles funds — Stripe manages transfers.

sphere_get_payment_settings()
→ {
    stripe_account_id: string | null,
    stripe_status: "not_connected | pending | active",
    payout_schedule: { frequency, minimum_amount, currency },
    next_payout_date: string | null
  }

sphere_set_payout_schedule(
  frequency: "monthly | weekly",
  minimum_amount: number,
  currency?: "USD | EUR"   ← default: USD
) → { schedule_updated: true, next_payout_date }

sphere_get_pending_payout()
→ { amount: number, currency: string, available_from: string }

sphere_request_payout()
→ { payout_id, amount, currency, estimated_arrival }
  ← Only available if Stripe account is active and
     pending amount exceeds minimum threshold.

sphere_list_payouts(
  limit?: number
) → [ { payout_id, amount, currency, status, paid_at } ]
```

---

## Agent Workflow — How to Build and Publish a Sphere Fragment

### Step 1 — Understand the input

Identify:
- Input type: single file, single folder, folder with sub-folders?
- Content type: post, episode, document, dataset?
- Author and language (infer from content if not stated)
- Canonical URL if imported
- Access policy — may be declared per folder: "i contenuti in /blog sono free, in /premium sono paid"

If access policy or license is ambiguous, ask. Do not guess.

### Step 2 — Map structure

If input is a folder with sub-folders:

```
root folder  → corpus   (sphere-corpus.json)
sub-folder   → series   (sphere-series.json)
leaf folder  → fragment   (sphere.json + content.md)
```

Apply access policy per directory. Fragments inherit from series and corpus, override only what differs.

### Step 3 — Generate fragment_ids

Slug format: `{yyyy}-{mm}-{dd}-{title-slug}`. Infer date from content or metadata. Fall back to today.

### Step 4 — Write content.md

Clean Markdown, full content, no summarization.

### Step 5 — Write manifests

`sphere.json` per fragment, `sphere-series.json` per series, `sphere-corpus.json` for root. Apply inheritance.

### Step 6 — Show human-readable preview

```
Corpus: my-publisher
  Licenza default: CC-BY-NC  |  llm_retrieval: true  |  llm_training: false

  series-martech/     → 3 fragment  |  policy: free
    2026-03-27-futuro-martech     1.240 parole  |  free
      ## Introduzione
      ## Il problema del dato di prima parte
      ## Conclusioni
    2026-03-20-altro-post          980 parole  |  free
    2026-03-15-terzo-post        1.100 parole  |  free

  series-premium/     → 2 fragment  |  policy: paid @ 0.002 USD
    2026-03-10-analisi           2.300 parole  |  paid
    2026-03-01-approfondimento   1.800 parole  |  paid

Totale: 5 fragment, 2 serie
Confermi la pubblicazione?
```

### Step 7 — Publish

Only after explicit confirmation. Use the available Sphere interface to publish each fragment. If corpus is new, publish corpus and series manifests first. Present the result:

```
✓ 2026-03-27-futuro-martech    pubblicato
  https://sphere.publisher.example/series-martech/2026-03-27-futuro-martech/

✓ 2026-03-20-altro-post        pubblicato
✓ 2026-03-15-terzo-post        pubblicato
✓ 2026-03-10-analisi           pubblicato
✓ 2026-03-01-approfondimento   pubblicato

5 fragment pubblicate in 4.2s
```

---

## Access Policy — Decision Guide

| Scenario | Policy |
|---|---|
| Personal blog post, no monetization intent | `free` |
| Content with brand mention and compensation | `sponsored` |
| Content behind a paywall on original platform | `paid` |
| First N chars free, full content paid | `metered` |
| Free content, pay only for automated access | `metered` with low `price_per_access` |

---

## License — Decision Guide

| Intent | License |
|---|---|
| Open, attribution required | `CC-BY` |
| Open, no commercial use | `CC-BY-NC` |
| Open, no derivatives | `CC-BY-NC-ND` |
| Retrieval yes, training no | `proprietary` + `llm_training: false` |
| Full proprietary | `proprietary` + both false |

Default if not specified: `CC-BY-NC`, `llm_retrieval: true`, `llm_training: false`.

---

## Validation Checklist

Before calling sphere_publish_fragment, verify:

- [ ] `fragment_id` is a valid slug
- [ ] `sphere.json` has all required fields
- [ ] `identity.language` is valid ISO 639-1
- [ ] `access.policy` confirmed by user
- [ ] `license.type` confirmed by user
- [ ] `content.md` contains no HTML
- [ ] Media files referenced in content.md are included
- [ ] If part of a series: `hierarchy.series_id` is set
- [ ] User has confirmed preview

---

## Example Invocations

**Publish a single fragment:**
> "Ho scritto questo post sul futuro del MarTech, pubblicalo su Sphere come contenuto free."

1. Ask: lingua? autore? URL canonico?
2. Generate manifest and content.md in memory
3. Show preview
4. On confirmation: call `sphere_publish_fragment`
5. Return published endpoint

**Transform a folder with policy per directory:**
> "Trasforma in Sphere questa cartella. I contenuti in /blog sono liberi, quelli in /premium sono paid a 0.002 USD."

1. Map folder → corpus/series/fragments
2. Apply policies per directory
3. Infer languages, generate slugs
4. Show corpus-level preview
5. Ask: nome publisher? licenza default?
6. On confirmation: publish corpus → series → fragments in order

**Update a fragment:**
> "Aggiorna questo post, ho cambiato la conclusione."

1. Identify `fragment_id` from context or ask
2. Regenerate content.md with updated content
3. Show diff summary: "Sezione ## Conclusioni aggiornata — 340 → 420 parole"
4. On confirmation: call `sphere_update_fragment`

**Remove a fragment:**
> "Rimuovi questo post da Sphere."

Show preview: "Stai per rimuovere {title} ({fragment_id}). Questa operazione è irreversibile. Confermi?"
On confirmation: call `sphere_delete_fragment`.

**Check earnings:**
> "Quanto ho guadagnato questo mese?"

Call `sphere_get_earnings()` + `sphere_get_top_content()`. Respond:

```
Marzo 2026

  Consumo totale:     1.847 richieste
    free:             1.240  (67%)
    paid:               607  (33%)

  Guadagni:
    paid access:      $ 48.20
    sponsored:        $ 12.50
    totale:           $ 60.70
    in attesa:        $ 60.70  (payout: 1 aprile)

  Top 3 contenuti:
    1. Il futuro del MarTech      312 richieste  $ 8.40
    2. Analisi approfondita       289 richieste  $ 7.80
    3. Contenuto esclusivo        201 richieste  $ 5.40
```

**Connect Stripe:**
> "Collega il mio account Stripe a Sphere."

1. Call `sphere_get_payment_settings()` — verify not already connected
2. Call `sphere_connect_stripe()` — get onboarding URL
3. Return: "Completa la configurazione su Stripe: {url}. Torna qui quando hai finito per verificare lo stato."
4. On return: call `sphere_get_payment_settings()` to confirm active status

**Set payout schedule:**
> "Imposta payout mensile con minimo 50 dollari."

Call `sphere_set_payout_schedule(frequency=monthly, minimum_amount=50)`.
Respond: "Ok, riceverai i pagamenti il primo del mese quando il saldo supera $50. Prossimo payout stimato: 1 aprile."

**Check payout history:**
> "Ho ricevuto il pagamento di marzo?"

Call `sphere_list_payouts(limit=3)`. Respond with amounts, dates, and status in plain language.
