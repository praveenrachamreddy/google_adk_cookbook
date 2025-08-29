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

"""Researcher Agent - Specialized for information gathering and web search.

This module implements the ResearcherAgent, which is specialized in researching
topics and gathering information from reliable sources using web search tools.
It's the first agent in the research workflow sequence.
"""

import sys
import os

# Add the parent directory to the path so we can import base_agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import Agent
from google.adk.tools import google_search

# Import the base agent
from agents.base_agent import BaseAgent


class ResearcherAgent(BaseAgent):
    """Agent specialized in researching topics and gathering information.
    
    This agent is the first in the research workflow sequence. It uses the
    Google Search tool to find relevant information about research topics,
    evaluates source credibility, and summarizes findings.
    """

    def __init__(self):
        """Initialize the researcher agent with a specific name and description."""
        super().__init__(
            name="ResearcherAgent",
            description="an agent specialized in researching topics and gathering information from reliable sources"
        )

    def get_system_prompt(self) -> str:
        """Get the system prompt for the researcher agent.
        
        This prompt guides the agent to thoroughly research topics, use search
        tools effectively, evaluate source credibility, and provide concise
        summaries with proper citations.
        
        Returns:
            The system prompt as a string
        """
        return f"""You are {self.name}, {self.description}.

Your task is to research topics thoroughly and gather accurate information.
When given a research topic:
1. Break down the topic into key questions that need to be answered
2. Use the search tool to find relevant information
3. Evaluate the credibility of sources
4. Summarize findings clearly and concisely
5. Cite your sources when possible

Focus on providing factual, well-researched information that directly addresses the research topic."""

    def create_agent(self) -> Agent:
        """Create and return the researcher agent with Google Search tool.
        
        This method configures and returns an ADK Agent instance specifically
        for research tasks, with the Google Search tool enabled.
        
        Returns:
            An ADK Agent instance configured for research tasks
        """
        return Agent(
            model="gemini-2.5-flash",
            name=self.name,
            instruction=self.get_system_prompt(),
            tools=[google_search],
        )


# Create an instance of the researcher agent for use in the workflow
researcher_agent = ResearcherAgent()