# Copyright 2025 Your Name
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

"""Deployment script for the agent system."""

import os
import sys
import dotenv
import argparse

# Load environment variables
dotenv.load_dotenv()

from google.cloud import aiplatform
from google.cloud.aiplatform import reasoning_engines
from google.adk.deploy import AdkAppDeployer


def deploy_agent():
    """Deploy the agent to Vertex AI Agent Engine."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    staging_bucket = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
    
    if not project_id or not location:
        print("Error: GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION must be set in environment variables")
        sys.exit(1)
    
    # Initialize Vertex AI
    aiplatform.init(
        project=project_id,
        location=location,
        staging_bucket=staging_bucket
    )
    
    # Deploy using ADK deployer
    deployer = AdkAppDeployer(
        project=project_id,
        location=location
    )
    
    try:
        # Deploy the agent
        deployed_app = deployer.deploy(
            app_name="modular-research-agent",
            agent_module="my_agent_system.agent",
            agent_name="root_agent"
        )
        
        print(f"Agent deployed successfully!")
        print(f"Agent ID: {deployed_app.name}")
        return deployed_app
    except Exception as e:
        print(f"Error deploying agent: {e}")
        sys.exit(1)


def list_agents():
    """List all deployed agents."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")
    
    if not project_id or not location:
        print("Error: GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION must be set in environment variables")
        sys.exit(1)
    
    try:
        # List agents
        agents = reasoning_engines.ReasoningEngine.list(
            project=project_id,
            location=location
        )
        
        print("Deployed Agents:")
        for agent in agents:
            print(f"- {agent.display_name} (ID: {agent.name})")
    except Exception as e:
        print(f"Error listing agents: {e}")


def delete_agent(agent_id):
    """Delete a deployed agent."""
    try:
        agent = reasoning_engines.ReasoningEngine(agent_id)
        agent.delete()
        print(f"Agent {agent_id} deleted successfully!")
    except Exception as e:
        print(f"Error deleting agent: {e}")


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description="Deploy and manage the agent system")
    parser.add_argument(
        "--create",
        action="store_true",
        help="Deploy the agent"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List deployed agents"
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete a deployed agent"
    )
    parser.add_argument(
        "--resource_id",
        type=str,
        help="The ID of the agent to delete"
    )
    
    args = parser.parse_args()
    
    if args.create:
        deploy_agent()
    elif args.list:
        list_agents()
    elif args.delete and args.resource_id:
        delete_agent(args.resource_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()