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

import logging
import os
import yaml
from abc import ABC, abstractmethod
from typing import List, Optional, Any, Type
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from pydantic import BaseModel

# Import session tools
from tools.session_tools import save_note


class BaseAgent(ABC):
    """Abstract base class for all agents in the system.
    
    This class defines the common interface that all agents must implement.
    It provides a consistent structure for creating specialized agents with
    their own unique capabilities while maintaining a uniform API.
    """
    _config = None

    def __init__(self, name: str, description: str):
        """Initialize the base agent with a name and description.
        
        Args:
            name: The name of the agent (must be a valid Python identifier)
            description: A description of the agent's purpose and capabilities
        """
        self.name = name
        self.description = description
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = self._load_config()
        self.logger.info("Agent '%s' initialized with config: %s", self.name, self.config)

    @classmethod
    def _load_config(cls) -> dict:
        """Load the system configuration from config.yaml."""
        if cls._config is None:
            try:
                # Assuming config.yaml is in the root of the 'google_adk_cookbook' project
                current_dir = os.path.dirname(os.path.abspath(__file__))
                config_path = os.path.join(current_dir, '..', '..', 'config.yaml')
                with open(config_path, 'r', encoding='utf-8') as f:
                    cls._config = yaml.safe_load(f)
            except FileNotFoundError:
                # Fallback or error handling if config.yaml is not found
                cls._config = {'agent_settings': {'model': 'gemini-1.5-flash'}}
        return cls._config

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

    def get_input_schema(self) -> Type[BaseModel] | None:
        """Define the Pydantic model for this agent's input. Optional."""
        return None

    def get_output_schema(self) -> Type[BaseModel] | None:
        """Define the Pydantic model for this agent's output. Optional."""
        return None

    def get_tools(self) -> List:
        """Get the tools available to this agent.
        
        This method can be overridden by subclasses to provide
        agent-specific tools. By default, it returns the base tools.
        
        Returns:
            A list of base Tool instances.
        """
        self.logger.info("Getting base tools...")
        base_tools = [FunctionTool(func=save_note)]
        return base_tools

    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent.
        
        This method constructs a system prompt based on the agent's
        name and description. It can be overridden by subclasses for
        more complex prompt engineering.
        
        Returns:
            The system prompt as a string
        """
        self.logger.info("Generating system prompt...")
        return f"You are {self.name}, {self.description}"