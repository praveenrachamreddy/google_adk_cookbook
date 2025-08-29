# Google ADK Cookbook

A comprehensive cookbook for building agentic systems with the Google Agent Development Kit (ADK), featuring modular architecture, custom tools, and Model Context Protocol (MCP) integration.

## Project Overview

This repository contains a complete, production-ready agentic system built with the Google Agent Development Kit (ADK). It demonstrates best practices for creating modular, extensible agents with custom tools and external system integration.

### Key Features

1. **Modular Architecture**: Clean separation of concerns with a base agent class and specialized sub-agents
2. **Custom Tools**: Implementation of custom tools with the FunctionTool wrapper
3. **MCP Integration**: Integration with the Model Context Protocol for external system interaction
4. **Database Integration**: SQLite database interaction through MCP tools
5. **Extensibility**: Clear patterns for adding new agents and tools
6. **Testing**: Comprehensive test suite for verifying functionality
7. **Documentation**: Detailed documentation for understanding and extending the system

## Project Structure

```
google_adk_cookbook/
├── my_agent_system/           # Main agent system code
│   ├── __init__.py           # Package initialization
│   ├── agent.py              # Main orchestrator and agent switching
│   ├── agents/               # Agent implementations
│   │   ├── base_agent.py     # Base agent abstract class
│   │   └── sub_agents/       # Specialized agents
│   │       ├── researcher.py # Research agent
│   │       ├── analyzer.py   # Analysis agent
│   │       ├── responder.py  # Response generation agent
│   │       └── tool_demo.py  # Tool demonstration agent
│   ├── tools/                # Custom tools
│   │   └── custom_tools.py   # Example custom tools
│   ├── shared/               # Shared utilities
│   │   └── utils.py          # Utility functions
│   ├── mcp/                  # MCP integration
│   │   ├── db_server/        # Database MCP server
│   │   └── mcp_agents/       # MCP agents
├── testing/                  # Test scripts and verification tools
├── deployment/               # Deployment configurations
├── docs/                     # Documentation
├── tests/                    # Unit tests
├── eval/                     # Evaluation scripts
├── .env.example             # Environment variables template
├── pyproject.toml           # Project dependencies (Poetry)
├── requirements.txt         # Project dependencies (pip)
├── README.md                # Project documentation
└── run_agent.py             # Example runner script
```

## Getting Started

### Prerequisites

1. Python 3.10 or higher
2. pip package manager
3. Google Cloud account or Google Gemini API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/praveenrachamreddy/google_adk_cookbook.git
   cd google_adk_cookbook
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and configure your environment variables:
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file with a text editor and add your credentials:
   - For Vertex AI: Set `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION`
   - For Gemini API: Set `GOOGLE_API_KEY` and `GOOGLE_GENAI_USE_VERTEXAI=false`

5. Create the database for MCP integration:
   ```bash
   cd my_agent_system/mcp/db_server
   python create_db.py
   cd ../../..
   ```

## Using the System

### Method 1: ADK Web Interface (Recommended)
1. Start the ADK web interface:
   ```bash
   adk web
   ```

2. Open your browser to the provided URL
3. Select an agent from the dropdown menu:
   - `my_agent_system` - Main research assistant (SequentialAgent)
   - `my_agent_system.tool_demo_test_agent` - Tool demonstration agent
   - `my_agent_system.db_mcp_test_agent` - Database MCP agent

### Method 2: ADK CLI
Run the agent directly from command line:
```bash
adk run my_agent_system
```

### Method 3: Programmatic Access
Run the example script:
```bash
python run_agent.py
```

## Agent Descriptions

### SequentialAgent (Main Research Assistant)
A three-stage research workflow:
1. **ResearcherAgent** - Gathers information using Google Search
2. **AnalyzerAgent** - Analyzes and structures the information
3. **ResponderAgent** - Generates a well-formatted response

**Example prompts:**
- "Research the latest developments in quantum computing"
- "Explain the benefits of renewable energy"
- "Analyze the impact of AI on job markets"

### ToolDemoAgent (Tool Demonstration)
Demonstrates custom tool usage:
1. **data_formatter** - Formats data in JSON, XML, CSV
2. **sentiment_analyzer** - Analyzes text sentiment

**Example prompts:**
- "Format this data as JSON: name: John, age: 30, city: New York"
- "Analyze the sentiment of this text: I love this new technology!"
- "Format this data as XML: product: Laptop, price: 999, brand: TechCorp"

### Database MCP Agent
Interacts with a SQLite database through MCP tools:
1. **list_db_tables** - Lists all tables in the database
2. **get_table_schema** - Gets the schema of a specific table
3. **query_db_table** - Queries data from a table
4. **insert_data** - Inserts new data into a table
5. **delete_data** - Deletes data from a table

**Example prompts:**
- "List all users in the database"
- "Show me the schema for the todos table"
- "Find all completed todos"
- "Add a new user with username 'dave' and email 'dave@example.com'"

## Switching Between Agents

To switch between agents for testing:
1. Open `my_agent_system/agent.py`
2. Uncomment the agent you want to test
3. Comment out the other agent
4. Restart the ADK web interface

```python
# For testing the main research workflow:
# root_agent = main_research_agent

# For testing custom tools:
# root_agent = tool_demo_test_agent

# For testing the database MCP agent (default):
root_agent = db_mcp_test_agent
```

## Architecture Details

### Base Agent Class
All agents inherit from `BaseAgent` which provides:
- Consistent initialization interface
- Standardized method signatures
- Common functionality for agent creation

### Sequential Agent Workflow
The main research assistant follows this flow:
```
User Query
    ↓
ResearcherAgent (Google Search)
    ↓
AnalyzerAgent (Information Analysis)
    ↓
ResponderAgent (Final Response)
    ↓
User Response
```

### Custom Tools
Two example tools are implemented:
1. **data_formatter**: Converts text to structured formats
2. **sentiment_analyzer**: Determines text sentiment (positive/negative/neutral)

### MCP Integration
The Model Context Protocol integration allows agents to interact with external systems:
1. **MCP Server**: Exposes tools for external system interaction
2. **MCP Client**: Uses MCP tools through the ADK MCPToolset
3. **Database Tools**: SQLite database operations through MCP

## Extending the System

### Adding New Agents
1. Create a new file in `my_agent_system/agents/sub_agents/`
2. Inherit from `BaseAgent`
3. Implement required methods:
   - `__init__`: Initialize with name and description
   - `get_system_prompt`: Return agent instructions
   - `create_agent`: Return configured ADK Agent
4. Register in the main orchestrator

### Adding New Tools
1. Add functions to `my_agent_system/tools/custom_tools.py`
2. Register them in an agent's `get_tools()` method
3. Use `FunctionTool` wrapper for ADK compatibility

### Adding New MCP Tools
1. Add functions to `my_agent_system/mcp/db_server/server.py`
2. Register them in the `ADK_DB_TOOLS` dictionary
3. The MCP server will automatically expose them to agents

### Modifying Workflows
1. Change agent order in `my_agent_system/agent.py`
2. Replace `SequentialAgent` with other agent types
3. Create parallel processing workflows

## Testing

Several test scripts are available in the `testing/` directory:
- `test_imports.py` - Verify module imports
- `test_custom_tools.py` - Test custom tool functionality
- `verify_system.py` - Comprehensive system verification

Run tests from the project root:
```bash
cd testing
python test_imports.py
python test_custom_tools.py
python verify_system.py
```

## Deployment

The `deployment/` directory contains scripts for deploying agents to Google Cloud:
- `deploy.py` - Deployment script for Vertex AI Agent Engine

## Troubleshooting

### Common Issues
1. **Async event loop errors**: This is a known ADK compatibility issue on Windows
2. **Missing environment variables**: Ensure `.env` is properly configured
3. **Agent not appearing in UI**: Check that `root_agent` is properly exported
4. **MCP server not starting**: Verify Python path and dependencies

### Solutions
1. Use ADK web interface instead of programmatic access for better compatibility
2. Verify all required environment variables are set
3. Ensure only one agent is exported as `root_agent` in `agent.py`
4. Check that the MCP server dependencies are installed

## Running on Linux Server

This project works best on Linux servers where all ADK features are fully supported:

1. Clone the repository on your Linux server:
   ```bash
   git clone https://github.com/praveenrachamreddy/google_adk_cookbook.git
   cd google_adk_cookbook
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. Create the database:
   ```bash
   cd my_agent_system/mcp/db_server
   python create_db.py
   cd ../../..
   ```

5. Run the web interface:
   ```bash
   adk web
   ```

## Next Steps

The system is ready for immediate use and extension:
1. Customize agent prompts for domain-specific applications
2. Add new specialized agents for specific tasks
3. Implement custom tools for unique workflows
4. Deploy agents to Vertex AI Agent Engine using scripts in `deployment/`



Updated `README.md` Content Summary

  1. Project Overview (Update)
   * Emphasize the evolution into a robust, modular, and extensible agentic system.

  2. Key Features (Update/Add)
   * Hybrid Orchestration: Central OrchestratorAgent delegates tasks using both "Agent as a Tool" pattern (for
     simple tasks) and ADK's built-in transfer mechanism (for complex workflows).
   * Centralized Configuration: Agent models and other settings are managed via a config.yaml file.
   * Enhanced BaseAgent: All agents inherit from BaseAgent, providing:
       * Centralized Logging: Standardized logging for agent lifecycle events.
       * Optional Input/Output Schemas: Agents can define Pydantic schemas for structured data (e.g.,
         ResponderAgent's output).
       * Session State Management: Agents can save notes to the current session memory using the MemoryAgent and
         its save_note tool.
   * Modular Agent Design: SearchAgent and MemoryAgent are now standalone, reusable components.
   * Refactored ResearcherAgent: Acts as a manager, using SearchAgent and MemoryAgent as its tools.
   * Model Consistency: All agents use the model specified in config.yaml (e.g., gemini-2.0-flash).
   * (Keep existing features like Custom Tools, MCP Integration, Extensibility, Testing, Documentation)

  3. Project Structure (Update)
   * Add config.yaml at the root level.
   * Under my_agent_system/agents/sub_agents/:
       * Add memory_agent.py
       * Add search_agent.py
   * Under my_agent_system/tools/:
       * Add session_tools.py

  4. Agent Descriptions (Update)
   * OrchestratorAgent (formerly `my_agent_system`'s root agent):
       * Description: "A master orchestrator that intelligently delegates tasks. It uses SearchAgent and
         CodingAgent as direct tools for simple queries, and transfers control to ModularResearchAssistant for
         complex research workflows."
   * ModularResearchAssistant (SequentialAgent):
       * Description: "A multi-stage research workflow. Its ResearcherAgent now uses dedicated SearchAgent and
         MemoryAgent tools."
   * (Keep descriptions for ToolDemoAgent and Database MCP Agent)

  5. Architecture Details (Update/Add New Section)
   * Hybrid Orchestration Model:
       * Explain how OrchestratorAgent uses AgentTool for SearchAgent/CodingAgent (simple tasks) and the ADK's
         sub_agents parameter for ModularResearchAssistant (complex transfers).
       * Mention the transfer_to_agent mechanism is automatically provided by ADK when sub_agents are defined.
   * Base Agent Class Enhancements:
       * Detail the role of BaseAgent in providing common functionalities:
           * Centralized Logging: self.logger for consistent logging.
           * Configuration Loading: self.config for accessing config.yaml settings.
           * Optional Schemas: get_input_schema() and get_output_schema() for Pydantic validation (opt-in).
           * Default Tools: Provides save_note tool via MemoryAgent.
   * Refactored ResearcherAgent:
       * Explain that ResearcherAgent now acts as a manager.
       * It uses SearchAgent (for web search) and MemoryAgent (for saving notes) as its internal tools, respecting
         the "one built-in tool" limitation.
   * Session State Management:
       * Explain the save_note tool in MemoryAgent and how it saves data to the current session state.
       * Mention that session state is automatically shared between agents in the same conversation.

  6. Using the System (Update)
   * Update the agent names in the adk web section to reflect the new OrchestratorAgent as the primary entry point.
   * Provide example prompts that demonstrate the orchestrator's delegation:
       * "What is the capital of Japan?" (triggers SearchAgent)
       * "What is 2 to the power of 16?" (triggers CodingAgent)
       * "Write a report on the impact of renewable energy on the global economy." (triggers
         ModularResearchAssistant)





## License

Copyright 2025 Praveen Rachamreddy

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
