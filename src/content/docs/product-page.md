---
title: Product Page
description: Public-facing positioning and the structure of the first Sphere page.
summary: Public-facing positioning and the structure of the first Sphere page.
status: mixed
order: 12
note: Positioning notes. Some capabilities described here are shipped (the self-hostable Node and the local plugin); others are future direction.
---

# Product Page

> Public-facing positioning for the first Sphere page.

---

## Goal

The first public page should make Sphere understandable without exposing too much unfinished infrastructure.

Primary message:

> Prepare your public knowledge for AI agents.

Supporting message:

> Sphere turns articles, documents, datasets, and media into licensed, provenance-aware fragments with readiness reports, simulated agent access, and export paths for publisher-controlled nodes.

---

## What to Present Now

Public:

- Fragment Intelligence.
- Private sandbox.
- Controlled ChatGPT access.
- Fragment format.
- Readiness report.
- Before/after transformation.
- Licensing, provenance, relations, media/data checks.
- Export path toward publisher-owned Sphere Nodes.
- Technical preview for interested builders.

Careful / secondary:

- Payment readiness.
- Future agent access control.
- Future revenue attribution.
- Future `sphere.pub` ancillary services.

Avoid as headline:

- Accepting unsolicited content uploads.
- Live monetization.
- Marketplace.
- Guaranteed AI revenue.
- Automated copyright approval.
- Fully managed content hosting.

---

## Suggested Page Sections

1. Hero: short product promise, sample visual, controlled-access CTA.
2. Before/after: messy source material becomes a Sphere fragment.
3. Fragment Intelligence report: readiness, provenance, rights, media, data, relations, estimated value.
4. Sandbox: private draft preparation and test flows.
5. Protocol path: export to publisher-owned Sphere Node, optional `sphere.pub` services.
6. Audience: publishers, researchers, archives, knowledge teams, technical builders.
7. Technical preview: CLI, validator, skill, docs.
8. CTA: request ChatGPT/sandbox access.

---

## Intake Principle

Do not ask unknown visitors to send raw content as the first interaction.

Safer first step:

```text
Request access
```

or:

```text
Request private sandbox access
```

This keeps source material inside an authenticated, permissioned workflow where the user can prepare fragments, inspect risks, and decide whether to export or publish.

---

## Repository Plan

Keep the page in this repository for now:

```text
site/
  index.html
  styles.css
  assets/
```

Reasons:

- Avoid early fragmentation.
- Keep product copy, docs, examples, skill, and demo page aligned.
- Let Cloudflare deploy only the `site/` directory while the rest of the repo remains source/docs/tooling.
- Split into a separate repository only when the website has its own team, build system, release cadence, or marketing workflow.

---

## Cloudflare Plan

Use a private GitHub repository connected to Cloudflare Pages.

Recommended Cloudflare Pages settings:

```text
Project root: site
Build command: none
Output directory: .
Production branch: main
```

If the page later becomes Astro, Next, or another framework, update only the `site/` build settings.
