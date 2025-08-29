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
from typing import List, Type
from pydantic import BaseModel

# Add the parent directory to the path so we can import base_agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import Agent

# Import the base agent
from agents.base_agent import BaseAgent


class FinalResponse(BaseModel):
    """Defines the structured output for the final response."""
    summary: str
    sources: List[str]


class ResponderAgent(BaseAgent):
    """Agent specialized in generating clear, well-structured responses."""

    def __init__(self):
        """Initialize the responder agent with a specific name and description."""
        super().__init__(
            name="ResponderAgent",
            description="an agent specialized in generating clear, well-structured responses based on analyzed information"
        )

    def get_output_schema(self) -> Type[BaseModel] | None:
        """Return the Pydantic schema for the final response."""
        return FinalResponse

    def get_system_prompt(self) -> str:
        """Get the system prompt for the responder agent."""
        return f"""You are {self.name}, {self.description}.

Your task is to generate a final, well-structured response based on the information provided to you.

You MUST format your response as a JSON object that conforms to the following structure:
{{
  "summary": "<A comprehensive summary of the findings>",
  "sources": [
    "<source_url_1>",
    "<source_url_2>"
  ]
}}

Organize the information logically and coherently within the summary. Ensure the sources list contains the URLs of the information you used."""

    def create_agent(self) -> Agent:
        """Create and return the responder agent."""
        return Agent(
            model=self.config['agent_settings']['model'],
            name=self.name,
            instruction=self.get_system_prompt(),
        )


# Create an instance of the responder agent for use in the workflow
responder_agent = ResponderAgent()