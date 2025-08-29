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

"""Memory Agent - Specialized for saving notes to session state."""

import sys
import os

# Add the parent directory to the path so we can import base_agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

# Import the base agent and session tools
from agents.base_agent import BaseAgent
from tools.session_tools import save_note


class MemoryAgent(BaseAgent):
    """Agent specialized in saving notes to the session state."""

    def __init__(self):
        """Initialize the memory agent."""
        super().__init__(
            name="MemoryAgent",
            description="an agent that can save notes to the session memory."
        )

    def get_tools(self):
        """Return the tools for this agent."""
        base_tools = super().get_tools()
        my_tools = [FunctionTool(func=save_note)]
        return base_tools + my_tools

    def create_agent(self) -> Agent:
        """Create and return the memory agent."""
        return Agent(
            model=self.config['agent_settings']['model'],
            name=self.name,
            instruction=self.get_system_prompt(),
            tools=self.get_tools(),
        )


# Create an instance of the memory agent
memory_agent = MemoryAgent()
