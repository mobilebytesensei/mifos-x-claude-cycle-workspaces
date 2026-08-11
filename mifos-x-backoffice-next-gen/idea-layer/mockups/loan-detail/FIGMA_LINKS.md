# FIGMA_LINKS.md — loan-detail

<!-- schema: v3.2 | generated: 2026-08-03T14:50:29.604Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [10243803383444073820](https://stitch.google.com/projects/10243803383444073820) |
| Design System ID | 312064780206383264 |
| Generated | 2026-08-03T14:50:29.604Z |
| Success | 4/4 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | bb6c527d252542ddb02473281106c7a1 | 01-loan-detail-loading | PNG ✅ | HTML ✅ | ♻ resumed |
| content | ad804ab475854ce0ae37557fc630df37 | 02-loan-detail-content | PNG ✅ | HTML ✅ | ♻ resumed |
| empty | 8306fe8a97e1489186698a3b6e446760 | 03-loan-detail-empty | PNG ✅ | HTML ✅ | ♻ resumed |
| error | 973c26f4844c4a1db2fc6d5329d545f4 | 04-loan-detail-error | PNG ✅ | HTML ✅ | ♻ resumed |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | [Open](https://stitch.google.com/projects/10243803383444073820/screens/bb6c527d252542ddb02473281106c7a1) | — |
| content | [Open](https://stitch.google.com/projects/10243803383444073820/screens/ad804ab475854ce0ae37557fc630df37) | — |
| empty | [Open](https://stitch.google.com/projects/10243803383444073820/screens/8306fe8a97e1489186698a3b6e446760) | — |
| error | [Open](https://stitch.google.com/projects/10243803383444073820/screens/973c26f4844c4a1db2fc6d5329d545f4) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-backoffice-next-gen --features loan-detail --force
```