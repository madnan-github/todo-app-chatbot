# Implementation Plan: Phase II Compliance - Neon PostgreSQL + Better Auth Integration

**Branch**: `003-neon-better-auth` | **Date**: 2025-12-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-neon-better-auth/spec.md`

## Summary

Migrate the existing Todo application from SQLite to Neon Serverless PostgreSQL and from localStorage-based custom JWT to cookie-based Better Auth compatible authentication. This ensures high availability, production readiness, and enhanced security while maintaining all Phase II functional features.

## Technical Context

**Language/Version**: Python 3.13+ (Backend), TypeScript 5.x / Next.js 15+ (Frontend)
**Primary Dependencies**: FastAPI, SQLModel, asyncpg, @better-auth/client
**Storage**: Neon Serverless PostgreSQL (asyncpg driver)
**Testing**: pytest (Backend), Vitest/Playwright (Frontend)
**Target Platform**: Linux/Vercel/Neon
**Project Type**: Full-stack Web (Monorepo)
**Performance Goals**: Database operations < 2s; Auth verification < 200ms
**Constraints**: Neon Free Tier limits; HttpOnly cookies for auth; Cross-origin credentials
**Scale/Scope**: Single user sessions; hundreds of tasks; production-ready infra

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Principle I: Spec-Driven**: `spec.md` created and validated.
- [x] **Principle IV: Free-Tier First**: Neon Free Tier used; no paid services.
- [x] **Principle VI: Stateless**: Removing local SQLite; database is the only source of truth.
- [x] **Principle VII: Simplicity**: Mimicking Better Auth via FastAPI to avoid adding a Node.js auth server.

## Project Structure

### Documentation (this feature)

```text
specs/003-neon-better-auth/
├── spec.md              # Feature requirements
├── plan.md              # This file
├── research.md          # Database and Auth research
├── data-model.md        # PostgreSQL schema details
├── quickstart.md        # Setup and migration guide
├── contracts/
│   └── auth-api.yaml    # OpenAPI spec for auth endpoints
└── tasks.md             # Implementation tasks (generated later)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── auth.py          # Modified: Cookie extraction
│   ├── database.py      # Modified: Async engine for Postgres
│   ├── main.py          # Modified: CORS and cookie middleware
│   └── routes/
│       └── auth.py      # New: Better Auth compatible routes
└── tests/               # New: Integration tests for Postgres/Cookies

frontend/
├── lib/
│   └── api.ts           # Modified: Use credentials: include
└── hooks/
    └── useAuth.tsx      # Modified: Remove localStorage, use cookies
```

**Structure Decision**: Web application monorepo structure maintained. Backend logic updated for async PostgreSQL; Frontend hooks updated for cookie sessions.

## Complexity Tracking

*No violations detected. Implementation follows standard async and cookie-based patterns.*

## Implementation Strategy

### Phase 1: Infrastructure & Data
- Update `backend/src/database.py` to use `create_async_engine` with `asyncpg`.
- Configure connection pooling and `pool_pre_ping` for Neon.
- Update `backend/src/models.py` for PostgreSQL compatibility (if needed).
- Verify connection to Neon via health check.

### Phase 2: Authentication Backend
- Implement `/api/v1/auth/signin` and `/signup` returning `{ user, session }`.
- Use `response.set_cookie()` for HttpOnly `session_token`.
- Implement `/api/v1/auth/session` to verify cookie and return current session.
- Update `backend/src/auth.py` to check cookies before headers.

### Phase 3: Frontend Integration
- Update `frontend/lib/api.ts` to include `credentials: 'include'` in all fetch calls.
- Update `useAuth` hook to rely on browser cookie management.
- Remove all `localStorage.setItem('auth_token', ...)` calls.
- Verify session persistence across tab close/reopen.

### Phase 4: Verification & Cleanup
- Run full regression suite for Task CRUD.
- Verify User Isolation in PostgreSQL.
- Delete `backend/todo_app.db` and remove `aiosqlite` from dependencies.
