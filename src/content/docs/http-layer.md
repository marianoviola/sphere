---
title: HTTP Layer
description: Sphere discovery and content endpoints, status codes, metadata, and caching.
status: mixed
order: 3
note: The shipped HTTP contract is canonical in sphere-node (spec/node-api.md). Parts of this document describe intended behavior beyond v1.
---

# HTTP Layer

> How Sphere exposes content — discovery, access-controlled endpoints, and status codes.

---

## Two Separate Endpoints

```
https://sphere.publisher.example/          ← discovery — HTML only, always 200
https://content.publisher.example/
  free/{fragment_id}.md                         ← 200, no auth, fully cacheable
  paid/{fragment_id}.md                         ← 402 without token, 200 with token
```

These endpoints belong to a publisher-controlled Sphere Node. `sphere.pub` may maintain a registry that points agents to these URLs. A private sandbox may expose temporary test URLs, but sandbox URLs are not public publication endpoints.

The separation is operational, not cosmetic:

- The **discovery layer** is static HTML served from a CDN (Cloudflare Pages). Always 200. Fully cacheable. A bot can crawl the entire catalogue without paying a cent.
- The **free content endpoint** is a public R2-backed path. No application logic. Zero cost to serve.
- The **paid content endpoint** is a Worker. It validates tokens, logs events, and proxies R2. It is the only component with application logic.

---

## Discovery — Corpus Entry Point

```
https://sphere.publisher.example/
  index.html                          ← corpus catalogue
  series-martech/
    index.html                        ← series index
    2026-03-27-futuro-martech/
      index.html                      ← fragment descriptor
```

---

## Fragment index.html — Machine-Readable Descriptor

Not a human page. A structured document that carries all metadata an LLM needs before requesting content.

```html
<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <title>{title} — {publisher}</title>
  <link rel="canonical" href="{canonical_url}">

  <!-- Sphere identity -->
  <meta name="sphere:fragment_id"    content="{fragment_id}">
  <meta name="sphere:version"      content="0.4.0">
  <meta name="sphere:publisher_id" content="{publisher_id}">

  <!-- Access policy — read before requesting content -->
  <meta name="sphere:access:policy"        content="{free|metered|paid|sponsored}">
  <meta name="sphere:access:preview_chars" content="500">
  <meta name="sphere:access:price"         content="{price}">
  <meta name="sphere:access:currency"      content="USD">
  <meta name="sphere:payment:profile"      content="mpp-paymentauth">
  <meta name="sphere:payment:method"       content="stripe">
  <meta name="sphere:payment:endpoint"     content="https://api.publisher.example/v1/pay">

  <!-- Content flags -->
  <meta name="sphere:nsfw"                 content="false">

  <!-- License — read before ingesting -->
  <meta name="sphere:license"          content="{license_type}">
  <meta name="sphere:llm_retrieval"    content="true">
  <meta name="sphere:llm_training"     content="false">
  <meta name="sphere:llm_citation"     content="true">

  <!-- Content link -->
  <link rel="sphere:content"  type="text/markdown"
        href="https://content.publisher.example/{free|paid}/{fragment_id}.md">
  <link rel="sphere:manifest" type="application/json" href="sphere.json">

  <!-- Navigation -->
  <link rel="up"   href="../index.html">
  <link rel="prev" href="../../{prev_fragment}/index.html">
  <link rel="next" href="../../{next_fragment}/index.html">
  <link rel="home" href="../../index.html">

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "author": { "@type": "Person", "name": "{author_name}" },
    "datePublished": "{date}",
    "inLanguage": "{language}",
    "isAccessibleForFree": {true|false},
    "license": "https://sphere.pub/license/{license_type}"
  }
  </script>
</head>
<body>
  <p class="preview">{preview_text}</p>
</body>
</html>
```

---

## HTTP Status Codes

| Status | Meaning |
|---|---|
| `200` | Free content, or paid content with valid payment credential / receipt / fallback token |
| `402` | Payment required — `WWW-Authenticate: Payment` carries the payment challenge |
| `401` | Payment credential or fallback token invalid, expired, or already used |
| `410` | Fragment removed — content deleted or below quality threshold |
| `404` | Fragment not found |

---

## Payment Compatibility

Sphere is payment-protocol agnostic. Its default paid-access profile is `mpp-paymentauth`: a 402 response carries a `WWW-Authenticate: Payment` challenge, and the retry carries a payment credential in the standard `Authorization` header. When available, the server may also return a `Payment-Receipt` header for accounting and reconciliation.

Sphere-specific metadata remains useful at the discovery layer: fragment identifier, license, price, currency, payment method, and payment profile. Those fields tell agents what they are buying before they hit the paid content endpoint.

Implementations may also map the same access requirement to x402-compatible flows or a Sphere prepaid-token fallback. Those are compatibility profiles, not the core Sphere payment protocol.

The content layer should stay agent-vendor-neutral. Any client that can read HTML metadata, make HTTP requests, and satisfy a 402 payment challenge can consume Sphere content.

---

## Caching Strategy

| Endpoint | Cache | TTL |
|---|---|---|
| Discovery HTML | Cloudflare CDN | 1 hour (purged on fragment update) |
| Free content | R2 + CDN | 24 hours |
| Paid content | No cache | — |
| Payment API | No cache | — |

Paid content is never cached. Every request hits the Worker for token validation and event logging.
