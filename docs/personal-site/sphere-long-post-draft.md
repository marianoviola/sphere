---
title: "Preparing public knowledge for AI agents"
type: "post"
status: "draft"
project: "Sphere"
canonical_url: "https://sphere.pub"
tags:
  - AI
  - publishing
  - public knowledge
  - agents
  - knowledge infrastructure
---

# Preparing public knowledge for AI agents

I have started to make public a personal project I have been exploring: **Sphere**.

Sphere began from a simple question:

> What should public knowledge look like when the first reader may be an AI agent?

The web was designed primarily for human readers. Search engines crawled it, social platforms redistributed it, and content management systems made it easier to publish. But AI agents are becoming a different kind of intermediary. They do not only index pages. They retrieve, summarize, compare, cite, rank, transform, and sometimes act on behalf of people.

That changes the problem.

If agents are going to read public knowledge, then public knowledge needs to become more explicit. Not just available, but structured. Not just visible, but accountable. Not just crawlable, but licensed, provenance-aware, citable, and understandable by machines without losing the conditions that make it trustworthy for humans.

This is the space Sphere explores.

## From pages to fragments

Sphere is an experiment in agent-readable publishing.

Its basic unit is the **fragment**: a bounded piece of public knowledge that can include content, sources, data, media, licensing, provenance, relations, and access policy.

A fragment is not meant to replace a web page. It is a different surface. It is designed for agents, retrieval systems, research tools, and knowledge workflows that need more structure than HTML usually provides.

A fragment can say:

- what the content is;
- who created it;
- where it came from;
- which sources were preserved;
- whether it can be retrieved by LLMs;
- whether it can be used for training;
- how it relates to other fragments;
- whether media and data have descriptions or caveats;
- what risks exist before publication.

This is not only a technical format. It is a way to make knowledge more accountable when machines mediate access to it.

## Fragment Intelligence first

The first focus of Sphere is not monetization.

It is **Fragment Intelligence**.

Before asking whether AI agents should pay for content, there is a more immediate question:

> Is this content ready to be read, cited, retrieved, and interpreted by AI agents?

Sphere tries to answer that question by inspecting structure, provenance, rights, media descriptions, data notes, semantic relations, and access policies.

For a publisher, author, archive, or knowledge team, this can surface practical issues:

- sources are missing;
- rights are unclear;
- media files have no descriptions;
- data exists but has no schema or caveats;
- content can be read but not cited cleanly;
- related materials are not connected;
- licensing does not say what LLM systems can or cannot do.

This is useful even before a payment network exists.

## Why Sphere

The name refers to the public sphere: the shared civic space where information circulates, is evaluated, challenged, cited, and transformed into judgment.

I am also using the term fragment deliberately. In Walter Benjamin's method of montage and constellation, fragments become meaningful through relation, juxtaposition, and citation. They do not have to pretend to be complete systems. Their value is partly in how they connect.

That is a useful metaphor for agent-readable knowledge.

An AI system should not consume an isolated blob of text with no memory of where it came from. It should encounter a fragment with provenance, rights, context, relations, and signals about how it may be used.

## Sandbox, then nodes

Sphere starts with a private sandbox model.

The sandbox is a place to prepare, validate, review, and test fragments. It is not the same as public hosting. Draft fragments should not be publicly listed, monetized, or treated as published content.

Real publication should work through publisher-controlled Sphere Nodes. That keeps responsibility closer to the publisher and avoids making Sphere a centralized content platform too early.

Longer term, `sphere.pub` may provide ancillary services: registry, analytics, payment coordination, trust signals, MCP tools, and ChatGPT access. But the protocol should not depend on a single hosted platform.

## Why now

The current AI conversation often jumps directly to training data, scraping, licensing, or paywalls.

Those are important questions. But there is another layer underneath them:

> What is the shape of knowledge when agents become part of the reading infrastructure?

Sphere is my attempt to explore that layer.

It is early, personal, and independent. The current prototype includes a public page, a fragment format, documentation, CLI tools, example fragments, a validator, and a roadmap toward sandbox workflows and publisher intelligence.

I am sharing it because I think we need more experiments at the intersection of AI, publishing, knowledge systems, and public accountability.

If AI agents are becoming readers of the public sphere, then the public sphere needs better infrastructure for agents to read responsibly.

Sphere is one small attempt in that direction.
