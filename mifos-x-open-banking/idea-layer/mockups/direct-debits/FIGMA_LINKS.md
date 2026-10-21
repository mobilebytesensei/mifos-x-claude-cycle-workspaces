# FIGMA_LINKS.md — direct-debits

<!-- schema: v3.2 | generated: 2026-06-05T11:23:44.547Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [17153754672098888646](https://stitch.google.com/projects/17153754672098888646) |
| Design System ID | 2005644667042354169 |
| Generated | 2026-06-05T11:23:30.392Z |
| Success | 0/5 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | — | 01-direct-debits-loading | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: The service is currently unavailable. |
| populated | — | 02-direct-debits-populated | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: Request is missing required authentication credential. Expected OAuth 2 access token, login cookie or other valid authentication credential. See https://developers.google.com/identity/sign-in/web/devconsole-project. |
| empty | — | 03-direct-debits-empty | PNG ❌ | HTML ❌ | ❌ StitchError: Incomplete API response from generate_screen_from_text: expected object at projection path |
| cancel_confirm | — | 04-direct-debits-cancel_confirm | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: The service is currently unavailable. |
| error | — | 05-direct-debits-error | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: The service is currently unavailable. |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | — | — |
| populated | — | — |
| empty | — | — |
| cancel_confirm | — | — |
| error | — | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-open-banking --features direct-debits --force
```