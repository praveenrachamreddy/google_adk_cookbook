import asyncio
import json
import logging
import os
import sqlite3
from pathlib import Path

import mcp.server.stdio
from dotenv import load_dotenv
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type
from mcp import types as mcp_types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# Load environment variables
load_dotenv()

# Setup logging
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "mcp_server_activity.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, mode="w"),
        logging.StreamHandler()  # Also log to console for debugging
    ],
)

# Database path
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "database.db")

# Safe print function that won't crash when stdout is closed
def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
    except:
        pass  # Silently ignore print errors

safe_print(f"DEBUG: MCP Server starting...")
safe_print(f"DEBUG: Database path: {DATABASE_PATH}")
safe_print(f"DEBUG: Database exists: {os.path.exists(DATABASE_PATH)}")

# Database utility functions
def get_db_connection():
    safe_print(f"DEBUG: Connecting to database at {DATABASE_PATH}")
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def list_db_tables(dummy_param: str) -> dict:
    safe_print(f"DEBUG: list_db_tables called with dummy_param: {dummy_param}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        result = {
            "success": True,
            "message": "Tables listed successfully.",
            "tables": tables,
        }
        safe_print(f"DEBUG: list_db_tables result: {result}")
        return result
    except sqlite3.Error as e:
        error_result = {"success": False, "message": f"Error listing tables: {e}", "tables": []}
        safe_print(f"DEBUG: list_db_tables error: {error_result}")
        return error_result
    except Exception as e:
        error_result = {
            "success": False,
            "message": f"An unexpected error occurred while listing tables: {e}",
            "tables": [],
        }
        safe_print(f"DEBUG: list_db_tables unexpected error: {error_result}")
        return error_result

def get_table_schema(table_name: str) -> dict:
    safe_print(f"DEBUG: get_table_schema called with table_name: {table_name}")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info('{table_name}');")
    schema_info = cursor.fetchall()
    conn.close()
    if not schema_info:
        error_msg = f"Table '{table_name}' not found or no schema information."
        safe_print(f"DEBUG: get_table_schema error: {error_msg}")
        raise ValueError(error_msg)

    columns = [{"name": row["name"], "type": row["type"]} for row in schema_info]
    result = {"table_name": table_name, "columns": columns}
    safe_print(f"DEBUG: get_table_schema result: {result}")
    return result

def query_db_table(table_name: str, columns: str = "*", condition: str = "1=1") -> list[dict]:
    safe_print(f"DEBUG: query_db_table called with table_name: {table_name}, columns: {columns}, condition: {condition}")
    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"SELECT {columns} FROM {table_name}"
    if condition:
        query += f" WHERE {condition}"
    query += ";"

    try:
        cursor.execute(query)
        results = [dict(row) for row in cursor.fetchall()]
        safe_print(f"DEBUG: query_db_table result count: {len(results)}")
        return results
    except sqlite3.Error as e:
        conn.close()
        error_msg = f"Error querying table '{table_name}': {e}"
        safe_print(f"DEBUG: query_db_table error: {error_msg}")
        raise ValueError(error_msg)
    finally:
        conn.close()

def insert_data(table_name: str, data: dict) -> dict:
    safe_print(f"DEBUG: insert_data called with table_name: {table_name}, data: {data}")
    if not data:
        error_result = {"success": False, "message": "No data provided for insertion."}
        safe_print(f"DEBUG: insert_data error: {error_result}")
        return error_result

    conn = get_db_connection()
    cursor = conn.cursor()

    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?" for _ in data])
    values = tuple(data.values())

    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    try:
        cursor.execute(query, values)
        conn.commit()
        last_row_id = cursor.lastrowid
        result = {
            "success": True,
            "message": f"Data inserted successfully. Row ID: {last_row_id}",
            "row_id": last_row_id,
        }
        safe_print(f"DEBUG: insert_data result: {result}")
        return result
    except sqlite3.Error as e:
        conn.rollback()
        error_result = {
            "success": False,
            "message": f"Error inserting data into table '{table_name}': {e}",
        }
        safe_print(f"DEBUG: insert_data error: {error_result}")
        return error_result
    finally:
        conn.close()

def delete_data(table_name: str, condition: str) -> dict:
    safe_print(f"DEBUG: delete_data called with table_name: {table_name}, condition: {condition}")
    if not condition or not condition.strip():
        error_result = {
            "success": False,
            "message": "Deletion condition cannot be empty. This is a safety measure to prevent accidental deletion of all rows.",
        }
        safe_print(f"DEBUG: delete_data error: {error_result}")
        return error_result

    conn = get_db_connection()
    cursor = conn.cursor()

    query = f"DELETE FROM {table_name} WHERE {condition}"

    try:
        cursor.execute(query)
        rows_deleted = cursor.rowcount
        conn.commit()
        result = {
            "success": True,
            "message": f"{rows_deleted} row(s) deleted successfully from table '{table_name}'.",
            "rows_deleted": rows_deleted,
        }
        safe_print(f"DEBUG: delete_data result: {result}")
        return result
    except sqlite3.Error as e:
        conn.rollback()
        error_result = {
            "success": False,
            "message": f"Error deleting data from table '{table_name}': {e}",
        }
        safe_print(f"DEBUG: delete_data error: {error_result}")
        return error_result
    finally:
        conn.close()

# MCP Server setup
safe_print("DEBUG: Creating MCP Server instance for SQLite DB...")
logging.info("Creating MCP Server instance for SQLite DB...")
app = Server("sqlite-db-mcp-server")

# Wrap database utility functions as ADK FunctionTools
safe_print("DEBUG: Wrapping database utility functions as ADK FunctionTools...")
ADK_DB_TOOLS = {
    "list_db_tables": FunctionTool(func=list_db_tables),
    "get_table_schema": FunctionTool(func=get_table_schema),
    "query_db_table": FunctionTool(func=query_db_table),
    "insert_data": FunctionTool(func=insert_data),
    "delete_data": FunctionTool(func=delete_data),
}

@app.list_tools()
async def list_mcp_tools() -> list[mcp_types.Tool]:
    safe_print("DEBUG: MCP Server: Received list_tools request.")
    logging.info("MCP Server: Received list_tools request.")
    mcp_tools_list = []
    for tool_name, adk_tool_instance in ADK_DB_TOOLS.items():
        if not adk_tool_instance.name:
            adk_tool_instance.name = tool_name

        mcp_tool_schema = adk_to_mcp_tool_type(adk_tool_instance)
        safe_print(f"DEBUG: MCP Server: Advertising tool: {mcp_tool_schema.name}")
        logging.info(f"MCP Server: Advertising tool: {mcp_tool_schema.name}")
        mcp_tools_list.append(mcp_tool_schema)
    return mcp_tools_list

@app.call_tool()
async def call_mcp_tool(name: str, arguments: dict) -> list[mcp_types.TextContent]:
    safe_print(f"DEBUG: MCP Server: Received call_tool request for '{name}' with args: {arguments}")
    logging.info(f"MCP Server: Received call_tool request for '{name}' with args: {arguments}")

    if name in ADK_DB_TOOLS:
        adk_tool_instance = ADK_DB_TOOLS[name]
        try:
            adk_tool_response = await adk_tool_instance.run_async(
                args=arguments,
                tool_context=None,
            )
            safe_print(f"DEBUG: MCP Server: ADK tool '{name}' executed. Response: {adk_tool_response}")
            logging.info(f"MCP Server: ADK tool '{name}' executed. Response: {adk_tool_response}")
            response_text = json.dumps(adk_tool_response, indent=2)
            return [mcp_types.TextContent(type="text", text=response_text)]

        except Exception as e:
            safe_print(f"DEBUG: MCP Server: Error executing ADK tool '{name}': {e}")
            logging.error(f"MCP Server: Error executing ADK tool '{name}': {e}", exc_info=True)
            error_payload = {
                "success": False,
                "message": f"Failed to execute tool '{name}': {str(e)}",
            }
            error_text = json.dumps(error_payload)
            return [mcp_types.TextContent(type="text", text=error_text)]
    else:
        safe_print(f"DEBUG: MCP Server: Tool '{name}' not found/exposed by this server.")
        logging.warning(f"MCP Server: Tool '{name}' not found/exposed by this server.")
        error_payload = {
            "success": False,
            "message": f"Tool '{name}' not implemented by this server.",
        }
        error_text = json.dumps(error_payload)
        return [mcp_types.TextContent(type="text", text=error_text)]

# MCP Server Runner
async def run_mcp_stdio_server():
    safe_print("DEBUG: MCP Stdio Server: Starting handshake with client...")
    logging.info("MCP Stdio Server: Starting handshake with client...")
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        safe_print("DEBUG: MCP Stdio Server: Running server...")
        logging.info("MCP Stdio Server: Running server...")
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=app.name,
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
        safe_print("DEBUG: MCP Stdio Server: Run loop finished or client disconnected.")
        logging.info("MCP Stdio Server: Run loop finished or client disconnected.")

if __name__ == "__main__":
    safe_print("DEBUG: Launching SQLite DB MCP Server via stdio...")
    logging.info("Launching SQLite DB MCP Server via stdio...")
    try:
        asyncio.run(run_mcp_stdio_server())
    except KeyboardInterrupt:
        safe_print("\nDEBUG: MCP Server (stdio) stopped by user.")
        logging.info("\nMCP Server (stdio) stopped by user.")
    except Exception as e:
        safe_print(f"DEBUG: MCP Server (stdio) encountered an unhandled error: {e}")
        logging.critical(f"MCP Server (stdio) encountered an unhandled error: {e}", exc_info=True)
    finally:
        safe_print("DEBUG: MCP Server (stdio) process exiting.")
        logging.info("MCP Server (stdio) process exiting.")