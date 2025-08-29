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

"""Test script for the main agent orchestrator."""

import sys
import os

# Add the project root to the path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'my_agent_system'))

def test_main_agent():
    """Test that we can import and create the main agent."""
    try:
        # Test importing the main agent
        from my_agent_system.agent import root_agent
        print("OK: Main agent imported successfully")
        
        # Check that it's a SequentialAgent
        from google.adk.agents import SequentialAgent
        assert isinstance(root_agent, SequentialAgent)
        print("OK: Main agent is a SequentialAgent")
        
        # Check the name and description
        assert root_agent.name == "ModularResearchAssistant"
        print("OK: Main agent has correct name")
        
        print("\nMain agent test passed!")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_main_agent()
    sys.exit(0 if success else 1)