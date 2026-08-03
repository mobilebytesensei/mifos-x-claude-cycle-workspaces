# FIGMA_LINKS.md — passcode-lock

<!-- schema: v3.2 | generated: 2026-08-03T16:34:23.853Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [10243803383444073820](https://stitch.google.com/projects/10243803383444073820) |
| Design System ID | 312064780206383264 |
| Generated | 2026-08-03T16:34:23.704Z |
| Success | 6/6 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| setup | 9fa10aa1f7a34980a8091d9be289db48 | 01-passcode-lock-setup | PNG ✅ | HTML ✅ | ✅ generated |
| confirm | 32b998c6ee3e4796b42999443c0a55b4 | 02-passcode-lock-confirm | PNG ✅ | HTML ✅ | ✅ generated |
| locked | decb72796cc3464b8319d5fa20d9a6ae | 03-passcode-lock-locked | PNG ✅ | HTML ✅ | ✅ generated |
| locked_biometric | 317219bce54f409b880939582ab23194 | 04-passcode-lock-locked_biometric | PNG ✅ | HTML ✅ | ✅ generated |
| locked_out | 5545e19771534871bab220a06d563efb | 05-passcode-lock-locked_out | PNG ✅ | HTML ✅ | ✅ generated |
| error | 6f0901d085dc45beb3e6e7d9b6ae9c29 | 06-passcode-lock-error | PNG ✅ | HTML ✅ | ✅ generated |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| setup | [Open](https://stitch.google.com/projects/10243803383444073820/screens/9fa10aa1f7a34980a8091d9be289db48) | — |
| confirm | [Open](https://stitch.google.com/projects/10243803383444073820/screens/32b998c6ee3e4796b42999443c0a55b4) | — |
| locked | [Open](https://stitch.google.com/projects/10243803383444073820/screens/decb72796cc3464b8319d5fa20d9a6ae) | — |
| locked_biometric | [Open](https://stitch.google.com/projects/10243803383444073820/screens/317219bce54f409b880939582ab23194) | — |
| locked_out | [Open](https://stitch.google.com/projects/10243803383444073820/screens/5545e19771534871bab220a06d563efb) | — |
| error | [Open](https://stitch.google.com/projects/10243803383444073820/screens/2af4584033c744c6976447db11a4c3a6) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-backoffice-next-gen --features passcode-lock --force
```