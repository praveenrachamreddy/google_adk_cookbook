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

This module defines a root agent that acts as an orchestrator, using a hybrid
model of delegation: using simple agents as tools, and transferring to complex
sub-agents for sequential workflows.
"""

import sys
import os
import yaml

# Add the project root and subdirectories to the path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'agents'))
sys.path.insert(0, os.path.join(project_root, 'agents', 'sub_agents'))

from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import agent_tool
from google.adk.code_executors import BuiltInCodeExecutor

# =============================================================================
# LOAD CONFIGURATION
# =============================================================================

with open(os.path.join(project_root, '..', 'config.yaml'), 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
model_name = config['agent_settings']['model']


# =============================================================================
# 1. DEFINE SPECIALIZED AGENTS (THE "EXPERTS")
# =============================================================================

# Import the simple, single-purpose agents
from agents.sub_agents.search_agent import search_agent

# An agent that can only execute code.
coding_agent = Agent(
    name="CodingAgent",
    model=model_name,
    description="A coding specialist. Use this for math, logic, or coding tasks.",
    code_executor=BuiltInCodeExecutor(),
)

# The sequential agent for complex research tasks.
from agents.sub_agents.researcher import researcher_agent
from agents.sub_agents.analyzer import analyzer_agent
from agents.sub_agents.responder import responder_agent

main_research_agent = SequentialAgent(
    name="ModularResearchAssistant",
    description=(
        "A modular agentic system that researches topics, analyzes information, "
        "and generates well-structured responses. Use this for complex, multi-step research tasks."
    ),
    sub_agents=[
        researcher_agent.create_agent(),
        analyzer_agent.create_agent(),
        responder_agent.create_agent(),
    ],
)

# =============================================================================
# 2. DEFINE THE ORCHESTRATOR (ROOT AGENT)
# =============================================================================

# This root agent uses the hybrid model of orchestration.
root_agent = Agent(
    name="OrchestratorAgent",
    model=model_name,
    instruction="""You are a master orchestrator. Your job is to delegate tasks.

You have two ways of delegating:
1. Use a Tool: For simple, single-purpose tasks like searching or coding, call the appropriate tool (SearchAgent, CodingAgent).
2. Transfer to a Sub-Agent: For complex, multi-step tasks like research, transfer control to the appropriate sub-agent (ModularResearchAssistant).""",
    tools=[
        agent_tool.AgentTool(agent=search_agent.create_agent()),
        agent_tool.AgentTool(agent=coding_agent),
    ],
    sub_agents=[
        main_research_agent,
    ]
)

# To test a specific agent directly, you can uncomment one of the following lines:
# root_agent = search_agent.create_agent()
# root_agent = coding_agent
# root_agent = main_research_agent
