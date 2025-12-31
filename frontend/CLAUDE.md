# Frontend Claude Code Rules

This file provides frontend-specific guidance for Claude Code when working on the Next.js frontend.

## Technology Stack

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript 5.x
- **Styling**: Tailwind CSS 4.x
- **Authentication**: Better Auth with JWT
- **API Client**: Custom centralized client with automatic JWT injection

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx         # Root layout with providers
│   ├── page.tsx           # Home page
│   ├── (auth)/            # Auth route group
│   │   ├── signin/        # Sign in page
│   │   └── signup/        # Sign up page
│   └── (dashboard)/       # Protected dashboard group
│       ├── layout.tsx     # Dashboard layout with auth check
│       └── tasks/         # Tasks management
├── components/            # React components
│   ├── ui/               # Reusable UI components (Button, Input, etc.)
│   ├── tasks/            # Task-specific components
│   └── auth/             # Auth-related components
├── lib/                   # Utilities and configurations
│   ├── auth.ts           # Better Auth configuration
│   ├── api.ts            # API client with JWT
│   └── utils.ts          # Utility functions (cn, etc.)
├── types/                 # TypeScript type definitions
└── hooks/                 # Custom React hooks
```

## Key Patterns

### Server Components (Default)
- Default to Server Components for data fetching
- Use `async/await` for database/API calls
- Pass data to Client Components as props

### Client Components
- Use `'use client'` directive at top of file
- Use hooks: `useState`, `useEffect`, `useContext`
- Handle user events: `onClick`, `onSubmit`, `onChange`

### API Client
- All API calls go through `/lib/api.ts`
- Automatic JWT token injection from Better Auth
- Proper error handling with user-friendly messages

### Authentication
- Better Auth handles sign up, sign in, session management
- JWT tokens stored in cookies
- Middleware protects routes under `/dashboard`

## Environment Variables

Required in `.env.local`:
- `NEXT_PUBLIC_API_URL` - Backend API URL
- `JWT_SECRET` - For token verification
- `BETTER_AUTH_SECRET` - For auth configuration

## Common Commands

```bash
# Development
npm run dev                # Start dev server on port 3000

# Build & Production
npm run build              # Build for production
npm run start              # Start production server

# Code Quality
npm run lint               # Run ESLint
```

## Available Skills

When working on frontend tasks, check these skills first:
- `nextjs_app_router_setup` - Initial project setup
- `server_component_patterns` - Data fetching in Server Components
- `client_component_patterns` - Interactive Client Components
- `tailwind_styling` - Responsive design
- `api_client_creation` - API communication layer
- `better_auth_setup` - Authentication configuration

## Related Documentation

- **Root CLAUDE.md**: Project-wide rules and agent guidelines
- **Backend CLAUDE.md**: FastAPI backend patterns
- **specs/002-fullstack-web/**: Feature specifications and tasks

---

*Adhere to all guidelines in the root CLAUDE.md for PHR creation and ADR suggestions.*
