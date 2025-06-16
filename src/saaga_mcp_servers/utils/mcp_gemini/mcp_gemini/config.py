"""Server configuration for MCP Gemini MCP server"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class ServerConfig:
    """Configuration for the MCP server"""
    name: str = "MCP Gemini"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")


def load_config() -> ServerConfig:
    """Load server configuration from environment or defaults"""
    return ServerConfig(
        name=os.getenv("MCP_SERVER_NAME", "MCP Gemini"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        gemini_api_key=os.getenv("GEMINI_API_KEY", "")
    )
