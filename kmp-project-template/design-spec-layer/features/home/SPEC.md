# Feature Spec: home

## Overview

Task management feature with calendar-based date selection and task CRUD operations.

## Screens

### TasksScreen
- **ViewModel**: TasksViewModel
- **State**: TasksUiState (selectedYear, selectedMonthIndex, selectedDayInMonth, weekdaysAndDaysInMonth)
- **Layout**:
  - Top toolbar with year/month navigation
  - Calendar grid showing days of selected month
  - Task list filtered by selected date
  - FAB to create new task
- **Navigation**: FAB → EditTaskScreen, Task item → EditTaskScreen
- **Requirements**: FR-001, FR-003, FR-004

### EditTaskScreen
- **ViewModel**: EditTaskViewModel
- **Layout**:
  - Top bar with back navigation
  - Task title input field
  - Task description input
  - Date/time picker
  - Save/Cancel buttons
- **Navigation**: Back → TasksScreen
- **Requirements**: FR-002

## Services

- **StorageService**: Task CRUD (create, read, update, delete)
- **CacheManager**: LRU cache for task data

## DI

- HomeModule provides: StorageServiceImpl, TasksViewModel, EditTaskViewModel
