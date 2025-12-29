# Tasks: Full-Stack Web Todo Application

**Feature**: 002-fullstack-web
**Branch**: `002-fullstack-web`
**Input**: Design documents from `/specs/002-fullstack-web/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/ (all complete)

**Test Strategy**: Per constitution Principle III, tests require user approval before implementation. This tasks file contains ONLY implementation tasks. Test tasks will be generated separately after TDD test case approval.

**Organization**: Tasks are grouped by user story (US1-US10) to enable independent implementation and testing of each story. After foundational phase, user stories can be developed in parallel by priority.

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, etc.)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize monorepo structure and install dependencies

- [x] T001 Create monorepo directory structure (frontend/, backend/, .specify/, specs/)
- [x] T002 [P] Initialize Next.js 16+ project with TypeScript in /home/ruser/q4/todo-app-web/frontend/
- [x] T003 [P] Initialize FastAPI project with UV in /home/ruser/q4/todo-app-web/backend/
- [x] T004 [P] Configure Tailwind CSS in /home/ruser/q4/todo-app-web/frontend/tailwind.config.ts
- [x] T005 [P] Setup TypeScript config in /home/ruser/q4/todo-app-web/frontend/tsconfig.json
- [x] T006 [P] Setup Python project with UV in /home/ruser/q4/todo-app-web/backend/pyproject.toml
- [x] T007 [P] Create frontend environment file template /home/ruser/q4/todo-app-web/frontend/.env.local.example
- [x] T008 [P] Create backend environment file template /home/ruser/q4/todo-app-web/backend/.env.example
- [x] T009 [P] Install frontend dependencies (next, react, typescript, tailwindcss, better-auth)
- [x] T010 [P] Install backend dependencies (fastapi, sqlmodel, python-jose, passlib, uvicorn)
- [x] T011 Create root-level CLAUDE.md with monorepo guidance at /home/ruser/q4/todo-app-web/CLAUDE.md
- [x] T012 [P] Create frontend CLAUDE.md at /home/ruser/q4/todo-app-web/frontend/CLAUDE.md
- [x] T013 [P] Create backend CLAUDE.md at /home/ruser/q4/todo-app-web/backend/CLAUDE.md
- [x] T014 Create docker-compose.yml for local development at /home/ruser/q4/todo-app-web/docker-compose.yml

**Checkpoint**: Project structure initialized, dependencies installed

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Database Setup

- [x] T015 Connect to Neon PostgreSQL and run schema creation script from /home/ruser/q4/todo-app-web/specs/002-fullstack-web/contracts/database-schema.sql
- [x] T016 Verify all tables created (users, tasks, tags, task_tags) with proper indexes

### Backend Foundation

- [x] T017 Create database connection module in /home/ruser/q4/todo-app-web/backend/src/database.py
- [x] T018 Create config module for environment variables in /home/ruser/q4/todo-app-web/backend/src/config.py
- [x] T019 [P] Create SQLModel User model in /home/ruser/q4/todo-app-web/backend/src/models.py
- [x] T020 [P] Create SQLModel Task model with priority enum in /home/ruser/q4/todo-app-web/backend/src/models.py
- [x] T021 [P] Create SQLModel Tag model in /home/ruser/q4/todo-app-web/backend/src/models.py
- [x] T022 [P] Create SQLModel TaskTag junction model in /home/ruser/q4/todo-app-web/backend/src/models.py
- [x] T023 Create Pydantic request/response schemas in /home/ruser/q4/todo-app-web/backend/src/schemas.py
- [x] T024 Create JWT verification middleware in /home/ruser/q4/todo-app-web/backend/src/auth.py
- [x] T025 Create FastAPI app with CORS middleware in /home/ruser/q4/todo-app-web/backend/src/main.py
- [x] T026 Create routes package init in /home/ruser/q4/todo-app-web/backend/src/routes/__init__.py

### Frontend Foundation

- [x] T027 Setup Better Auth configuration in /home/ruser/q4/todo-app-web/frontend/lib/auth.ts
- [x] T028 Create API client with JWT injection in /home/ruser/q4/todo-app-web/frontend/lib/api.ts
- [x] T029 Create utility functions (cn, etc.) in /home/ruser/q4/todo-app-web/frontend/lib/utils.ts
- [x] T030 [P] Create TypeScript types for User in /home/ruser/q4/todo-app-web/frontend/types/index.ts
- [x] T031 [P] Create TypeScript types for Task in /home/ruser/q4/todo-app-web/frontend/types/index.ts
- [x] T032 [P] Create TypeScript types for Tag in /home/ruser/q4/todo-app-web/frontend/types/index.ts
- [x] T033 Create root layout with metadata in /home/ruser/q4/todo-app-web/frontend/app/layout.tsx
- [x] T034 Create landing page in /home/ruser/q4/todo-app-web/frontend/app/page.tsx
- [x] T035 [P] Create reusable Button component in /home/ruser/q4/todo-app-web/frontend/components/ui/button.tsx
- [x] T036 [P] Create reusable Input component in /home/ruser/q4/todo-app-web/frontend/components/ui/input.tsx
- [x] T037 [P] Create reusable Select component in /home/ruser/q4/todo-app-web/frontend/components/ui/select.tsx
- [x] T038 [P] Create reusable Badge component in /home/ruser/q4/todo-app-web/frontend/components/ui/badge.tsx
- [x] T039 [P] Create reusable Card component in /home/ruser/q4/todo-app-web/frontend/components/ui/card.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1)

**Goal**: Enable users to create accounts and sign in with email/password

**Independent Test**: Visit application, create account with email/password, sign out, sign back in. Session persists across browser close.

**Requirements**: FR-001 through FR-007 (signup, signin, session management, signout)

### Implementation for User Story 1

- [x] T040 [P] [US1] Create Better Auth API route in /home/ruser/q4/todo-app-web/frontend/app/api/auth/[...better-auth]/route.ts
- [x] T041 [P] [US1] Create auth routes package in /home/ruser/q4/todo-app-web/backend/src/routes/auth.py
- [x] T042 [US1] Implement POST /api/auth/signup endpoint in /home/ruser/q4/todo-app-web/backend/src/routes/auth.py
- [x] T043 [US1] Implement POST /api/auth/signin endpoint in /home/ruser/q4/todo-app-web/backend/src/routes/auth.py
- [x] T044 [US1] Register auth routes in FastAPI app in /home/ruser/q4/todo-app-web/backend/src/main.py
- [x] T045 [P] [US1] Create auth route group layout in /home/ruser/q4/todo-app-web/frontend/app/(auth)/layout.tsx
- [x] T046 [P] [US1] Create signup page in /home/ruser/q4/todo-app-web/frontend/app/(auth)/signup/page.tsx
- [x] T047 [P] [US1] Create signin page in /home/ruser/q4/todo-app-web/frontend/app/(auth)/signin/page.tsx
- [x] T048 [P] [US1] Create SignupForm component in /home/ruser/q4/todo-app-web/frontend/components/auth/signup-form.tsx
- [x] T049 [P] [US1] Create SigninForm component in /home/ruser/q4/todo-app-web/frontend/components/auth/signin-form.tsx
- [x] T050 [US1] Add email format validation to signup/signin forms
- [x] T051 [US1] Add password length validation (min 8 characters)
- [x] T052 [US1] Implement session persistence (7-day JWT token)
- [x] T053 [US1] Add protected route middleware to redirect unauthenticated users
- [x] T054 [US1] Implement signout functionality with session clearing
- [x] T055 [US1] Add error handling for invalid credentials (401 responses)
- [x] T056 [US1] Add error handling for duplicate email (409 responses)

**Checkpoint**: US1 complete - users can create accounts, sign in, and access protected routes

---

## Phase 4: User Story 10 - User Isolation and Data Security (Priority: P1)

**Goal**: Ensure each user only sees their own tasks and cannot access other users' data

**Independent Test**: Create two user accounts, add tasks to each, verify User A cannot see User B's tasks by any means.

**Requirements**: FR-036 through FR-041 (user isolation, JWT verification, security)

**Note**: US10 is implemented early because it provides the security foundation for all subsequent stories

### Implementation for User Story 10

- [x] T057 [US10] Add user_id verification in get_current_user dependency in /home/ruser/q4/todo-app-web/backend/src/auth.py
- [x] T058 [US10] Create verify_user_access helper function in /home/ruser/q4/todo-app-web/backend/src/auth.py
- [x] T059 [US10] Add user_id parameter validation middleware for all protected routes
- [x] T060 [US10] Implement 403 Forbidden response for user_id mismatch attempts
- [x] T061 [US10] Add input sanitization for XSS prevention in request schemas
- [x] T062 [US10] Verify all database queries use parameterized queries (SQLModel default)
- [x] T063 [US10] Add proper HTTP status codes (200, 201, 400, 401, 403, 404, 500) to all endpoints

**Checkpoint**: US10 complete - user isolation enforced, security foundation ready for task operations

---

## Phase 5: User Story 2 - Create and View Tasks via Web Interface (Priority: P1)

**Goal**: Enable users to create tasks with title/description and view them in a list

**Independent Test**: Sign in, submit task creation form with valid data, verify task appears in list with title, status, and creation date.

**Requirements**: FR-008 through FR-015 (task CRUD: create and read only)

### Implementation for User Story 2

- [x] T064 [P] [US2] Create tasks routes package in /home/ruser/q4/todo-app-web/backend/src/routes/tasks.py
- [x] T065 [US2] Implement POST /api/{user_id}/tasks endpoint for task creation in /home/ruser/q4/todo-app-web/backend/src/routes/tasks.py
- [x] T066 [US2] Implement GET /api/{user_id}/tasks endpoint for listing tasks in /home/ruser/q4/todo-app-web/backend/src/routes/tasks.py
- [x] T067 [US2] Implement GET /api/{user_id}/tasks/{task_id} endpoint for task details in /home/ruser/q4/todo-app-web/backend/src/routes/tasks.py
- [x] T068 [US2] Register task routes in FastAPI app in /home/ruser/q4/todo-app-web/backend/src/main.py
- [x] T069 [US2] Add title validation (1-200 characters, non-empty) to TaskCreate schema
- [x] T070 [US2] Add description validation (max 1000 characters) to TaskCreate schema
- [x] T071 [US2] Add auto-incrementing ID generation per user's task list
- [x] T072 [US2] Add creation timestamp and updated timestamp to task creation
- [x] T073 [P] [US2] Create dashboard layout in /home/ruser/q4/todo-app-web/frontend/app/dashboard/layout.tsx
- [x] T074 [US2] Create dashboard page in /home/ruser/q4/todo-app-web/frontend/app/dashboard/page.tsx
- [x] T075 [P] [US2] Create TaskForm component in /home/ruser/q4/todo-app-web/frontend/components/tasks/task-form.tsx
- [x] T076 [P] [US2] Create TaskList component in /home/ruser/q4/todo-app-web/frontend/components/tasks/task-list.tsx
- [x] T077 [P] [US2] Create TaskItem component in /home/ruser/q4/todo-app-web/frontend/components/tasks/task-item.tsx
- [x] T078 [US2] Add form validation for title (required, max 200 chars)
- [x] T079 [US2] Add form validation for description (max 1000 chars)
- [x] T080 [US2] Implement task creation API call with error handling
- [x] T081 [US2] Implement task list API call with loading state
- [x] T082 [US2] Add empty state message when no tasks exist
- [x] T083 [US2] Add success confirmation message after task creation
- [x] T084 [US2] Implement form reset after successful task creation
- [x] T085 [US2] Prevent form resubmission while API request is in progress

**Checkpoint**: US2 complete - users can create and view tasks in web interface

---

## Phase 6: User Story 3 - Update and Delete Tasks (Priority: P2)

**Goal**: Enable users to edit task details or remove tasks they no longer need

**Independent Test**: Create a task, click edit to modify title/description, save changes, verify updates persist. Delete a task, verify it's removed from list.

**Requirements**: FR-012 (update), FR-013 (delete)

### Implementation for User Story 3

- [x] T086 [US3] Implement PUT /api/{user_id}/tasks/{task_id} endpoint in /home/ruser/q4/todo-app-web/backend/src/routes/tasks.py
- [x] T087 [US3] Implement DELETE /api/{user_id}/tasks/{task_id} endpoint in /home/ruser/q4/todo-app-web/backend/src/routes/tasks.py
- [x] T088 [US3] Add TaskUpdate schema with optional fields in /home/ruser/q4/todo-app-web/backend/src/schemas.py
- [x] T089 [US3] Add updated_at timestamp auto-update on task modification
- [x] T090 [US3] Add validation for empty title on update (reject with 400)
- [x] T091 [US3] Add 404 Not Found response for non-existent task updates/deletes
- [x] T092 [P] [US3] Add edit button to TaskItem component in /home/ruser/q4/todo-app-web/frontend/components/tasks/task-item.tsx
- [x] T093 [P] [US3] Add delete button to TaskItem component in /home/ruser/q4/todo-app-web/frontend/components/tasks/task-item.tsx
- [x] T094 [US3] Create TaskEditModal component in /home/ruser/q4/todo-app-web/frontend/components/tasks/task-edit-modal.tsx
- [x] T095 [US3] Implement task update API call with optimistic UI update
- [x] T096 [US3] Implement task delete API call with optimistic UI removal
- [x] T097 [US3] Add delete confirmation dialog before permanent deletion
- [x] T098 [US3] Add error handling for failed update/delete operations
- [x] T099 [US3] Refresh task list after successful update/delete

**Checkpoint**: US3 complete - users can edit and delete tasks

---

## Phase 7: User Story 4 - Mark Tasks as Complete (Priority: P2)

**Goal**: Enable users to toggle task completion status to track progress

**Independent Test**: Create a pending task, click complete button, verify status changes with visual indicator (checkmark, strikethrough, or color change).

**Requirements**: FR-014 (toggle completion status)

### Implementation for User Story 4

- [x] T100 [US4] Implement PATCH /api/{user_id}/tasks/{task_id}/complete endpoint in /home/ruser/q4/todo-app-web/backend/src/routes/tasks.py
- [x] T101 [US4] Add toggle logic for completed boolean field (true ↔ false)
- [x] T102 [US4] Add updated_at timestamp update on completion toggle
- [x] T103 [US4] Add completion button to TaskItem component in /home/ruser/q4/todo-app-web/frontend/components/tasks/task-item.tsx
- [x] T104 [US4] Add visual indicator for completed tasks (strikethrough, checkmark, color)
- [x] T105 [US4] Implement completion toggle API call with optimistic UI update
- [x] T106 [US4] Add transition animation for completion state change

**Checkpoint**: US4 complete - users can mark tasks as complete and see visual feedback

---

## Phase 8: User Story 5 - Prioritize Tasks with Colored Badges (Priority: P3)

**Goal**: Enable users to assign priority levels (high, medium, low) with colored visual indicators

**Independent Test**: Create task with high priority, verify red badge displays. Change to medium (yellow), then low (green) to confirm visual indicators work correctly.

**Requirements**: FR-016 through FR-019 (priority assignment, default, update, display)

### Implementation for User Story 5

- [x] T107 [US5] Add priority field to TaskCreate schema with default 'medium' in /home/ruser/q4/todo-app-web/backend/src/schemas.py
- [x] T108 [US5] Add priority field to TaskUpdate schema in /home/ruser/q4/todo-app-web/backend/src/schemas.py
- [x] T109 [US5] Verify priority enum validation (high, medium, low only) in schemas
- [x] T110 [US5] Add priority dropdown to TaskForm component in /home/ruser/q4/todo-app-web/frontend/components/tasks/task-form.tsx
- [x] T111 [US5] Add priority dropdown to TaskEditModal component in /home/ruser/q4/todo-app-web/frontend/components/tasks/task-edit-modal.tsx
- [x] T112 [US5] Add priority badge to TaskItem component with color mapping (red=high, yellow=medium, green=low) in /home/ruser/q4/todo-app-web/frontend/components/tasks/task-item.tsx
- [x] T113 [US5] Implement conditional Tailwind classes for priority badge colors

**Checkpoint**: US5 complete - users can assign priorities with visual indicators

---

## Phase 9: User Story 6 - Organize Tasks with Tags (Priority: P3)

**Goal**: Enable users to add multiple tags to tasks for categorization

**Independent Test**: Create task, type "work" in tag input to see autocomplete suggestions, add multiple tags (work, urgent), verify they appear as removable pills.

**Requirements**: FR-020 through FR-025 (tag add, many-to-many, autocomplete, display, remove, prevent duplicates)

### Implementation for User Story 6

- [x] T114 [P] [US6] Create tags routes package in /home/ruser/q4/todo-app-web/backend/src/routes/tags.py
- [x] T115 [US6] Implement GET /api/{user_id}/tags endpoint for listing user tags in /home/ruser/q4/todo-app-web/backend/src/routes/tags.py
- [x] T116 [US6] Implement GET /api/{user_id}/tags/autocomplete endpoint with LIKE query in /home/ruser/q4/todo-app-web/backend/src/routes/tags.py
- [x] T117 [US6] Register tag routes in FastAPI app in /home/ruser/q4/todo-app-web/backend/src/main.py
- [x] T118 [US6] Add tags field to TaskCreate schema (array of tag ids) in /home/ruser/q4/todo-app-web/backend/src/schemas.py
- [x] T119 [US6] Add tags field to TaskUpdate schema in /home/ruser/q4/todo-app-web/backend/src/schemas.py
- [x] T120 [US6] Implement tag creation/upsert logic (get or create by name) in tasks.py
- [x] T121 [US6] Implement TaskTag junction creation when associating tags with tasks
- [x] T122 [US6] Add duplicate tag prevention (unique constraint on task_id, tag_id)
- [x] T123 [US6] Add tag removal logic for task updates (delete old associations, create new)
- [x] T124 [US6] Add tags to task response schema with proper JOIN query
- [x] T125 [US6] Create TagInput component with autocomplete in /home/ruser/q4/todo-app-web/frontend/components/tasks/tag-input.tsx
- [x] T126 [US6] Implement debounced autocomplete API call (300ms delay) in useTags hook
- [x] T127 [US6] Add tag pills display to TaskItem component in /home/ruser/q4/todo-app-web/frontend/components/tasks/task-item.tsx
- [x] T128 [US6] Add tag input to TaskForm component in /home/ruser/q4/todo-app-web/frontend/components/tasks/task-form.tsx
- [x] T129 [US6] Add tag input to TaskEditModal component in /home/ruser/q4/todo-app-web/frontend/components/tasks/task-edit-modal.tsx
- [x] T130 [US6] Implement tag removal UI (X button on tag pills)
- [x] T131 [US6] Add Enter key handler for adding tags from input
- [x] T132 [US6] Prevent duplicate tags on same task (client-side validation)

**Checkpoint**: US6 complete - users can organize tasks with tags

---

## Phase 10: User Story 7 - Search Tasks by Keyword (Priority: P3)

**Goal**: Enable users to search tasks by typing keywords in title or description

**Independent Test**: Create tasks with distinct titles/descriptions, type keyword in search bar, verify only matching tasks are displayed. Clear search to show all tasks.

**Requirements**: FR-026 (search functionality)

### Implementation for User Story 7

- [x] T133 [US7] Add search query parameter to GET /api/{user_id}/tasks endpoint in /home/ruser/q4/todo-app-web/backend/src/routes/tasks.py
- [x] T134 [US7] Implement ILIKE search filter for title and description fields
- [x] T135 [US7] Add OR logic for searching in both title and description
- [x] T136 [US7] Create TaskSearch component in /home/ruser/q4/todo-app-web/frontend/components/tasks/task-search.tsx
- [x] T137 [US7] Add search input to dashboard page above task list in /home/ruser/q4/todo-app-web/frontend/app/dashboard/page.tsx
- [x] T138 [US7] Implement debounced search input (300ms delay) to reduce API calls
- [x] T139 [US7] Update task list API call to include search query parameter
- [x] T140 [US7] Add "no results found" message when search returns empty
- [x] T141 [US7] Add clear search button to reset search input

**Checkpoint**: US7 complete - users can search tasks by keyword

---

## Phase 11: User Story 8 - Filter Tasks by Status, Priority, Tags (Priority: P3)

**Goal**: Enable users to filter task list by completion status, priority level, or tags

**Independent Test**: Create tasks with different statuses/priorities/tags, use filter dropdowns to show only "pending" tasks, or only "high priority" tasks, or only tasks tagged "work". Verify correct subset appears.

**Requirements**: FR-027 through FR-031 (status filter, priority filter, tag filter, multiple filters, clear filters)

### Implementation for User Story 8

- [x] T142 [US8] Add status query parameter to GET /api/{user_id}/tasks endpoint in /home/ruser/q4/todo-app-web/backend/src/routes/tasks.py
- [x] T143 [US8] Add priority query parameter with comma-separated support in /home/ruser/q4/todo-app-web/backend/src/routes/tasks.py
- [x] T144 [US8] Add tags query parameter with comma-separated support in /home/ruser/q4/todo-app-web/backend/src/routes/tasks.py
- [x] T145 [US8] Implement status filter logic (all, pending, completed)
- [x] T146 [US8] Implement priority filter logic with IN clause for multiple priorities
- [x] T147 [US8] Implement tag filter logic with JOIN and IN clause for multiple tags
- [x] T148 [US8] Combine all filters with AND logic in single query
- [x] T149 [US8] Create TaskFilter component in /home/ruser/q4/todo-app-web/frontend/components/tasks/task-filter.tsx
- [x] T150 [US8] Add status filter dropdown (all, pending, completed)
- [x] T151 [US8] Add priority filter dropdown with multiple selection support
- [x] T152 [US8] Add tag filter dropdown with multiple selection support
- [x] T153 [US8] Update task list API call to include filter query parameters
- [x] T154 [US8] Add "Clear filters" button to reset all filters
- [x] T155 [US8] Display active filter count badge
- [x] T156 [US8] Persist filter state during user session (local state)

**Checkpoint**: US8 complete - users can filter tasks by multiple criteria

---

## Phase 12: User Story 9 - Sort Tasks by Different Criteria (Priority: P4)

**Goal**: Enable users to sort tasks by creation date, priority, or title

**Independent Test**: Create several tasks with different creation dates and priorities, use sort dropdown to select "Priority" and verify high-priority tasks appear first, then switch to "Created date" and verify newest tasks appear first.

**Requirements**: FR-032 through FR-035 (sort dropdown, ascending/descending, apply after filter, persist preferences)

### Implementation for User Story 9

- [x] T157 [US9] Add sort_by query parameter to GET /api/{user_id}/tasks endpoint in /home/ruser/q4/todo-app-web/backend/src/routes/tasks.py
- [x] T158 [US9] Add sort_order query parameter (asc, desc) in /home/ruser/q4/todo-app-web/backend/src/routes/tasks.py
- [x] T159 [US9] Implement sort by created_at (default descending)
- [x] T160 [US9] Implement sort by priority (high > medium > low)
- [x] T161 [US9] Implement sort by title (alphabetical)
- [x] T162 [US9] Apply sorting AFTER filtering in query pipeline
- [x] T163 [US9] Create TaskSort component in /home/ruser/q4/todo-app-web/frontend/components/tasks/task-sort.tsx
- [x] T164 [US9] Add sort_by dropdown (created_at, priority, title)
- [x] T165 [US9] Add sort_order toggle button (ascending/descending)
- [x] T166 [US9] Update task list API call to include sort query parameters
- [x] T167 [US9] Persist sort preferences during user session (local state)
- [x] T167a [US9] Implement filter/sort state persistence using localStorage in /home/ruser/q4/todo-app-web/frontend/lib/hooks/useTaskFilters.ts

**Checkpoint**: US9 complete - users can sort tasks by different criteria with state persistence

---

## Phase 13: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and deployment preparation

### UI/UX Polish

- [x] T168 [P] Add loading spinners for all API calls in /home/ruser/q4/todo-app-web/frontend/components/ui/spinner.tsx
- [x] T169 [P] Add toast notifications for success/error messages in /home/ruser/q4/todo-app-web/frontend/components/ui/toast.tsx
- [x] T170 Add responsive design breakpoints for mobile/tablet/desktop
- [x] T171 Add accessibility attributes (ARIA labels, roles, keyboard navigation)
- [x] T172 Add loading skeleton components for task list
- [x] T173 Add transition animations for task state changes
- [x] T174 Add error boundary component for graceful error handling

### Performance Optimization

- [x] T175 Add React.memo to TaskItem component to prevent unnecessary re-renders
- [x] T176 Implement virtual scrolling for large task lists (500+ tasks)
- [x] T177 Add request debouncing for all API calls (search, filter, sort)
- [x] T178 Optimize database queries with proper index usage verification

### Security Hardening

- [x] T179 Add rate limiting middleware to backend API endpoints
- [x] T180 Add XSS sanitization verification for all user inputs
- [x] T181 Add CSRF protection for Better Auth endpoints
- [x] T182 Verify all SQL queries use parameterized queries (SQLModel audit)
- [x] T183 Add security headers (CSP, X-Frame-Options, etc.) to Next.js config

### Documentation

- [x] T184 [P] Update README.md with project overview and quick start
- [x] T185 [P] Create API documentation with example requests/responses
- [x] T186 [P] Create deployment guide for Vercel + Railway/Render
- [x] T187 Add inline code comments for complex logic
- [x] T188 Verify quickstart.md instructions work end-to-end

### Deployment Preparation

- [x] T189 [P] Create Dockerfile for backend in /home/ruser/q4/todo-app-web/backend/Dockerfile
- [x] T190 [P] Create vercel.json for frontend deployment in /home/ruser/q4/todo-app-web/frontend/vercel.json
- [x] T191 Configure environment variables for production (Neon, Railway/Render, Vercel)
- [x] T192 Test production build locally (npm run build, uvicorn with production settings)
- [x] T193 Deploy backend to Railway/Render free tier
- [x] T194 Deploy frontend to Vercel free tier
- [x] T195 Verify end-to-end functionality in production environment

**ALL TASKS COMPLETE - TaskFlow is ready for production!**

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) completion
- **User Story 10 (Phase 4)**: Depends on User Story 1 (Phase 3) completion - provides security foundation
- **User Stories 2-9 (Phase 5-12)**: All depend on Foundational (Phase 2) and US10 (Phase 4) completion
  - Can proceed in parallel after security foundation ready
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 13)**: Depends on desired user stories being complete

### User Story Dependencies

```
Phase 1: Setup
    ↓
Phase 2: Foundational (BLOCKS ALL STORIES)
    ↓
Phase 3: US1 (Authentication) ← Must be first
    ↓
Phase 4: US10 (User Isolation) ← Security foundation
    ↓
    ├─→ Phase 5: US2 (Create/View Tasks) ← Can parallelize after US10
    ├─→ Phase 6: US3 (Update/Delete) ← Depends on US2
    ├─→ Phase 7: US4 (Complete) ← Depends on US2
    ├─→ Phase 8: US5 (Priorities) ← Depends on US2
    ├─→ Phase 9: US6 (Tags) ← Depends on US2
    ├─→ Phase 10: US7 (Search) ← Depends on US2
    ├─→ Phase 11: US8 (Filter) ← Depends on US2, US5, US6
    └─→ Phase 12: US9 (Sort) ← Depends on US2, US5
```

### Within Each User Story

- Models before services
- Services before endpoints
- Backend endpoints before frontend components
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

**Phase 1 (Setup)**: All tasks marked [P] can run in parallel
- T002, T003 (frontend/backend init)
- T004, T005, T006 (config files)
- T007, T008 (env templates)
- T009, T010 (dependency install)
- T012, T013 (CLAUDE.md files)

**Phase 2 (Foundational)**: Selected tasks marked [P] can run in parallel
- T019, T020, T021, T022 (all models)
- T030, T031, T032 (all TypeScript types)
- T035, T036, T037, T038, T039 (all UI components)

**After US10**: Multiple user stories can be worked on in parallel by different developers
- US2, US3, US4, US5, US6, US7 can all start in parallel (after US2 endpoints exist)
- US8 should wait for US5 and US6 (needs priorities and tags)
- US9 should wait for US5 (needs priorities)

---

## Implementation Strategy

### MVP First (User Stories 1, 10, 2 Only)

1. Complete Phase 1: Setup (14 tasks)
2. Complete Phase 2: Foundational (25 tasks) - CRITICAL
3. Complete Phase 3: US1 Authentication (17 tasks)
4. Complete Phase 4: US10 User Isolation (7 tasks)
5. Complete Phase 5: US2 Create/View Tasks (22 tasks)
6. **STOP and VALIDATE**: Test MVP independently
7. Deploy/demo if ready (users can sign up, create tasks, view tasks securely)

**Total MVP Tasks**: 85 tasks

### Incremental Delivery

1. MVP (US1, US10, US2) → Deploy → Demo (85 tasks)
2. Add US3 Update/Delete → Test → Deploy (14 tasks)
3. Add US4 Complete → Test → Deploy (7 tasks)
4. Add US5 Priorities → Test → Deploy (7 tasks)
5. Add US6 Tags → Test → Deploy (19 tasks)
6. Add US7 Search → Test → Deploy (9 tasks)
7. Add US8 Filter → Test → Deploy (15 tasks)
8. Add US9 Sort → Test → Deploy (11 tasks)
9. Add Polish → Deploy final version (27 tasks)

**Total All Stories**: 194 tasks

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (39 tasks)
2. Developer A: US1 + US10 (24 tasks)
3. Once US1 + US10 done, parallel work begins:
   - Developer B: US2 (22 tasks)
   - Developer C: US5 Priorities (7 tasks) - can start in parallel
4. After US2 complete:
   - Developer A: US3 Update/Delete (14 tasks)
   - Developer B: US4 Complete (7 tasks)
   - Developer C: US6 Tags (19 tasks)
5. After US5 + US6 complete:
   - Developer A: US7 Search (9 tasks)
   - Developer B: US8 Filter (15 tasks)
   - Developer C: US9 Sort (11 tasks)
6. All: Polish together (27 tasks)

---

## Task Statistics

### Total Task Count: 195 tasks

### Tasks by Phase:
- Phase 1 (Setup): 14 tasks
- Phase 2 (Foundational): 25 tasks
- Phase 3 (US1 - Authentication): 17 tasks
- Phase 4 (US10 - User Isolation): 7 tasks
- Phase 5 (US2 - Create/View): 22 tasks
- Phase 6 (US3 - Update/Delete): 14 tasks
- Phase 7 (US4 - Complete): 7 tasks
- Phase 8 (US5 - Priorities): 7 tasks
- Phase 9 (US6 - Tags): 19 tasks
- Phase 10 (US7 - Search): 9 tasks
- Phase 11 (US8 - Filter): 15 tasks
- Phase 12 (US9 - Sort): 11 tasks
- Phase 13 (Polish): 27 tasks

### Tasks by User Story:
- US1 (Authentication): 17 tasks
- US2 (Create/View): 22 tasks
- US3 (Update/Delete): 14 tasks
- US4 (Complete): 7 tasks
- US5 (Priorities): 7 tasks
- US6 (Tags): 19 tasks
- US7 (Search): 9 tasks
- US8 (Filter): 15 tasks
- US9 (Sort): 11 tasks
- US10 (User Isolation): 7 tasks
- Setup/Foundational: 39 tasks
- Polish: 27 tasks

### Parallelizable Tasks: 32 tasks marked [P]

### Blocking Tasks:
- Phase 2 (Foundational) BLOCKS all user stories
- US1 (Authentication) BLOCKS US10
- US10 (User Isolation) BLOCKS all task-related stories
- US2 (Create/View) BLOCKS US3, US4, US5, US6, US7, US8, US9

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests are EXCLUDED per constitution - require user approval first
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All file paths are absolute for clarity
- Constitution compliance: No test tasks without explicit user approval
