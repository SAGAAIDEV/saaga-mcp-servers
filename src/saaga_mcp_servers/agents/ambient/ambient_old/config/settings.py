"""Pydantic settings for Ambient Agent configuration"""

from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Configuration settings for Ambient Agent"""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    ASSEMBLYAI_API_KEY: str = Field(default="", description="AssemblyAI API key")

    # Jira Configuration
    jira_project: str = "AGENT"
    poll_interval: int = 60  # seconds
    jql_query: Optional[str] = None  # Will be computed if not provided

    # Claude Configuration
    mcp_json: str = "/Users/andrew/saga/saaga-mcp-servers/.mcp.json"
    do_md: Path = Path(__file__).parent / "do.md"
    config_dir: Path = Path(__file__).parent

    # Logging Configuration
    log_dir: Path = Path("logs")
    log_retention_days: int = 1
    log_rotation_time: str = "00:00"  # Midnight

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set default JQL query if not provided
        if self.jql_query is None:
            self.jql_query = f'project = {self.jira_project} AND status = "To Do" AND assignee = "agent@saaga.dev"'


# Create a singleton instance
settings = Settings()
