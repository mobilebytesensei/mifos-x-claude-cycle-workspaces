# FIGMA_LINKS.md — login

<!-- schema: v3.2 | generated: 2026-05-29T17:13:16.345Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [17153754672098888646](https://stitch.google.com/projects/17153754672098888646) |
| Design System ID | 2005644667042354169 |
| Generated | 2026-05-29T17:13:16.232Z |
| Success | 0/8 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| idle | — | 01-login-idle | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: Resource has been exhausted (e.g. check quota). |
| loading | — | 02-login-loading | PNG ❌ | HTML ❌ | ❌ STN gate failure pre-API: STN2: prompt is 4015 chars (cap 4000) — apply the shrink ladder or split the screen |
| authenticating | — | 03-login-authenticating | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: Resource has been exhausted (e.g. check quota). |
| oauth_redirecting | — | 04-login-oauth_redirecting | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: Resource has been exhausted (e.g. check quota). |
| oauth_exchanging | — | 05-login-oauth_exchanging | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: Resource has been exhausted (e.g. check quota). |
| error | — | 06-login-error | PNG ❌ | HTML ❌ | ❌ STN gate failure pre-API: STN2: prompt is 4171 chars (cap 4000) — apply the shrink ladder or split the screen |
| content | — | 07-login-content | PNG ❌ | HTML ❌ | ❌ StitchError: Tool Call Failed [generate_screen_from_text]: Resource has been exhausted (e.g. check quota). |
| empty | — | 08-login-empty | PNG ❌ | HTML ❌ | ❌ STN gate failure pre-API: STN2: prompt is 4171 chars (cap 4000) — apply the shrink ladder or split the screen |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| idle | — | — |
| loading | — | — |
| authenticating | — | — |
| oauth_redirecting | — | — |
| oauth_exchanging | — | — |
| error | — | — |
| content | — | — |
| empty | — | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-open-banking --features login --force
```