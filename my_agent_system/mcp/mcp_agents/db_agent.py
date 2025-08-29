import sys
import os
from pathlib import Path

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
# Use StdioConnectionParams instead of StdioServerParameters
from google.adk.tools.mcp_tool.connection_params import StdioConnectionParams

# Database MCP prompt
DB_MCP_PROMPT = """
You are a highly proactive and efficient assistant for interacting with a local SQLite database.
Your primary goal is to fulfill user requests by directly using the available database tools.

Key Principles:
- Prioritize Action: When a user's request implies a database operation, use the relevant tool immediately.
- Smart Defaults: If a tool requires parameters not explicitly provided by the user:
    - For querying tables (e.g., the `query_db_table` tool):
        - If columns are not specified, default to selecting all columns (e.g., by providing "*" for the `columns` parameter).
        - If a filter condition is not specified, default to selecting all rows (e.g., by providing a universally true condition like "1=1" for the `condition` parameter).
    - For listing tables (e.g., `list_db_tables`): If it requires a dummy parameter, provide a sensible default value like "default_list_request".
- Minimize Clarification: Only ask clarifying questions if the user's intent is highly ambiguous and reasonable defaults cannot be inferred. Strive to act on the request using your best judgment.
- Efficiency: Provide concise and direct answers based on the tool's output.
- Make sure you return information in an easy to read format.
"""

# Path to MCP server script - ensure it's absolute
PATH_TO_YOUR_MCP_SERVER_SCRIPT = str((Path(__file__).parent / ".." / "db_server" / "server.py").resolve())

# Create the database MCP agent with proper connection parameters
db_mcp_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="db_mcp_client_agent",
    instruction=DB_MCP_PROMPT,
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                command=sys.executable,  # Use the current Python interpreter
                args=[PATH_TO_YOUR_MCP_SERVER_SCRIPT],
            )
        )
    ],
)