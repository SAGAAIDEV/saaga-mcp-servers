from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from pathlib import Path
import json


class ClaudeCommandConfig(BaseModel):
    """Configuration for generating a Claude command based on issue analysis."""

    allowed_tools: List[str] = Field(
        ...,
        description="List of tools that should be allowed for this issue. Include both MCP server tools (e.g., 'mcp__git__git_status') and Claude built-in tools (e.g., 'Read', 'Write', 'Bash').",
    )
    disallowed_tools: List[str] = Field(
        ...,
        description="List of tools that should be explicitly disallowed for this issue. These are tools that might be harmful or unnecessary for the task.",
    )
    required_mcp_servers: List[str] = Field(
        ...,
        description="List of MCP server names that are required for this issue (e.g., 'mcp-git', 'mcp-github', 'mcp-gsuite').",
    )
    reasoning: str = Field(
        ...,
        description="Brief explanation of why these specific tools and servers were chosen for this issue.",
    )


class IssueAnalysisInput(BaseModel):
    """Input model for analyzing an issue and determining required tools/servers."""

    issue_description: str = Field(
        ..., description="The description of the issue or task that needs to be solved"
    )
    mcp_documentation: str = Field(
        ..., description="The full MCP servers and tools documentation content"
    )
