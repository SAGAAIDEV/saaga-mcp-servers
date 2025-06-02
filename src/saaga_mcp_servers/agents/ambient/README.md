# Ambient Agent

A lightweight Python monitoring service that continuously observes Jira for new project tasks and automatically triggers Claude code execution.

## Overview

The Ambient Agent monitors a Jira project for new tasks in "To Do" status and automatically executes Claude code with the task information. It runs continuously until terminated with Ctrl+C.

## Features

- Continuous polling of Jira (every 60 seconds)
- Non-blocking Claude code execution for parallel processing
- File-based logging of stdout/stderr for each task
- Real-time monitoring of running processes
- Comprehensive logging of all operations
- Graceful shutdown on Ctrl+C with process cleanup
- Zero-configuration MVP (hard-coded for AGENT project)

## Installation

```bash
# Install using pip
pip install -e .

# Or install using uv
uv pip install -e .
```

## Configuration

Currently, the agent uses hard-coded configuration for the MVP:
- **Jira Project**: AGENT
- **Polling Interval**: 60 seconds
- **Task Status**: To Do
- **Claude Command**: `claude code --no-confirm do.md`

## Usage

1. Ensure Conduit is configured with your Jira credentials:
   ```bash
   conduit --init
   ```

2. Run the agent:
   ```bash
   ambient-agent
   ```

3. The agent will:
   - Connect to Jira via Conduit
   - Poll for new "To Do" tasks every minute
   - Execute Claude code for each new task
   - Log all operations to stdout

4. Stop the agent with Ctrl+C

## How It Works

1. **Jira Monitoring**: Uses Conduit library to query Jira with JQL
2. **Task Detection**: Tracks processed issues to avoid duplicates
3. **Non-blocking Execution**: Spawns Claude processes without blocking the main loop
4. **File Logging**: Writes stdout/stderr to timestamped log files in `logs/` directory
5. **Process Management**: Monitors running processes and cleans up on completion

## Logging

The agent uses Loguru for advanced logging capabilities:

### Console Logging
- Color-coded log levels (DEBUG, INFO, SUCCESS, WARNING, ERROR)
- Detailed context including file, function, and line number
- Real-time status updates for:
  - Jira connection status
  - Number of issues found
  - Claude command execution with PIDs
  - Running process count
  - Error conditions with stack traces

### File Logging
- **Agent Logs**: Daily rotating logs in `logs/ambient_YYYY-MM-DD.log`
  - Automatic rotation at midnight
  - 7-day retention policy
  - DEBUG level for detailed troubleshooting
  
- **Process Logs**: Individual logs for each Claude execution:
  - `logs/{ISSUE_KEY}_{TIMESTAMP}_stdout.log` - Standard output
  - `logs/{ISSUE_KEY}_{TIMESTAMP}_stderr.log` - Standard error
  - Preserved for debugging and audit purposes

## Development

```bash
# Clone the repository
git clone <repository-url>
cd src/saaga_mcp_servers/agents/ambient

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install in development mode
pip install -e .
```

## Future Enhancements

- YAML configuration file support
- Multiple project monitoring
- Configurable Claude commands
- Metrics and monitoring endpoints
- Docker containerization

## License

MIT License - see LICENSE file for details