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

"""Search Agent - Specialized for using the Google Search tool."""

import sys
import os

# Add the parent directory to the path so we can import base_agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import Agent
from google.adk.tools import google_search

# Import the base agent
from agents.base_agent import BaseAgent


class SearchAgent(BaseAgent):
    """Agent specialized in using the Google Search tool."""

    def __init__(self):
        """Initialize the search agent."""
        super().__init__(
            name="SearchAgent",
            description="A search specialist. Use this for simple questions that require web search."
        )

    def get_tools(self):
        """Return the tools for this agent."""
        # This agent only uses the built-in google_search tool.
        # It does not inherit base tools to avoid the "one built-in tool" limitation.
        return [google_search]

    def create_agent(self) -> Agent:
        """Create and return the search agent."""
        return Agent(
            model=self.config['agent_settings']['model'],
            name=self.name,
            instruction=self.get_system_prompt(),
            tools=self.get_tools(),
        )


# Create an instance of the search agent
search_agent = SearchAgent()
