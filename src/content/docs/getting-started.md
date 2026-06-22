---
title: Getting Started
description: The shipped v1 path - install the plugin, prepare and validate fragments locally, deploy your own Node, and publish.
summary: The happy path from zero to a published fragment on your own Node.
status: shipped
order: 1
note: "This page covers only the shipped v1 path: the local Claude plugin and the self-hostable Sphere Node on Cloudflare."
---

# Getting Started

Sphere prepares your public knowledge for AI agents: it turns articles, documents, datasets, and media into licensed, provenance-aware **fragments** that you validate locally and publish to a **Node you run yourself**. Nothing here depends on a managed service - the plugin runs on your machine and the Node runs in your own Cloudflare account.

This page is the happy path, in order. Each step is shipped today.

## 1. Install the Claude plugin

The [sphere-plugin](https://github.com/marianoviola/sphere-plugin) is a Claude plugin for authoring fragments. Install it, then use it to:

- **Prepare** raw content into a fragment folder (manifest, `content.md`, sources, relations).
- **Validate** the fragment against the manifest schema and content conventions.
- **Report** readiness locally - structure, license, media descriptions, data notes, and access policy - so you can see and close the gaps before publishing.

Everything in this step happens on your machine; no fragment leaves your computer until you choose to publish it.

## 2. Deploy your own Node

The [sphere-node](https://github.com/marianoviola/sphere-node) repository is a reference Sphere Node that runs on Cloudflare (Workers, R2, D1, and KV). Use the **Deploy to Cloudflare** button in the repository's README to create your own instance in your own account.

After it deploys, **set your owner token**. The owner token authenticates the read-only owner endpoints - it is how you, and only you, inspect what your Node is doing. Store it as a secret as described in the README; do not commit it.

## 3. Publish a fragment

With a validated fragment and a running Node, publish the fragment to your Node. Once published, the Node:

- **Serves** the fragment's discovery surface and `content.md` over the shipped HTTP contract (see [HTTP Layer](/docs/http-layer/)).
- **Lets you monitor it** through the read-only owner endpoints: discovery, manifest, and access events, backed by a privacy-lean ledger.

That is the full v1 loop: prepare and validate locally with the plugin, deploy a Node you control, publish, and watch it being served - all on infrastructure you own.

## Where to go next

- [Concept](/docs/concept/) - why Sphere exists and what a fragment is.
- [Fragment Format](/docs/format/) - fragment structure and where the canonical manifest schema lives.
- [Infrastructure](/docs/infrastructure/) - the Cloudflare stack behind a Node.
