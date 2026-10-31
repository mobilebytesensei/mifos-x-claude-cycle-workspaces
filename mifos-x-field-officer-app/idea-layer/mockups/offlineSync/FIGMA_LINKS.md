# FIGMA_LINKS.md — offlineSync

<!-- schema: v3.2 | generated: 2026-10-27T08:26:38.092Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [10780096558615730514](https://stitch.google.com/projects/10780096558615730514) |
| Design System ID | 9551377288795375599 |
| Generated | 2026-10-27T08:26:37.973Z |
| Success | 2/2 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| content | 6f0ac0e64d5a45ad91a4daeafbd23e16 | 02-offlineSync-content | PNG ✅ | HTML ✅ | ✅ generated |
| partial_failure | b810a4704bee431a979246b26cc73194 | 04-offlineSync-partial_failure | PNG ✅ | HTML ✅ | ✅ generated |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| content | [Open](https://stitch.google.com/projects/10780096558615730514/screens/6f0ac0e64d5a45ad91a4daeafbd23e16) | — |
| partial_failure | [Open](https://stitch.google.com/projects/10780096558615730514/screens/b810a4704bee431a979246b26cc73194) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-field-officer-app --features offlineSync --force
```