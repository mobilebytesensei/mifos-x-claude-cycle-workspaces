# FIGMA_LINKS.md — group-create

<!-- schema: v3.2 | generated: 2026-07-17T11:50:11.825Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [6387644860533383795](https://stitch.google.com/projects/6387644860533383795) |
| Design System ID | 17261554270924114992 |
| Generated | 2026-07-17T11:50:11.825Z |
| Success | 2/2 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| submitting | — | 01-group-create-submitting | PNG ❌ | HTML ✅ | ⏳ pending |
| error | — | 02-group-create-error | PNG ❌ | HTML ✅ | ⏳ pending |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| submitting | — | — |
| error | — | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-group-banking --features group-create --force
```