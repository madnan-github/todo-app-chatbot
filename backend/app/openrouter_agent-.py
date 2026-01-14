import os
import json
import httpx
from typing import Dict, Any, List
from dotenv import load_dotenv
from .mcp_server import add_task, list_tasks, complete_task, delete_task, update_task

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def process_user_message(user_id: str, conversation_id: int, message: str) -> Dict[str, Any]:
    """
    Process user message with OpenRouter API and execute appropriate tool functions
    """
    # Define available tools for the AI
    tools = [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task for a user",
                "parameters": {
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
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "Retrieve tasks for a user, optionally filtered by status",
                "parameters": {
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
            }
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as completed",
                "parameters": {
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
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Remove a task",
                "parameters": {
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
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Modify an existing task",
                "parameters": {
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
            }
        }
    ]

    # Prepare the request to OpenRouter
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # Get conversation history for context (simplified - in practice, you'd fetch from DB)
    # For now, we'll just send the current message

    payload = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful todo assistant. Users tell you what to do with their tasks. You have 5 tools: add_task - create new task, list_tasks - show tasks, complete_task - mark done, delete_task - remove task, update_task - change task. When user says 'add buy milk', use add_task. When they say 'show tasks', use list_tasks. When they say 'done with task 1', use complete_task. Always confirm what you did: '✓ Added 'buy milk' to your tasks'"
            },
            {
                "role": "user",
                "content": message
            }
        ],
        "tools": tools,
        "tool_choice": "auto"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )

            response_data = response.json()

            # Process the response and execute any tool calls
            tool_calls = []
            ai_response = ""

            if 'choices' in response_data and len(response_data['choices']) > 0:
                choice = response_data['choices'][0]

                if 'message' in choice:
                    msg = choice['message']

                    # Check if there are tool calls in the response
                    if 'tool_calls' in msg and msg['tool_calls']:
                        for tool_call in msg['tool_calls']:
                            function_name = tool_call['function']['name']
                            arguments = json.loads(tool_call['function']['arguments'])

                            # Execute the appropriate function based on the tool call
                            result = None
                            if function_name == "add_task":
                                result = add_task(arguments.get('user_id'), arguments.get('title'), arguments.get('description'))
                            elif function_name == "list_tasks":
                                result = list_tasks(arguments.get('user_id'), arguments.get('status', 'all'))
                            elif function_name == "complete_task":
                                result = complete_task(arguments.get('user_id'), arguments.get('task_id'))
                            elif function_name == "delete_task":
                                result = delete_task(arguments.get('user_id'), arguments.get('task_id'))
                            elif function_name == "update_task":
                                result = update_task(
                                    arguments.get('user_id'),
                                    arguments.get('task_id'),
                                    arguments.get('title'),
                                    arguments.get('description')
                                )

                            if result:
                                tool_calls.append({
                                    "tool_name": function_name,
                                    "result": result
                                })

                    # Get the AI's response text
                    ai_response = choice.get('message', {}).get('content', 'I processed your request.')
            else:
                ai_response = "Sorry, I couldn't process your request."

        return {
            "response": ai_response,
            "tool_calls": tool_calls
        }

    except Exception as e:
        print(f"Error calling OpenRouter API: {str(e)}")
        return {
            "response": "Sorry, I'm having trouble connecting to the AI service right now.",
            "tool_calls": []
        }