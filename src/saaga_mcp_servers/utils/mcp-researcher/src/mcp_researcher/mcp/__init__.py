"""MCP server module for the researcher service."""

from .server import mcp
from .tools import register_tools

__all__ = ["mcp", "register_tools"]