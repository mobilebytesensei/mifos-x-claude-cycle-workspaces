# Components Detailed — mifos-x-group-banking

## corpus_balance_card

**Purpose:** Shows group's total savings corpus with cycle progress.

```
┌─────────────────────────────────┐
│  Group Corpus        Cycle 1/12  │
│  KES 45,800          ████░░ 38%  │
│  +KES 1,500 this week            │
└─────────────────────────────────┘
```

Fields: corpus_amount (KES), cycle_number, cycle_length, weekly_delta, progress_pct.

## group_member_tile

**Purpose:** Member row in lists with role badge + status indicators.

```
[Avatar] Amina Wanjiru          [Treasurer]
         KES 4,200 saved  ● Active loan
```

Fields: name, role (dt_member_role), savings_balance, loan_status.

## loan_status_chip

**Purpose:** Color-coded loan state chip.

- Active → green (#2E7D32)
- Overdue → amber (#FF8F00)
- Defaulted → red (#B00020)
- Closed → grey (#757575)
- Pending Approval → blue (#1565C0)

## meeting_attendance_row

**Purpose:** Per-member attendance input in meeting-conduct.

```
[Avatar] Grace Muthoni   [Present ▼]   KES [___300___]
```

Fields: member_name, attendance_status (Present/Absent/Excused), savings_amount (editable).

## savings_collection_input

**Purpose:** Inline KES amount input for savings during meeting.

- Large 24sp number input for outdoor visibility
- Min/max from dt_group_config (contribution_min / contribution_max)
- Shows cumulative total as members are entered

## share_out_preview_card

**Purpose:** Per-member share-out calculation preview.

```
Grace Muthoni
Savings: KES 12,400  |  Interest: KES 1,240  |  Total: KES 13,640
```

Fields: member_name, savings_total, interest_share, payout_total.

## sync_status_indicator

**Purpose:** Global offline/sync badge in app bar.

- Online: hidden
- Offline: cloud_off icon (amber)
- Syncing: sync spinner (green)
- Sync error: error icon (red) with tap → sync-status screen
