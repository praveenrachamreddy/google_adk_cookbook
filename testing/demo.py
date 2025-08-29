#!/usr/bin/env python3
"""
Example usage script for the modular agentic system.

This script demonstrates how to use the implemented agentic system
with a sample research query.
"""

import sys
import os
import asyncio

# Add the project root to the path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

def demonstrate_system():
    """Demonstrate the agentic system capabilities."""
    print("=== Modular Agentic System Demo ===\n")
    
    # Show project structure
    print("Project Structure:")
    print("- Main orchestrator: agent.py")
    print("- Specialized agents: agents/sub_agents/")
    print("- Custom tools: tools/custom_tools.py")
    print("- Shared utilities: shared/utils.py\n")
    
    # Show agent capabilities
    print("Implemented Agents:")
    print("1. ResearcherAgent - Gathers information using web search")
    print("2. AnalyzerAgent - Analyzes information and draws insights")
    print("3. ResponderAgent - Generates well-structured responses")
    print("4. ToolDemoAgent - Demonstrates custom tool usage\n")
    
    # Show extensibility
    print("Extending the System:")
    print("1. Add new agents by inheriting from BaseAgent")
    print("2. Implement custom tools in tools/custom_tools.py")
    print("3. Register new agents in the main orchestrator")
    print("4. Customize prompts for domain-specific use cases\n")
    
    # Show how to run
    print("To run the system:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Configure environment: cp .env.example .env")
    print("3. Run the agent: python run_agent.py")
    print("4. Extend as needed for your use case\n")
    
    print("The system is ready for immediate use and extension!")

if __name__ == "__main__":
    demonstrate_system()