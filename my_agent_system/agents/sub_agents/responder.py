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

"""Responder Agent - Specialized for generating well-structured final responses.

This module implements the ResponderAgent, which is specialized in generating
clear, well-structured responses based on analyzed information. It's the final
agent in the research workflow sequence, producing the response that is returned to the user.
"""

import sys
import os

# Add the parent directory to the path so we can import base_agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import Agent

# Import the base agent
from agents.base_agent import BaseAgent


class ResponderAgent(BaseAgent):
    """Agent specialized in generating clear, well-structured responses.
    
    This agent is the final in the research workflow sequence. It takes the
    analysis from the AnalyzerAgent and generates a clear, well-structured,
    properly formatted response that directly addresses the original query.
    """

    def __init__(self):
        """Initialize the responder agent with a specific name and description."""
        super().__init__(
            name="ResponderAgent",
            description="an agent specialized in generating clear, well-structured responses based on analyzed information"
        )

    def get_system_prompt(self) -> str:
        """Get the system prompt for the responder agent.
        
        This prompt guides the agent to organize information logically,
        use clear language, ensure accuracy, and structure responses with
        appropriate formatting to effectively communicate the information.
        
        Returns:
            The system prompt as a string
        """
        return f"""You are {self.name}, {self.description}.

Your task is to generate clear, well-structured responses based on information provided to you.
When crafting responses:
1. Organize information logically and coherently
2. Use clear, concise language appropriate for the audience
3. Ensure accuracy by only including verified information
4. Structure responses with appropriate headings and formatting
5. Address the original query directly and completely

Focus on providing helpful, well-organized responses that effectively communicate the information."""

    def create_agent(self) -> Agent:
        """Create and return the responder agent.
        
        This method configures and returns an ADK Agent instance specifically
        for response generation. This agent works with the analyzed information
        to create the final user-facing response.
        
        Returns:
            An ADK Agent instance configured for response generation
        """
        return Agent(
            model="gemini-2.5-flash",
            name=self.name,
            instruction=self.get_system_prompt(),
        )


# Create an instance of the responder agent for use in the workflow
responder_agent = ResponderAgent()