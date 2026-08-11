# FIGMA_LINKS.md — loan-application-wizard

<!-- schema: v3.2 | generated: 2026-08-03T14:50:29.563Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [10243803383444073820](https://stitch.google.com/projects/10243803383444073820) |
| Design System ID | 312064780206383264 |
| Generated | 2026-08-03T14:50:29.562Z |
| Success | 4/4 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | 63f68df5e1a44fb2a304c8c777acfcc5 | 01-loan-application-wizard-loading | PNG ✅ | HTML ✅ | ♻ resumed |
| content | af434b13e3ec4908a9172395b8eed696 | 02-loan-application-wizard-content | PNG ✅ | HTML ✅ | ♻ resumed |
| empty | fd4fc0883e1f4a9aa6ad8ee8aa998a84 | 03-loan-application-wizard-empty | PNG ✅ | HTML ✅ | ♻ resumed |
| error | d276b372bc47412aabc0784cccff3832 | 04-loan-application-wizard-error | PNG ✅ | HTML ✅ | ♻ resumed |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | [Open](https://stitch.google.com/projects/10243803383444073820/screens/63f68df5e1a44fb2a304c8c777acfcc5) | — |
| content | [Open](https://stitch.google.com/projects/10243803383444073820/screens/af434b13e3ec4908a9172395b8eed696) | — |
| empty | [Open](https://stitch.google.com/projects/10243803383444073820/screens/fd4fc0883e1f4a9aa6ad8ee8aa998a84) | — |
| error | [Open](https://stitch.google.com/projects/10243803383444073820/screens/d276b372bc47412aabc0784cccff3832) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-backoffice-next-gen --features loan-application-wizard --force
```