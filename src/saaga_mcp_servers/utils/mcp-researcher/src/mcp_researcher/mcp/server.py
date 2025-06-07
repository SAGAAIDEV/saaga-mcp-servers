"""MCP server for the researcher service."""

import sys

from mcp.server.fastmcp import FastMCP
from ..core.logging import logger
from ..core.config import settings
from .tools import register_tools


# Create the MCP server
mcp = FastMCP("MCP Researcher")


# Register all tools
register_tools(mcp)


def main() -> None:
    """Main entry point for the MCP server."""
    logger.info("Starting MCP Researcher server...")

    # Log API key status
    try:
        tavily_key: str = (
            settings.tavily_api_key[:4] + "..."
            if settings.tavily_api_key
            else "NOT SET"
        )
        openai_key: str = (
            settings.openai_api_key[:4] + "..."
            if hasattr(settings, "openai_api_key") and settings.openai_api_key
            else "NOT SET"
        )

        logger.info("API Keys Status:")
        logger.info(f"  Tavily API Key: {tavily_key}")
        logger.info(f"  OpenAI API Key: {openai_key}")

        logger.info("Research Configuration:")
        logger.info(f"  Deep Research Breadth: {settings.deep_research.breadth}")
        logger.info(f"  Deep Research Depth: {settings.deep_research.depth}")
        logger.info(
            f"  Deep Research Concurrency: {settings.deep_research.concurrency}"
        )
        logger.info(f"  Total Words: {settings.deep_research.total_words}")
    except Exception as e:
        logger.error(f"Failed to check API keys: {e}")

    # Run the MCP server
    mcp.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)
