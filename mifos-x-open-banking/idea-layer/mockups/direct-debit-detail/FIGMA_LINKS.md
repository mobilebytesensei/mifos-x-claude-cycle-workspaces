# FIGMA_LINKS.md — direct-debit-detail

<!-- schema: v3.2 | generated: 2026-05-31T03:25:41.638Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [17153754672098888646](https://stitch.google.com/projects/17153754672098888646) |
| Design System ID | 2005644667042354169 |
| Generated | 2026-05-31T03:25:41.637Z |
| Success | 4/4 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | 77f939a1b2414d789526ca555ecdbe59 | 01-direct-debit-detail-loading | PNG ✅ | HTML ✅ | ♻ resumed |
| content | d311989b4f8b48989970501015b52038 | 02-direct-debit-detail-content | PNG ✅ | HTML ✅ | ♻ resumed |
| error | 8d6ee6e72a8c4062862681f3c022d152 | 03-direct-debit-detail-error | PNG ✅ | HTML ❌ | ✅ generated |
| empty | adf16c1dd16b4bed805a8c7677a74ebf | 04-direct-debit-detail-empty | PNG ✅ | HTML ✅ | ♻ resumed |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | [Open](https://stitch.google.com/projects/17153754672098888646/screens/77f939a1b2414d789526ca555ecdbe59) | — |
| content | [Open](https://stitch.google.com/projects/17153754672098888646/screens/d311989b4f8b48989970501015b52038) | — |
| error | [Open](https://stitch.google.com/projects/17153754672098888646/screens/8d6ee6e72a8c4062862681f3c022d152) | — |
| empty | [Open](https://stitch.google.com/projects/17153754672098888646/screens/adf16c1dd16b4bed805a8c7677a74ebf) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-open-banking --features direct-debit-detail --force
```