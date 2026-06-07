---
name: sphere-fragment-authoring
description: Use this Agent Skill to transform user-provided content into Sphere fragments. Trigger when the user asks to prepare, convert, package, validate, preview, or publish content as Sphere fragments, or mentions sphere.json, content.md, agent-readable publishing, MPP/PaymentAuth paid access, LLM retrieval/training licensing, or fragment authoring. Always preserve source meaning, show a human-readable preview, and ask for explicit approval before writing, publishing, updating, or deleting anything.
---

# Sphere Fragment Authoring

Sphere fragments package content for agent-readable discovery, licensing, access control, and attribution.

Use this skill to turn raw user content into:

```text
{fragment_id}/
  sphere.json
  content.md
  index.html
  sources/
  data/
  media/
```

## Operating Modes

Choose the safest available mode:

1. **Preview-only**: return a fragment preview plus `sphere.json` and `content.md` in the chat.
2. **Local files**: write fragment files when file access is available and the user approves.
3. **Validated local files**: run `python3 scripts/sphere.py validate {fragment_dir}` if the Sphere CLI is available.
4. **Private sandbox**: prepare, validate, review, and test draft fragments in a private sandbox when available.
5. **Publish or export**: publish to a publisher-controlled Sphere Node, or export for publication, only when Sphere API/MCP/CLI tools are available and the user explicitly confirms.

Do not publish by default.
Sandbox fragments are private drafts: they are not publicly listed, monetized, or equivalent to publication.

## Workflow

1. Understand the source content: type, language, author, canonical URL, media, and intended corpus/series.
2. Infer a fragment title and `fragment_id` only when safe; otherwise ask.
3. Normalize content into clean Markdown. H1 is reserved for the manifest title, so content headings start at `##`.
4. Build `sphere.json` with identity, hierarchy, sources, relations, access, payment, content flags, and license.
5. Show a human-readable preview before writing or publishing.
6. Validate when possible.
7. Publish or export only after explicit approval.

## Transformation Guarantees

- Preserve meaning.
- Preserve attribution and canonical links.
- Do not summarize unless the user explicitly asks.
- Do not invent sources, authors, dates, quotes, or rights.
- Do not infer paid/sponsored status aggressively.
- Do not allow LLM training unless the user explicitly approves it.
- Ask before publication, destructive updates, deletion, or irreversible operations.

## Source Handling

Use one fragment when multiple sources form one bounded act of knowledge. Use multiple fragments when sources are independently citable or need separate policy, license, attribution, access price, or relations.

Text sources (`md`, `txt`, `rtf`, `docx`, Notion exports, PDF extracts) become canonical `content.md`; preserve originals in `sources/` when possible and declare them in `sphere.json`.

Data sources (`csv`, `tsv`, `xlsx`, `sql`, `json`) should be preserved in `data/`. `content.md` should describe purpose, schema, columns, units, row count, query assumptions, caveats, and license. Do not flatten large datasets into prose.

Media sources (`image`, `audio`, `video`) should be preserved in `media/`, declared in `sources`, and described in `content.md`. If media is standalone, add a `## Media` section with captions, alt text, transcript, or description.

Use relations such as `cites`, `extends`, `responds_to`, `updates`, `contradicts`, `supports`, `part_of`, `derived_from`, `translation_of`, and `same_as` when a fragment connects to another fragment or external source.

## Access Policy Defaults

If the user does not specify policy, ask. If they ask for a draft or local fragment only, use `free` as a safe temporary default and explain that policy can be changed before publishing.

For `paid` or `metered`, include:

```json
"payment": {
  "profile": "mpp-paymentauth",
  "method": "stripe",
  "endpoint": "https://api.publisher.example/v1/pay"
}
```

## License Defaults

If the user does not specify license, ask. For drafts, use:

```json
"license": {
  "type": "CC-BY-NC",
  "llm_retrieval": true,
  "llm_training": false,
  "llm_citation_required": true
}
```

## References

- For schema details, read `references/sphere-schema.md`.
- For preview format and examples, read `examples/expected-preview.md`.
