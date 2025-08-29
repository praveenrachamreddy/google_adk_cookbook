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

"""Researcher Agent - Manages research and information gathering.

This module implements the ResearcherAgent. It acts as a manager, using
specialized sub-agents as tools for searching and saving notes.
"""

import sys
import os

# Add the parent directory to the path so we can import base_agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import Agent
from google.adk.tools import agent_tool

# Import the base agent and the specialist agents to be used as tools
from agents.base_agent import BaseAgent
from agents.sub_agents.search_agent import search_agent
from agents.sub_agents.memory_agent import memory_agent


class ResearcherAgent(BaseAgent):
    """Agent that manages the research process by delegating to specialist tools."""

    def __init__(self):
        """Initialize the researcher agent."""
        super().__init__(
            name="ResearcherAgent",
            description="an agent that researches topics by using other agents for search and memory."
        )

    def get_system_prompt(self) -> str:
        """Get the system prompt for the researcher agent."""
        return f"""You are {self.name}, {self.description}.

Your task is to research topics thoroughly. You have two specialist agents available as tools:
- **SearchAgent**: Use this agent to perform web searches and find information.
- **MemoryAgent**: Use this agent to save important facts and findings to your session notes.

When given a research topic:
1. Break down the topic into key questions.
2. Use the SearchAgent tool to find answers to those questions.
3. Use the MemoryAgent tool to save key findings.
4. Synthesize the gathered information into a cohesive report."""

    def create_agent(self) -> Agent:
        """Create and return the researcher agent with its specialist agent tools."""
        return Agent(
            model=self.config['agent_settings']['model'],
            name=self.name,
            instruction=self.get_system_prompt(),
            tools=[
                agent_tool.AgentTool(agent=search_agent.create_agent()),
                agent_tool.AgentTool(agent=memory_agent.create_agent()),
            ],
        )


# Create an instance of the researcher agent for use in the workflow
researcher_agent = ResearcherAgent()