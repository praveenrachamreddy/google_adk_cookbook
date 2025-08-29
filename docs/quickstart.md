# My Modular Agentic System - Quick Start Guide

This guide will help you set up and run the modular agentic system.

## Prerequisites

1. Python 3.10 or higher
2. Poetry (for dependency management) or pip
3. A Google Cloud Project with Vertex AI enabled (for full functionality)
4. Google Cloud credentials configured

## Installation

### Option 1: Using Poetry (Recommended)

1. Install Poetry if you haven't already:
   ```bash
   pip install poetry
   ```

2. Navigate to the project directory:
   ```bash
   cd my_adk_project
   ```

3. Install dependencies:
   ```bash
   poetry install
   ```

### Option 2: Using pip

1. Navigate to the project directory:
   ```bash
   cd my_adk_project
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your Google Cloud project details:
   ```bash
   # For Vertex AI usage
   GOOGLE_GENAI_USE_VERTEXAI=true
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=us-central1

   # For Gemini API usage (instead of Vertex AI)
   # GOOGLE_GENAI_USE_VERTEXAI=false
   # GOOGLE_API_KEY=your-api-key-here
   ```

## Running the Agent

### Local Testing

To run the agent locally for testing:

```bash
python run_agent.py
```

This will run the agent with a sample input about quantum computing.

### Using ADK CLI

You can also use the ADK CLI to interact with the agent:

```bash
adk run my_agent_system
```

Or for a web interface:

```bash
adk web
```

## Running Tests

To run the unit tests:

```bash
python -m pytest tests/
```

## Running Evaluation

To run the evaluation script:

```bash
python eval/test_eval.py
```

## Deployment

To deploy the agent to Vertex AI Agent Engine:

```bash
python deployment/deploy.py --create
```

To list deployed agents:

```bash
python deployment/deploy.py --list
```

To delete a deployed agent:

```bash
python deployment/deploy.py --delete --resource_id=AGENT_ID
```

## Extending the System

See `docs/extending.md` for detailed information on how to extend the system with new agents and tools.