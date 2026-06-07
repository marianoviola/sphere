# Sphere Fragment Schema Notes

Required fragment files:

```text
{fragment_id}/
  sphere.json
  content.md
```

Optional:

```text
index.html
sources/
data/
media/
```

Required manifest fields:

- `sphere_version`
- `fragment_id`
- `identity.title`
- `identity.author.name`
- `identity.language`
- `identity.type`
- `hierarchy`
- `sources`
- `relations`
- `access.policy`
- `access.preview_chars`
- `access.price_per_access`
- `access.currency`
- `content_flags.nsfw`
- `license.type`
- `license.llm_retrieval`
- `license.llm_training`
- `license.llm_citation_required`

Valid policies:

- `free`
- `metered`
- `paid`
- `sponsored`

Paid and metered fragments require `access.payment` metadata. Default profile:

```json
{
  "profile": "mpp-paymentauth",
  "method": "stripe",
  "endpoint": "https://api.publisher.example/v1/pay"
}
```

Valid content types:

- `post`
- `episode`
- `document`
- `dataset`

Content conventions:

- Pure Markdown, no HTML.
- Headings start at `##`.
- H1 is reserved for `identity.title`.
- Images use `![alt](media/filename.ext)`.
- Code fences include language tags where possible.

Optional `sources` entries:

```json
{
  "source_id": "source_1",
  "path": "sources/original.docx",
  "kind": "text | data | image | audio | video | mixed | external",
  "format": "docx | pdf | md | csv | xlsx | sql | jpg | mp3 | mp4 | url",
  "role": "primary | supporting | evidence | media | standalone",
  "transformation": "extracted | converted | summarized | transcribed | described | preserved",
  "included_in_content": true
}
```

Optional relation entries:

```json
{
  "type": "cites | extends | responds_to | updates | contradicts | supports | part_of | derived_from | translation_of | same_as",
  "target": "fragment_id or external URL",
  "description": "string | null"
}
```
