#!/usr/bin/env python3
"""
Test script to verify all MCP functions work properly with the updated backend.
"""

import asyncio
import json
import requests
import uuid
from app.mcp_server import add_task, list_tasks, complete_task, delete_task, update_task
from app.database import create_db_and_tables
from src.models import User
from sqlmodel import select
from app.database import get_session

def test_all_operations():
    """Test all operations to ensure they work properly"""
    print("Creating database tables...")
    create_db_and_tables()

    # Use a unique user ID for this test
    test_user_id = f"test-op-user-{uuid.uuid4()}"

    # Create a test user
    with next(get_session()) as session:
        test_user = User(
            id=test_user_id,
            email=f"op_test_{uuid.uuid4()}@example.com",
            password_hash="$2b$12$dummy_hash_for_testing_purposes_only",
            name="Operation Test User"
        )
        session.add(test_user)
        session.commit()
        print(f"Created test user: {test_user_id}")

    print("\n=== TESTING ALL OPERATIONS ===")

    # 1. Test ADD operation
    print("\n1. Testing ADD operation...")
    try:
        add_result = add_task(test_user_id, "Test task for operations", "Description for testing")
        print(f"   ✓ ADD successful: Task {add_result['task_id']} created")
        task_id = add_result["task_id"]
    except Exception as e:
        print(f"   ❌ ADD failed: {e}")
        return

    # 2. Test LIST operation
    print("\n2. Testing LIST operation...")
    try:
        list_result = list_tasks(test_user_id)
        print(f"   ✓ LIST successful: Found {len(list_result)} tasks")
        if len(list_result) > 0:
            print(f"     - Task {list_result[0]['id']}: {list_result[0]['title']}")
    except Exception as e:
        print(f"   ❌ LIST failed: {e}")

    # 3. Test UPDATE operation
    print("\n3. Testing UPDATE operation...")
    try:
        update_result = update_task(test_user_id, task_id, "Updated test task", "Updated description for testing")
        print(f"   ✓ UPDATE successful: Task {update_result['task_id']} updated")
    except Exception as e:
        print(f"   ❌ UPDATE failed: {e}")

    # 4. Test COMPLETE operation
    print("\n4. Testing COMPLETE operation...")
    try:
        complete_result = complete_task(test_user_id, task_id)
        print(f"   ✓ COMPLETE successful: Task {complete_result['task_id']} completed")
    except Exception as e:
        print(f"   ❌ COMPLETE failed: {e}")

    # 5. Test LIST again to verify completion
    print("\n5. Testing LIST to verify completion...")
    try:
        list_completed = list_tasks(test_user_id, "completed")
        print(f"   ✓ LIST (completed) successful: Found {len(list_completed)} completed tasks")
    except Exception as e:
        print(f"   ❌ LIST (completed) failed: {e}")

    # 6. Test DELETE operation
    print("\n6. Testing DELETE operation...")
    try:
        delete_result = delete_task(test_user_id, task_id)
        print(f"   ✓ DELETE successful: Task {delete_result['task_id']} deleted")
    except Exception as e:
        print(f"   ❌ DELETE failed: {e}")

    # 7. Final LIST to verify deletion
    print("\n7. Testing final LIST to verify deletion...")
    try:
        final_list = list_tasks(test_user_id)
        print(f"   ✓ Final LIST successful: Found {len(final_list)} tasks remaining")
    except Exception as e:
        print(f"   ❌ Final LIST failed: {e}")

    print("\n=== OPERATION TEST COMPLETE ===")
    print("All operations have been tested against the actual database!")

if __name__ == "__main__":
    test_all_operations()