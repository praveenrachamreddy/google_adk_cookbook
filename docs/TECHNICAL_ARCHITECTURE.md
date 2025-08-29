# Technical Architecture Documentation

## System Overview

This document provides detailed technical documentation for the modular agentic system implemented with Google Agent Development Kit (ADK).

## Core Components

### 1. Base Agent Framework
**File**: `my_agent_system/agents/base_agent.py`
- Abstract base class defining the agent interface
- Enforces consistent agent structure and methods
- Provides common functionality for all specialized agents

### 2. Sequential Agent Orchestrator
**File**: `my_agent_system/agent.py`
- Main entry point for ADK web interface
- Configures and exports the `root_agent`
- Supports switching between different agent configurations

### 3. Specialized Agents

#### ResearcherAgent
**File**: `my_agent_system/agents/sub_agents/researcher.py`
- **Purpose**: Information gathering using web search
- **Tools**: Google Search integration
- **Workflow Stage**: First stage in research sequence
- **Model**: gemini-2.5-flash

#### AnalyzerAgent
**File**: `my_agent_system/agents/sub_agents/analyzer.py`
- **Purpose**: Information analysis and insight generation
- **Tools**: None (works with provided information)
- **Workflow Stage**: Second stage in research sequence
- **Model**: gemini-2.5-flash

#### ResponderAgent
**File**: `my_agent_system/agents/sub_agents/responder.py`
- **Purpose**: Final response generation and formatting
- **Tools**: None (formats analyzed information)
- **Workflow Stage**: Final stage in research sequence
- **Model**: gemini-2.5-flash

#### ToolDemoAgent
**File**: `my_agent_system/agents/sub_agents/tool_demo.py`
- **Purpose**: Demonstrate custom tool implementation
- **Tools**: data_formatter, sentiment_analyzer
- **Model**: gemini-2.5-flash

### 4. Custom Tools
**File**: `my_agent_system/tools/custom_tools.py`

#### data_formatter
- **Function**: Format text data in various formats
- **Supported Formats**: JSON, XML, CSV
- **Async**: Yes
- **Parameters**: data (str), format_type (str)

#### sentiment_analyzer
- **Function**: Analyze text sentiment
- **Returns**: Dictionary with sentiment, score, explanation
- **Async**: Yes
- **Parameters**: text (str)

## System Architecture

### Directory Structure
```
my_agent_system/
├── __init__.py              # Package exports
├── agent.py                 # Root agent configuration
├── agents/                  # Agent implementations
│   ├── __init__.py         # Agents package
│   ├── base_agent.py       # Abstract base class
│   └── sub_agents/         # Specialized agents
│       ├── __init__.py    # Sub-agents package
│       ├── researcher.py  # Research agent
│       ├── analyzer.py    # Analysis agent
│       ├── responder.py   # Response agent
│       └── tool_demo.py   # Tool demo agent
├── tools/                   # Custom tools
│   ├── __init__.py        # Tools package
│   └── custom_tools.py    # Tool implementations
└── shared/                  # Shared utilities
    ├── __init__.py        # Shared package
    └── utils.py           # Utility functions
```

## Key Technical Patterns

### 1. Inheritance Pattern
All agents inherit from `BaseAgent`:
```python
class SpecializedAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="AgentName", description="...")
    
    def create_agent(self) -> Agent:
        return Agent(...)
```

### 2. Tool Integration
Custom tools are wrapped with `FunctionTool`:
```python
def get_tools(self):
    return [
        FunctionTool(func=custom_function),
    ]
```

### 3. Agent Switching
Root agent can be switched by modifying `agent.py`:
```python
# root_agent = main_research_agent
root_agent = tool_demo_test_agent
```

## Event Flow and Tracing

### Sequential Agent Flow
1. User query received by ADK runner
2. ResearcherAgent processes with Google Search
3. AnalyzerAgent processes research findings
4. ResponderAgent generates final response
5. Response returned to user

**Note**: Tool calls are executed within agents but may not appear in high-level event traces.

## Configuration Management

### Environment Variables
**File**: `.env` (copy from `.env.example`)
- `GOOGLE_GENAI_USE_VERTEXAI`: Boolean for service selection
- `GOOGLE_CLOUD_PROJECT`: GCP project ID
- `GOOGLE_CLOUD_LOCATION`: GCP region
- `GOOGLE_API_KEY`: Gemini API key

### Dependencies
**File**: `requirements.txt`
- `google-adk`: Core ADK framework
- `google-cloud-aiplatform`: Google Cloud integration
- `google-genai`: Gemini model access
- `pydantic`: Data validation
- `python-dotenv`: Environment management
- Testing dependencies: `pytest`, `pytest-asyncio`

## Testing Framework

### Test Organization
**Directory**: `testing/`
- Unit tests for individual components
- Integration tests for agent workflows
- Verification scripts for system health

### Test Execution
```bash
cd testing
python test_imports.py      # Module import verification
python test_custom_tools.py # Tool functionality tests
python verify_system.py     # Comprehensive system check
```

## Extensibility Points

### 1. Adding New Agents
1. Create new file in `agents/sub_agents/`
2. Inherit from `BaseAgent`
3. Implement required abstract methods
4. Register in main orchestrator

### 2. Adding New Tools
1. Implement function in `tools/custom_tools.py`
2. Wrap with `FunctionTool`
3. Register in agent's `get_tools()` method

### 3. Modifying Workflows
1. Change agent sequence in `SequentialAgent` configuration
2. Replace with `ParallelAgent` for concurrent processing
3. Create custom agent orchestrators

## Performance Considerations

### Async Operations
- All custom tools are implemented as async functions
- ADK handles async/await patterns internally
- Windows compatibility may require specific event loop configuration

### Model Selection
- All agents use `gemini-2.5-flash` for balanced performance
- Can be modified to use other Gemini models
- Model selection affects response quality and latency

## Security Considerations

### Environment Management
- Sensitive credentials stored in `.env` file
- `.env` excluded from version control via `.gitignore`
- Example configuration in `.env.example`

### Input Validation
- ADK provides built-in input sanitization
- Custom tools should validate input parameters
- Agents should handle malformed inputs gracefully

## Deployment Architecture

### Local Development
- ADK web interface for interactive testing
- Programmatic access via `InMemoryRunner`
- Environment-based configuration

### Cloud Deployment
- Vertex AI Agent Engine deployment scripts
- Google Cloud project integration
- Production environment configuration

## Troubleshooting Guide

### Common Issues

1. **Import Errors**
   - Verify Python path includes project root
   - Check `__init__.py` files exist in all directories
   - Ensure dependencies are installed

2. **Tool Not Executing**
   - Verify `FunctionTool` wrapper is used
   - Check tool registration in agent configuration
   - Confirm async/await patterns are correct

3. **Agent Not Appearing in UI**
   - Ensure `root_agent` is exported from module
   - Verify ADK web interface is restarted after changes
   - Check for syntax errors in agent module

4. **API Authentication Errors**
   - Verify environment variables are set correctly
   - Check Google Cloud project and API enablement
   - Confirm API key validity and permissions

## Future Enhancements

### Planned Improvements
1. Enhanced error handling and logging
2. Additional custom tools for common operations
3. Improved tool argument validation
4. Extended testing coverage
5. Performance optimization for large workflows

### Scalability Considerations
1. Agent state management for long-running processes
2. Distributed agent execution patterns
3. Caching mechanisms for repeated queries
4. Rate limiting for API calls
5. Monitoring and metrics collection

## License Information

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