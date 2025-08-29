# Copyright 2025 Your Name
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

"""Unit tests for the agent system."""

import sys
import os
import pytest

# Add the project root to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from my_agent_system.agents.sub_agents.researcher import ResearcherAgent
from my_agent_system.agents.sub_agents.analyzer import AnalyzerAgent
from my_agent_system.agents.sub_agents.responder import ResponderAgent


def test_researcher_agent_creation():
    """Test that the researcher agent can be created."""
    agent_instance = ResearcherAgent()
    assert agent_instance.name == "Researcher Agent"
    assert "research" in agent_instance.description.lower()
    
    # Test that we can create the ADK agent
    adk_agent = agent_instance.create_agent()
    assert adk_agent is not None
    assert adk_agent.name == "Researcher Agent"


def test_analyzer_agent_creation():
    """Test that the analyzer agent can be created."""
    agent_instance = AnalyzerAgent()
    assert agent_instance.name == "Analyzer Agent"
    assert "analyze" in agent_instance.description.lower()
    
    # Test that we can create the ADK agent
    adk_agent = agent_instance.create_agent()
    assert adk_agent is not None
    assert adk_agent.name == "Analyzer Agent"


def test_responder_agent_creation():
    """Test that the responder agent can be created."""
    agent_instance = ResponderAgent()
    assert agent_instance.name == "Responder Agent"
    assert "response" in agent_instance.description.lower()
    
    # Test that we can create the ADK agent
    adk_agent = agent_instance.create_agent()
    assert adk_agent is not None
    assert adk_agent.name == "Responder Agent"


def test_agent_prompts():
    """Test that agents have proper prompts."""
    researcher = ResearcherAgent()
    analyzer = AnalyzerAgent()
    responder = ResponderAgent()
    
    # Check that each agent has a prompt with their name and description
    assert researcher.name in researcher.get_system_prompt()
    assert researcher.description in researcher.get_system_prompt()
    
    assert analyzer.name in analyzer.get_system_prompt()
    assert analyzer.description in analyzer.get_system_prompt()
    
    assert responder.name in responder.get_system_prompt()
    assert responder.description in responder.get_system_prompt()