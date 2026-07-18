# template_meta
# template_version: "2.86.0"
# template_path: "core/blueprints/workspace-project/idea-layer/DATA_MODEL.md"
# generated_by: "/project-add layer scaffold (from idea-plan.yaml §requirements + research/FINERACT_API_SURFACE.md + research/OFFLINE_FIRST_BLUEPRINT.md)"

# Data Model — mifos-x-backoffice-next-gen

> **Version**: 1.0
> **Last Updated**: 2026-07-17
> **Status**: Draft — generated from idea-plan.yaml + Fineract API audit; refine as schema firms up.
> **Source of truth**: Apache Fineract server (entities) + `idea-layer/idea-plan.yaml` + `idea-layer/research/`

---

## 1. Entities

> Fineract owns the canonical business entities; the app caches them in Room (per-entity `SourceOfTruth`) and adds four **NEW** local infra entities for the offline-first outbox + permission layers.

| Entity | Description | Owner store | Source |
|--------|-------------|-------------|--------|
| Client | KYC/360° customer (identifiers, addresses, family, documents, notes, charges) | Fineract + Room cache | external API |
| Group / Center | Group & center hierarchy, membership, meetings, attendance | Fineract + Room cache | external API |
| Loan | Full lifecycle (product → application → approve → disburse → service → close); incl. Working-Capital | Fineract + Room cache | external API |
| SavingsAccount / FixedDeposit / RecurringDeposit / ShareAccount | Deposit & share products + accounts + transactions | Fineract + Room cache | external API |
| CollectionSheet | Center/group/individual dues sheet (field-ops workhorse) | Fineract + Room cache | external API |
| JournalEntry / GLAccount / GLClosure | Accounting & GL (balanced journals, closures, provisioning) | Fineract (online-only) | external API |
| Product / Charge | Loan/savings/FD/share products + charges + floating rates | Fineract + Room cache | external API |
| Office / Staff / Holiday / Fund / Code+CodeValue / PaymentType / Currency | Organization + reference data (dropdown vocabularies) | Fineract + Room cache | external API |
| User / Role / Permission | Admin control plane (users, roles, role→permission matrix) | Fineract (online-only) | external API |
| Teller / Cashier | Teller mgmt + cash allocation/settlement + cash position | Fineract + Room cache | external API |
| Datatable | Custom-field schema CRUD + rows (drives dynamic forms) | Fineract + Room cache | external API |
| Report / Audit / Notification / MakerChecker | Reports, audit trail, notifications, checker inbox | Fineract | external API |
| **DraftEntity** (`framework_submit_drafts`) | **NEW** — queued offline mutation w/ durable `idempotency_key` + `(action,entity)` | Room v11 (local) | local |
| **BookkeeperEntity** | Store5 write-back bookkeeping for entity-shaped edits | Room (local) | local |
| **FetchedAtEntity** | Per-cache freshness / TTL tracking | Room (local) | local |
| **PermissionSet + CapabilityMap** | Normalized login permissions[] (O(1) + fingerprint) + data-driven capability map | encrypted local store + `core/permissions` | derived (login) |

---

## 2. Entity Relationships

```
Office ──1:N──► Staff ──assigned──► Client ──1:N──► Loan ──1:N──► LoanTransaction
  │               │                   │  │            │
  │               │                   │  └─1:N──► SavingsAccount ──1:N──► SavingsTransaction
  │               │                   └─1:N──► Identifier/Address/Document/Note/Charge
  │               └──► CollectionSheet (center/group/individual)
  └──1:N──► Group ──N:M──► Client        (via GLIM/GSIM)
       │                                  Loan/Savings ──command──► MakerChecker (queued 2xx)
       └──► Center ──1:N──► Group
User ──N:M──► Role ──N:M──► Permission     (role→permission matrix; drives login permissions[])
Product ──template──► Loan/SavingsAccount   (GET /{entity}/template → dynamic form)
JournalEntry ──N:1──► GLAccount ──within──► GLClosure
DraftEntity ──replayed via──► POST /batches ──resolves──► the target Fineract command
```

---

## 3. Entity Details

### DraftEntity (`framework_submit_drafts`) — NEW (offline outbox)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| formKey | String | PK part (`(formKey, uniqueKey)`) | e.g. `loan_repayment`, `collection_sheet` |
| uniqueKey | String | PK part | e.g. loanId, centerId (multi-pending: N coexist) |
| payload | String (@Serializable JSON) | not null | the command body sent to Fineract |
| action | String | not null | maps to Fineract `command=` |
| entity | String | not null | target entity type |
| idempotency_key | String (UUIDv4) | **durable (Room v11)** | reused on retry → attached as Fineract `Idempotency-Key`; prevents double-post |
| status | Enum | `PENDING → RETRYING → SUBMITTED \| FAILED` | PENDING never pruned; 30d prune for terminal |
| created_at | Long (epoch) | not null | outbox ordering |
| server_error | String? | nullable | populated on FAILED → Needs-Attention inbox |

### PermissionSet / CapabilityMap — NEW (permission engine)

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| permissions | Set<String> | O(1) lookup | flat opaque codes; compose `{ACTION}_{ENTITY}`, never decompose |
| fingerprint | String | encrypted | change-detect for CapabilityMap re-resolve |
| umbrellas | Set<String> | — | `ALL_FUNCTIONS`, `ALL_FUNCTIONS_READ`, `CHECKER_SUPER_USER`, `REPORTING_SUPER_USER`, `TWOFACTOR_BYPASS` |
| capabilityMap | Map (data, remote-updatable) | `capability-map.json` | module/screen/action → required permission group; unmapped = HIDDEN (fail closed) |

> Cached Fineract entities (Client, Loan, SavingsAccount, …) follow the server's field shapes verbatim; per-entity Room `@Entity` + `@Dao` + mapper are generated during `/kmp-implement` from the Fineract client/DTOs — not re-specified here.

---

## 4. Data Sources & Ownership

| Entity | Origin | Authoritative store | Sync / refresh |
|--------|--------|---------------------|----------------|
| Client / Loan / Savings / Collections (read) | Fineract | Fineract (server) | CACHE_FIRST_SWR; delta-pull `changeListSync` over `lastModifiedSince` |
| Money-movement mutations (repayment/deposit/withdrawal/collection sheet) | app (offline outbox) | DraftEntity until replayed, then Fineract | queued → `POST /batches` replay on reconnect |
| Accounting / roles / product edits | app (online only) | Fineract | online-only + maker-checker (no deferred sync) |
| Reference data (offices, codes, paymenttypes, templates) | Fineract | Fineract + Room cache | hydrated at boot; feeds offline dropdown vocabularies + dynamic forms |
| Permissions | Fineract (`POST /v1/authentication`) | encrypted local PermissionSet | re-login / 403 drift refresh |

---

## 5. API ↔ Entity Mapping

> From `research/FINERACT_API_SURFACE.md` (965 ops). Grouped by module.

| API / endpoint group | Reads | Writes |
|----------------------|-------|--------|
| `/v1/authentication`, `/v1/userdetails` | permissions[], user/office/staff | — (session) |
| `/v1/clients` (+template, +external-id, sub-resources) | Client 360° | Client CRUD + lifecycle commands |
| `/v1/groups`, `/v1/centers`, `/v1/collectionsheet` | Group/Center, dues | membership, attendance, collection sheet save |
| `/v1/loans` (+template, calculateLoanSchedule), `/transactions`, `/rescheduleloans` | Loan, schedule preview | approve/disburse/repayment/writeoff/reschedule |
| `/v1/savingsaccounts`, `/v1/fixeddepositaccounts`, `/v1/recurringdepositaccounts`, `/v1/accounttransfers` | Deposit/share accounts + txns | deposit/withdrawal/hold/transfer commands |
| `/v1/glaccounts`, `/v1/journalentries`, `/v1/glclosures` | GL, journals | balanced journal entry, reverse, closure (online-only) |
| `/v1/loanproducts`, `/v1/savingsproducts`, `/v1/charges` | Products, charges | product + charge lifecycle (template-driven) |
| `/v1/offices`, `/v1/staff`, `/v1/codes`+`/codevalues`, `/v1/paymenttypes` | Org + reference data | org/reference-data admin |
| `/v1/users`, `/v1/roles`, `/v1/roles/{id}/permissions`, `/v1/permissions` | admin control plane | create users, role→permission matrix, maker-checker toggle |
| `/v1/tellers` + `/cashiers` | teller/cash position | allocate/settle cash |
| `/v1/datatables`, `/v1/configurations` | custom-field schemas, config | datatable + config CRUD (drives dynamic forms) |
| `/v1/runreports/{name}`, `/v1/search`, `/v1/audits`, `/v1/makercheckers` | reports, search, audit, checker inbox | approve/reject queued commands |
| `POST /v1/batches` | — | **transactional replay of the offline outbox (keystone)** |

---

## 6. Privacy & Access Control

| Entity | Classification | Protection |
|--------|----------------|------------|
| Client / KYC (identifiers, addresses, documents, family) | sensitive (PII) | SQLCipher DB + encrypted media; PII-scrubbed logs; screenshot-block; DPDP/GDPR consent/retention/erasure |
| Money-movement txns + DraftEntity payloads | sensitive | encrypted at rest; durable idempotency; maker-checker end-to-end |
| PermissionSet + fingerprint | sensitive | Keystore/Keychain-wrapped; biometric local lock |
| Accounting / GL | sensitive | online-only + maker-checker; server authorization is the only real gate |
| Reference data (codes, paymenttypes, currencies) | internal | cached; no special protection |
| Reports / audit | user-private (per report permission) | gated per `READ_{report}` / `REPORTING_SUPER_USER`; audit is read-only |

---

> Regenerate by `/idea-plan` / `/idea-sync` when §requirements or the Fineract API audit change.
> Hand-edits are preserved — the wizard prompts [Overwrite]/[Merge]/[Keep] before rewriting.
