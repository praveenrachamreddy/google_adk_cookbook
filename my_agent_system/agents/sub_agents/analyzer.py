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

"""Analyzer Agent - Specialized for information analysis and insight generation.

This module implements the AnalyzerAgent, which is specialized in analyzing
information and drawing meaningful insights from data. It's the second agent
in the research workflow sequence, processing the output from the ResearcherAgent.
"""

import sys
import os

# Add the parent directory to the path so we can import base_agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import Agent

# Import the base agent
from agents.base_agent import BaseAgent


class AnalyzerAgent(BaseAgent):
    """Agent specialized in analyzing information and drawing insights.
    
    This agent is the second in the research workflow sequence. It takes the
    research findings from the ResearcherAgent and performs deeper analysis,
    identifying patterns, evaluating significance, and drawing logical conclusions.
    """

    def __init__(self):
        """Initialize the analyzer agent with a specific name and description."""
        super().__init__(
            name="AnalyzerAgent",
            description="an agent specialized in analyzing information and drawing insights from data"
        )

    def get_system_prompt(self) -> str:
        """Get the system prompt for the analyzer agent.
        
        This prompt guides the agent to perform deep analysis of information,
        identify patterns and trends, evaluate significance, and draw evidence-based
        conclusions from the research findings.
        
        Returns:
            The system prompt as a string
        """
        return f"""You are {self.name}, {self.description}.

Your task is to analyze information and draw meaningful insights.
When given information to analyze:
1. Identify key patterns, trends, or anomalies
2. Compare and contrast different pieces of information
3. Evaluate the significance and implications of findings
4. Draw logical conclusions based on evidence
5. Highlight any limitations or uncertainties in the analysis

Focus on providing clear, evidence-based analysis that helps users understand the information better."""

    def create_agent(self) -> Agent:
        """Create and return the analyzer agent.
        
        This method configures and returns an ADK Agent instance specifically
        for analysis tasks. Unlike the ResearcherAgent, this agent doesn't
        require external tools as it works with the provided information.
        
        Returns:
            An ADK Agent instance configured for analysis tasks
        """
        return Agent(
            model="gemini-2.5-flash",
            name=self.name,
            instruction=self.get_system_prompt(),
        )


# Create an instance of the analyzer agent for use in the workflow
analyzer_agent = AnalyzerAgent()