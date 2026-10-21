# FIGMA_LINKS.md — home

<!-- schema: v3.2 | generated: 2026-06-05T11:50:53.652Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [17153754672098888646](https://stitch.google.com/projects/17153754672098888646) |
| Design System ID | 2005644667042354169 |
| Generated | 2026-06-05T11:50:30.679Z |
| Success | 0/4 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | — | 01-home-loading | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: Request is missing required authentication credential. Expected OAuth 2 access token, login cookie or other valid authentication credential. See https://developers.google.com/identity/sign-in/web/devconsole-project. |
| content | — | 02-home-content | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: The service is currently unavailable. |
| error | — | 03-home-error | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: The service is currently unavailable. |
| empty | — | 04-home-empty | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: The service is currently unavailable. |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | — | — |
| content | — | — |
| error | — | — |
| empty | — | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-open-banking --features home --force
```