# ADR-0002: Cookie-Based Authentication Integration

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-30
- **Feature:** 003-neon-better-auth
- **Context:** The application currently stores JWT tokens in `localStorage`, making them vulnerable to XSS and providing a poor session experience across browser restarts. We need to migrate to a secure, cookie-based authentication system that aligns with "Better Auth" client expectations while keeping the FastAPI backend.

## Decision

We will implement a cookie-based authentication architecture:
- **Client Strategy**: Use `@better-auth/client` patterns via a custom React hook (`useAuth`) on the frontend.
- **Session Transport**: HttpOnly, SameSite=Lax cookies for JWT storage.
- **Cross-Origin Auth**: Enable `credentials: 'include'` on frontend and `allow_credentials=True` in backend CORS for localhost:3000 -> localhost:8000 communication.
- **Backend Compatibility**: FastAPI endpoints to mimic Better Auth response format: `{ user: User, session: { token: string } }`.

## Consequences

### Positive

- **Enhanced Security**: HttpOnly prevents JavaScript access to JWTs, mitigating XSS token theft.
- **Improved UX**: Browser session management provides easier persistence across tab closures and restarts.
- **Better Auth Readiness**: Mimicking the Better Auth client API simplifies a potential future migration to a full Node.js Better Auth server.

### Negative

- **CORS Complexity**: Cross-origin cookies require strict CORS configuration and `credentials: 'include'` on every fetch call.
- **Backend Customization**: Requires manual implementation of cookie setting/clearing and Better Auth response formatting in FastAPI.
- **CSRF Risk**: Cookie-based auth introduces CSRF vulnerability risks (mitigated by `SameSite=Lax` and custom headers requirement).

## Alternatives Considered

- **localStorage JWT**: Easy to implement but less secure and lacks native browser session management features.
- **Full Better Auth (Node.js)**: Offloads auth completely but requires adding and maintaining a second backend service (Node.js/Next.js).
- **Session Tokens (DB-backed)**: More secure but adds database overhead for every request compared to self-contained stateless JWTs.

## References

- Feature Spec: specs/003-neon-better-auth/spec.md
- Implementation Plan: specs/003-neon-better-auth/plan.md
- Research: specs/003-neon-better-auth/research.md
- Related ADRs: ADR-0001 (Cloud Data Architecture)
