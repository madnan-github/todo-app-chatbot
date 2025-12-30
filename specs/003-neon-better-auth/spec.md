# Feature Specification: Phase II Compliance - Neon PostgreSQL + Better Auth Integration

**Feature Branch**: `003-neon-better-auth`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "Replace SQLite with Neon PostgreSQL and custom JWT auth with Better Auth client library"

## Overview

The Phase II todo application is functionally complete with all 195 tasks marked done. However, two architectural deviations from the original Phase II requirements exist:

1. **Database**: Currently using SQLite locally instead of Neon PostgreSQL
2. **Authentication**: Using custom JWT implementation with localStorage instead of Better Auth client library with cookie-based sessions

This specification defines the migration path to bring the application into full Phase II compliance.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Database Migration to Cloud (Priority: P1)

As a user, I want my tasks stored in a cloud database so that my data persists across devices and deployments, and I don't lose data when the local server restarts.

**Why this priority**: Data persistence is foundational. Without a production-ready database, the application cannot be deployed or used reliably. This blocks all other work.

**Independent Test**: Can be fully tested by creating a task, stopping/restarting the server, and verifying the task still exists. Delivers persistent, production-ready data storage.

**Acceptance Scenarios**:

1. **Given** a user creates a new task, **When** the server restarts, **Then** the task is still visible and intact
2. **Given** a user with existing tasks in SQLite, **When** the migration runs, **Then** all existing tasks appear in the new database
3. **Given** the application is configured with database credentials, **When** the backend starts, **Then** it connects to the cloud database without errors
4. **Given** network latency to the cloud database, **When** performing CRUD operations, **Then** operations complete within acceptable time limits

---

### User Story 2 - Cookie-Based Authentication (Priority: P2)

As a user, I want my login session to persist across browser tabs and sessions so that I don't have to re-authenticate frequently, and my session is more secure than localStorage-based tokens.

**Why this priority**: Authentication is critical for user isolation and security. Cookie-based auth is more secure against XSS attacks than localStorage and provides better session management.

**Independent Test**: Can be fully tested by logging in, closing the browser, reopening it, and verifying the user is still authenticated. Delivers secure, persistent authentication.

**Acceptance Scenarios**:

1. **Given** a user signs in successfully, **When** they close and reopen the browser within 7 days, **Then** they remain authenticated
2. **Given** a user is authenticated, **When** they open the app in a new tab, **Then** they are already logged in (session shared)
3. **Given** a user signs out, **When** they check cookies, **Then** the session cookie is removed
4. **Given** cross-origin requests between frontend (port 3000) and backend (port 8000), **When** making API calls, **Then** cookies are properly sent and received

---

### User Story 3 - Seamless Feature Continuity (Priority: P3)

As a user, I want all existing features (task CRUD, tags, search, filter, sort, completion toggle) to continue working exactly as before after the infrastructure changes.

**Why this priority**: Users should not experience any functional regression. The migration must be transparent to end users.

**Independent Test**: Can be fully tested by exercising all CRUD operations, tag management, search, filter, and sort after migration. Delivers confidence that no features broke.

**Acceptance Scenarios**:

1. **Given** the migration is complete, **When** a user creates/reads/updates/deletes a task, **Then** the operation succeeds as before
2. **Given** a task with tags, **When** the user filters by tag, **Then** correct results are shown
3. **Given** multiple tasks, **When** the user searches by keyword, **Then** matching tasks are returned
4. **Given** a task list, **When** the user sorts by priority or date, **Then** tasks are ordered correctly

---

### Edge Cases

- What happens when database connection fails during startup?
  - Application should fail fast with clear error message indicating connection issue
- What happens when database connection drops mid-operation?
  - Operation should fail gracefully with user-friendly error, retry mechanism optional
- What happens when session cookie expires?
  - User should be redirected to login page on next API call
- What happens if frontend and backend have clock skew affecting token validation?
  - Should have reasonable tolerance (e.g., 30 seconds) for clock differences
- What happens when user clears cookies manually?
  - User should be treated as logged out on next request

## Requirements *(mandatory)*

### Functional Requirements

**Database Migration**:
- **FR-001**: System MUST connect to Neon PostgreSQL using asyncpg driver for all database operations
- **FR-002**: System MUST use connection pooling appropriate for serverless deployments
- **FR-003**: System MUST use SSL/TLS for all database connections (sslmode=require)
- **FR-004**: System MUST remove all SQLite-specific code and dependencies
- **FR-005**: System MUST support the existing data model (User, Task, Tag, TaskTag) in PostgreSQL

**Authentication Migration**:
- **FR-006**: Frontend MUST use Better Auth client library for authentication flows
- **FR-007**: System MUST use HTTP-only cookies for session management (not localStorage)
- **FR-008**: System MUST set cookies with SameSite=Lax for development environment
- **FR-009**: System MUST support cross-origin cookie sharing between ports 3000 and 8000
- **FR-010**: Sessions MUST persist for 7 days unless explicitly logged out
- **FR-011**: Backend MUST expose endpoints compatible with Better Auth client expectations
- **FR-012**: System MUST remove localStorage-based token storage from frontend

**Feature Continuity**:
- **FR-013**: System MUST maintain all existing task CRUD operations
- **FR-014**: System MUST maintain all existing tag CRUD and association operations
- **FR-015**: System MUST maintain search, filter, and sort capabilities
- **FR-016**: System MUST maintain user isolation (users see only their own tasks)

### Key Entities

- **User**: Authenticated user with email, password hash, and unique ID. Owner of tasks and tags.
- **Task**: User's todo item with title, description, priority, completion status, and timestamps.
- **Tag**: User-defined label for categorizing tasks. Unique name per user.
- **TaskTag**: Many-to-many relationship between tasks and tags.
- **Session**: Authentication session with token, user reference, expiration, and creation timestamp.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Application successfully connects to cloud database on every startup
- **SC-002**: All existing features work without modification to user-facing behavior
- **SC-003**: User sessions persist for 7 days across browser restarts
- **SC-004**: Authentication cookies are properly set with secure attributes (HttpOnly, SameSite)
- **SC-005**: No localStorage usage for authentication tokens in the final implementation
- **SC-006**: Database operations complete within 2 seconds under normal conditions
- **SC-007**: Zero data loss during migration from SQLite to PostgreSQL (if existing data exists)

## Constraints

- Must work within Neon PostgreSQL free tier limits (0.5GB storage, 190 compute hours/month)
- Backend must remain FastAPI + SQLModel (not migrating to Node.js)
- Frontend must remain Next.js 15+ with App Router
- Must work in local development environment (ports 3000 and 8000)
- Must use free-tier services only

## Out of Scope

- OAuth/social login (Google, GitHub, etc.)
- Email verification flow
- Password reset functionality
- Two-factor authentication (2FA/MFA)
- Database migrations tool (Alembic) - using direct table creation
- Production deployment configuration
- Rate limiting and abuse prevention

## Assumptions

- Neon PostgreSQL account is already created and connection string is available
- Better Auth client library (@better-auth/client) is already installed in frontend
- Existing SQLite data migration is optional (fresh start acceptable)
- Local development will use the same Neon database as production (free tier simplicity)
- CORS configuration for cookies will work with explicit origin configuration
