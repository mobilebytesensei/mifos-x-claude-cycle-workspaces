# Field Officer View — Feature Specification
**Project**: CommonPurse (mifos-x-group-banking)
**Feature ID**: field-officer-view
**Requirement**: FR-009
**Version**: 1.0.0
**Status**: enriched

---

## Overview

The field officer dashboard provides a supervision view for Fineract field officers overseeing multiple VSLA groups. Unlike the group-admin view (chairperson/treasurer), the field officer sees an aggregate portfolio: 4 KPI summary cards (groups, members, total savings, loans outstanding), group health cards with GREEN/AMBER/RED overdue-rate indicators, and 3 filter chips (Region, Status, Overdue rate). An "Export Report" action generates a CSV summary of all groups. The dashboard is read-only — field officers observe group health and escalate issues; they do not initiate transactions.

---

## Acceptance Criteria

- **FR-009**: Field officers can see an aggregated view of all groups they supervise. The dashboard shows: (1) 4 KPI cards (total groups, total members, total savings, loans outstanding) using MD3 container colors; (2) group health cards with health indicator colored GREEN (overdueRate < 5%), AMBER (5–20%), or RED (≥ 20%); (3) filter chips for Region, Status, and Overdue rate; (4) an Export Report button that generates and shares a CSV summary. The field officer cannot initiate transactions — clicking a group card navigates to read-only group detail.

---

## Screens Table

| Screen ID | Route | Type | Role Required |
|-----------|-------|------|---------------|
| field-officer-dashboard | /field-officer | dashboard | FIELD_OFFICER (Fineract staff role) |

---

## State Model

### FieldOfficerDashboardViewModel
| Field | Type | Default |
|-------|------|---------|
| isLoading | Boolean | true |
| isRefreshing | Boolean | false |
| kpiTotalGroups | Int | 0 |
| kpiTotalMembers | Int | 0 |
| kpiTotalSavings | Long | 0L |
| kpiLoansOutstanding | Long | 0L |
| groups | List<GroupHealthCard> | emptyList() |
| filteredGroups | List<GroupHealthCard> | emptyList() |
| selectedRegion | String? | null |
| selectedStatus | GroupStatus? | null |
| selectedOverdueFilter | OverdueFilter? | null |
| isExporting | Boolean | false |
| error | String? | null |

**Screen states**: Loading, Content, Error

**Actions**: LoadDashboard, RefreshDashboard, FilterByRegion(region), FilterByStatus(status), FilterByOverdue(filter), ExportReport, OpenGroupDetail(groupId), ClearFilters

**Events**: NavigateToGroupDetail(groupId), ShareCsvFile(uri), ShowSnackbar(message)

**DI**: FieldOfficerRepository, ExportRepository, NavigationManager, ConnectivityObserver

---

## KPI Cards

| KPI | Label | Color Pair | Demo Value |
|-----|-------|-----------|-----------|
| KPITotalGroups | Total Groups | primaryContainer (#A6F1A6) / onPrimaryContainer (#002106) | 8 |
| KPITotalMembers | Total Members | secondaryContainer (#FFDDB3) / onSecondaryContainer (#2A1700) | 94 |
| KPITotalSavings | Total Savings | tertiaryContainer (#D2E4FF) / onTertiaryContainer (#001C39) | KES 142,000 |
| KPILoansOutstanding | Loans Outstanding | errorContainer (#FFDAD6) / onErrorContainer (#410002) | KES 87,500 |

---

## Group Health Indicators

| Health Level | Condition | Color | Label |
|-------------|-----------|-------|-------|
| GREEN | overdueRate < 5% | primary #2E7D32 / primaryContainer | Healthy |
| AMBER | 5% ≤ overdueRate < 20% | secondary #FF8F00 / secondaryContainer | At Risk |
| RED | overdueRate ≥ 20% | error #D32F2F / errorContainer | Critical |

---

## Filter Chips

| Filter | Values |
|--------|--------|
| Region | Nairobi / Mombasa / Kisumu / Nakuru (all available regions) |
| Status | ACTIVE / PENDING / CLOSED |
| Overdue | NONE (<1%) / LOW (<10%) / HIGH (>10%) |

---

## Navigation Table

| From | Action | To | Params |
|------|--------|----|--------|
| login (field officer role) | Auto-route | /field-officer | — |
| field-officer-dashboard | Tap group card | group-detail (read-only) | groupId |
| field-officer-dashboard | Tap Export Report | CSV share intent | — |

---

## API Endpoints Table

| Method | Path | Description |
|--------|------|-------------|
| GET | /fineract-provider/api/v1/centers?staffId={staffId}&limit=100 | All centers supervised by this field officer |
| GET | /fineract-provider/api/v1/loans?groupId={groupId}&loanStatus=active | Active loans per group (for overdue rate) |
| GET | /fineract-provider/api/v1/datatables/dt_group_corpus/{centerId} | Corpus balance per group |

---

## Design Tokens Used

| Token | Value | Usage |
|-------|-------|-------|
| primary | #2E7D32 | GREEN health indicator, KPI icon tint |
| primaryContainer | #A6F1A6 | KPI total groups background, GREEN health card tint |
| onPrimaryContainer | #002106 | Groups KPI text |
| secondary | #FF8F00 | AMBER health indicator |
| secondaryContainer | #FFDDB3 | KPI total members background, AMBER health card tint |
| onSecondaryContainer | #2A1700 | Members KPI text |
| tertiary | #1565C0 | Tertiary accent (savings icon) |
| tertiaryContainer | #D2E4FF | KPI total savings background |
| onTertiaryContainer | #001C39 | Savings KPI text |
| error | #D32F2F | RED health indicator |
| errorContainer | #FFDAD6 | KPI loans outstanding background, RED health card tint |
| onErrorContainer | #410002 | Loans KPI text |
| surface | #FAFAFA | Group health card background |
| onSurfaceVariant | #424942 | Subtitle text, secondary labels |
