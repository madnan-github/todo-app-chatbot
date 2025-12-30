# Data Model: Neon PostgreSQL + Better Auth Integration

**Feature**: 003-neon-better-auth
**Date**: 2025-12-30

## Overview

This migration moves from SQLite to Neon PostgreSQL. The existing data model remains the same; only the database driver and connection configuration change.

## Entities

### User

Authenticated user who owns tasks and tags.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID (string) | PK, NOT NULL | Unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| name | VARCHAR(100) | NULLABLE | Display name |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update time |

**Indexes**:
- `idx_user_email` on `email` (for login lookup)

### Task

User's todo item.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | SERIAL | PK | Auto-incrementing ID |
| user_id | UUID (string) | FK → User.id, NOT NULL | Owner of the task |
| title | VARCHAR(255) | NOT NULL | Task title |
| description | TEXT | NULLABLE | Task description |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| priority | VARCHAR(10) | NOT NULL, DEFAULT 'medium' | high/medium/low |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update time |

**Indexes**:
- `idx_task_user_id` on `user_id` (for user isolation queries)
- `idx_task_completed` on `completed` (for filtering)
- `idx_task_priority` on `priority` (for filtering)

**Constraints**:
- `priority` CHECK IN ('high', 'medium', 'low')

### Tag

User-defined label for categorizing tasks.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | SERIAL | PK | Auto-incrementing ID |
| user_id | UUID (string) | FK → User.id, NOT NULL | Owner of the tag |
| name | VARCHAR(50) | NOT NULL | Tag name (lowercase) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation time |

**Indexes**:
- `idx_tag_user_id` on `user_id` (for user isolation)
- UNIQUE constraint on `(user_id, name)` (prevent duplicate tags per user)

### TaskTag (Junction Table)

Many-to-many relationship between tasks and tags.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| task_id | INTEGER | FK → Task.id, NOT NULL | Related task |
| tag_id | INTEGER | FK → Tag.id, NOT NULL | Related tag |

**Indexes**:
- PRIMARY KEY on `(task_id, tag_id)`
- `idx_tasktag_tag_id` on `tag_id` (for reverse lookups)

**Cascade Rules**:
- ON DELETE CASCADE for both foreign keys (deleting task/tag removes associations)

## Relationships

```
User (1) ──< Task (*)        One user has many tasks
User (1) ──< Tag (*)         One user has many tags
Task (*) ──< TaskTag >── (*) Tag   Many-to-many via junction
```

## State Transitions

### Task.completed
- `false` → `true` (mark complete)
- `true` → `false` (mark incomplete)

### Task.priority
- Any of `['high', 'medium', 'low']` → Any other value

## Validation Rules

### User
- `email`: Valid email format, max 255 chars
- `password`: Min 8 chars (before hashing)
- `name`: Max 100 chars (optional)

### Task
- `title`: Min 1 char, max 255 chars, required
- `description`: Max 2000 chars (optional)
- `priority`: Must be one of 'high', 'medium', 'low'

### Tag
- `name`: Min 1 char, max 50 chars, lowercase, no spaces

## Migration Notes

### From SQLite to PostgreSQL

**No schema changes required** - the existing SQLModel definitions work with both SQLite and PostgreSQL.

**Changes needed**:
1. Replace `aiosqlite` driver with `asyncpg`
2. Update connection string format
3. Tables will be auto-created on first startup (existing behavior)

### Data Migration

Per spec assumptions, fresh start is acceptable. No data migration script required.

If data migration is needed later:
1. Export SQLite data to JSON
2. Import JSON to PostgreSQL
3. Update sequences for auto-increment columns

## PostgreSQL-Specific Considerations

### UUID vs String for user_id
Current implementation uses string (UUID format). PostgreSQL supports native UUID type but keeping as VARCHAR for compatibility.

### Timestamp Handling
PostgreSQL `TIMESTAMP WITH TIME ZONE` recommended for proper timezone handling. SQLModel's `datetime` maps correctly.

### Connection Pooling
Neon serverless requires:
- `pool_pre_ping=True` - validates connections before use
- `pool_recycle=300` - recycles connections every 5 minutes
- SSL required via connection string

### SSL Requirements
Neon requires SSL: `?ssl=require` in connection string.
