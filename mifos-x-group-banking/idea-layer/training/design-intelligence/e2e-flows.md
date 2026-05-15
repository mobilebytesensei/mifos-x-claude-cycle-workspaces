# E2E Flows — mifos-x-group-banking

## Flow 1: First Meeting (Group Cycle Start)

1. Treasurer (Amina) opens app → biometric login → admin-dashboard
2. Taps "Conduct Meeting" → meeting-calendar → selects today
3. meeting-conduct: marks all 5 members present
4. Records savings: KES 300 each × 5 = KES 1,500 total
5. No loan agenda items (cycle 1)
6. Submits → meeting-summary confirms: 5/5 attended, KES 1,500 collected
7. admin-dashboard updates corpus: KES 1,500

## Flow 2: Loan Application → Approval (Chairperson)

1. Member (Grace) logs in via personal-dashboard → requests KES 5,000 loan
2. loan-request form: purpose=school fees, collateral=phone
3. Treasurer sees pending request on admin-dashboard badge
4. Opens loan-apply for Grace → reviews → submits to chairperson
5. Chairperson (Joseph) approves → loan-detail shows disbursed
6. Grace sees active loan on personal-loans

## Flow 3: Offline Meeting Conduct

1. Field location has no connectivity
2. App shows offline banner (amber)
3. Treasurer conducts meeting — all inputs accepted
4. Submit → queued in SyncQueue (sync-status shows 1 pending)
5. On drive back to town — connectivity restored
6. Auto-sync fires → meeting record + attendance + savings pushed to Fineract
7. sync-status: 0 pending

## Flow 4: Share-Out (End of Cycle)

1. Chairperson opens group-dashboard → "Share Out" button active (cycle 12 complete)
2. share-out-preview: see each member's payout (pro-rata: KES 12,400–15,600 range)
3. Confirm total: KES 67,800
4. share-out-execute: biometric confirmation → execute
5. Fineract records withdrawals per member
6. dt_share_out datatable entry created
7. Group corpus resets to 0 → new cycle begins
