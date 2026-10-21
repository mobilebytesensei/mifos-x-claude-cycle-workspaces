# FIGMA_LINKS.md — terms-of-service

<!-- schema: v3.2 | generated: 2026-05-29T17:13:20.221Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [17153754672098888646](https://stitch.google.com/projects/17153754672098888646) |
| Design System ID | 2005644667042354169 |
| Generated | 2026-05-29T17:13:19.898Z |
| Success | 0/4 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| content | — | 01-terms-of-service-content | PNG ❌ | HTML ❌ | ❌ STN gate failure pre-API: STN2: prompt is 4061 chars (cap 4000) — apply the shrink ladder or split the screen |
| loading | — | 02-terms-of-service-loading | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: Resource has been exhausted (e.g. check quota). |
| error | — | 03-terms-of-service-error | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: Resource has been exhausted (e.g. check quota). |
| empty | — | 04-terms-of-service-empty | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: Resource has been exhausted (e.g. check quota). |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| content | — | — |
| loading | — | — |
| error | — | — |
| empty | — | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-open-banking --features terms-of-service --force
```