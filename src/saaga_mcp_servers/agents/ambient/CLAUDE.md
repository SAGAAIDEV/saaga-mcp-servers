# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

The Ambient Agent is a lightweight Python monitoring service that continuously observes Jira for new project tasks and automatically triggers Claude code execution. It's part of the SAAGA MCP Servers monorepo and runs as a standalone agent that bridges Jira task management with AI-powered task execution.

## Architecture

The agent follows an asynchronous polling architecture with non-blocking subprocess management:

### Core Components
- `src/ambient/main.py` - Core agent implementation with AmbientAgent class
- `src/ambient/cli.py` - Fire-based CLI interface with multiple commands (run, watch, status, config)
- `src/ambient/config/settings.py` - Pydantic-based configuration with environment variable support
- `src/ambient/config_loader.py` - Loads command-specific configurations (.md and .mcp.json files)
- `src/ambient/process_manager.py` - Process lifecycle management (exists but not yet integrated)
- `src/ambient/utils/transcriber.py` - AssemblyAI-based real-time audio transcription

### Key Patterns
1. **Non-blocking Execution**: Claude processes run asynchronously via `subprocess.Popen`
2. **Process Tracking**: Dictionary maintains running processes with automatic cleanup
3. **Graceful Shutdown**: Signal handlers ensure all subprocesses terminate on exit
4. **Configuration Flexibility**: Multiple command configurations via `.md` and `.mcp.json` files
5. **Task State Management**: Monitors Jira status changes (done/failed/confused) and terminates processes accordingly

## Common Commands

### Running the Agent
```bash
# Install dependencies with UV
uv sync

# Run as Jira monitor (main functionality)
uv run ambient-agent

# Run CLI commands
uv run ambient run <command>     # Execute a specific command configuration
uv run ambient watch             # Watch for voice commands via transcription
uv run ambient status            # Show agent status
uv run ambient config <command>  # Show configuration for a command

# Run directly from monorepo root
uv --directory=/Users/andrew/saga/saaga-mcp-servers/src/saaga_mcp_servers/agents/ambient run ambient-agent
```

### Development
```bash
# Install in development mode
uv pip install -e .

# Run tests (when implemented)
uv run pytest

# Check types (when configured)
uv run mypy src/ambient
```

## Configuration System

### Settings (`config/settings.py`)
Uses Pydantic Settings with environment variable support:
- **JIRA_PROJECT**: Default "AGENT" - The Jira project to monitor
- **POLL_INTERVAL**: Default 60 seconds - How often to check for new tasks
- **JQL_QUERY**: Computed property - Searches for tasks in "To Do" status
- **ASSEMBLYAI_API_KEY**: Required for voice transcription features
- **MCP_CONFIG_PATH**: Path to MCP configuration files

Environment variables are loaded from `.env` file.

### Command Configurations
- `config/do.md`: Instructions for async task management
- `config/delegate.md`: Task delegation instructions
- Command-specific: `{command}.md` and `.mcp.{command}.json` files

## Claude Integration Details

The agent constructs Claude commands with specific parameters:
- Loads instructions from command-specific `.md` files
- Fetches full Jira issue details including description
- Combines prompt with task directive and Jira content
- Uses `--disallowedTools Write` by default (configurable)
- Enables MCP config with `--mcp-config` flag
- Non-blocking execution allows parallel processing

## Jira Integration

- Uses Conduit library for authentication and API access
- Monitors tasks with "To Do" status in configured project
- Tracks processed issues to avoid duplicates
- Responds to status changes:
  - "Done", "Solved", "Resolved": Terminates associated process
  - "Failed", "Confused": Logs warning and terminates process

## Logging Structure

- **Console**: Color-coded INFO level logs with timestamps
- **Files**: Daily rotating DEBUG logs in `logs/ambient_YYYY-MM-DD.log`
- **Process Logs**: Individual `{ISSUE_KEY}_{TIMESTAMP}_stdout/stderr.log` files
- **Log Rotation**: 7-day retention with 10MB file size limit

## Dependencies

- **conduit-connect**: Jira API integration
- **loguru**: Advanced logging with rotation
- **fire**: Google's CLI framework
- **pydantic-settings**: Type-safe configuration management
- **aiohttp**: Async HTTP client
- **pyyaml**: Configuration parsing (installed but not yet used)
- **python-dotenv**: Environment variable management
- **assemblyai[extras]**: Real-time audio transcription