# Extending the Modular Agentic System

This document explains how to extend the modular agentic system with new agents and tools.

## Adding a New Sub-Agent

To add a new sub-agent to the system:

1. Create a new Python file in the `agents/sub_agents/` directory
2. Inherit from the `BaseAgent` class
3. Implement the required methods:
   - `__init__`: Initialize your agent with a name and description
   - `get_system_prompt`: Return the system prompt for your agent
   - `create_agent`: Create and return the ADK Agent instance
4. Create an instance of your agent class
5. Register your agent in the main orchestrator (`agent.py`)

Example:

```python
# agents/sub_agents/my_new_agent.py
from google.adk.agents import Agent
from google.adk.tools import google_search
from ..base_agent import BaseAgent

class MyNewAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="My New Agent",
            description="an agent that does something new and exciting"
        )

    def get_system_prompt(self) -> str:
        return f"You are {self.name}, {self.description}."

    def create_agent(self) -> Agent:
        return Agent(
            model="gemini-2.5-flash",
            name=self.name,
            instruction=self.get_system_prompt(),
            tools=[google_search],  # Add any tools your agent needs
        )

my_new_agent = MyNewAgent()
```

Then register it in `agent.py`:

```python
# agent.py
from .sub_agents.my_new_agent import my_new_agent

main_agent = SequentialAgent(
    name="Modular Research Assistant",
    sub_agents=[
        researcher_agent.create_agent(),
        analyzer_agent.create_agent(),
        my_new_agent.create_agent(),  # Add your new agent here
        responder_agent.create_agent(),
    ],
)
```

## Adding a New Tool

To add a new tool to the system:

1. Create a new function in `tools/custom_tools.py` or create a new tool file
2. Implement the tool function with appropriate parameters
3. Make sure to include `tool_context: ToolContext = None` as a parameter
4. Register the tool with an agent by adding it to the agent's `get_tools()` method

Example:

```python
# tools/custom_tools.py
async def my_new_tool(
    param1: str,
    param2: int,
    tool_context: ToolContext = None
) -> str:
    """A new tool that does something useful.
    
    Args:
        param1: A string parameter
        param2: An integer parameter
        tool_context: The tool context
        
    Returns:
        A string result
    """
    # Implementation here
    return f"Processed {param1} with value {param2}"

# In your agent class
from ..tools.custom_tools import my_new_tool

class MyAgentWithTool(BaseAgent):
    # ... other methods ...
    
    def get_tools(self):
        return [
            FunctionTool(func=my_new_tool)
        ]
```

## Modifying the Agent Workflow

To modify the agent workflow:

1. Edit the `agent.py` file
2. Change the order of sub-agents in the `SequentialAgent`
3. Or replace `SequentialAgent` with a different agent type (e.g., `Agent` for a single agent)

Example - Parallel processing:

```python
# agent.py
from google.adk.agents import ParallelAgent

main_agent = ParallelAgent(
    name="Parallel Research Assistant",
    sub_agents=[
        researcher_agent.create_agent(),
        analyzer_agent.create_agent(),
    ],
)
```

## Customizing Agent Prompts

To customize agent prompts:

1. Modify the `get_system_prompt()` method in the agent class
2. Or create a new prompt file in the agent's directory

Example:

```python
# agents/sub_agents/researcher.py
class ResearcherAgent(BaseAgent):
    # ... other methods ...
    
    def get_system_prompt(self) -> str:
        return """You are a research specialist with expertise in finding accurate information.
        
        When researching topics:
        1. Always verify information from multiple sources
        2. Prioritize peer-reviewed sources when available
        3. Clearly cite your sources
        4. Highlight any conflicting information you find
        
        Your goal is to provide comprehensive, accurate research results."""
```

## Adding New Evaluation Metrics

To add new evaluation metrics:

1. Create a new evaluation function in `eval/`
2. Use the existing evaluation scripts as templates
3. Add your new metrics to the evaluation pipeline

This modular design allows you to easily extend the system with new capabilities while maintaining a clean, organized codebase.