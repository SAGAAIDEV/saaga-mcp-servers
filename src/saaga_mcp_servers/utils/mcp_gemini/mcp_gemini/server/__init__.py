"""MCP server package initialization"""

from mcp_gemini.config import load_config
from mcp_gemini.server.app import create_mcp_server

# Create server instance with default configuration
server = create_mcp_server(load_config())

__all__ = ["server", "create_mcp_server"]
