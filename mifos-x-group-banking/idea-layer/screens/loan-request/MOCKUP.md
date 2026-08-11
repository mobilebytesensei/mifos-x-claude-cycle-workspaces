# Loan Request — Stitch Mockup

**Status**: Generated (metadata refreshed from current ui.yaml + demo-data)
**Project**: MifosSave (mifos-x-group-banking)
**Stitch Project ID**: `2628966868931366090`
**Screen ID**: `a93904e687de4a38a2f0293c153b559f`
**Design System**: MifosSave-v3 (`assets/17261554270924114992`)
**Device**: Mobile (Android)
**Generated**: 2026-05-09 (initial stitch render)
**Metadata refreshed**: 2026-07-18 (mtime bump — reflects ui.yaml v4.0 + demo-data v2.1.0)

## Preview

View in Stitch: `projects/2628966868931366090/screens/a93904e687de4a38a2f0293c153b559f`

## States Covered

Per `ui.yaml#states` (5 declared, initial `content`):

- content — form ready, all fields enabled, submit disabled until valid
- submitting — submission in progress, fields disabled, spinner shown
- submit_success — success dialog shown, navigates to personal-dashboard
- submit_error — error snackbar visible with Retry action
- offline_queued — payload saved to SyncQueue, offline banner + success dialog with offline copy

## Prompts

Per-state stitch prompts live at `prompts/` (regenerated 2026-07-18):

- `prompts/content.md`
- `prompts/submitting.md`
- `prompts/submit_success.md`
- `prompts/submit_error.md`
- `prompts/offline_queued.md`

## Artifacts — content state (canonical stitch render)

- HTML: `../../mockups/loan-request/stitch/01-loan-request-content/code.html`
- PNG:  `../../mockups/loan-request/stitch/01-loan-request-content/screen.png`

## Deferred

Stitch re-render for the 4 additional states (`submitting`, `submit_success`, `submit_error`, `offline_queued`) is deferred pending Stitch API access — probe returned unavailable. Existing `content`-state HTML/PNG remain the fidelity anchor; the four sibling prompts are authored and ready for the next Stitch-enabled run.
