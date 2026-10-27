# Idea Evolution Log — mifos-x-field-officer-app

## 2026-03-22 — idea-layer generated from existing project
- **What**: Reverse-engineered from PROJECT.md, FEATURES_INDEX, SPEC files
- **Source**: /project-migration v2.86.5
- **Features**: 20 discovered
- [design-system-stitch] 2026-10-02 — DESIGN.md uploaded to Stitch (asset_id=9551377288795375599, design_md_sha=c1e7dbe50f77)

## 2026-10-27 — profile designed (/idea-plan-add --rebind profile)
- **What**: The signed-in officer's account, opened from the Home avatar: full name, username, Loan officer / Staff chip, office, roles; what Home shows (my portfolio vs office); the live server instance, URL and tenant; Change password (server refusal shown verbatim, re-sign-in on success); Sign out (the Settings dialog). Detail shell with a back arrow; offline shows the identity saved at sign-in.
- **Why**: The navigation drawer was removed and its header was the only way to Profile; the existing screen was three lines with no app bar.
- **Requirements**: FR-PRO-01..06, SFR-031..032, NFR-PRO-01.
- **Docset**: screens/profile/{docs,ui,api,flow,data-flow,demo-data,tests}.yaml + maestro/happy_path.yaml; 27 strings under screens.profile.*.
- **Gateway (measured)**: POST users/{id}/pwd routes and validates (policy 12–50 chars, upper/lower/digit/symbol; server-side repeat match); fieldofficer = Irving Zepeda, no staff link, role OFICIAL DE CAMPO. Probes used mismatched pairs — no password changed.

## 2026-10-27 — offlineSync added (/idea-plan-add)
- **What**: Settings → Offline sync, a separate feature from Sync & Drafts. The officer selects existing centres / groups / clients; a background job (sync/) downloads each one's full downstream tree — groups, clients, every loan and savings account (closed included), addresses, identifiers, notes, charges, documents with file contents, datatables, templates — through the screens' own stores; offline loan repayments and savings transactions upload as soon as online. Live dashboard from durable job state; Manual or Automatic refresh (interval, Wi-Fi only, while charging).
- **Why**: Field officers work without signal; the v1 drawer "Offline Sync" was never ported, and offline repayments were queued with nothing to send them.
- **Source**: Operator decisions 2026-10-27; redesign of 6b66e8a43 feature/offline (dashboard + 5 sync screens).
- **Requirements**: FR-OFF-01..08, SFR-029..032, NFR-OFF-01.
- **Docset**: screens/offlineSync/{docs,ui,api,flow,data-flow,demo-data,tests}.yaml + maestro/happy_path.yaml.

## 2026-10-26 — home dashboard added (/idea-plan-add)
- **What**: Permission-aware field officer home dashboard — today's collections, work queue, meetings today, portfolio at a glance, quick actions, recent records. Becomes the Home tab body; search stays on the top-bar icon.
- **Why**: A field officer's first screen should be the day's work; the original Home was search only.
- **Source**: Fineract API + permission audit (sandbox 1.17.0-SNAPSHOT: 603 paths, 710 permission codes) and the gateway field officer role.
- **Decisions**: staff-linked "my portfolio" with office-wide fallback · own-loan approval/disbursal queues · dashboard IS Home.
- **Requirements**: FR-DASH-01..07, SFR-024..028, NFR-PERM-01.
- **Docset**: screens/home/{docs,ui,api,flow,data-flow,demo-data,tests}.yaml + maestro/happy_path.yaml.
- **Rename**: feature id `home` (operator: "keep the name clean"); the previous `home` plan row — the search surface — is now `search`.
