# CommonPurse — Mifos X Group Banking

> Offline-first KMP community banking app digitizing VSLA/ROSCA group savings, lending & share-out via Mifos Fineract.

| Field | Value |
|-------|-------|
| Status | **initialized** (planning → initialized on 2026-05-05) |
| Display name | CommonPurse |
| Slug | mifos-x-group-banking |
| Type | kmp |
| Workspace | mifos-x |
| Package | org.mifos.groupbanking |
| Repo (origin = fork) | [therajanmaurya/mifos-x-group-banking](https://github.com/therajanmaurya/mifos-x-group-banking) — push target |
| Repo (upstream) | [openMF/mifos-x-group-banking](https://github.com/openMF/mifos-x-group-banking) — PR target |
| Repo (template) | [openMF/kmp-project-template](https://github.com/openMF/kmp-project-template) — template upstream |
| Backend | Mifos Fineract (sandbox.mifos.community) + 36 generated MCP tools |
| Created | 2026-05-02 |
| Promoted | 2026-05-05 (via `/idea-plan` [P]) |

## Layers (8 enabled)

| Layer | State |
|-------|-------|
| idea-layer | populated — IDEA.md, FEATURES.md, REQUIREMENTS.md, design-tokens.yaml, PROJECT_DEMO_DATA.yaml, screens/README, flows/README |
| server-layer | populated — API_CONTRACT.yaml (76 endpoints, 15 datatables), API.md, BRIDGE_AUDIT_LOG.yaml |
| client-layer | empty (populate via `/client`) |
| feature-layer | empty (populate via `/feature` or `/implement`) |
| infrastructure-layer | empty (populate via `/server-init` or `/infrastructure`) |
| platform-layer | empty (populate via `/ai-agent-platform`) |
| testing-layer | empty (populate via `/test`) |
| release-layer | empty (populate via `/release`) |

## Source

`source/mifos-x-group-banking/` — fork-aware clone of `openMF/kmp-project-template@dev` (commit `7146992`), customized with `org.mifos.groupbanking` package + `CommonPurse` brand.

Remotes:
- `origin`   → `git@github.com:therajanmaurya/mifos-x-group-banking.git` (fork — push here)
- `upstream` → `git@github.com:openMF/mifos-x-group-banking.git` (PR target)
- `template` → `git@github.com:openMF/kmp-project-template.git` (template upstream)

Customization: `customizer.sh` ran successfully after fixing 3 upstream bugs:
1. `((count++))` clashes with `set -e` — replaced with `count=$((count + 1))`
2. `\s` not supported by BSD sed — replaced with `[[:space:]]`
3. `mkdir -p $kotlin_dir/$SUBDIR` followed by `cp -r $kotlin_dir/org/mifos/* $SUBDIR/` then `rm -rf $kotlin_dir/org/mifos` caused recursive-copy data loss when SUBDIR overlaps `org/mifos` — rewrote `process_module_dirs` to stage via `mktemp -d` outside the source tree.

These patches are committed in the fork's `customizer.sh`. PR them upstream when ready.

Three customizer-blind paths required manual cleanup (`cmp-shared/src/nativeMain`, `core/database/src/{androidUnitTest,nativeTest}` — missing from `base_dirs`/`src_dirs` arrays).

## Deferred

- **Per-screen YAMLs** (`idea-layer/screens/*.yaml`) — generate via `/idea sync`.
- **Per-flow YAMLs** (`idea-layer/flows/*.yaml`) — generate via `/idea sync` or `/flow-generate`.
- **PR customizer-fix upstream** — three openMF/kmp-project-template `customizer.sh` bugs documented above; consider PR'ing fix to openMF.
- **First push to fork** — source/ has uncommitted changes (template clone + customization + manual cleanup). Run `/git-pr-create` or `git -C source/... add . && commit` to commit, then `git push origin dev`. Then open PR fork → upstream.

## Next steps

- `/idea sync` — decompose §screens + §flows into per-file YAMLs, generate Mermaid diagrams
- `/idea export` — generate SPEC.md, API.md per-feature
- `/implement` — start feature implementation pipeline
- `/git-pr-create` — open PR from local source/ to `openMF/mifos-x-group-banking`
