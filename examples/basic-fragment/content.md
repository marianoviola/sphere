## Summary

Sphere is an infrastructure layer for publishing content that can be read, licensed, cited, and paid for by automated agents.

The fragment is the atomic unit of publication. It combines clean Markdown with a manifest that declares provenance, access policy, licensing constraints, and payment metadata.

## Why Fragments Exist

Most web content was designed for browsers and human readers. Automated systems can fetch it, but they often lose the surrounding context: who created it, what license applies, whether training is allowed, whether citation is required, and how revenue should be attributed.

A Sphere fragment makes those terms explicit before access. Discovery remains public and machine-readable, while full content can be free, metered, paid, or sponsored.

## Payment Layer

Sphere does not define a new payment protocol. Paid access should use MPP / PaymentAuth-style HTTP payment challenges by default.

When an agent requests paid content, the server can respond with `402 Payment Required` and a `WWW-Authenticate: Payment` challenge. The agent retries with an `Authorization: Payment` credential, and the server may return a `Payment-Receipt` header for accounting.

## Licensing

This example allows LLM retrieval but does not allow LLM training. Citation is required when the content is used in generated answers, summaries, or downstream research artifacts.

## Attribution

Sphere is designed to attribute value to the content that generated it. In larger corpora, revenue can be mapped back to the fragments and contributors responsible for the accessed material.
