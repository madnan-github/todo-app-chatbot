# Implementation Plan: Todo AI Chatbot

**Branch**: `005-todo-ai-chatbot` | **Date**: 2026-01-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-todo-ai-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of an AI chatbot that allows users to manage their todo tasks using natural language commands. The system will use OpenRouter API (Claude) to interpret user commands and execute appropriate task operations through MCP tools. The backend will be built with FastAPI and use Neon PostgreSQL for persistence of tasks, conversations, and messages. The system will maintain conversation history and provide user isolation through authentication.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.13+ (per constitution)
**Primary Dependencies**: FastAPI, SQLModel, OpenAI Agents SDK, OpenRouter API, Better Auth, Neon PostgreSQL
**Storage**: PostgreSQL (Neon) with 3 tables (Task, Conversation, Message)
**Testing**: pytest with unit, integration, and contract tests
**Target Platform**: Linux server (deployable to Railway/Kubernetes per constitution)
**Project Type**: Web application with AI integration (backend service with MCP tools)
**Performance Goals**: <5s response time for 95% of AI requests (per spec SC-003), 95% accuracy in command interpretation (per spec SC-001)
**Constraints**: Must use free-tier services only (per constitution Principle IV), stateless server design (per constitution Principle VI), user isolation (per spec FR-013)
**Scale/Scope**: Individual user access only (per spec FR-013), conversation-based task management (per spec FR-001-FR-015)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Initial Check (Pre-Research)
1. **Spec-Driven Development (Principle I)**: ✅ PASS - Feature specification exists at `specs/005-todo-ai-chatbot/spec.md`
2. **AI-First Development (Principle II)**: ✅ PASS - Using Claude Code for implementation planning
3. **Test-First (Principle III)**: ✅ PASS - Tests will be written before implementation
4. **Free-Tier First (Principle IV)**: ✅ PASS - Using OpenRouter free tier, Neon PostgreSQL free tier, Railway for deployment
5. **Progressive Architecture (Principle V)**: ✅ PASS - Building on existing Phase I & II infrastructure
6. **Stateless & Cloud-Native Design (Principle VI)**: ✅ PASS - Server will be stateless, storing all data in database
7. **Simplicity & YAGNI (Principle VII)**: ✅ PASS - Implementing only required functionality from spec

### Post-Design Check (Post-Phase 1)
1. **Spec-Driven Development**: ✅ VERIFIED - Design aligns with feature specification requirements
2. **AI-First Development**: ✅ VERIFIED - MCP tools and OpenRouter API properly integrated
3. **Test-First Approach**: ✅ VERIFIED - Contract tests defined for MCP tools
4. **Free-Tier Compliance**: ✅ VERIFIED - All technology choices have free tier options
5. **Progressive Architecture**: ✅ VERIFIED - Extends existing backend infrastructure
6. **Stateless Design**: ✅ VERIFIED - Server statelessness maintained via database persistence
7. **Simplicity**: ✅ VERIFIED - Minimal viable implementation matching spec requirements

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── models.py          # Task, Conversation, Message tables
│   ├── database.py        # Database connection
│   ├── routes.py          # /api/{user_id}/chat endpoint
│   ├── openrouter_agent.py # Call OpenRouter API
│   └── mcp_server.py      # MCP tools (add_task, list_tasks, etc.)
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── .env                   # Environment variables

frontend/
├── src/
│   ├── components/
│   │   └── ChatKitWrapper.tsx
│   └── App.tsx
├── .env.local
└── package.json

.env
README.md
```

**Structure Decision**: Web application with separate frontend and backend components (Option 2). The backend will be built with FastAPI and contain the AI chatbot logic with MCP tools, while the frontend will use OpenAI ChatKit for the user interface.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
