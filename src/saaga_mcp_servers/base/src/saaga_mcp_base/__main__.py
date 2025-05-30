"""Entry point module for the base MCP package.

This module initializes and runs the MCP (Model Control Protocol) service
for the base functionality. It creates an instance of the MCP service with
the necessary tools and runs it with the stdio transport when executed directly.

This base server extends the capabilities of all MCP server development.
It provides the ability for MCP tools to be logged to an SQL database
specified in the logging file, enabling tracking and analysis of tool usage.
"""
from . import run_server




if __name__ == "__main__":
    run_server()

