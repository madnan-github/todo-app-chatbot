# Research: Todo AI Chatbot

## Overview
Research for implementing the Todo AI Chatbot feature that allows users to manage their todo tasks using natural language commands.

## Technology Decisions

### 1. MCP (Model Context Protocol) Server Implementation
**Decision**: Use the official MCP SDK to implement the tool server that exposes the 5 required functions (add_task, list_tasks, complete_task, delete_task, update_task).

**Rationale**: MCP is specifically designed for exposing tools to AI models in a standardized way. It provides a clean separation between the AI service and the backend operations, allowing Claude to call specific functions based on user input.

**Alternatives considered**:
- Direct API calls from AI: Would tightly couple the AI to our backend API
- Polling mechanism: Less efficient than direct function calls
- Webhook-based system: More complex than necessary for this use case

### 2. OpenRouter API Integration
**Decision**: Use OpenRouter API with Claude as the AI backend for interpreting natural language commands.

**Rationale**: OpenRouter provides access to Claude and other models with a generous free tier. It's more cost-effective than OpenAI API while providing similar capabilities. The API is compatible with OpenAI's format, making it easy to switch if needed.

**Alternatives considered**:
- OpenAI API: More expensive, especially for hackathon use
- Self-hosted models: Require more computational resources
- Other AI providers: Limited free tier options

### 3. Database Design for Conversations
**Decision**: Implement three tables (Task, Conversation, Message) as specified in the feature requirements to maintain conversation history and user isolation.

**Rationale**: This design allows for proper conversation context management while maintaining clear separation between different data concerns. Each conversation can have multiple messages, and all are tied to a specific user.

**Alternatives considered**:
- Storing conversations in memory: Not persistent across server restarts
- Single combined table: Would make querying more complex
- Document database: Overkill for this relational data structure

### 4. Authentication Method
**Decision**: Use Better Auth as specified in the constitution for user authentication and isolation.

**Rationale**: Better Auth is already part of our technology stack (Phase II) and provides JWT-based authentication which fits well with our stateless server design. It provides user isolation as required by the spec.

**Alternatives considered**:
- Custom authentication: Would require more development time
- Third-party OAuth: More complex setup than needed for this project

### 5. Frontend Chat Interface
**Decision**: Use OpenAI ChatKit as the frontend component for the chat interface.

**Rationale**: ChatKit provides a ready-made, well-designed chat interface that handles the UI/UX aspects of chatting with an AI. It's designed specifically for this use case and integrates well with AI backend services.

**Alternatives considered**:
- Custom chat UI: Would require significant frontend development
- Other chat libraries: ChatKit is specifically designed for AI interactions
- Traditional form-based interface: Doesn't match the natural language requirement

## Key Findings

### AI Function Calling Patterns
- Claude via OpenRouter supports function calling with JSON schemas
- MCP tools can be defined with specific input/output schemas
- Error handling in function calls needs to be robust to maintain conversation flow

### Conversation Memory Management
- Need to limit conversation history sent to AI to avoid token limits
- Should include recent context but not entire conversation history
- Database queries should be optimized to fetch only necessary history

### Natural Language Processing
- Claude is well-suited for understanding simple task management commands
- Need clear examples in system prompt to guide interpretation
- Should handle variations in user phrasing for the same action

## Risks and Mitigations

### 1. API Rate Limits
**Risk**: OpenRouter API may have rate limits that affect user experience
**Mitigation**: Implement proper error handling and retry logic; consider request queuing

### 2. Token Limitations
**Risk**: Long conversations may exceed token limits
**Mitigation**: Implement conversation summarization or history truncation

### 3. AI Misinterpretation
**Risk**: AI may misinterpret user commands
**Mitigation**: Clear system prompt with examples; validation of AI's planned actions before execution; user confirmation for destructive actions

### 4. Database Performance
**Risk**: Large conversation histories may slow down queries
**Mitigation**: Proper indexing on user_id, conversation_id; pagination for history retrieval