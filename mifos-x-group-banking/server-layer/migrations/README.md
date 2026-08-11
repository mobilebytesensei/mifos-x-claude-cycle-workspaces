# MifosSave Server Migrations

Runnable migrations that provision the MifosSave (mifos-x-group-banking) backend on a
Fineract instance + its companion API (mcp-mifosx). These are the **executable** form of the
schemas that previously existed only as prose in `../API_CONTRACT.yaml` and
`../COMPANION_API_BUILD_DEPLOY.md`.

> **What is runnable here vs what is externally gated**
> - **Runnable now** (no live server needed): the migration *definitions* + the runner scripts
>   are checked in and lint/`--dry-run` clean. `bash register-datatables.sh --dry-run` and
>   `bash seed-demo/seed-demo.sh --dry-run` execute end-to-end offline.
> - **Externally gated** (needs the live deploy — see `../COMPANION_API_BUILD_DEPLOY.md §3`):
>   actually *applying* them requires (a) a reachable Fineract with the self-service module and
>   (b) the deployed companion API. Standing those up is the human-gated step; these scripts do
>   not and cannot do it.

## Layout

```
migrations/
├── README.md                                  ← this file
├── register-datatables.sh                     ← provisions all 21 datatables (idempotent)
├── datatables/
│   └── datatables.manifest.json               ← 21 register definitions (15 tier2 + 6 companion)
└── seed-demo/
    ├── demo-fixture.json                       ← canonical demo data (SoT, mirrors idea-layer/PROJECT_DEMO_DATA.yaml)
    └── seed-demo.sh                            ← creates the demo user + group + savings + meetings + corpus + invite
```

## 1. Register the 21 datatables

`datatables/datatables.manifest.json` holds one Fineract `POST /datatables` (COMP-DT-001
"register") payload per custom table. Types are lowercase (`string|number|decimal|boolean|date|datetime|text`)
— the casing `bridge-260504-001` confirmed against `sandbox.mifos.community` (see
`../BRIDGE_AUDIT_LOG.yaml` K1 / T2-1). `entitySubType` (CENTER|CLIENT|GROUP|LOAN) is included
because modern Fineract requires it.

| # | Table | apptable | rows | feature |
|---|-------|----------|------|---------|
| 1 | dt_group_config | m_group | single | group-management |
| 2 | dt_meeting_record | m_group | multi | meeting-lifecycle |
| 3 | dt_meeting_attendance | m_client | multi | meeting / fines |
| 4 | dt_member_role | m_client | single | auth / onboarding |
| 5 | dt_share_out | m_group | multi | share-out |
| 6 | dt_social_fund | m_group | single | social-fund |
| 7 | dt_loan_vote | m_loan | single | loan-management |
| 8 | dt_sync_metadata | m_group | single | offline-sync |
| 9 | dt_loan_request | m_client | multi | end-user-dashboard |
| 10 | dt_group_corpus | m_group | single | corpus-tracking |
| 11 | dt_group_loan_policy | m_group | single | loan-ceilings |
| 12 | dt_member_ceiling_override | m_client | single | loan-ceilings |
| 13 | dt_loan_guarantor | m_loan | multi | loan-guarantees |
| 14 | dt_notification | m_client | multi | notifications |
| 15 | dt_member_invitation | m_client | multi | member-invitations |
| 16 | dt_group_type_config | m_group | single | group-type-config (9-row archetype registry) |
| 17 | dt_companion_invitations | m_group | multi | invitations (token-keyed) |
| 18 | dt_rosca_rotation | m_group | multi | pluggable-distribution |
| 19 | dt_rosca_auction | m_group | multi | pluggable-distribution |
| 20 | dt_vsla_cycle | m_group | single | pluggable-distribution / share-out |
| 21 | dt_welfare_fund | m_group | single | social-fund |

Run:

```bash
# Dry run — offline, prints what would POST:
bash register-datatables.sh --dry-run

# Against a live Fineract:
FINERACT_BASE_URL=https://your-host/fineract-provider/api/v1 \
FINERACT_USER=mifos FINERACT_PASSWORD=password FINERACT_TENANT=default \
bash register-datatables.sh

# Single table:
FINERACT_BASE_URL=... bash register-datatables.sh --only dt_group_type_config
```

Already-registered tables are detected and skipped, so the script is safe to re-run.

## 2. Seed the demo account + demo data

`seed-demo/seed-demo.sh` reads `seed-demo/demo-fixture.json` and creates the demo user
(**Amina Otieno**), the demo group (**Mwangaza Women's Group**, a VSLA), 5 members + roles,
group-linked + voluntary savings, 3 meeting records, a corpus row, a VSLA cycle row, and
**one live invite code `DEMO24`** so accept-invitation / join-with-code is demonstrable
end-to-end.

The same fixture is mirrored (Claude-authored) into `idea-layer/PROJECT_DEMO_DATA.yaml` — that
YAML is what the **Demo Explore** feature reads offline when there is no live server. Keep the
two consistent (same ids, names, invite code, balances).

```bash
# Register tables first, then:
bash seed-demo/seed-demo.sh --dry-run          # offline preview

FINERACT_BASE_URL=https://your-host/fineract-provider/api/v1 \
COMPANION_BASE_URL=https://your-host/companion \
FINERACT_USER=mifos FINERACT_PASSWORD=password FINERACT_TENANT=default \
bash seed-demo/seed-demo.sh
```

> The savings-account creation step (§4) is described rather than hard-coded because the
> real call needs a savings `productId` resolved on the target Fineract. Wire that productId,
> then the create → approve → activate → deposit sequence runs as noted inline in the script.

## 3. Regeneration by `/mifos-bridge`

`datatables.manifest.json` is the emit target of the bridge auto-migrate extension (S10 /
FR-029). Re-running `/mifos-bridge --auto` after a feature adds a datatable appends its
register definition here, so "add a feature → its missing API is migrated" is a closed loop.
See `../COMPANION_API_BUILD_DEPLOY.md §5 (Bridge auto-migrate)`.

## Requirements

`bash`, `curl`, `jq`. `INSECURE=1` adds `curl -k` for self-signed sandbox certs.
