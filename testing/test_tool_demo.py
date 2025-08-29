#!/usr/bin/env python3
# Copyright 2025 Your Name
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

# Script to test the ToolDemoAgent with custom tools.

import sys
import os
import asyncio

# Add the project root to the path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

import dotenv
dotenv.load_dotenv()

from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent


def test_tool_demo_agent():
    # Import the tool demo agent
    from my_agent_system.agents.sub_agents.tool_demo import tool_demo_agent
    
    # Create the ADK agent
    adk_agent = tool_demo_agent.create_agent()
    
    # Create a runner
    runner = InMemoryRunner(agent=adk_agent)
    
    # Test cases for the custom tools
    test_cases = [
        "Format this data as JSON: name: John, age: 30, city: New York",
        "Analyze the sentiment of this text: I love this new technology!",
        "Format this data as XML: product: Laptop, price: 999, brand: TechCorp",
        "Analyze the sentiment of this text: This product is terrible and disappointing."
    ]
    
    print("=== Tool Demo Agent Test ===\n")
    
    # Run tests for each case
    for i, user_input in enumerate(test_cases, 1):
        print(f"Test {i}: {user_input}\n")
        print("Response:")
        print("-" * 40)
        
        # Create a session
        import asyncio
        session = asyncio.run(runner.session_service.create_session(
            app_name=runner.app_name, user_id=f"test_user_{i}"
        ))
        
        # Run the agent
        content = UserContent(parts=[Part(text=user_input)])
        for event in runner.run(
            user_id=session.user_id, session_id=session.id, new_message=content
        ):
            for part in event.content.parts:
                print(part.text)
        
        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    test_tool_demo_agent()