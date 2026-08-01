# EVOLVE_PLAN — Production Sign-up + Server Migration + Device-Verified Deploy

| | |
|---|---|
| **Project** | mifos-x/mifos-x-group-banking (CommonPurse — VSLA group banking, KMP) |
| **Date** | 2026-08-01 |
| **Command** | `/idea-evolve-plan "<production sign-up / server migration / demo-explore / device-verify feedback>"` |
| **Auditors** | 5 parallel Claude-Intelligence completability auditors (CP-A/B/C · CP-D/E+server · CP-F · CP-G ×2) |
| **Findings** | 47 raw findings · **≈30 distinct blocking gaps** after cross-dimension dedup |
| **Completability verdict** | **INCOMPLETABLE for production deploy** — the idea-layer is *structurally* green (nav/DTO/flow closure: 32/32 screens reachable, 0 orphans, 14 DTOs, 0 drift) but has **no live-server backing, no runnable table migrations, no demo-seed, and three absent launch capabilities** (demo-explore, first-class accept-invitation, Play-Store test track). Structural matrix-green ≠ deployable. |

## Feedback (verbatim)

> There few improvements we need to do,
> - make sure /server layer is have proper migration instructions of seeding the demo data for demo user and also have full migration instruction to build all data tables that we are using of missing APIs example meeting api etc.
> - on Authentication screen let's have a professional ui where user can login or accept invitation and also have button to sign up and this sign up user can create groups and invite members etc.
> - On login screen let's have a button "Demo Explore" on click show dialog that this is demo user logging in to explore the application.
> - Our next goal to build the features in production level so we can deploy for users and they can sign up or sign in or accept the invitation and continue useing the app.
> - regenerate the llm mockups and implement features end to end like some feature like meeting, group create etc proper steps feature screens mockups generates.
> - let's focus on building a production level applciation that we can distribute on playstore for first testing and make sure server layer is properly connected with idea layer so as we gonna add new feature etc and it does migrate the missing API and make sure server ready /mifos-bridge
> - verify each and every feature in real enumator and test it using mastro so you can verify network and ui is fully implemented and working and use claude intelligeence to implement the screens so it does implementation production level.

---

## 1 · Traceability matrix (breaks marked ✗)

| Level | Status | Breaks found |
|---|---|---|
| **Vision → FR** (CP-A) | ✅ coherent | every `vision.in_scope` promise maps to ≥1 FR |
| **FR → Feature** (CP-B) | ✗ 7 breaks | orphan FR-025 (no feature) · FR-026 miscategorized `must` non-goal · notifications↔FR-019 cross-map · **no FR/feature for demo-explore, server-demo-seed, auto-migrate/server-ready, accept-invitation** |
| **Roadmap / phase** (CP-C) | ✗ 4 breaks | group-type-config (must) + pluggable-distribution (must) in **no milestone/epic** · member-invitations feature=1.0.0 but milestone=1.1.0 · **no Play-Store internal-test milestone** |
| **Feature → Screen** (CP-D) | ✅ complete | 32/32 screens reachable, every screen has a parent feature/flow |
| **Feature-Data** (CP-E) | ✗ backing absent | DTOs coherent (14, 0 drift) BUT every user-facing WRITE resolves to a `PENDING_DEPLOYMENT` companion facade |
| **Server / migration** | ✗ 11 breaks | whole `/companion/*` backend **not deployed** · **0 runnable table migrations** (21 datatables prose-only) · **no demo-seed** · meeting-calendar API absent · `GET /loans` absent · 4 absent api group files · `/mifos-bridge` generates contract only + is stale · advanceCycle/disburse mis-mappings |
| **Flow / journey** (CP-F) | ✗ 6 breaks | demo-explore journey **missing** · auth not a login/accept-invite/signup chooser · `pendingInviteCode` handoff unwired · meeting-schedule leg not in-app |
| **Screen behavior** (CP-G) | ✗ 18 breaks | demo-explore action absent · accept-invitation not first-class · dead notification/overflow affordances · nav-param/destination drift on ~8 screens |

**Root insight:** the last `/idea-agent` drive reached `matrix-green` because that verdict measures *structural* closure (reachability, DTO registration, flow coherence). It does **not** model whether a live server backs the writes, whether tables exist, or whether the demo/accept-invitation/Play-Store launch capabilities are specced. Every gap below is invisible to the structural matrix — which is the core reason the app "looks green" but is not deployable.

---

## 2 · Gaps by dimension

### CP-B — Requirement → Feature (7)
| # | level_entity | gap_type | what_blocks_completion | evidence | fix_direction |
|---|---|---|---|---|---|
| B1 | demo-explore mode | missing-capability | No FR/feature/screen for a "Demo Explore" login button + confirm dialog + demo session | `login-signup/ui.yaml` actions have no demo action; no demo FR | Add FR + `demo-explore` feature (guest/offline-seeded session + confirm dialog), phase 1.0.0 |
| B2 | server demo-data seeding | missing-capability | No requirement to seed demo data for a demo user (IR-005 provisions empty tables only) | `REQUIREMENTS.md` IR-005; `PROJECT_DEMO_DATA.yaml` is a client fixture | Add IR "seed demo account + demo data via migrations" to the companion-api external gate |
| B3 | auto-migrate-on-new-feature / server-ready | missing-capability | No requirement for a standing idea→server bridge that migrates a new feature's API | `_mifos_bridge_run` one-shot artifact; no auto-migrate IR/FR | Add IR/FR: re-run `/mifos-bridge` + emit runnable migrations on every feature add |
| B4 | accept-invitation auth path | structural-risk | "login OR accept-invitation + sign-up on ONE auth screen" is not modeled; join-with-code is post-auth only | `unified-auth` `screen_refs:[login-signup]`; no "accept-invitation" term | Add accept-invitation entry to login-signup spec + unified-auth acceptance criteria |
| B5 | FR-025 (must) | orphan-requirement | MUST FR (group-type state as Fineract datatables) referenced by no `features[].requirement_refs` | `idea-plan.yaml` FR-025 @L860 | Add FR-025 to group-type-config / companion-api-backend refs |
| B6 | FR-026 (must) | orphan-requirement | FR-026 ("NON-GOALS for v1") is `priority:must` but a non-goal with no feature | `idea-plan.yaml` FR-026 @L868 | Re-tag FR-026 as constraint/non-goal (not a must FR) |
| B7 | notifications ↔ FR-019 | missing-feature | notifications `requirement_refs:[FR-019]` but FR-019 is "Enhanced meeting flow"; notifications satisfies no matching FR | `idea-plan.yaml` @L1262 vs FR-019 @L794 | Re-point meeting-lifecycle to add FR-019; give notifications a real FR |

### CP-C — Roadmap / phase (4)
| # | level_entity | gap_type | what_blocks_completion | evidence | fix_direction |
|---|---|---|---|---|---|
| C1 | group-type-config (must) | phase-incoherence | MUST feature in no milestone and no epic — cannot be planned/tracked | absent from `deployment_plan.milestones` @L3144-3179 + `epic_breakdown` | Add to 1.0.0 milestone + distribution epic |
| C2 | pluggable-distribution (must) | phase-incoherence | MUST payout-engine feature in no milestone/epic | absent from milestones/epics @L3144-3204 | Add to 1.0.0 milestone + distribution epic |
| C3 | member-invitations (must) / FR-024 | phase-incoherence | feature=1.0.0 but deployment plan schedules 1.1.0 → invite-to-join deferred out of v1 | feature @L1277 vs milestones "1.1.0" @L3169 | Move member-invitations to 1.0.0 milestone (or re-scope FR-024) |
| C4 | Play-Store internal-testing milestone | missing-capability | Rollout has NGO closed_alpha + open GA but no Play-Store internal/closed test track for "first testing" | `rollout_strategy` @L3093-3104 | Add a Play-Store internal-testing milestone before closed_alpha |

### CP-E + SERVER — Feature-Data & migration (12)
| # | level_entity | gap_type | what_blocks_completion | evidence | fix_direction |
|---|---|---|---|---|---|
| S1 | `/companion/*` facade (12+ screens) | missing-migration | Whole companion backend not deployed → sign-up/sign-in/create-group/invite/join/dashboards/share-out have zero real backing | `API_CONTRACT.yaml` all `sandbox_test: PENDING_DEPLOYMENT`; `COMPANION_API_BUILD_DEPLOY.md` §0 | Build+deploy `mcp-mifosx` companion tools (auth-model lift + datatable-CRUD); **externally gated** |
| S2 | 21 datatables (15 tier2 + 6 companion) | missing-migration | No executable migration creates the tables the app reads/writes (0 `*.sql`, no migrations dir) | confirmed absence; `COMPANION_API_BUILD_DEPLOY.md` §2 prose-only | Materialize runnable `POST /datatables/register` migrations checked into server-layer |
| S3 | demo-data seed | missing-demo-seed | No demo-seed migration; `PROJECT_DEMO_DATA.yaml` is `status: skeleton` (1 group, 5 members, no savings/loan/meeting/invite rows) | `PROJECT_DEMO_DATA.yaml` `_meta.status: skeleton` | Author `/server-seed` runnable seed (clients+group activation, savings, meeting records, corpus, a live invite code) |
| S4 | `GET /centers/{centerId}/meetings` (MEETING api) | missing-api-op | meeting-calendar's scheduled-meetings read has no real endpoint; `list_meetings` mis-points to `dt_meeting_record` | `apis/meetings.yaml` vs `API_CONTRACT.yaml`; COMP-CAL "ABSENT in mcp" | Build COMP-CAL calendar + collection-sheet tools; fix mcp_tool mapping |
| S5 | `GET /loans` (list) | missing-api-op | meeting-conduct + group loan lists call `GET /loans` but contract only has `GET /loans/{id}` + `POST /loans` | `meeting-conduct/api.yaml#get_active_loans` | Add `list_loans` group-loans wrapper |
| S6 | `apis/clients-members.yaml` | missing-api-op | member-list/member-profile/member-add have no materialized api group file | `api_manifest.yaml#gaps.missing_group_files[0]` | `/idea-api-extend` materialize + bridge |
| S7 | `apis/savings.yaml` | missing-api-op | savings-dashboard/personal-savings/meeting-conduct savings leg unmapped | `api_manifest.yaml#gaps.missing_group_files[1]` | Materialize + wire companion savings summaries |
| S8 | `apis/share-out.yaml` | missing-api-op | share-out-preview/execute reference an absent group file; COMP-DIST PENDING | `api_manifest.yaml#gaps.missing_group_files[2]` | Materialize; deploy COMP-DIST tools |
| S9 | `apis/field-officer.yaml` | missing-api-op | field-officer-dashboard (reachable entry state) has no api group file | `api_manifest.yaml#gaps.missing_group_files[3]` | Materialize cross-group read + bridge |
| S10 | mifos-bridge auto-migrate loop | structural-risk | Bridge generates contract only (no deploy/provision) and is stale (4 group files + COMP-CAL open since bridge-260717) | `mifos-bridge/CAPSULE.md`; `BRIDGE_AUDIT_LOG.yaml` | Re-run `/mifos-bridge --auto` per feature add + extend to emit runnable datatable migrations |
| S11 | advanceCycle / loan-disburse mappings | structural-risk | `advance-cycle`→`command=advanceCycle`, `get-previous-meeting`→`list_attendance` (wrong table); disburse via `/loans/{id}/transactions` not `/loans/{id}?command=disburse` → 404 at runtime | `apis/meetings.yaml`; `meeting-conduct/api.yaml#post_loan_disbursal` | Correct mcp_tool/path mappings to real Fineract command endpoints |
| E1 | writes → PENDING_DEPLOYMENT targets | missing-mutation | execute-share-out / create-invite / self-register / create-group have contracts but `writes_to` targets are PENDING | `share-out-execute/api.yaml`, `member-invite/api.yaml`, `login-signup/api.yaml` | Resolved by S1–S3 (deploy + provision); contracts are correct |

### CP-F — Flow / journey (6)
| # | level_entity | gap_type | what_blocks_completion | evidence | fix_direction |
|---|---|---|---|---|---|
| F1 | journey: demo-explore | missing-journey | No demo affordance anywhere — no button, dialog, session, or journey | confirmed absence across `flows/ journeys/ screens/` | Add `demo_explore_button`→confirm dialog→seeded demo session; author `flows/demo-explore-flow.yaml` + `journeys/demo-explore.yaml` |
| F2 | unified-auth / login-signup | broken-journey | Auth offers only login+signup tabs; join-with-code is post-auth zero-groups only | `mode_toggle_tabs`={login,signup}; join button in `states.zero_groups` | Add first-class "Accept Invitation" entry on the auth content state |
| F3 | login-signup (invite resume) | unwired-route | join-with-code emits `NavigateToLoginSignup(pendingInviteCode)`; TC-LS-010 expects resume; but login-signup `nav_params:{}` and on_login/on_signup never read it → code dropped | `join-with-code/flow.yaml` vs `login-signup/ui.yaml nav_params:{}` | Add `nav_params.pendingInviteCode`; branch on_success → `NavigateToJoinWithCode(code)` |
| F4 | member-invitation-flow | broken-journey | Flow step 5 claims post-auth POST …/join auto-associates invitee, but login-signup has no join call → invitee lands in ZeroGroups | `member-invitation-flow.yaml#steps[5]` vs `login-signup/flow.yaml` deps | Same root as F3 — wire pendingInviteCode→associate, or redirect to join-with-code |
| F5 | journey: join-with-code | structural-risk | Three post-join destinations (personal-dashboard / loan-request / NavigateToGroupDashboard) | `journeys/join-with-code.yaml#exit_point` vs `flow.yaml on_success` | Reconcile to one landing (personal-dashboard per member role) |
| F6 | flow: meeting-flow | structural-risk | "schedule" leg not in-app; meeting-calendar only reads Fineract, no schedule action | `meeting-calendar/ui.yaml` (no schedule/fab); `flows/meeting-flow.yaml#entry` | Add schedule affordance + flow step, OR document meetings auto-generate from group `meetingDay` and add reschedule |

### CP-G — Screen behavior (18, most-blocking first)
| # | level_entity | gap_type | what_blocks_completion | evidence | fix_direction |
|---|---|---|---|---|---|
| G1 | login-signup / OnDemoExplore | missing-capability | Demo Explore button + confirm dialog + demo session absent | confirmed absence in ui/flow/api | Add `demo_explore_button` + `OnDemoExplore` + confirm-dialog event + demo/offline-seeded session route |
| G2 | login-signup / join in zero_groups only | missing-action | Invited new user has no accept-invitation entry on the auth screen | ui `states.content` excludes join button | Surface "Accept Invitation" on login/signup content → join-with-code |
| G3 | meeting-calendar / no ScheduleMeeting | missing-capability | Organizer can't schedule/reschedule; no-upcoming branch dead-ends on placeholder | ui actions = Load/Refresh/Toggle/StartMeeting/OpenPast only | Add schedule action + FAB/CTA (or document auto-generated + add reschedule) |
| G4 | organizer-dashboard / OnOpenNotifications | dead-onclick | Handler + `NotificationsDeferred` event not declared in ViewModel | ui L92 vs actions/events lists | Declare action+event (deferred-snackbar) or remove icon |
| G5 | previous-meeting-review / launched_from | flow-ui-drift | Required nav_param never supplied → falsely shows "Completed" + hides "Start Meeting #N" CTA | callers omit `launched_from` | Pass `launched_from:"conduct"`/`"calendar"` from both callers |
| G6 | meeting-conduct / ViewFullPreviousMeeting | flow-ui-drift | meeting NUMBER (Int) bound to `meeting_id` (String); `meeting_number` dropped | ui L203 vs target nav_params | Bind real meeting_id; pass meeting_number separately |
| G7 | organizer-dashboard / schedule row + KPI | flow-ui-drift | Today's-Schedule tap + Meetings-Today KPI route to group-list, not the meeting | ui targets group-list | Route to meeting-calendar/meeting-conduct for that group |
| G8 | member-add / save_button | flow-ui-drift | ui target member-list vs flow emits NavigateToMemberProfile | ui L300 vs flow L25 | Reconcile to member-profile of the new member |
| G9 | group-dashboard / view_savings (MEMBER) | structural-risk | Target needs memberId+typeConfig; dashboard holds only groupId+viewerRole → can't parameterize | ui vs member-savings-detail nav_params | Route MEMBER "My Savings" to personal-savings, or resolve memberId+typeConfig |
| G10 | personal-dashboard / savings_summary_card | flow-ui-drift | ui target personal-savings vs flow navigate savings-dashboard | ui L211 vs flow L31 | Reconcile to personal-savings with params |
| G11 | savings-dashboard / OpenMemberDetail | flow-ui-drift | Drops required `typeConfig` for member-savings-detail | ui/flow params vs target required | Forward typeConfig in ui + flow |
| G12 | group-list / FAB+join+on_group_click | flow-ui-drift | Stale flow navigates_to; join-with-code missing; drops required `viewerRole` | ui vs flow.yaml | Rewrite flow: FAB→group-type-picker, add join, forward viewerRole |
| G13 | group-dashboard / more_vert menu | dead-onclick | `OnMoreOptions` not in actions; menu undefined | ui L112-124 vs actions | Declare action + menu items, or remove |
| G14 | personal-dashboard / notification bell | dead-onclick | Badge icon with no on_click at all | ui L98-104 | Wire to notifications or declare explicit deferred action |
| G15 | group-list / notifications | missing-action | Emits `NotificationsDeferred` but action+event undeclared | ui L85-92 | Declare action+event; keep snackbar honest |
| G16 | loan-apply / submit_button | flow-ui-drift | Post-submit ui target loan-list vs flow navigate meeting-conduct | ui L256 vs flow L36 | Pick one destination; align ui+flow+event |
| G17 | loan-mark-defaulted-dialog / api ref | flow-ui-drift | ui refs `write_off_loan` (function) vs api `id: mark_loan_defaulted` | ui L109 vs api L6 | Standardize on api `id` across ui+flow |
| G18 | savings-dashboard / param keys | flow-ui-drift | snake `member_id`/`savings_type` vs action `{memberId}` | ui vs actions | Normalize to camelCase |

---

## 3 · Root-cause patterns

1. **Structural-green ≠ deployable.** The single most important finding: `matrix-green` measures nav/DTO/flow closure, not live-server backing or launch-capability presence. The whole server dimension (S1–S11, E1) + the three launch capabilities (demo-explore, accept-invitation, Play-Store track) are invisible to it.
2. **Server backing is authored-but-undeployed + unmigrated.** Contracts exist; runnable migrations, a demo seed, and a live companion server do not. This is the dominant blocking class and is partly **externally gated** (needs a self-service Fineract + `mcp-mifosx` deployed).
3. **Launch capabilities have zero upper-chain footprint.** demo-explore, first-class accept-invitation, server-demo-seed, auto-migrate/server-ready, and a Play-Store internal-test milestone have no FR/feature/phase — so they can't be planned or tracked.
4. **Auth round-trip loses the invite.** login-signup drops `pendingInviteCode` (F3/F4/G2) despite a P1 test asserting resume — the accept-invitation journey can't complete for a cold-launched invitee.
5. **Behavioral nav-drift on ~10 screens.** Dead notification/overflow affordances + destination/param mismatches (G4–G18) that a structural audit can't see but that break a clean emulator+Maestro pass.
6. **MUST features unscheduled / phase-split** (C1–C3): the self-signup thesis can't ship in v1 as specced.

---

## 4 · Enrich prompt (ready to run)

```
/idea-agent evolve "Make CommonPurse a production-deployable, device-verified group-banking app with real self-signup, accept-invitation, and demo-explore, backed by a migrated server. Close every gap in evolve-plans/20260801-production-signup-server-migration.md, bottom-up:

(1) REQUIREMENTS+ROADMAP: Add FRs+features for (a) demo-explore mode (guest/offline-seeded session), (b) a server demo-data-seed deliverable, (c) a standing idea→server auto-migrate/server-ready capability, (d) a first-class accept-invitation auth path. Fix orphan FR-025 (add to group-type-config requirement_refs), re-tag FR-026 as a constraint (not a must FR), and fix the notifications↔FR-019 cross-map (re-point meeting-lifecycle to FR-019; give notifications a real notification FR). Schedule the two unscheduled MUST features group-type-config + pluggable-distribution into the 1.0.0 milestone + distribution epic, move member-invitations (FR-024) into the 1.0.0 milestone, and add a Play-Store internal-testing milestone before closed_alpha.

(2) SERVER + FEATURE-DATA: In the server-layer, author RUNNABLE migrations (not prose) that (a) create ALL 21 datatables (15 tier2 + 6 companion) via POST /datatables/register, and (b) seed demo data for a demo user (clients + group activation, savings accounts, meeting records, corpus rows, one live invite code). Materialize the 4 absent api group files apis/{clients-members,savings,share-out,field-officer}.yaml. Add the missing MEETING calendar API GET /centers/{centerId}/meetings + collection-sheet (COMP-CAL) and fix the list_meetings→dt_meeting_record mis-mapping; add the GET /loans list op; correct the advanceCycle and loan-disburse command paths (Fineract /loans/{id}?command=disburse). Re-run /mifos-bridge --auto to regenerate the contract and EXTEND it to emit runnable datatable migrations so adding a feature migrates its missing API (server-ready). Wire every write's writes_to to the provisioned tables.

(3) FLOWS: Author flows/demo-explore-flow.yaml + journeys/demo-explore.yaml (login-signup → confirm dialog → demo session → dashboard). Make accept-invitation a first-class pre-auth entry in unified-auth-flow. Wire the invite resume: add login-signup nav_params.pendingInviteCode and branch on_login/on_signup on_success → NavigateToJoinWithCode(code) (satisfies TC-LS-010); make member-invitation-flow auto-associate the invitee. Reconcile join-with-code's single post-join landing. Add the in-app meeting schedule leg (or document auto-generation from group meetingDay + add reschedule).

(4) SCREEN BEHAVIOR: On login-signup add a professional auth UI with login / accept-invitation / sign-up AND a Demo Explore button whose on_click shows a confirm dialog ('this is a demo user logging in to explore the application') then enters a demo session. Add ScheduleMeeting on meeting-calendar. Fix the dead affordances and nav/param drift: organizer-dashboard notifications (G4) + schedule-row target (G7); previous-meeting-review launched_from (G5) + meeting-conduct meeting_id format (G6); member-add post-save (G8); group-dashboard My Savings nav (G9) + overflow menu (G13); personal-dashboard savings-card (G10) + notification bell (G14); savings-dashboard typeConfig + param keys (G11,G18); group-list FAB/join/viewerRole (G12) + deferred notifications (G15); loan-apply post-submit (G16); loan-mark-defaulted api ref (G17).

Regenerate the LLM mockups for the new/changed screens (demo-explore, the professional auth screen, meeting schedule, group-create steps). Implement every touched feature to PRODUCTION fidelity with Claude Intelligence (no stubs, no placeholders), wire real action_contracts, reconcile every flow.yaml with its ui.yaml, and VERIFY each feature on a real emulator + Maestro (network + UI). Server deployment (standing up the companion mcp-mifosx server + live Fineract) is externally gated — author + migrate everything, and where a live server is required to device-verify, HALT on that external dependency with pending-device-verify rather than a silent skip. Drive to matrix-green + zero CAPABILITY_GAPS + all pipeline capabilities terminal."
```

---

## 5 · Execution note

- **Auto-chain:** default (no `--plan-only`) → this plan hands off to `/idea-agent evolve` immediately.
- **Externally gated:** the server *deployment* (live Fineract + `mcp-mifosx` companion) is the one piece the drive cannot self-complete. It will materialize + migrate all server-layer artifacts (runnable migrations, demo seed, api group files, contract fixes, bridge extension) and implement + device-verify everything that does not require the live server, then **HALT on the external server-deploy dependency** (`pending-device-verify` / `external_dep_missing`) rather than claim a false green — per RULE-IDEA-AGENT-003 device-truth. Standing up the companion server is the human-gated step that unlocks the final live-network device verification.

---

## Capability Status

> Dashboard-tracked (SP-DASH). Phased R0..R6. Read/written by `/idea-evolve-plan --refine`.

| # | id | capability | type | phase | status |
|---|---|---|---|---|---|
| 1 | roadmap-schedule-must-features | Schedule group-type-config + pluggable-distribution + member-invitations into 1.0.0 milestone/epic | roadmap | R0 | ○ not-run |
| 2 | req-fix-orphans-crossmaps | Fix FR-025 orphan, FR-026 miscategorization, notifications↔FR-019 | requirement | R0 | ○ not-run |
| 3 | req-launch-capabilities | Add FRs/features: demo-explore, server-demo-seed, auto-migrate/server-ready, accept-invitation | requirement | R0 | ○ not-run |
| 4 | roadmap-playstore-testing-track | Add Play-Store internal-testing milestone | roadmap | R0 | ○ not-run |
| 5 | server-datatable-migrations | Runnable migrations for all 21 datatables | server | R1 | ○ not-run |
| 6 | server-demo-seed | Runnable demo-data seed for the demo user | server | R1 | ○ not-run |
| 7 | server-meeting-calendar-api | COMP-CAL GET /centers/{id}/meetings + collection-sheet | server | R1 | ○ not-run |
| 8 | server-missing-api-ops | GET /loans list + advanceCycle/disburse path fixes | server | R1 | ○ not-run |
| 9 | server-api-group-files | Materialize clients-members/savings/share-out/field-officer api files | server | R1 | ○ not-run |
| 10 | server-bridge-auto-migrate | Re-run + extend /mifos-bridge to emit runnable migrations | server | R1 | ○ not-run |
| 11 | flow-demo-explore | demo-explore flow + journey | flow | R2 | ○ not-run |
| 12 | flow-accept-invitation-firstclass | accept-invitation pre-auth entry + pendingInviteCode resume | flow | R2 | ○ not-run |
| 13 | flow-meeting-schedule-leg | in-app meeting schedule/reschedule (or documented auto-gen) | flow | R2 | ○ not-run |
| 14 | flow-nav-reconcile | join-with-code landing + member-invitation auto-associate | flow | R2 | ○ not-run |
| 15 | behavior-auth-screen | Professional auth UI: login/accept-invite/sign-up + Demo Explore button + dialog | behavior | R3 | ○ not-run |
| 16 | behavior-meeting-schedule-ui | ScheduleMeeting action on meeting-calendar | behavior | R3 | ○ not-run |
| 17 | behavior-dead-affordances | Fix G4/G13/G14/G15 dead notification/overflow affordances | behavior | R3 | ○ not-run |
| 18 | behavior-nav-param-drift | Fix G5–G12,G16–G18 destination/param drift | behavior | R3 | ○ not-run |
| 19 | mockups-regen | Regenerate LLM mockups for new/changed screens | design | R4 | ○ not-run |
| 20 | implement-production-fidelity | Implement every touched feature to production fidelity | implement | R5 | ○ not-run |
| 21 | device-verify-emulator-maestro | Emulator + Maestro network+UI verification per feature | verify | R6 | ○ not-run |
| 22 | server-deploy-live | Deploy companion mcp-mifosx + live Fineract (EXTERNALLY GATED) | server-deploy | R6 | ○ not-run |
