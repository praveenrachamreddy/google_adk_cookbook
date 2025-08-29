#!/usr/bin/env python3
# Copyright 2025 Praveen Rachamreddy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Script to test the MCP agent system locally.

This script demonstrates how to run the MCP agent system programmatically
using the ADK InMemoryRunner. It creates a session and sends a sample
database query to the MCP agent.
"""

import sys
import os
import asyncio
import logging

# Add the project root to the path to enable imports
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# Load environment variables from .env file
import dotenv
dotenv.load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Import ADK components
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

# Import the root agent (configured in my_agent_system.agent)
from my_agent_system.agent import root_agent


def test_mcp_agent():
    """Run the MCP agent system with a sample database query.
    
    This function creates an InMemoryRunner, establishes a session,
    and sends a sample database query to the MCP agent.
    """
    # Create a runner with the configured root agent
    runner = InMemoryRunner(agent=root_agent)
    
    # Create a session (required for agent interactions)
    import asyncio
    session = asyncio.run(runner.session_service.create_session(
        app_name=runner.app_name, user_id="test_user"
    ))
    
    # Define a sample database query
    user_input = "List all users in the database."
    
    # Display the query to the user
    print(f"User: {user_input}\n")
    print("Agent Response:")
    print("=" * 50)
    
    # Run the agent and display responses as they arrive
    content = UserContent(parts=[Part(text=user_input)])
    try:
        for event in runner.run(
            user_id=session.user_id, session_id=session.id, new_message=content
        ):
            for part in event.content.parts:
                print(part.text)
    except Exception as e:
        print(f"Error running agent: {e}")


# Execute the script when run directly
if __name__ == "__main__":
    # Set the event loop policy for Windows
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    test_mcp_agent()