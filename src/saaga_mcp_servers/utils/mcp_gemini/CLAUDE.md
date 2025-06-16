# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MCP Gemini is a Model Context Protocol (MCP) server implementation that provides tools for AI assistants. It's a Python-based MCP server using the FastMCP framework with support for both stdio and SSE (Server-Sent Events) transports.

## Development Commands

### Initial Setup
```bash
# Create and activate virtual environment
uv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode (REQUIRED before running any commands)
uv pip install -e .
```

### Running the Server
```bash
# Run server with stdio transport (default)
mcp_gemini-server

# Run server with SSE transport
mcp_gemini-server --transport sse --port 3001

# Test with the convenience client
mcp_gemini-client "Hello, World"
mcp_gemini-client "Hello, World" --transform upper
```

### Development Tools
```bash
# Start MCP Inspector for testing (requires package to be installed)
PYTHONPATH=. mcp dev mcp_gemini/server/app.py

# Build distribution
python -m build --wheel
```

## Architecture

### Project Structure
- `mcp_gemini/server/app.py`: Main server entry point with unified transport handling
- `mcp_gemini/tools/`: Directory for tool implementations (currently contains `echo.py`)
- `mcp_gemini/client/app.py`: Convenience client for testing
- `mcp_gemini/config.py`: Server configuration management
- `mcp_gemini/logging_config.py`: Logging setup with OS-specific log locations

### Key Components

1. **Server Architecture**: 
   - Single entry point (`mcp_gemini-server`) supporting both stdio and SSE transports
   - Uses FastMCP framework for tool registration
   - Tools are registered in `register_tools()` function in `server/app.py`

2. **Tool Implementation Pattern**:
   - Tools are implemented as separate modules in `mcp_gemini/tools/`
   - Each tool returns an MCP content type (TextContent, ImageContent, JsonContent, etc.)
   - Tools are wrapped and registered in the server's `register_tools()` function

3. **Logging**:
   - Logs to both stderr and rotating file logs
   - Log locations are OS-specific (macOS: `~/Library/Logs/mcp-servers/`)
   - Configurable via `LOG_LEVEL` environment variable

### Adding New Tools

1. Create a new tool module in `mcp_gemini/tools/`:
```python
from mcp import types

def your_tool(param1: str) -> types.TextContent:
    """Tool implementation"""
    result = process_data(param1)
    return types.TextContent(
        type="text",
        text=result,
        format="text/plain"
    )
```

2. Register the tool in `server/app.py`:
```python
from mcp_gemini.tools.your_tool import your_tool

def register_tools(mcp_server: FastMCP) -> None:
    @mcp_server.tool(
        name="your_tool_name",
        description="What your tool does"
    )
    def your_tool_wrapper(param1: str) -> types.TextContent:
        return your_tool(param1)
```

## Important Notes

- The server module must be installed (`uv pip install -e .`) before running any commands
- When using `mcp dev`, set `PYTHONPATH=.` to ensure module imports work correctly
- The project supports Python 3.11-3.12 (not 3.13+)
- Entry points are configured in `pyproject.toml`