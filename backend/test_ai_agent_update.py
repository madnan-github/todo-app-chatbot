#!/usr/bin/env python3
"""
Test to verify that the AI agent properly calls update_task and returns it in tool_calls.
"""

import asyncio
import uuid
from app.openrouter_agent import process_user_message_sync
from app.mcp_server import add_task
from app.database import create_db_and_tables
from src.models import User
from sqlmodel import select
from app.database import get_session

def test_ai_agent_update():
    """Test if AI agent properly calls update function"""
    print("Creating database tables...")
    create_db_and_tables()

    # Use a unique user ID for this test
    test_user_id = f"ai-update-test-{uuid.uuid4()}"

    # Create a test user
    with next(get_session()) as session:
        test_user = User(
            id=test_user_id,
            email=f"ai_update_test_{uuid.uuid4()}@example.com",
            password_hash="$2b$12$dummy_hash_for_testing_purposes_only",
            name="AI Update Test User"
        )
        session.add(test_user)
        session.commit()
        print(f"Created test user: {test_user_id}")

    print("\n=== TESTING AI AGENT UPDATE CALL ===")

    # Add a test task manually
    print("\n1. Adding a test task...")
    try:
        add_result = add_task(test_user_id, "Test task to update", "Original description")
        task_id = add_result["task_id"]
        print(f"   ✓ Task {task_id} created: 'Test task to update'")
    except Exception as e:
        print(f"   ❌ ADD failed: {e}")
        return

    # Simulate AI update command
    print(f"\n2. Simulating AI update command...")
    print(f"   Command: 'update task {task_id} title to buy Laptop System'")

    try:
        result = process_user_message_sync(
            user_id=test_user_id,
            conversation_id=1,
            message=f"update task {task_id} title to buy Laptop System"
        )

        print(f"   ✓ AI Response: {result['response']}")
        print(f"   ✓ Tool calls: {result['tool_calls']}")

        # Check if update_task was called
        update_called = any(call.get('tool_name') == 'update_task' for call in result['tool_calls'])
        if update_called:
            print(f"   ✓ update_task was called in AI agent")
        else:
            print(f"   ❌ update_task was NOT called in AI agent")

    except Exception as e:
        print(f"   ❌ AI processing failed: {e}")

    print("\n=== TEST COMPLETE ===")

if __name__ == "__main__":
    test_ai_agent_update()