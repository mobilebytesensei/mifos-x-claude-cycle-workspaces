# FIGMA_LINKS.md — profile

<!-- schema: v3.2 | generated: 2026-05-29T17:13:17.693Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [17153754672098888646](https://stitch.google.com/projects/17153754672098888646) |
| Design System ID | 2005644667042354169 |
| Generated | 2026-05-29T17:13:17.599Z |
| Success | 0/8 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | — | 01-profile-loading | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: Resource has been exhausted (e.g. check quota). |
| viewing | — | 02-profile-viewing | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: Resource has been exhausted (e.g. check quota). |
| editing | — | 03-profile-editing | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: Resource has been exhausted (e.g. check quota). |
| saving | — | 04-profile-saving | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: Resource has been exhausted (e.g. check quota). |
| saved | — | 05-profile-saved | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: Resource has been exhausted (e.g. check quota). |
| content | — | 06-profile-content | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: Resource has been exhausted (e.g. check quota). |
| empty | — | 07-profile-empty | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: Resource has been exhausted (e.g. check quota). |
| error | — | 08-profile-error | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: Resource has been exhausted (e.g. check quota). |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | — | — |
| viewing | — | — |
| editing | — | — |
| saving | — | — |
| saved | — | — |
| content | — | — |
| empty | — | — |
| error | — | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-open-banking --features profile --force
```