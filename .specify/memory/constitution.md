# TaskFlow Constitution

## Project Vision

TaskFlow is an AI-powered todo application that evolves from a simple console app to a fully-featured, cloud-native AI chatbot deployed on Kubernetes. This project demonstrates mastery of Spec-Driven Development, AI-native architecture, and modern cloud technologies—all using **free-tier services**.

**Problem Solved:** Managing personal tasks with natural language while learning progressive software architecture.

**Team Context:** Solo developer (hackathon participant)

**Development Philosophy:** Spec-Driven, AI-First, Test-First

---

## Core Principles

### I. Spec-Driven Development (Non-Negotiable)

Every feature MUST begin with a specification before implementation.

**Guidelines:**
- Write `spec.md` before any code using the `/sp.specify` workflow
- Specifications define WHAT, not HOW
- All acceptance criteria must be testable and verifiable
- No manual coding allowed—refine specs until AI generates correct output

**Rationale:** Spec-driven development ensures clear requirements, reproducible AI-generated code, and traceable implementation decisions. This is the foundation of the hackathon methodology.

**Verification:** Check that `specs/<feature>/spec.md` exists before any implementation PR.

---

### II. AI-First Development

Leverage AI assistance (Claude Code) throughout the entire development lifecycle.

**Guidelines:**
- Use Claude Code for spec generation, planning, task breakdown, and implementation
- Maintain clear context through CLAUDE.md files at each project level
- All AI interactions must be recorded in Prompt History Records (PHRs)
- Verify AI outputs against specifications before acceptance
- **Always check available skills/agents before any action** (see CLAUDE.md Pre-Action Checklist)

**Rationale:** AI-first development maximizes productivity and demonstrates the "Architecture of Intelligence" theme. The developer acts as System Architect, not syntax writer.

**Verification:** PHR files exist in `history/prompts/` for all significant work.

---

### III. Test-First (TDD Mandatory)

Tests MUST be written before implementation code.

**Guidelines:**
- Red-Green-Refactor cycle strictly enforced
- Tests must fail before implementation (red phase)
- User approves test cases before implementation begins
- Minimum 80% code coverage for core business logic

**Rationale:** TDD ensures correctness, prevents regressions, and produces self-documenting code. Critical for multi-phase evolution where each phase builds on previous work.

**Verification:** CI pipeline enforces coverage thresholds; PRs require passing tests.

---

### IV. Free-Tier First

All external services MUST use free-tier offerings that do not require payment.

**Guidelines:**
- Prefer services with generous or always-free tiers
- Document all service limits and plan for graceful degradation
- No credit card charges—free credits or truly free tiers only
- Maintain list of alternative free services as fallbacks

**Rationale:** Demonstrates practical skills accessible to all developers. Ensures the project can be reproduced without financial barriers.

**Verification:** No paid service keys in `.env`; all services documented in Technology Stack with free tier limits.

---

### V. Progressive Architecture

The application MUST evolve through 5 defined phases without breaking previous functionality.

**Guidelines:**
- Each phase builds incrementally on the previous
- Backward compatibility maintained throughout evolution
- Clean separation of concerns enables phase transitions
- Monorepo structure keeps frontend/backend in single context

**Rationale:** Simulates real-world software evolution from MVP to production-grade distributed system.

**Verification:** All Phase N features still work after Phase N+1 implementation.

---

### VI. Stateless & Cloud-Native Design

All services MUST be designed for horizontal scalability and resilience.

**Guidelines:**
- Server holds NO state between requests (database is source of truth)
- Use JWT for stateless authentication
- Design for Kubernetes deployment from Phase II onward
- Support graceful degradation when external services are unavailable

**Rationale:** Cloud-native design enables the Kubernetes deployment phases and teaches production-ready architecture patterns.

**Verification:** Server restart doesn't lose any user data; multiple instances can run concurrently.

---

### VII. Simplicity & YAGNI

Implement only what is specified—no premature optimization or feature creep.

**Guidelines:**
- Start simple, add complexity only when required by specs
- No organizational-only abstractions; every abstraction must serve a purpose
- Prefer standard library solutions over external dependencies
- Remove unused code immediately

**Rationale:** Complexity must be justified. The hackathon evaluates spec compliance, not additional features.

**Verification:** Code review checks for unused imports, dead code, and unjustified abstractions.

---

## Technology Stack

### Phase I: Console Application

| Layer | Technology | Justification |
|-------|------------|---------------|
| Language | Python 3.13+ | Modern Python with latest features |
| Package Manager | UV | Fast, modern Python package management |
| Data Storage | In-Memory Dict | Simplest solution for Phase I requirements |
| CLI Framework | Rich | Beautiful terminal output, tables, prompts |
| Validation | Pydantic | Type-safe data validation |

### Phase II: Full-Stack Web Application

| Layer | Technology | Justification | Free Tier |
|-------|------------|---------------|-----------|
| Frontend | Next.js 15+ (App Router) | Modern React with Server Components | Vercel (100GB bandwidth) |
| Backend | FastAPI | High-performance async Python API | Render/Railway free tier |
| ORM | SQLModel | SQLAlchemy + Pydantic integration | N/A |
| Database | Neon PostgreSQL | Serverless Postgres | 0.5GB, 190 compute hrs/mo |
| Authentication | Better Auth | Modern auth with JWT support | Self-hosted |

### Phase III: AI Chatbot

| Layer | Technology | Justification | Free Tier |
|-------|------------|---------------|-----------|
| LLM Provider | Openrouter | Fast inference, completely free tier | Generous rate limits |
| AI Framework | OpenAI Agents SDK | Official SDK for agent development | N/A (uses Groq backend) |
| MCP Server | Official MCP SDK | Model Context Protocol for tools | Open source |
| Chat UI | OpenAI ChatKit | Standard chat interface | Domain allowlist required |
| State Storage | Neon PostgreSQL | Conversation/message persistence | Same as Phase II |

### Phase IV: Local Kubernetes

| Layer | Technology | Justification | Free Tier |
|-------|------------|---------------|-----------|
| Containerization | Docker | Industry standard | Docker Desktop free |
| Local K8s | Minikube | Full K8s locally | Open source |
| Package Manager | Helm Charts | K8s application packaging | Open source |
| AI DevOps | kubectl-ai, kagent | AI-assisted K8s operations | Open source |
| Docker AI | Gordon (if available) | AI-assisted Docker operations | Docker Desktop feature |

### Phase V: Cloud Deployment

| Layer | Technology | Justification | Free Tier |
|-------|------------|---------------|-----------|
| Cloud K8s | Oracle Cloud OKE | Always Free tier (no expiration) | 4 OCPUs, 24GB RAM |
| Event Streaming | Redpanda Cloud | Kafka-compatible, serverless | Free serverless tier |
| Alternative Kafka | Strimzi (self-hosted) | K8s-native Kafka operator | Runs on OKE free tier |
| Runtime | Dapr | Distributed app building blocks | Open source |
| CI/CD | GitHub Actions | Automated deployment pipeline | 2000 mins/mo free |

---

## Development Constraints

### Mandatory Tooling

| Tool | Purpose | Required |
|------|---------|----------|
| Claude Code | All implementation via AI assistant | Yes |
| Spec-Kit Plus | Specification management and workflow | Yes |
| UV | Python package management (not pip) | Yes |
| Git | Version control with meaningful commits | Yes |

### Code Organization

```
taskflow/
├── .specify/                 # Spec-Kit configuration
│   └── memory/constitution.md
├── .claude/                  # Claude Code configuration
│   ├── agents/               # Specialized AI agents
│   └── skills/               # Reusable AI skills
├── specs/                    # Feature specifications
│   ├── features/
│   ├── api/
│   └── database/
├── history/                  # Prompt History Records
│   └── prompts/
├── CLAUDE.md                 # Root AI instructions
├── frontend/                 # Next.js application
│   └── CLAUDE.md
├── backend/                  # FastAPI application
│   └── CLAUDE.md
├── helm/                     # Kubernetes charts
└── dapr/                     # Dapr components
```

### API Design Standards

- RESTful endpoints under `/api/`
- All routes require JWT authentication (Phase II+)
- User isolation: `GET /api/{user_id}/tasks`
- JSON request/response bodies
- Proper HTTP status codes (200, 201, 400, 401, 404, 500)

### Security Requirements

- Never hardcode secrets or tokens
- Use `.env` files for local development
- Kubernetes Secrets or Dapr Secrets for production
- JWT tokens with expiration (7 days default)
- HTTPS only in production

---

## Quality Standards

### Code Quality

- All code must pass linting (ruff for Python, eslint for TypeScript)
- Type hints required for all Python functions
- TypeScript strict mode enabled
- Functions must have single responsibility
- No commented-out code in commits

### Testing Requirements

| Test Type | Requirement | Phase |
|-----------|-------------|-------|
| Unit Tests | 80% coverage minimum for business logic | All |
| Integration Tests | All API endpoints covered | II+ |
| E2E Tests | Critical user journeys | II+ |
| Contract Tests | MCP tool interfaces | III+ |

### Documentation Requirements

- README.md with setup instructions per phase
- CLAUDE.md files at project, frontend, and backend levels
- API documentation via OpenAPI/Swagger
- Spec files for every feature

### Review Process

- All implementations verified against specifications
- PHR created for every significant interaction
- ADR suggested for architectural decisions
- No merging without passing CI checks

---

## Success Criteria

### Phase I: Basic Level (100 points) ✅ COMPLETE

| Feature | Acceptance Criteria | Status |
|---------|---------------------|--------|
| Add Task | User can create task with title and description | [x] |
| Delete Task | User can remove task by ID | [x] |
| Update Task | User can modify existing task details | [x] |
| View Task List | User can see all tasks with status indicators | [x] |
| Mark as Complete | User can toggle task completion status | [x] |

**Completed**: 2025-12-27 | **PR**: [#1](https://github.com/madnan-github/todo-app-cli/pull/1) | **Tests**: 179 passing

### Phase II: Basic Level Web (150 points)

| Feature | Acceptance Criteria | Status |
|---------|---------------------|--------|
| Web CRUD | All Phase I features work via web UI | [ ] |
| Authentication | User can signup/signin with Better Auth | [ ] |
| REST API | All endpoints return proper JSON responses | [ ] |
| Responsive UI | Works on mobile and desktop | [ ] |
| Database | Tasks persist across server restarts | [ ] |

### Phase III: AI Chatbot (200 points)

| Feature | Acceptance Criteria | Status |
|---------|---------------------|--------|
| Natural Language | User can add/view/update/delete tasks via chat | [ ] |
| MCP Tools | 5 tools exposed (add, list, complete, delete, update) | [ ] |
| Conversation State | Chat history persists in database | [ ] |
| Stateless Server | Server restart doesn't break conversations | [ ] |

### Phase IV: Local K8s (250 points)

| Feature | Acceptance Criteria | Status |
|---------|---------------------|--------|
| Containerization | Frontend and backend have working Dockerfiles | [ ] |
| Helm Charts | Deployable via `helm install` | [ ] |
| Minikube | Full app runs on local Minikube | [ ] |
| AI DevOps | kubectl-ai used for at least one operation | [ ] |

### Phase V: Cloud + Advanced (300 points)

| Feature | Acceptance Criteria | Status |
|---------|---------------------|--------|
| Oracle OKE | App deployed and accessible on cloud | [ ] |
| Event Streaming | Kafka/Redpanda handles task events | [ ] |
| Dapr | Pub/Sub and State management working | [ ] |
| Intermediate Features | Priorities, tags, search, filter, sort | [ ] |
| Advanced Features | Recurring tasks, due dates, reminders | [ ] |
| CI/CD | GitHub Actions deploys on push to main | [ ] |

---

## Governance

- This Constitution supersedes all other project documentation
- Amendments require: documented rationale in ADR, version bump, migration plan
- All implementations must verify compliance with Core Principles
- Exceptions require explicit documentation and approval
- Use CLAUDE.md for runtime development guidance

### Document Hierarchy

```
Constitution (WHY) > Specify (WHAT) > Plan (HOW) > Tasks (DO)
```

If conflicts arise, higher-level documents take precedence.

### Version Control

- MAJOR: Breaking changes to principles or architecture
- MINOR: New principles, sections, or significant expansions
- PATCH: Clarifications, typos, non-semantic changes

### Compliance Verification

Every PR/implementation must answer:

1. Does this follow Spec-Driven Development? (Principle I)
2. Was this generated via AI assistance? (Principle II)
3. Were tests written first? (Principle III)
4. Does this use free-tier services only? (Principle IV)
5. Does this maintain backward compatibility? (Principle V)
6. Is the server stateless? (Principle VI)
7. Is this the simplest solution? (Principle VII)

---

**Version**: 1.2.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2025-12-27

### Changelog

- **1.2.0** (2025-12-27): Phase I Complete - All 5 features implemented with 179 tests passing, PR #1 merged
- **1.1.0** (2025-12-27): Added Success Criteria section, Verification methods for each principle, Document Hierarchy, enhanced formatting per constitution_creation skill guidelines
- **1.0.0** (2025-12-27): Initial constitution created with 7 core principles, technology stack, quality standards, and governance
