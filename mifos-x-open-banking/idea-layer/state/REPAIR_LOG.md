# REPAIR_LOG.md — state-repair audit trail

| Timestamp | Check | Action | Details |
|-----------|-------|--------|---------|
| 2026-05-27T17:30:00Z | stale-running | fixed | `idea-preview` running since 2026-05-25T15:35:17Z (>48h) → reconciled to `failure` |
| 2026-05-27T17:30:00Z | legacy-blocks | migrated | Top-level `design_system:` block → merged into `capabilities.design_system` with hashes |
| 2026-05-27T17:30:00Z | legacy-blocks | migrated | Top-level `verify:` block → merged into `capabilities.idea-verify.warning_summary` |
| 2026-05-27T17:30:00Z | duplicate-blocks | removed | Stale `capabilities.idea-sync` (2026-05-22, status: partial) removed; kept latest (2026-05-27, status: complete) |
| 2026-05-27T17:30:00Z | legacy-dashboard-removed | fixed | Deleted `dashboard/DEV_STATUS.md` + `dashboard/dev-status.html` + empty `dashboard/` dir (RULE-DASHBOARD-SINGLETON-001) |
| 2026-08-03T08:13:47Z | legacy-blocks | migrated | Top-level `design_system:` (only a `stitch:` sub-block) removed; `tokens_hash` / `tokens_hashed_at` / staleness flags absorbed into `state/STITCH_STATE.yaml`. Existing `tokens_hash` (sha256, uploaded 2026-05-29) preserved; legacy `020c30cc` (2026-07-01) recorded as `tokens_hash_current` rather than clobbering it |
| 2026-08-03T08:13:47Z | legacy-blocks | not-fixed | 8 top-level keys remain — `project`, `generated`, `last_reverse_sync`, `artifacts_voided_by_reverse_sync`, `features`, `pending_semver_bump`, `pending_phase_rebalance`, `pending_phase_rebalance_reason`. Outside the helper's detect list, no destination sibling declared ("Out of scope — P8 may extend"). Not deleted: each carries live data. `state-validate-emitted.ts` still fails on all 8 |
| 2026-08-03T08:13:47Z | stale-running | clean | 0 blocks in `running` state across project + framework |
| 2026-08-03T08:13:47Z | degraded-records | clean | 0 blocks matched (duration_ms 0 AND no artifacts_written AND no metrics) — `idea-heal` / `idea-migrate-schema` carry `metrics` nested under `last_run` |
| 2026-08-03T08:13:47Z | unmerged-backfill | clean | No `*.backfill.jsonl` in either domain |
| 2026-08-03T08:13:47Z | missing-rotation | clean | Largest journal `FRAMEWORK_ACTIVITY.jsonl` at 1.1 MB, under the 10 MB threshold |
| 2026-08-03T08:13:47Z | stale-archives | clean | No rotated `ACTIVITY_LOG.{YYYY-MM}.jsonl` siblings exist — nothing to archive |
| 2026-08-03T08:13:47Z | orphan-records | advisory | 623 lines carrying `orphan` in `FRAMEWORK_ACTIVITY.jsonl` — manual decision per runtime, not auto-re-homed |
| 2026-08-03T08:13:47Z | legacy-dashboard | reported | `dashboard/DEV_STATUS.md` present again (deleted once on 2026-05-27). `--remove-legacy-dashboard` not passed → reported, not removed |
