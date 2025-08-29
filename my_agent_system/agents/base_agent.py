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

"""Base Agent Class - Foundation for all specialized agents.

This module provides the abstract base class that all specialized agents
inherit from. It defines the common interface and structure that ensures
consistency across all agents in the system.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any
from google.adk.agents import Agent
# We'll import Tool when we need it, or use FunctionTool instead


class BaseAgent(ABC):
    """Abstract base class for all agents in the system.
    
    This class defines the common interface that all agents must implement.
    It provides a consistent structure for creating specialized agents with
    their own unique capabilities while maintaining a uniform API.
    """

    def __init__(self, name: str, description: str):
        """Initialize the base agent with a name and description.
        
        Args:
            name: The name of the agent (must be a valid Python identifier)
            description: A description of the agent's purpose and capabilities
        """
        self.name = name
        self.description = description

    @abstractmethod
    def create_agent(self) -> Agent:
        """Create and return the ADK Agent instance.
        
        This abstract method must be implemented by all subclasses.
        It should configure and return a fully functional ADK Agent
        with the appropriate model, instructions, and tools.
        
        Returns:
            An ADK Agent instance configured for this agent's purpose
        """
        pass

    def get_tools(self) -> List:
        """Get the tools available to this agent.
        
        This method can be overridden by subclasses to provide
        agent-specific tools. By default, it returns an empty list.
        
        Returns:
            A list of Tool instances (empty by default)
        """
        return []

    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent.
        
        This method constructs a system prompt based on the agent's
        name and description. It can be overridden by subclasses for
        more complex prompt engineering.
        
        Returns:
            The system prompt as a string
        """
        return f"You are {self.name}, {self.description}"