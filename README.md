# My Modular Agentic System

This project implements a modular, extensible agentic system built with the Google Agent Development Kit (ADK).

## Project Overview

We've successfully implemented a modular, extensible agentic system based on the Google Agent Development Kit (ADK) with the following key features:

### Key Features

1. **Modular Architecture**:
   - Created a base `BaseAgent` class for consistent agent implementation
   - Implemented specialized sub-agents (Researcher, Analyzer, Responder)
   - Designed a main orchestrator that coordinates sub-agents in sequence

2. **Extensibility**:
   - Provided clear patterns for adding new agents
   - Created examples of custom tools with the ToolDemoAgent
   - Established a plugin-like architecture for tools

3. **Clear Separation of Concerns**:
   - Each agent has a single, well-defined responsibility
   - Tools are separated from agent logic
   - Shared utilities are organized in a dedicated module

4. **Documentation and Examples**:
   - Comprehensive README with project structure explanation
   - Quick start guide for installation and usage
   - Extension guide for adding new functionality
   - Example agents and tools

## Project Structure

```
my_adk_project/
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
1. Python 3.10 or higher installed
2. pip package manager (usually comes with Python)
3. Google Cloud account or Google Gemini API key

### Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and configure your environment variables:
   ```bash
   copy .env.example .env
   ```
   
   Edit the `.env` file with a text editor and add your credentials:
   - For Vertex AI: Set `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION`
   - For Gemini API: Set `GOOGLE_API_KEY` and `GOOGLE_GENAI_USE_VERTEXAI=false`

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

## Switching Between Agents

To switch between agents for testing:
1. Open `my_agent_system/agent.py`
2. Uncomment the agent you want to test
3. Comment out the other agent
4. Restart the ADK web interface

```python
# For testing the main research workflow:
# root_agent = main_research_agent

# For testing custom tools (default):
root_agent = tool_demo_test_agent
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

## Troubleshooting

### Common Issues
1. **Async event loop errors on Windows**: This is a known ADK compatibility issue
2. **Missing environment variables**: Ensure `.env` is properly configured
3. **Agent not appearing in UI**: Check that `root_agent` is properly exported

### Solutions
1. Use ADK web interface instead of programmatic access for better Windows compatibility
2. Verify all required environment variables are set
3. Ensure only one agent is exported as `root_agent` in `agent.py`

## Next Steps

The system is ready for immediate use and extension:
1. Customize agent prompts for domain-specific applications
2. Add new specialized agents for specific tasks
3. Implement custom tools for unique workflows
4. Deploy agents to Vertex AI Agent Engine using scripts in `deployment/`

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