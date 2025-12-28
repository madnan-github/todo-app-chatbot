# Skills & Agents Mapping to Project Phases

This document maps the available skills and agents to the hackathon project phases.

## Phase I: Console App (Completed)

### Agent
- `python-console-agent` - Main agent for CLI development

### Skills
1. `python_project_structure` - UV project setup
2. `cli_interface_design` - Rich CLI interface
3. `command_pattern_implementation` - Command pattern
4. `data_validation` - Pydantic models
5. `in_memory_storage` - Dict-based storage

### Universal Skills Used
- `constitution_creation` - Project principles
- `spec_writing` - Feature specifications
- `spec_kit_structure` - Spec organization
- `claude_md_generation` - Documentation

---

## Phase II: Full-Stack Web Application (Current)

### Agents
- `nextjs-frontend-agent` - Frontend development
- `fastapi-backend-agent` - Backend API development
- `authentication-agent` - Auth implementation

### Frontend Skills (6)
1. `nextjs_app_router_setup` - **Initial Setup**
   - Next.js 16+ with App Router
   - TypeScript strict mode
   - Tailwind CSS configuration
   - Directory structure (app/, components/, lib/)

2. `server_component_patterns` - **Data Fetching**
   - Async/await in Server Components
   - Passing data to Client Components
   - Error boundaries and loading states
   - Suspense and streaming

3. `client_component_patterns` - **Interactivity**
   - 'use client' directive
   - useState, useEffect hooks
   - Event handlers and forms
   - Custom hooks (useAuth, useLocalStorage)

4. `tailwind_styling` - **UI/Styling**
   - Responsive design (sm:, md:, lg:)
   - Consistent spacing (p-4, gap-4, space-y-4)
   - Component patterns (buttons, forms, cards)
   - Mobile-first approach

5. `api_client_creation` - **API Integration**
   - Centralized API client class
   - Automatic JWT token injection
   - Generic request method with types
   - Error handling and retry logic

6. `better_auth_setup` - **Authentication**
   - Better Auth configuration
   - Email/password authentication
   - JWT plugin setup
   - Session management
   - Sign-up/Sign-in pages

### Backend Skills (7)
7. `fastapi_project_setup` - **Initial Setup**
   - FastAPI app structure
   - Routes organization
   - CORS configuration
   - Async endpoints
   - Environment variables

8. `sqlmodel_schema_design` - **Database Models**
   - SQLModel classes with table=True
   - Foreign key relationships
   - Indexes on queried fields
   - created_at/updated_at timestamps
   - Many-to-many junction tables

9. `pydantic_schema_creation` - **API Schemas**
   - Separate Create, Update, Response schemas
   - Field validation (min/max, patterns)
   - Optional fields for updates
   - Type hints throughout

10. `database_connection_setup` - **Database**
    - Neon PostgreSQL connection
    - SQLModel create_engine
    - AsyncSession dependency injection
    - Connection pooling
    - Session lifecycle management

11. `restful_api_design` - **API Endpoints**
    - GET, POST, PUT, PATCH, DELETE methods
    - Proper HTTP status codes (200, 201, 204, 404, 403)
    - Resource-based URLs
    - Query parameters for filtering/sorting
    - Pagination support

12. `jwt_verification` - **Token Verification**
    - Extract Bearer token from header
    - Verify signature with shared secret
    - Decode payload to get user_id
    - HTTPException for invalid tokens
    - Middleware implementation

13. `protected_route_implementation` - **Authorization**
    - get_current_user dependency
    - Verify user_id in URL matches token
    - Filter all queries by user_id
    - Return 403 for unauthorized access
    - User isolation enforcement

### Universal Skills
- `constitution_creation` - Project principles
- `spec_writing` - Feature specifications
- `spec_kit_structure` - Spec organization

---

## Phase II Requirements Coverage

### ✅ Basic Level Features (All Covered)
| Feature | Skills Used |
|---------|-------------|
| Add Task | `restful_api_design` + `protected_route_implementation` |
| Delete Task | `restful_api_design` + `protected_route_implementation` |
| Update Task | `restful_api_design` + `protected_route_implementation` |
| View Task List | `server_component_patterns` + `api_client_creation` |
| Mark as Complete | `restful_api_design` + `client_component_patterns` |

### ✅ Intermediate Level Features (All Covered)
| Feature | Skills Used |
|---------|-------------|
| Priorities & Tags | `sqlmodel_schema_design` (many-to-many) + `pydantic_schema_creation` |
| Search & Filter | `restful_api_design` (query params) + `server_component_patterns` |
| Sort Tasks | `restful_api_design` (query params) + `tailwind_styling` (UI) |

### ✅ Authentication (Covered)
| Requirement | Skills Used |
|-------------|-------------|
| User Signup/Signin | `better_auth_setup` (Better Auth) |
| JWT Token Generation | `better_auth_setup` (JWT plugin) |
| Token Verification | `jwt_verification` (FastAPI middleware) |
| User Isolation | `protected_route_implementation` (query filtering) |

### ✅ Technology Stack (Complete)
| Layer | Technology | Setup Skill |
|-------|------------|-------------|
| Frontend | Next.js 16+ | `nextjs_app_router_setup` |
| Backend | FastAPI | `fastapi_project_setup` |
| ORM | SQLModel | `sqlmodel_schema_design` |
| Database | Neon PostgreSQL | `database_connection_setup` |
| Auth | Better Auth | `better_auth_setup` |
| Styling | Tailwind CSS | `tailwind_styling` |

---

## Skill Dependencies

### Frontend Stack
```
nextjs_app_router_setup (base)
  ├─→ server_component_patterns (data fetching)
  ├─→ client_component_patterns (interactivity)
  ├─→ tailwind_styling (styling)
  ├─→ api_client_creation (API calls)
  └─→ better_auth_setup (authentication)
```

### Backend Stack
```
fastapi_project_setup (base)
  ├─→ database_connection_setup (database)
  ├─→ sqlmodel_schema_design (models)
  ├─→ pydantic_schema_creation (schemas)
  ├─→ restful_api_design (endpoints)
  ├─→ jwt_verification (auth middleware)
  └─→ protected_route_implementation (authorization)
```

### Authentication Flow
```
better_auth_setup (frontend)
  ├─→ Generates JWT tokens
  └─→ Stores in session

api_client_creation (frontend)
  └─→ Attaches JWT to API requests

jwt_verification (backend)
  ├─→ Verifies token signature
  └─→ Extracts user_id

protected_route_implementation (backend)
  └─→ Enforces user isolation
```

---

## Implementation Order Recommendation

### Phase II Implementation Steps

1. **Backend Foundation** (Days 1-2)
   - `fastapi_project_setup`
   - `database_connection_setup`
   - `sqlmodel_schema_design` (User, Task, Tag models)

2. **Frontend Foundation** (Days 1-2, parallel)
   - `nextjs_app_router_setup`
   - `tailwind_styling` (base components)

3. **Authentication** (Days 3-4)
   - `better_auth_setup` (frontend)
   - `jwt_verification` (backend)
   - `protected_route_implementation` (backend)

4. **Core Features** (Days 5-7)
   - `pydantic_schema_creation` (API schemas)
   - `restful_api_design` (CRUD endpoints)
   - `api_client_creation` (frontend API client)
   - `server_component_patterns` (pages)
   - `client_component_patterns` (interactive components)

5. **Polish** (Days 8-9)
   - Complete UI with `tailwind_styling`
   - Error handling and edge cases
   - Testing and debugging

6. **Documentation** (Day 10)
   - README updates
   - Deployment instructions
   - Demo video

---

## Context7 MCP Server Libraries

The following libraries are configured in Context7 for documentation lookup:

### Frontend
- next (Next.js)
- react (React)
- better-auth (Better Auth)
- tailwindcss (Tailwind CSS)
- typescript (TypeScript)
- clsx / tailwind-merge (CSS utilities)

### Backend
- fastapi (FastAPI)
- sqlmodel (SQLModel ORM)
- uvicorn (ASGI server)
- python-jose (JWT)
- passlib (Password hashing)
- pydantic (Validation)
- asyncpg (PostgreSQL driver)

---

## Summary

**Total Skills**: 22 (5 Phase I + 13 Phase II + 4 Universal)
**Total Agents**: 5 (1 Phase I + 3 Phase II + 1 Universal)

**Phase I Status**: ✅ Complete (100%)
**Phase II Status**: 🔄 Skills Created, Ready for Implementation

All skills required for Phase II are now available and documented. The skills cover:
- Complete frontend stack (Next.js + React + Tailwind + Better Auth)
- Complete backend stack (FastAPI + SQLModel + PostgreSQL + JWT)
- All basic and intermediate features
- Full authentication and authorization
- RESTful API design and implementation
