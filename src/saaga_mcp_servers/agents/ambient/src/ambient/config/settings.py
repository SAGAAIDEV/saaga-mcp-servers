"""
Ambient Agent Configuration Settings

Pydantic-based settings for the Ambient Agent v2 polling system.
Settings can be configured via environment variables or .env files.
"""

from pathlib import Path
from typing import Optional
from pydantic import Field, validator
from pydantic_settings import SettingsConfigDict
from pydantic_settings import BaseSettings

print(
    Path(__file__).parent.parent.parent.parent / ".env",
)


class Settings(BaseSettings):
    """Configuration for the Jira polling system using Pydantic BaseSettings"""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    ASSEMBLYAI_API_KEY: str = Field(default="", description="AssemblyAI API key")
    ANTHROPIC_API_KEY: str = Field(default="", description="Anthropic API key")
    # Polling configuration
    poll_interval_seconds: int = Field(
        default=300,
        description="How often to check for new issues (seconds)",
        ge=1,  # Must be at least 1 second
    )

    max_issues_per_poll: int = Field(
        default=10,
        description="Maximum issues to process per poll",
        ge=1,
        le=100,  # Reasonable upper limit
    )

    base_mcp_config_path: str = Field(
        default="config/mcp.json", description="Path to MCP configuration file"
    )

    dry_run: bool = Field(
        default=False, description="If True, don't actually process issues"
    )

    # Optional advanced configuration
    max_retries: int = Field(
        default=3, description="Maximum retries for failed operations", ge=0
    )

    timeout_seconds: Optional[int] = Field(
        default=None,
        description="Timeout for individual operations (None for no timeout)",
        gt=0,
    )

    # Jira configuration
    jira_query_timeout: int = Field(
        default=30, description="Timeout for Jira API queries (seconds)", gt=0
    )

    # Logging configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    mcp_json_dir: Path = Field(
        default=Path(__file__).parent / "mcp_servers",
        description="Directory to save MCP JSON files",
    )
    prompt_dir: Path = Field(
        default=Path(__file__).parent / "prompts",
        description="Directory to save prompts",
    )

    @validator("log_level")
    def validate_log_level(cls, v):
        """Validate log level is a valid logging level"""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in valid_levels:
            raise ValueError(f"log_level must be one of: {', '.join(valid_levels)}")
        return v.upper()

    @validator("base_mcp_config_path")
    def validate_mcp_config_path(cls, v):
        """Validate MCP config path is not empty"""
        if not v or not v.strip():
            raise ValueError("base_mcp_config_path cannot be empty")
        return v.strip()

    @property
    def mcp_config_path(self) -> Path:
        """Get MCP config path as a Path object"""
        return Path(self.base_mcp_config_path)

    def get_effective_timeout(self) -> Optional[int]:
        """Get the effective timeout value for operations"""
        return self.timeout_seconds

    def is_development_mode(self) -> bool:
        """Check if running in development mode (dry_run with debug logging)"""
        return self.dry_run and self.log_level == "DEBUG"


# Create a default instance that can be imported
config = Settings()
