# FIGMA_LINKS.md — signin

<!-- schema: v3.2 | generated: 2026-10-03T08:15:47.185Z -->

## Stitch Project

| Field | Value |
|-------|-------|
| Project URL | [10780096558615730514](https://stitch.google.com/projects/10780096558615730514) |
| Design System ID | 9551377288795375599 |
| Generated | 2026-10-03T08:15:46.949Z |
| Success | 8/8 states |

## Screen Status

| State | Screen ID | Folder | PNG | HTML | Status |
|-------|-----------|--------|-----|------|--------|
| empty | 77175a620ac4497a82f3f78129b18dea | 01-signin-empty | PNG ✅ | HTML ✅ | ✅ generated |
| biometric_ready | 510a85f0b3c248d6bce83d73d94c985e | 02-signin-biometric_ready | PNG ✅ | HTML ✅ | ✅ generated |
| submitting | — | 03-signin-submitting | PNG ❌ | HTML ✅ | ⏳ pending |
| validation_error | — | 04-signin-validation_error | PNG ❌ | HTML ✅ | ⏳ pending |
| transport_error | 9c61d975cd6b46c8bfa9c8293af5b9c4 | 05-signin-transport_error | PNG ✅ | HTML ✅ | ✅ generated |
| offline | d608277e5d344bab8b1e70c850c79aef | 06-signin-offline | PNG ✅ | HTML ✅ | ✅ generated |
| locked_out | fab27a81036b4391971c583ec1225a13 | 07-signin-locked_out | PNG ✅ | HTML ✅ | ✅ generated |
| success | 2a7f35d0fde34ef0a20ae95029e78722 | 08-signin-success | PNG ✅ | HTML ✅ | ✅ generated |

## Open in Figma / Stitch

| State | Stitch Screen | Figma Export |
|-------|--------------|--------------|
| empty | [Open](https://stitch.google.com/projects/10780096558615730514/screens/77175a620ac4497a82f3f78129b18dea) | — |
| biometric_ready | [Open](https://stitch.google.com/projects/10780096558615730514/screens/510a85f0b3c248d6bce83d73d94c985e) | — |
| submitting | — | — |
| validation_error | — | — |
| transport_error | [Open](https://stitch.google.com/projects/10780096558615730514/screens/9c61d975cd6b46c8bfa9c8293af5b9c4) | — |
| offline | [Open](https://stitch.google.com/projects/10780096558615730514/screens/d608277e5d344bab8b1e70c850c79aef) | — |
| locked_out | [Open](https://stitch.google.com/projects/10780096558615730514/screens/fab27a81036b4391971c583ec1225a13) | — |
| success | [Open](https://stitch.google.com/projects/10780096558615730514/screens/2a7f35d0fde34ef0a20ae95029e78722) | — |

> **Figma Export**: direct download URL captured from Stitch SDK `screen.data.figmaExport.downloadUrl`. May be `—` if Stitch did not generate a Figma export for this screen.
>
> **Stitch Screen**: opens the screen in Stitch web UI — use the Figma export button there for native Figma transfer.

## Re-run

```bash
STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
  .claude-runtime/scripts/stitch-generate.ts \
  --workspace mifos-x/mifos-x-field-officer-app --features signin --force
```