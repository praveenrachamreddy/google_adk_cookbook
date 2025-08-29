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

"""Simple test script to verify the agent system works."""

import sys
import os

# Add the project root and subdirectories to the path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'my_agent_system'))
sys.path.insert(0, os.path.join(project_root, 'my_agent_system', 'agents'))
sys.path.insert(0, os.path.join(project_root, 'my_agent_system', 'agents', 'sub_agents'))

def test_imports():
    """Test that we can import all our modules."""
    try:
        # Test importing individual agent modules directly
        import researcher
        print("OK: Researcher module imported successfully")
        
        import analyzer
        print("OK: Analyzer module imported successfully")
        
        import responder
        print("OK: Responder module imported successfully")
        
        # Test creating agents
        researcher_agent = researcher.ResearcherAgent()
        adk_researcher = researcher_agent.create_agent()
        print("OK: Researcher agent created successfully")
        
        analyzer_agent = analyzer.AnalyzerAgent()
        adk_analyzer = analyzer_agent.create_agent()
        print("OK: Analyzer agent created successfully")
        
        responder_agent = responder.ResponderAgent()
        adk_responder = responder_agent.create_agent()
        print("OK: Responder agent created successfully")
        
        print("\nAll tests passed! The agent system is working correctly.")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)