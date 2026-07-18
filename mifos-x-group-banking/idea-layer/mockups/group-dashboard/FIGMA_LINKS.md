# FIGMA_LINKS.md — group-dashboard

<!-- schema: v3.2 | generated: 2026-07-17T05:44:11.540Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [6387644860533383795](https://stitch.google.com/projects/6387644860533383795) |
| Design System ID | 17261554270924114992 |
| Generated | 2026-07-17T05:44:11.540Z |
| Success | 4/4 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | d41c14756c014ccf9effb1a1bffb5d3f | 01-group-dashboard-loading | PNG ✅ | HTML ✅ | ✅ generated |
| content_accumulating | ffc1383f18f0472e8a0a4f4ec286ff11 | 02-group-dashboard-content_accumulating | PNG ✅ | HTML ✅ | ✅ generated |
| content_rotating | 8f0897b9cd7643ffb7abc60d0e2f043b | 03-group-dashboard-content_rotating | PNG ✅ | HTML ✅ | ✅ generated |
| error | dfa2c5e7a202448898154a9ceb9947b7 | 04-group-dashboard-error | PNG ✅ | HTML ✅ | ✅ generated |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | [Open](https://stitch.google.com/projects/6387644860533383795/screens/d41c14756c014ccf9effb1a1bffb5d3f) | — |
| content_accumulating | [Open](https://stitch.google.com/projects/6387644860533383795/screens/ffc1383f18f0472e8a0a4f4ec286ff11) | — |
| content_rotating | [Open](https://stitch.google.com/projects/6387644860533383795/screens/8f0897b9cd7643ffb7abc60d0e2f043b) | — |
| error | [Open](https://stitch.google.com/projects/6387644860533383795/screens/dfa2c5e7a202448898154a9ceb9947b7) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-group-banking --features group-dashboard --force
```