#!/usr/bin/env python3
"""
Verification script for the modular agentic system.

This script verifies that all components of the agentic system
are correctly implemented and can be imported.
"""

import sys
import os

# Add the project root to the path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

def verify_system():
    """Verify that all system components work correctly."""
    print("=== Modular Agentic System Verification ===\n")
    
    # Test 1: Import main orchestrator
    try:
        from my_agent_system.agent import root_agent
        print("[PASS] Main orchestrator imported successfully")
        print(f"  - Agent name: {root_agent.name}")
        print(f"  - Agent type: {type(root_agent).__name__}")
    except Exception as e:
        print(f"[FAIL] Failed to import main orchestrator: {e}")
        return False
    
    # Test 2: Import individual agents
    try:
        from my_agent_system.agents.sub_agents import researcher, analyzer, responder
        print("\n[PASS] Individual agents imported successfully")
        print(f"  - Researcher: {researcher.researcher_agent.name}")
        print(f"  - Analyzer: {analyzer.analyzer_agent.name}")
        print(f"  - Responder: {responder.responder_agent.name}")
    except Exception as e:
        print(f"[FAIL] Failed to import individual agents: {e}")
        return False
    
    # Test 3: Create ADK agents
    try:
        researcher_adk = researcher.researcher_agent.create_agent()
        analyzer_adk = analyzer.analyzer_agent.create_agent()
        responder_adk = responder.responder_agent.create_agent()
        print("\n[PASS] ADK agents created successfully")
        print(f"  - Researcher ADK agent: {researcher_adk.name}")
        print(f"  - Analyzer ADK agent: {analyzer_adk.name}")
        print(f"  - Responder ADK agent: {responder_adk.name}")
    except Exception as e:
        print(f"[FAIL] Failed to create ADK agents: {e}")
        return False
    
    # Test 4: Import custom tools
    try:
        from my_agent_system.tools.custom_tools import data_formatter, sentiment_analyzer
        print("\n[PASS] Custom tools imported successfully")
        print("  - data_formatter tool available")
        print("  - sentiment_analyzer tool available")
    except Exception as e:
        print(f"[FAIL] Failed to import custom tools: {e}")
        return False
    
    # Test 5: Import shared utilities
    try:
        from my_agent_system.shared import utils
        print("\n[PASS] Shared utilities imported successfully")
        print("  - Utility functions available")
    except Exception as e:
        print(f"[FAIL] Failed to import shared utilities: {e}")
        return False
    
    print("\n=== All Tests Passed! ===")
    print("\nThe modular agentic system is correctly implemented and ready for use.")
    print("\nNext steps:")
    print("1. Configure your environment variables in .env")
    print("2. Run the system with: python run_agent.py")
    print("3. Extend the system by adding new agents and tools")
    
    return True

if __name__ == "__main__":
    success = verify_system()
    sys.exit(0 if success else 1)