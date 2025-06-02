# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

The Ambient Agent is a lightweight Python monitoring service that continuously observes Jira for new project tasks and automatically triggers Claude code execution. It's part of the SAAGA MCP Servers monorepo and runs as a standalone agent that bridges Jira task management with AI-powered task execution.

## Architecture

The agent follows a simple polling architecture:
- **Main Loop**: Async polling mechanism that checks Jira every 60 seconds
- **Jira Integration**: Uses Conduit library for Jira API access
- **Claude Execution**: Spawns non-blocking subprocesses for parallel task processing
- **Logging**: Comprehensive Loguru-based logging with file rotation

Key components:
- `src/ambient/main.py` - Core agent implementation with AmbientAgent class
- `pyproject.toml` - UV package configuration with dependencies
- `logs/` - Directory for agent logs and Claude process output

## Common Commands

### Running the Agent
```bash
# Install dependencies with UV
uv sync

# Run the agent
uv run ambient-agent

# Or run directly
uv --directory=/Users/andrew/saga/saaga-mcp-servers/src/saaga_mcp_servers/agents/ambient run ambient-agent
```

### Development
```bash
# Install in development mode
uv pip install -e .

# Run tests (when implemented)
uv run pytest
```

## Key Configuration

Currently uses hard-coded configuration in `main.py`:
- **JIRA_PROJECT**: "AGENT" - The Jira project to monitor
- **POLL_INTERVAL**: 60 seconds - How often to check for new tasks
- **JQL_QUERY**: Searches for tasks in "To Do" status
- **MCP_JSON**: Path to MCP configuration file for Claude

## Important Patterns

1. **Non-blocking Execution**: Claude processes run asynchronously to handle multiple tasks in parallel
2. **Process Monitoring**: Each subprocess is tracked and cleaned up on completion or shutdown
3. **Graceful Shutdown**: Ctrl+C triggers cleanup of all running processes
4. **File Logging**: Each Claude execution logs stdout/stderr to separate timestamped files

## Claude Integration Details

The agent constructs Claude commands with specific parameters:
- Reads task instructions from `.claude/commands/do.md`
- Fetches full Jira issue details including description
- Passes combined prompt with task directive and Jira content
- Uses `--disallowedTools Write` to prevent file modifications
- Enables MCP config with `--mcp-config` flag

## Logging Structure

- **Console**: Color-coded INFO level logs with timestamps
- **Files**: Daily rotating DEBUG logs in `logs/ambient_YYYY-MM-DD.log`
- **Process Logs**: Individual `{ISSUE_KEY}_{TIMESTAMP}_stdout/stderr.log` files

## Dependencies

- **conduit-connect**: Jira API integration
- **loguru**: Advanced logging with rotation
- **aiohttp**: Async HTTP client
- **pyyaml**: Configuration parsing (future use)
- **python-dotenv**: Environment variable management