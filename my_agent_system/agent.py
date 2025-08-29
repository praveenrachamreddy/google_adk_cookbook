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

"""Main Agent Orchestrator - Entry point for the ADK web interface.

This module serves as the entry point for the ADK web interface.
It exports a root_agent that the ADK discovers and loads.

To switch between agents for testing:
1. Uncomment the agent you want to test
2. Comment out the other agent
3. Restart the ADK web interface

Currently configured to test the ToolDemoAgent.
To test the SequentialAgent (main research assistant), 
uncomment the SequentialAgent lines and comment the ToolDemoAgent line.
"""

import sys
import os

# Add the project root and subdirectories to the path
# This ensures we can import modules from subdirectories
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'agents'))
sys.path.insert(0, os.path.join(project_root, 'agents', 'sub_agents'))
sys.path.insert(0, os.path.join(project_root, 'mcp'))

from google.adk.agents import SequentialAgent

# =============================================================================
# IMPORT SUB-AGENTS
# =============================================================================

# Import the research workflow agents
from agents.sub_agents.researcher import researcher_agent
from agents.sub_agents.analyzer import analyzer_agent
from agents.sub_agents.responder import responder_agent

# Import the tool demonstration agent
from agents.sub_agents.tool_demo import tool_demo_agent

# Import the MCP agent
from .mcp.mcp_agents.db_agent import db_mcp_agent

# =============================================================================
# CREATE AGENT INSTANCES
# =============================================================================

# Create the main sequential agent that orchestrates the research workflow
# This agent processes requests through three stages:
# 1. ResearcherAgent - Gathers information using web search
# 2. AnalyzerAgent - Analyzes and structures the information
# 3. ResponderAgent - Generates a well-formatted response
main_research_agent = SequentialAgent(
    name="ModularResearchAssistant",
    description=(
        "A modular agentic system that researches topics, analyzes information, "
        "and generates well-structured responses."
    ),
    sub_agents=[
        researcher_agent.create_agent(),
        analyzer_agent.create_agent(),
        responder_agent.create_agent(),
    ],
)

# Create the tool demonstration agent for testing custom tools
# This agent demonstrates:
# 1. data_formatter tool - Formats data in JSON, XML, CSV
# 2. sentiment_analyzer tool - Analyzes text sentiment
tool_demo_test_agent = tool_demo_agent.create_agent()

# Create the database MCP agent for testing database interactions
db_mcp_test_agent = db_mcp_agent

# =============================================================================
# EXPORT ROOT AGENT FOR ADK WEB INTERFACE
# =============================================================================

# IMPORTANT: Only one agent can be exported as root_agent for the ADK web interface
# Uncomment the agent you want to test and comment the other

# For testing the main research workflow:
# root_agent = main_research_agent

# For testing custom tools (default):
# root_agent = tool_demo_test_agent

# For testing the database MCP agent:
root_agent = db_mcp_test_agent