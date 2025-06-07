"""Constants for MCP Researcher."""

from pathlib import Path

# Configuration file path
DEFAULT_CONFIG_PATH = Path.home() / "mcp-researcher" / "config.yaml"

# Configuration file header
CONFIG_FILE_HEADER = """# MCP Researcher Configuration
# API keys can be set here or via environment variables

# tavily_api_key: "your-tavily-api-key"
# anthropic_api_key: "your-anthropic-api-key"
# openai_api_key: "your-openai-api-key"

# Deep research settings
"""

# Default deep research configuration
DEFAULT_DEEP_RESEARCH_CONFIG = {
    "breadth": 4,
    "depth": 2,
    "concurrency": 4,
    "total_words": 2500
}