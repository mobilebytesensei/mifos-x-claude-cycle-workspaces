# FIGMA_LINKS.md — m09-organization

<!-- schema: v3.2 | generated: 2026-07-26T10:49:34.700Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [10243803383444073820](https://stitch.google.com/projects/10243803383444073820) |
| Design System ID | 312064780206383264 |
| Generated | 2026-07-26T10:49:34.630Z |
| Success | 6/6 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | 01473a7c86844c0eb02f889351f00975 | 01-m09-organization-loading | PNG ✅ | HTML ✅ | ✅ generated |
| content | 1b1008c6692e4c06a5ed3349a5da0d0b | 02-m09-organization-content | PNG ✅ | HTML ✅ | ✅ generated |
| empty | 6642fe1ebab94dc393a2366048fcd018 | 03-m09-organization-empty | PNG ✅ | HTML ✅ | ✅ generated |
| submitting | 20b72efd5525476397f642721f007132 | 04-m09-organization-submitting | PNG ✅ | HTML ✅ | ✅ generated |
| action-disabled | 82bc414d7cfb49629bfc4460052627ed | 05-m09-organization-action-disabled | PNG ✅ | HTML ✅ | ✅ generated |
| error | — | 06-m09-organization-error | PNG ❌ | HTML ✅ | ⏳ pending |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | [Open](https://stitch.google.com/projects/10243803383444073820/screens/01473a7c86844c0eb02f889351f00975) | — |
| content | [Open](https://stitch.google.com/projects/10243803383444073820/screens/1b1008c6692e4c06a5ed3349a5da0d0b) | — |
| empty | [Open](https://stitch.google.com/projects/10243803383444073820/screens/6642fe1ebab94dc393a2366048fcd018) | — |
| submitting | [Open](https://stitch.google.com/projects/10243803383444073820/screens/20b72efd5525476397f642721f007132) | — |
| action-disabled | [Open](https://stitch.google.com/projects/10243803383444073820/screens/82bc414d7cfb49629bfc4460052627ed) | — |
| error | — | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-backoffice-next-gen --features m09-organization --force
```