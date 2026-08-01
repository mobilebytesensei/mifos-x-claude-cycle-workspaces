# Journeys Index — CommonPurse (mifos-x-group-banking)

> 15 journeys | 8 critical | 7 medium | unified self-signup identity (per-group roles)

All journeys are first-class artifacts linked to features and flows.
Regenerated for the global self-signup pivot | 2026-07-17.
Coverage backfill (4 new journeys + 2 extended) for journey-missing
features | 2026-07-31.

Identity is unified — one login/signup for everyone; capabilities resolve
per-group after auth. Personas: Kofi=organizer (primary), Amina=treasurer,
Joseph=chairperson, Grace=member (all delegated per-group roles);
David/Sarah=optional supervisory tier (not the default identity).

## Journey Registry

| Journey ID | Name | Persona | Tier | Entry | Exit |
|------------|------|---------|------|-------|------|
| `organizer-end-to-end` | Organizer End-to-End: Signup to Share-Out | organizer (Kofi) | critical | login-signup | share-out-execute |
| `demo-explore` | Explore CommonPurse as a Demo User | prospective organizer (pre-signup) | critical | login-signup | savings-dashboard |
| `join-with-code` | Join a Group with an Invite Code | member (Grace) | critical | join-with-code | loan-request |
| `group-creation-flow` | Create a New Savings Group (Organizer Self-Serve) | organizer | critical | group-type-picker | group-dashboard |
| `meeting-conduct-full` | Conduct Full Group Meeting | organizer / treasurer | critical | meeting-calendar | meeting-summary |
| `loan-apply-to-approval` | Loan Application to Approval | treasurer + chairperson | critical | loan-list | loan-detail |
| `share-out-cycle` | Annual Share-Out Cycle Distribution | organizer / treasurer | critical | group-dashboard | share-out-execute |
| `member-onboarding` | Onboard a New Group Member (Organizer-Driven) | organizer / treasurer | critical | member-list | member-profile |
| `loan-repayment` | Service a Loan: Record Repayment or Mark Defaulted | treasurer / chairperson | medium | loan-list | loan-repayment-dialog |
| `offline-sync` | Check and Trigger Offline Sync | organizer / member | medium | organizer-dashboard | sync-status |
| `end-user-loan-request` | Member Loan Request Submission | member | medium | personal-loans | loan-request |
| `savings-review` | Review Group Savings and a Member's Savings Detail | organizer / treasurer | medium | savings-dashboard | member-savings-detail |
| `group-browse` | Browse Groups and Open a Group | organizer | medium | group-list | group-dashboard |
| `field-officer-oversight` | Field Officer Group Oversight | field officer (supervisory) | medium | field-officer-dashboard | group-dashboard |
| `settings-management` | Manage App Settings and Sign Out | any authenticated user | medium | settings | settings-logout-dialog |

## Feature Coverage Matrix

| Feature | Journeys |
|---------|---------|
| login-signup (unified-auth) | `organizer-end-to-end`, `join-with-code`, `demo-explore` |
| demo-explore | `demo-explore` |
| group-type-picker | `organizer-end-to-end`, `group-creation-flow` |
| group-create / group-management | `organizer-end-to-end`, `group-creation-flow`, `share-out-cycle` |
| member-invite / member-invitations | `organizer-end-to-end`, `join-with-code` |
| member-onboarding | `member-onboarding` |
| meeting-conduct / meeting-lifecycle | `organizer-end-to-end`, `meeting-conduct-full` |
| savings-collection | `organizer-end-to-end`, `meeting-conduct-full` |
| corpus-tracking | `meeting-conduct-full`, `share-out-cycle` |
| loan-management | `loan-apply-to-approval`, `loan-repayment`, `meeting-conduct-full` |
| loan-request | `join-with-code`, `end-user-loan-request` |
| share-out | `organizer-end-to-end`, `share-out-cycle` |
| sync-status / offline-sync | `offline-sync` |
| personal-dashboard / end-user-dashboard | `join-with-code`, `end-user-loan-request` |
| previous-meeting-review | `meeting-conduct-full` |
| loan-mark-defaulted-dialog | `loan-repayment` (collections branch) |
| savings-dashboard | `savings-review` |
| member-savings-detail | `savings-review` |
| group-list | `group-browse` |
| field-officer-dashboard | `field-officer-oversight` |
| settings | `settings-management` |
| settings-logout-dialog | `settings-management` |

## Critical Path (tier=critical, order matters)

```
1. organizer-end-to-end  → PRIMARY: self-signup → create group → invite → meeting → share-out
2. join-with-code        → member self-registers via invite → personal dashboard → loan request
3. group-creation-flow   → group-type-picker → group-create wizard → group-dashboard
4. member-onboarding     → organizer adds a member directly
5. meeting-conduct-full  → 7-step meeting wizard (most complex)
6. loan-apply-to-approval → treasurer applies, chairperson approves
7. share-out-cycle       → cycle-end preview → execute
```
