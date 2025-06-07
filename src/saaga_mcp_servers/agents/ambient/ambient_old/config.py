"""Configuration settings for Ambient Agent"""

from pathlib import Path

# Jira Configuration
JIRA_PROJECT = "AGENT"
POLL_INTERVAL = 60  # seconds
JQL_QUERY = f'project = {JIRA_PROJECT} AND status = "To Do"'

# Claude Configuration
MCP_JSON = "/Users/andrew/saga/saaga-mcp-servers/.mcp.json"
DO_MD_PATH = Path("/Users/andrew/saga/saaga-mcp-servers/.claude/commands/do.md")

# Logging Configuration
LOG_DIR = Path("logs")
LOG_RETENTION_DAYS = 7
LOG_ROTATION_TIME = "00:00"  # Midnight