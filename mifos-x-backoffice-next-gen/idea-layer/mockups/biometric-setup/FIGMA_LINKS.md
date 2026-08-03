# FIGMA_LINKS.md — biometric-setup

<!-- schema: v3.2 | generated: 2026-08-03T17:34:02.020Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [10243803383444073820](https://stitch.google.com/projects/10243803383444073820) |
| Design System ID | 312064780206383264 |
| Generated | 2026-08-03T17:34:01.954Z |
| Success | 6/6 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| prompt | 072a2a15a52c419f99c8a379057b6f6d | 01-biometric-setup-prompt | PNG ✅ | HTML ✅ | ✅ generated |
| enrolling | 7698f463894c4981b2abf17ce23583ad | 02-biometric-setup-enrolling | PNG ✅ | HTML ✅ | ✅ generated |
| success | 42138dbe07464f1b9987c48fd0ca0450 | 03-biometric-setup-success | PNG ✅ | HTML ✅ | ✅ generated |
| unavailable | 05b7aa434a0b4a99bb07d23b2007c0af | 04-biometric-setup-unavailable | PNG ✅ | HTML ✅ | ✅ generated |
| not_enrolled_in_os | dcbd275e603844e29093792ac164372e | 05-biometric-setup-not_enrolled_in_os | PNG ✅ | HTML ✅ | ✅ generated |
| error | 36cdd04b26b34837a6c5de2c4c3f2ca9 | 06-biometric-setup-error | PNG ✅ | HTML ✅ | ✅ generated |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| prompt | [Open](https://stitch.google.com/projects/10243803383444073820/screens/072a2a15a52c419f99c8a379057b6f6d) | — |
| enrolling | [Open](https://stitch.google.com/projects/10243803383444073820/screens/7698f463894c4981b2abf17ce23583ad) | — |
| success | [Open](https://stitch.google.com/projects/10243803383444073820/screens/42138dbe07464f1b9987c48fd0ca0450) | — |
| unavailable | [Open](https://stitch.google.com/projects/10243803383444073820/screens/05b7aa434a0b4a99bb07d23b2007c0af) | — |
| not_enrolled_in_os | [Open](https://stitch.google.com/projects/10243803383444073820/screens/dcbd275e603844e29093792ac164372e) | — |
| error | [Open](https://stitch.google.com/projects/10243803383444073820/screens/36cdd04b26b34837a6c5de2c4c3f2ca9) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-backoffice-next-gen --features biometric-setup --force
```