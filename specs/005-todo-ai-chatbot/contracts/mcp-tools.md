# MCP Tool Contracts: Todo AI Chatbot

## Overview
Contract definitions for the Model Context Protocol (MCP) tools that the AI can call to manage tasks.

## Tool 1: add_task

**Description**: Create a new task for a user

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "The ID of the user creating the task"
    },
    "title": {
      "type": "string",
      "description": "The title of the task"
    },
    "description": {
      "type": "string",
      "description": "Optional description of the task"
    }
  },
  "required": ["user_id", "title"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "The ID of the created task"
    },
    "status": {
      "type": "string",
      "description": "Status of the operation",
      "enum": ["created"]
    },
    "title": {
      "type": "string",
      "description": "The title of the created task"
    }
  },
  "required": ["task_id", "status", "title"]
}
```

## Tool 2: list_tasks

**Description**: Retrieve tasks for a user, optionally filtered by status

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "The ID of the user whose tasks to retrieve"
    },
    "status": {
      "type": "string",
      "description": "Optional filter for task status",
      "enum": ["all", "pending", "completed"],
      "default": "all"
    }
  },
  "required": ["user_id"]
}
```

**Output Schema**:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "id": {
        "type": "integer",
        "description": "The ID of the task"
      },
      "title": {
        "type": "string",
        "description": "The title of the task"
      },
      "completed": {
        "type": "boolean",
        "description": "Whether the task is completed"
      }
    },
    "required": ["id", "title", "completed"]
  }
}
```

## Tool 3: complete_task

**Description**: Mark a task as completed

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "The ID of the user who owns the task"
    },
    "task_id": {
      "type": "integer",
      "description": "The ID of the task to mark as complete"
    }
  },
  "required": ["user_id", "task_id"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "The ID of the task that was completed"
    },
    "status": {
      "type": "string",
      "description": "Status of the operation",
      "enum": ["completed"]
    },
    "title": {
      "type": "string",
      "description": "The title of the completed task"
    }
  },
  "required": ["task_id", "status", "title"]
}
```

## Tool 4: delete_task

**Description**: Remove a task

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "The ID of the user who owns the task"
    },
    "task_id": {
      "type": "integer",
      "description": "The ID of the task to delete"
    }
  },
  "required": ["user_id", "task_id"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "The ID of the task that was deleted"
    },
    "status": {
      "type": "string",
      "description": "Status of the operation",
      "enum": ["deleted"]
    },
    "title": {
      "type": "string",
      "description": "The title of the deleted task"
    }
  },
  "required": ["task_id", "status", "title"]
}
```

## Tool 5: update_task

**Description**: Modify an existing task

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "The ID of the user who owns the task"
    },
    "task_id": {
      "type": "integer",
      "description": "The ID of the task to update"
    },
    "title": {
      "type": "string",
      "description": "Optional new title for the task"
    },
    "description": {
      "type": "string",
      "description": "Optional new description for the task"
    }
  },
  "required": ["user_id", "task_id"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "integer",
      "description": "The ID of the task that was updated"
    },
    "status": {
      "type": "string",
      "description": "Status of the operation",
      "enum": ["updated"]
    },
    "title": {
      "type": "string",
      "description": "The updated title of the task"
    }
  },
  "required": ["task_id", "status", "title"]
}
```