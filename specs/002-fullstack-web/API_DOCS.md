# TaskFlow API Documentation

## Base URL

```
Production: https://your-backend-api.onrender.com
Development: http://localhost:8000
```

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

---

## Endpoints

### Authentication

#### POST /api/v1/auth/signup
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 604800
}
```

**Errors:**
- `400 Bad Request` - Invalid input data
- `409 Conflict` - Email already registered

---

#### POST /api/v1/auth/signin
Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 604800
}
```

**Errors:**
- `400 Bad Request` - Invalid credentials
- `401 Unauthorized` - Wrong email or password

---

### Tasks

#### GET /api/v1/tasks
List all tasks for the authenticated user with filtering, search, and sorting.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `completed` | boolean | null | Filter by completion status |
| `priority` | string | null | Filter by priority (high, medium, low) - comma-separated for multiple |
| `tag_ids` | string | null | Filter by tag IDs - comma-separated |
| `search` | string | null | Search in title and description |
| `sort_by` | string | "created_at" | Sort field: created_at, updated_at, title, priority |
| `sort_order` | string | "desc" | Sort order: asc, desc |
| `page` | number | 1 | Page number |
| `per_page` | number | 20 | Items per page (max 100) |

**Example Request:**
```
GET /api/v1/tasks?completed=false&priority=high,medium&search=meeting&sort_by=created_at&sort_order=desc&page=1&per_page=20
```

**Response (200 OK):**
```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": "uuid-string",
      "title": "Quarterly review meeting",
      "description": "Prepare Q4 presentation",
      "completed": false,
      "priority": "high",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "tags": [
        {
          "id": 1,
          "user_id": "uuid-string",
          "name": "work"
        }
      ]
    }
  ],
  "total": 45,
  "page": 1,
  "per_page": 20
}
```

**Response Headers:**
- `X-RateLimit-Limit` - Maximum requests per window
- `X-RateLimit-Remaining` - Remaining requests in current window

---

#### POST /api/v1/tasks
Create a new task.

**Request Body:**
```json
{
  "title": "New task title",
  "description": "Optional description",
  "priority": "medium",
  "tag_ids": [1, 2, 3]
}
```

**Response (201 Created):**
```json
{
  "id": 46,
  "user_id": "uuid-string",
  "title": "New task title",
  "description": "Optional description",
  "completed": false,
  "priority": "medium",
  "created_at": "2024-01-15T12:00:00Z",
  "updated_at": "2024-01-15T12:00:00Z",
  "tags": []
}
```

**Errors:**
- `400 Bad Request` - Invalid input (title empty, title too long, etc.)
- `401 Unauthorized` - Missing or invalid token

---

#### GET /api/v1/tasks/{task_id}
Get a specific task by ID.

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "uuid-string",
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "priority": "high",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "tags": [
    {"id": 1, "user_id": "uuid-string", "name": "work"}
  ]
}
```

**Errors:**
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - User doesn't own this task
- `404 Not Found` - Task doesn't exist

---

#### PUT /api/v1/tasks/{task_id}
Update an existing task. All fields are optional.

**Request Body:**
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true,
  "priority": "low",
  "tag_ids": [2, 4]
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "uuid-string",
  "title": "Updated title",
  "description": "Updated description",
  "completed": true,
  "priority": "low",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T14:00:00Z",
  "tags": [
    {"id": 2, "user_id": "uuid-string", "name": "personal"}
  ]
}
```

---

#### DELETE /api/v1/tasks/{task_id}
Delete a task permanently.

**Response (204 No Content):** Empty body

**Errors:**
- `404 Not Found` - Task doesn't exist

---

#### PATCH /api/v1/tasks/{task_id}/complete
Toggle task completion status.

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "uuid-string",
  "title": "Task title",
  "description": "Task description",
  "completed": true,  // Toggled from false to true
  "priority": "high",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T15:00:00Z",
  "tags": []
}
```

---

### Tags

#### GET /api/v1/tags
List all tags for the authenticated user.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `search` | string | null | Filter tags by name prefix |
| `page` | number | 1 | Page number |
| `per_page` | number | 50 | Items per page (max 100) |

**Response (200 OK):**
```json
{
  "tags": [
    {"id": 1, "user_id": "uuid-string", "name": "work"},
    {"id": 2, "user_id": "uuid-string", "name": "personal"},
    {"id": 3, "user_id": "uuid-string", "name": "urgent"}
  ],
  "total": 3,
  "page": 1,
  "per_page": 50
}
```

---

#### POST /api/v1/tags
Create a new tag.

**Request Body:**
```json
{
  "name": "new-tag"
}
```

**Response (201 Created):**
```json
{
  "id": 4,
  "user_id": "uuid-string",
  "name": "new-tag"
}
```

**Errors:**
- `400 Bad Request` - Tag name too long or empty
- `409 Conflict` - Tag with this name already exists

---

#### GET /api/v1/tags/autocomplete
Get tag suggestions for autocomplete.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | required | Search query (min 1 char) |
| `limit` | number | 10 | Maximum suggestions (max 20) |

**Example Request:**
```
GET /api/v1/tags/autocomplete?q=wo&limit=5
```

**Response (200 OK):**
```json
{
  "suggestions": ["work", "workflow", "workshop"]
}
```

---

#### DELETE /api/v1/tags/{tag_id}
Delete a tag. This removes the tag from all tasks.

**Response (204 No Content):** Empty body

---

## Error Response Format

All errors follow this format:

```json
{
  "detail": "Human-readable error message",
  "error_code": "OPTIONAL_ERROR_CODE"
}
```

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created (new resource) |
| 204 | No Content (deleted) |
| 400 | Bad Request (invalid input) |
| 401 | Unauthorized (invalid/missing token) |
| 403 | Forbidden (not authorized) |
| 404 | Not Found (resource doesn't exist) |
| 409 | Conflict (duplicate resource) |
| 429 | Too Many Requests (rate limit) |
| 500 | Internal Server Error |

---

## Rate Limiting

The API limits requests to 100 per minute per IP address.

When rate limited, you receive:
- **Status:** `429 Too Many Requests`
- **Headers:** `Retry-After` (seconds until reset)
- **Body:**
```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Please wait 30 seconds.",
  "retry_after": 30
}
```

---

## Security

### Input Validation
- All inputs are validated using Pydantic models
- Title: 1-200 characters
- Description: 0-1000 characters
- Tag name: 1-50 characters
- Email: Valid email format required
- Password: 8-128 characters

### XSS Prevention
- All user inputs are escaped in responses
- HTML special characters are encoded

### SQL Injection Prevention
- All queries use SQLModel's parameterized queries
- No raw SQL execution

---

## Versioning

Current API version: `v1`

The API is prefixed with `/api/v1/` to allow for future versioning.

---

## Quick Start Example

```bash
# 1. Sign up
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","name":"Test"}'

# 2. Save the access_token from response

# 3. Create a task
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"title":"My first task","priority":"high"}'

# 4. List tasks with filters
curl "http://localhost:8000/api/v1/tasks?completed=false&sort_by=created_at&sort_order=desc" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
