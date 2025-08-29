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

"""Tool Demonstration Agent - Shows custom tool implementation and usage.

This module implements the ToolDemonstrationAgent, which demonstrates how to
create and use custom tools within the ADK framework. It showcases two custom
tools: data_formatter and sentiment_analyzer.
"""

import sys
import os

# Add the parent directory to the path so we can import base_agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

# Import the base agent
from agents.base_agent import BaseAgent

# Import custom tools
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools'))
from tools.custom_tools import data_formatter, sentiment_analyzer


class ToolDemonstrationAgent(BaseAgent):
    """Agent that demonstrates using custom tools.
    
    This agent showcases how to integrate custom tools into an ADK agent.
    It has access to two custom tools:
    1. data_formatter - Formats data in JSON, XML, or CSV formats
    2. sentiment_analyzer - Analyzes the sentiment of text input
    """

    def __init__(self):
        """Initialize the tool demonstration agent with a specific name and description."""
        super().__init__(
            name="ToolDemoAgent",
            description="an agent that demonstrates using custom tools for data formatting and sentiment analysis"
        )

    def get_system_prompt(self) -> str:
        """Get the system prompt for the tool demonstration agent.
        
        This prompt guides the agent to identify when to use its custom tools,
        apply them appropriately, and clearly explain the process and results.
        
        Returns:
            The system prompt as a string
        """
        return f"""You are {self.name}, {self.description}.

You have access to two custom tools:
1. data_formatter: Formats data in different formats (JSON, XML, CSV)
2. sentiment_analyzer: Analyzes the sentiment of text

When given a task:
1. Determine which tool(s) to use based on the request
2. Use the tools appropriately to process the data
3. Explain your process and present the results clearly

Always use the tools when relevant to the task."""

    def get_tools(self):
        """Get the custom tools available to this agent.
        
        This method returns the custom tools that this agent can use:
        - data_formatter: For formatting data in various formats
        - sentiment_analyzer: For analyzing text sentiment
        
        Returns:
            A list of FunctionTool instances wrapping the custom tools
        """
        return [
            FunctionTool(func=data_formatter),
            FunctionTool(func=sentiment_analyzer)
        ]

    def create_agent(self) -> Agent:
        """Create and return the tool demonstration agent with custom tools.
        
        This method configures and returns an ADK Agent instance with the
        custom tools registered and ready for use.
        
        Returns:
            An ADK Agent instance configured for demonstrating custom tools
        """
        return Agent(
            model="gemini-2.5-flash",
            name=self.name,
            instruction=self.get_system_prompt(),
            tools=self.get_tools(),
        )


# Create an instance of the tool demonstration agent for testing
tool_demo_agent = ToolDemonstrationAgent()