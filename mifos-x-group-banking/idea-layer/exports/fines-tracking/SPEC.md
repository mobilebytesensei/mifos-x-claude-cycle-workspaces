# Fines Tracking — Feature Specification
**Project**: CommonPurse (mifos-x-group-banking)
**Feature ID**: fines-tracking
**Requirements**: FR-012, FR-020
**Version**: 1.0.0
**Status**: enriched

---

## Overview

Fines tracking covers two distinct fine types applied during the meeting wizard:
1. **Attendance fines** (FR-012): Automatically calculated when a member is marked Late (KES 50) or Absent (KES 100) on Step 1 of the meeting wizard. Fine amounts are shown inline on the member row and included in `totalFinesCollected` on submission.
2. **Overdue loan fines** (FR-020): Manually entered by the treasurer on Step 4 (Loan Review) when a loan is overdue. Fines are entered per loan as an additional `loanFines` amount, added to the meeting's `totalFinesCollected`, and stored in the meeting record.

Both fine types are collected during the meeting, included in the corpus balance computation (`closingCorpus += totalFinesCollected`), and recorded in the meeting record datatable. No standalone fines-management screen exists — fines are captured exclusively through the meeting wizard.

---

## Acceptance Criteria

- **FR-012**: Attendance fines are applied automatically when a member is marked Late (KES 50) or Absent (KES 100). Fine amounts appear inline as chips below the attendance toggle for each member. The total fines collected from attendance are added to `totalFinesCollected` and included in the closing corpus calculation.
- **FR-020**: Overdue loan penalties are entered on Step 4 (Loan Review). Each overdue loan shows an additional "Penalty Fine" input. Treasurer enters the fine amount; it is summed into `totalFinesCollected` and included in the meeting record. The corpus band updates in real time as fines are entered.

---

## Screens Involved

Fines tracking is implemented within the meeting-conduct wizard. No dedicated screen. Fine data surfaces in:

| Step | Step Name | Fine Type | FR |
|------|-----------|-----------|-----|
| 1 | Attendance | Attendance fines (Late: KES 50, Absent: KES 100) | FR-012 |
| 4 | Loan Review | Overdue loan penalty fine (treasurer-entered) | FR-020 |
| 6 | Closing Balance | totalFinesCollected shown in summary | Both |

---

## State Model (Fine-Relevant Fields from MeetingConductViewModel)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| attendanceMap | Map<String, AttendanceStatus> | emptyMap() | PRESENT / LATE / ABSENT per memberId |
| lateFines | Map<String, Long> | emptyMap() | KES 50 per LATE member (auto-computed) |
| absentFines | Map<String, Long> | emptyMap() | KES 100 per ABSENT member (auto-computed) |
| loanFines | Map<String, Long> | emptyMap() | Treasurer-entered penalty fine per loanId |
| totalFinesCollected | Long | 0L | Sum of all attendance fines + loan fines |

**totalFinesCollected computation**:
```
totalFinesCollected = 
  lateFines.values.sum() +        // KES 50 × LATE count
  absentFines.values.sum() +       // KES 100 × ABSENT count  
  loanFines.values.sum()           // treasurer-entered per overdue loan
```

**Actions**:
- `SetAttendance(memberId, AttendanceStatus)` — triggers auto-calc of lateFines/absentFines
- `SetLoanFine(loanId, fineAmount)` — updates loanFines map, recomputes totalFinesCollected

**DI**: MeetingRepository, SyncQueueRepository (via MeetingConductViewModel)

---

## AttendanceStatus Fine Policy

| Status | Fine Amount | Auto-Applied | Who Pays |
|--------|------------|-------------|----------|
| PRESENT | KES 0 | N/A | — |
| LATE | KES 50 | Yes (auto) | Member |
| ABSENT | KES 100 | Yes (auto) | Member (collected at next meeting or forgiven) |

Fine amounts are group-configurable in theory; current v1.0.0 constants are KES 50 / KES 100.

---

## Loan Fine Policy

| Condition | Fine Entry | Computation |
|-----------|-----------|-------------|
| Loan is OVERDUE (isOverdue=true) | Treasurer enters penalty in fine input field | Added to loanFines map |
| Loan is current (not overdue) | Fine field hidden | 0 |
| Fine field left empty | Default 0 | No fine recorded |
| Maximum fine | No cap in v1.0.0 | Treasurer-discretion |

---

## Navigation Table (fine entry points in wizard)

| Step | Component | Action |
|------|-----------|--------|
| Step 1 — Attendance | AttendanceMemberRow → segmented toggle LATE/ABSENT | SetAttendance → auto fine chip appears |
| Step 4 — Loan Review | LoanReviewRow → penalty fine TextField (shown when isOverdue=true) | SetLoanFine |
| Step 6 — Closing Balance | Summary card shows totalFinesCollected | Read-only display |

---

## API Endpoints Table

| Method | Path | Description |
|--------|------|-------------|
| POST | /datatables/dt_meeting_record | Includes totalFinesCollected in meeting record |
| POST | /datatables/dt_meeting_attendance | Per-member attendance with fineAmount field |

Fines are not posted as separate Fineract transactions — they are included in the meeting record's summary totals and per-member attendance records. Fine amounts contribute to corpus balance only (not to savings account deposits).

---

## Design Tokens Used

| Token | Value | Usage |
|-------|-------|-------|
| warningContainer | #FFF9C4 | Fine policy info chip (attendance step) |
| onWarningContainer | #E65100 | Fine policy chip text |
| errorContainer | #FFDAD6 | Fine amount chip per member (LATE/ABSENT), overdue badge |
| onErrorContainer | #410002 | Fine chip text, penalty fine label |
| error | #D32F2F | ABSENT indicator icon, overdue loan badge |
| primaryContainer | #A6F1A6 | Attendance progress chip (all recorded state) |
| onPrimaryContainer | #002106 | Attendance progress chip text (completed state) |
| tertiaryContainer | #D2E4FF | Corpus band (shows running total including fines) |
| onTertiaryContainer | #001C39 | Corpus band text |
