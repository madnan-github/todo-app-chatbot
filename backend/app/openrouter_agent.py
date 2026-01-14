from dotenv import load_dotenv
import os
from typing import Dict, Any
from agents import (
    Agent,
    Runner,
    RunConfig,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    set_tracing_disabled,
    function_tool
)
from .mcp_server import add_task, list_tasks, complete_task, delete_task, update_task

load_dotenv()
set_tracing_disabled(disabled=True)

# Initialize OpenRouter provider
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
provider = AsyncOpenAI(
    api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
)

# Define model (using OpenRouter model)
model = OpenAIChatCompletionsModel(
    model="mistralai/devstral-2512:free",  # or "anthropic/claude-3.5-sonnet"
    openai_client=provider,
)

# Create RunConfig
config = RunConfig(
    model=model,
    model_provider=provider,
)

# Define tool functions with decorators
@function_tool(name_override="add_task")
def add_task_tool(user_id: str, title: str, description: str = None) -> str:
    """Create a new task for a user"""
    result = add_task(user_id, title, description)
    return f"✓ Added task: '{title}' {f'with description: {description}' if description else ''}"

@function_tool(name_override="list_tasks")
def list_tasks_tool(user_id: str, status: str = "all") -> str:
    """Retrieve tasks for a user, optionally filtered by status"""
    tasks = list_tasks(user_id, status)
    if not tasks:
        return "No tasks found."

    task_list = "\n".join([f"{i+1}. {task['title']} - {task['status']}" for i, task in enumerate(tasks)])
    return f"Your tasks:\n{task_list}"

@function_tool(name_override="complete_task")
def complete_task_tool(user_id: str, task_id: int) -> str:
    """Mark a task as completed"""
    result = complete_task(user_id, task_id)
    if result:
        return f"✓ Task {task_id} marked as completed"
    return f"Could not find task {task_id} to complete"

@function_tool(name_override="delete_task")
def delete_task_tool(user_id: str, task_id: int) -> str:
    """Remove a task"""
    result = delete_task(user_id, task_id)
    if result:
        return f"✓ Task {task_id} deleted"
    return f"Could not find task {task_id} to delete"

@function_tool(name_override="update_task")
def update_task_tool(user_id: str, task_id: int, title: str = None, description: str = None) -> str:
    """Modify an existing task"""
    result = update_task(user_id, task_id, title, description)
    if result:
        updates = []
        if title: updates.append(f"title to '{title}'")
        if description: updates.append(f"description to '{description}'")
        return f"✓ Task {task_id} updated: {', '.join(updates)}"
    return f"Could not find task {task_id} to update"

# Create the Agent with tools and instructions
agent = Agent(
    name="Task Assistant",
    instructions="""You are a helpful todo assistant. Users tell you what to do with their tasks.
You have 5 tools:
1. add_task - create new task
2. list_tasks - show tasks (status can be 'all', 'pending', or 'completed')
3. complete_task - mark task as done
4. delete_task - remove task
5. update_task - change task details

When user says 'add buy milk', use add_task.
When they say 'show my tasks', use list_tasks.
When they say 'done with task 1', use complete_task with task_id=1.
When they say 'update task 1 title to new title', use update_task with task_id=1, title='new title'.
When they say 'update task 1 title to new title description to new description', use update_task with task_id=1, title='new title', description='new description'.
When they say 'update "old title" to "new title"', first find the task ID by listing tasks, then use update_task with the found ID.
Always confirm what you did clearly and helpfully.

Important: The user_id parameter is automatically provided from context, so you don't need to ask for it.""",
    tools=[add_task_tool, list_tasks_tool, complete_task_tool, delete_task_tool, update_task_tool]
)

async def process_user_message(user_id: str, conversation_id: int, message: str) -> Dict[str, Any]:
    """
    Process user message using OpenAI Agents SDK with OpenRouter
    """
    try:
        # Run the agent with the user's message
        # Note: We need to inject the user_id into the context for tools to use
        enhanced_message = f"[User ID: {user_id}] {message}"
        
        result = await Runner.run(
            starting_agent=agent,
            input=enhanced_message,
            run_config=config
        )
        
        # Extract tool calls from the result
        tool_calls = []
        if hasattr(result, 'steps') and result.steps:
            for step in result.steps:
                if hasattr(step, 'tool_calls') and step.tool_calls:
                    for tool_call in step.tool_calls:
                        tool_calls.append({
                            "tool_name": tool_call.function_name,
                            "result": tool_call.result if hasattr(tool_call, 'result') else "Executed"
                        })
        
        return {
            "response": str(result.final_output),
            "tool_calls": tool_calls,
            "conversation_id": conversation_id
        }
        
    except Exception as e:
        print(f"Error processing message with OpenRouter agent: {str(e)}")
        return {
            "response": "Sorry, I'm having trouble processing your request right now.",
            "tool_calls": [],
            "conversation_id": conversation_id
        }

# Optional: Synchronous version for compatibility
def process_user_message_sync(user_id: str, conversation_id: int, message: str) -> Dict[str, Any]:
    """
    Synchronous version for compatibility with existing code
    """
    try:
        enhanced_message = f"[User ID: {user_id}] {message}"
        
        result = Runner.run_sync(
            starting_agent=agent,
            input=enhanced_message,
            run_config=config
        )
        
        tool_calls = []
        if hasattr(result, 'steps') and result.steps:
            for step in result.steps:
                if hasattr(step, 'tool_calls') and step.tool_calls:
                    for tool_call in step.tool_calls:
                        tool_calls.append({
                            "tool_name": tool_call.function_name,
                            "result": tool_call.result if hasattr(tool_call, 'result') else "Executed"
                        })
        
        return {
            "response": str(result.final_output),
            "tool_calls": tool_calls,
            "conversation_id": conversation_id
        }
        
    except Exception as e:
        print(f"Error processing message with OpenRouter agent: {str(e)}")
        return {
            "response": "Sorry, I'm having trouble processing your request right now.",
            "tool_calls": [],
            "conversation_id": conversation_id
        }