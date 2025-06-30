# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based MCP (Model Context Protocol) server that provides Google Suite (GSuite) integration capabilities for AI assistants. It enables interaction with Gmail and Google Calendar through standardized MCP tools.

## Development Commands

### Setup and Installation

```bash
# Install dependencies using uv
uv sync

# Build the package
uv build

# Run the server locally
uv run mcp-gsuite

# Configure via environment variables (Note: command-line args documented in README are not yet implemented)
export GSUITE_CREDENTIALS_DIR=/path/to/credentials
export GSUITE_ACCOUNTS_FILE=.accounts.json
uv run mcp-gsuite

# Run the OAuth authentication flow
uv run mcp-gsuite-auth
# Or use specific commands:
uv run mcp-gsuite-auth auth  # Authenticate and print credentials
uv run mcp-gsuite-auth kill_server  # Kill local OAuth server on port 4100
```

### Testing and Development

```bash
# Run the MCP Inspector for debugging
npx @modelcontextprotocol/inspector uv --directory /path/to/mcp-gsuite run mcp-gsuite

# Watch server logs
tail -n 20 -f ~/Library/Logs/Claude/mcp-server-mcp-gsuite.log

# Install for development (via pip in a virtual environment)
pip install -e .

# Run with Python directly (requires uv)
uv run python -m mcp_gsuite
```

### Publishing

```bash
# Publish to PyPI
uv publish

# Set PyPI credentials
export UV_PUBLISH_TOKEN=your_token
# or use --token flag
```

## Architecture

### Core Components

1. **MCP Server Entry Point** (`src/mcp_gsuite/__init__.py`)
   - Uses FastMCP framework
   - Registers all available tools
   - Runs on stdio transport

2. **Service Layer** (`src/mcp_gsuite/lib/`)
   - `calendar.py`: Google Calendar API wrapper with CalendarService class
   - `gmail.py`: Gmail API wrapper with GmailService class
   - `auth/`: OAuth2 authentication subsystem
   - `accounts.py`: Multi-account management
   - `admin.py`: Administrative functions

3. **Tools Layer** (`src/mcp_gsuite/tools/`)
   - Each tool is a separate async function decorated with `@format_docstring_with_user_id_arg`
   - Tools use `asyncio.to_thread` to run blocking Google API calls
   - All tools return JSON strings and handle errors by raising exceptions with JSON error details

4. **Configuration** (`src/mcp_gsuite/config/`)
   - Environment-based configuration using Pydantic
   - Supports custom paths for OAuth credentials and account files

### Authentication Flow

1. OAuth2 credentials stored in `.gauth.json` (client ID/secret)
2. Account information in `.accounts.json` (email addresses and metadata)
3. Per-account tokens stored as `.oauth.{email}.json` after first authentication
4. Browser-based OAuth flow initiated on first use of each account

### Tool Pattern

All tools follow this pattern:
```python
@format_docstring_with_user_id_arg
async def tool_name(user_id: str, **params) -> str:
    """Docstring with {user_id_arg} placeholder"""
    try:
        service = ServiceClass(user_id=user_id)
        result = await asyncio.to_thread(service.method, **params)
        return json.dumps(result, indent=2)
    except Exception as e:
        error_response = {"error": str(e), "user_id": user_id}
        raise Exception(json.dumps(error_response, indent=2))
```

## Key Technical Details

- **Python Version**: 3.13+ required
- **Async Pattern**: Uses `asyncio.to_thread` for blocking Google API calls
- **Error Handling**: Exceptions with JSON-formatted error messages
- **Logging**: Uses Loguru for structured logging
- **Transport**: stdio-based MCP communication
- **Google APIs**: Uses `google-api-python-client` with v3 Calendar API and v1 Gmail API
- **Package Manager**: Uses `uv` for dependency management and package building
- **Entry Points**: 
  - `mcp-gsuite`: Main MCP server
  - `mcp-gsuite-auth`: OAuth authentication flow CLI

## Recent Enhancements

### Calendar Color Support
- `list_calendars` now returns color information (background_color, foreground_color, color_id)
- `get_events` includes colorId field and optional RGB color values via `include_color_rgb` parameter
- New `get_calendar_colors` tool retrieves the full color palette definitions
- Color information enables visual representation in UI applications

## Testing Strategy

### Local Testing
```bash
# Test a specific tool manually
uv run python -c "
import asyncio
from mcp_gsuite.tools.gmail.query_emails import query_gmail_emails
result = asyncio.run(query_gmail_emails('user@example.com', 'is:unread'))
print(result)
"

# Use MCP Inspector for interactive testing
npx @modelcontextprotocol/inspector uv --directory . run mcp-gsuite
```

### Authentication Testing
```bash
# Test OAuth flow
uv run mcp-gsuite-auth auth

# If server is stuck on port 4100
uv run mcp-gsuite-auth kill_server
```

## Configuration Notes

- OAuth credentials stored in `.gauth.json` (client ID/secret)
- Account information in `.accounts.json` (email addresses and metadata)
- Per-account tokens stored as `.oauth.{email}.json` after first authentication
- Configuration currently uses environment variables:
  - `GSUITE_CREDENTIALS_DIR`: Directory for credentials (default: `.credentials`)
  - `GSUITE_ACCOUNTS_FILE`: Accounts file name (default: `.accounts.json`)
  
Note: Command-line arguments documented in README (`--gauth-file`, `--accounts-file`, `--credentials-dir`) are not yet implemented. Use environment variables instead.