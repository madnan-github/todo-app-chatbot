# ADR-0001: Cloud Data Architecture

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-30
- **Feature:** 003-neon-better-auth
- **Context:** The application currently uses local SQLite which lacks cloud persistence and production readiness. To meet Phase II requirements and prepare for cloud deployment, we need a robust, async-capable cloud database architecture.

## Decision

We will adopt a cloud-native data architecture using:
- **Database**: Neon Serverless PostgreSQL (Scale-to-zero capability)
- **ORM/Schema**: SQLModel (SQLAlchemy + Pydantic)
- **Driver**: asyncpg (High-performance async driver)
- **Connection Logic**: SQLAlchemy `AsyncSession` with `pool_pre_ping=True` and `sslmode=require`

## Consequences

### Positive

- **Persistence**: Data survives server restarts and deployments.
- **Performance**: asyncpg provides non-blocking I/O, critical for FastAPI's scaling.
- **Reliability**: `pool_pre_ping` handles Neon's compute suspension (scale-to-zero) gracefully by validating connections before use.
- **Security**: Mandatory SSL ensures data-in-transit encryption to the cloud.

### Negative

- **Latency**: Network latency to Neon is higher than local SQLite disk access (mitigated by async I/O).
- **Complexity**: Managing async engines and sessions is more complex than synchronous SQLite.
- **Dependency**: Dependency on Neon's availability and free tier limits.

## Alternatives Considered

- **SQLite (aiosqlite)**: Simple and fast but unsuitable for multi-device persistence or production cloud deployments.
- **Raw asyncpg**: Maximum performance but loses the developer productivity of SQLModel/SQLAlchemy ORM.
- **Cloud SQL / RDS**: Viable but lacks the "scale-to-zero" free tier efficiency of Neon.

## References

- Feature Spec: specs/003-neon-better-auth/spec.md
- Implementation Plan: specs/003-neon-better-auth/plan.md
- Research: specs/003-neon-better-auth/research.md
- Related ADRs: None
