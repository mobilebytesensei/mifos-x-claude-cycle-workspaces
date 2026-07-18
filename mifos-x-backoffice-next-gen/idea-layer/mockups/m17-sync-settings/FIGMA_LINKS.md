# FIGMA_LINKS.md — m17-sync-settings

<!-- schema: v3.2 | generated: 2026-07-17T22:54:26.899Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [4340646484225532819](https://stitch.google.com/projects/4340646484225532819) |
| Design System ID | 6971225134039640611 |
| Generated | 2026-07-17T22:54:26.899Z |
| Success | 5/6 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| idle | 0a9b7ac8e76948e285842b5d2ec0faa2 | 01-m17-sync-settings-idle | PNG ✅ | HTML ✅ | ♻ resumed |
| content | 1a841a982ab1402c9f877c8d6ae7206c | 02-m17-sync-settings-content | PNG ✅ | HTML ✅ | ❌ screen-not-landed-after-retry |
| syncing | 5cb99d8248f5495daf150b9be2707b84 | 03-m17-sync-settings-syncing | PNG ✅ | HTML ✅ | ♻ resumed |
| empty | fc37f15e6dfb4b3bb10500fc5f12a867 | 04-m17-sync-settings-empty | PNG ✅ | HTML ✅ | ♻ resumed |
| needs-attention | 1070c44c16b44dbb9136d6e7a21908e7 | 05-m17-sync-settings-needs-attention | PNG ✅ | HTML ✅ | ♻ resumed |
| error | 754da12054624cfeb30273ebebb82b92 | 06-m17-sync-settings-error | PNG ✅ | HTML ✅ | ♻ resumed |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| idle | [Open](https://stitch.google.com/projects/4340646484225532819/screens/0a9b7ac8e76948e285842b5d2ec0faa2) | — |
| content | [Open](https://stitch.google.com/projects/4340646484225532819/screens/1a841a982ab1402c9f877c8d6ae7206c) | — |
| syncing | [Open](https://stitch.google.com/projects/4340646484225532819/screens/5cb99d8248f5495daf150b9be2707b84) | — |
| empty | [Open](https://stitch.google.com/projects/4340646484225532819/screens/fc37f15e6dfb4b3bb10500fc5f12a867) | — |
| needs-attention | [Open](https://stitch.google.com/projects/4340646484225532819/screens/1070c44c16b44dbb9136d6e7a21908e7) | — |
| error | [Open](https://stitch.google.com/projects/4340646484225532819/screens/754da12054624cfeb30273ebebb82b92) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-backoffice-next-gen --features m17-sync-settings --force
```