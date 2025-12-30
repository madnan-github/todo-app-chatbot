---
id: "0001"
title: "Neon Better Auth Spec Creation"
stage: spec
date: 2025-12-30
surface: agent
model: claude-opus-4-5-20251101
feature: 003-neon-better-auth
branch: 003-neon-better-auth
user: ruser
command: /sp.specify
labels: ["neon", "postgresql", "better-auth", "phase-ii-compliance"]
links:
  spec: specs/003-neon-better-auth/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-neon-better-auth/spec.md
  - specs/003-neon-better-auth/checklists/requirements.md
tests:
  - N/A (specification phase)
---

## Prompt

/sp.specify create a specification for fixing the Neon PostgreSQL and Better Auth implementation:

Create a feature specification for "Phase II Compliance: Neon PostgreSQL + Better Auth Integration"

## Current State
The Phase II todo application is functionally complete but has two deviations from requirements:
1. **Database**: Using SQLite locally instead of Neon PostgreSQL
2. **Authentication**: Using custom JWT implementation instead of Better Auth client library

## Requirements to Implement

### 1. Neon PostgreSQL Integration
- Replace SQLite with Neon Serverless PostgreSQL for ALL environments (dev + prod)
- Use asyncpg driver for async PostgreSQL connections
- Configure connection pooling for serverless usage
- Database URL format: postgresql://user:password@host/database?sslmode=require
- Ensure SQLModel works with async PostgreSQL (not SQLite)
- Free tier limits: 0.5GB storage, 190 compute hours/month

### 2. Better Auth Integration (Frontend)
- Use @better-auth/client library on frontend (already installed)
- Configure Better Auth client to connect to FastAPI backend
- Use cookies for session management (not localStorage)
- Handle cross-origin auth between frontend (port 3000) and backend (port 8000)
- Session persistence: 7 days

### 3. Better Auth Compatible Backend
- Keep existing Better Auth compatible endpoints (/api/v1/sign-in/email, /api/v1/sign-up/email)
- Ensure response format matches Better Auth expectations: { user, session: { token } }
- Set proper CORS headers for cookie-based auth
- Configure SameSite=Lax for development cookies

## Constraints
- Must maintain all existing functionality (CRUD, tags, search, filter, sort)
- Must work in local development environment
- Must use free-tier services only
- Backend remains FastAPI + SQLModel (not Node.js)
- Frontend remains Next.js 15+ with App Router

## Success Criteria
1. Application connects to Neon PostgreSQL database
2. Better Auth client handles signup/signin on frontend
3. Sessions persist across browser close (cookie-based)
4. All existing features continue to work
5. User isolation maintained (each user sees only their tasks)

## Out of Scope
- OAuth/social login
- Email verification
- Password reset
- Two-factor authentication

## Response snapshot

Created comprehensive feature specification for Phase II compliance migration:

**Branch**: `003-neon-better-auth`
**Spec file**: `specs/003-neon-better-auth/spec.md`

**Key deliverables**:
1. Specification with 3 prioritized user stories:
   - P1: Database Migration to Cloud (foundational)
   - P2: Cookie-Based Authentication (security)
   - P3: Seamless Feature Continuity (regression prevention)
2. 16 functional requirements covering database, auth, and feature continuity
3. 7 measurable success criteria
4. Clear constraints, out-of-scope items, and assumptions
5. Quality checklist created and validated (all items pass)

**Checklist validation**: All items passed - no clarifications needed.

## Outcome

- ✅ Impact: Feature specification created for Phase II compliance migration
- 🧪 Tests: N/A (specification phase - no code tests)
- 📁 Files: 2 files created (spec.md, requirements.md checklist)
- 🔁 Next prompts: /sp.plan to create implementation plan, or /sp.clarify if questions arise
- 🧠 Reflection: Specification is complete and unambiguous. User provided clear requirements so no clarification markers needed.

## Evaluation notes (flywheel)

- Failure modes observed: None - user requirements were comprehensive
- Graders run and results (PASS/FAIL): Quality checklist - PASS (all 12 items)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - proceed to /sp.plan
