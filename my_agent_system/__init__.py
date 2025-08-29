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

"""My Agent System - A modular agentic system.

This package provides a modular, extensible agentic system built with the Google
Agent Development Kit (ADK). It includes:

- A main orchestrator agent that coordinates sub-agents
- Specialized sub-agents for research, analysis, and response generation
- Custom tools for data formatting and sentiment analysis
- A base agent class for creating new agents
- Shared utilities for common functionality
- MCP agents for interacting with external systems

The system is designed to be easily extensible by adding new sub-agents and tools.
"""

from . import agent
from . import agents
from . import tools
from . import shared
from . import mcp

# Export the main agent
root_agent = agent.root_agent

__all__ = [
    "agent",
    "agents",
    "tools",
    "shared",
    "mcp",
    "root_agent",
]