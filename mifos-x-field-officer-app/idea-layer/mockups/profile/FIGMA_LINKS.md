# FIGMA_LINKS.md — profile

<!-- schema: v3.2 | generated: 2026-10-27T13:12:01.283Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [10780096558615730514](https://stitch.google.com/projects/10780096558615730514) |
| Design System ID | 9551377288795375599 |
| Generated | 2026-10-27T13:12:01.171Z |
| Success | 2/2 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| loading | e385d085b0f54234aa850d3a57c89f1a | 01-profile-loading | PNG ✅ | HTML ✅ | ✅ generated |
| change_password | 91d38bc4c19049efbe7e6fcf40810389 | 05-profile-change_password | PNG ✅ | HTML ✅ | ✅ generated |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| loading | [Open](https://stitch.google.com/projects/10780096558615730514/screens/e385d085b0f54234aa850d3a57c89f1a) | — |
| change_password | [Open](https://stitch.google.com/projects/10780096558615730514/screens/91d38bc4c19049efbe7e6fcf40810389) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-field-officer-app --features profile --force
```