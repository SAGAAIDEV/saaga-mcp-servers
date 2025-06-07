from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import DEFAULT_CONFIG_PATH, CONFIG_FILE_HEADER, DEFAULT_DEEP_RESEARCH_CONFIG


class DeepResearchConfig(BaseModel):
    """Deep research configuration settings."""
    
    breadth: int = Field(
        default=DEFAULT_DEEP_RESEARCH_CONFIG["breadth"], 
        description="Number of research sources to explore"
    )
    depth: int = Field(
        default=DEFAULT_DEEP_RESEARCH_CONFIG["depth"], 
        description="Depth of research exploration"
    )
    concurrency: int = Field(
        default=DEFAULT_DEEP_RESEARCH_CONFIG["concurrency"], 
        description="Number of concurrent research tasks"
    )
    total_words: int = Field(
        default=DEFAULT_DEEP_RESEARCH_CONFIG["total_words"], 
        description="Target word count for reports"
    )


class Settings(BaseSettings):
    """Configuration settings for MCP Researcher."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Ignore extra fields in environment
        env_nested_delimiter="__",  # Allow nested env vars like DEEP_RESEARCH__BREADTH
    )

    # API Keys
    tavily_api_key: str
    anthropic_api_key: str
    openai_api_key: str
    
    # Research configuration
    deep_research: DeepResearchConfig = Field(default_factory=DeepResearchConfig)
    
    @classmethod
    def load_from_yaml(cls, config_path: Optional[Path] = None) -> "Settings":
        """Load settings from YAML file and environment variables."""
        if config_path is None:
            config_path = DEFAULT_CONFIG_PATH
        
        # Start with default values
        config_data = {}
        
        # Load from YAML if exists
        if config_path.exists():
            with open(config_path, "r") as f:
                yaml_data = yaml.safe_load(f) or {}
                config_data.update(yaml_data)
        
        # Create settings instance (env vars will override YAML)
        return cls(**config_data)
    
    @classmethod
    def init_config_file(cls, config_path: Optional[Path] = None) -> Path:
        """Initialize an empty YAML configuration file.
        
        Args:
            config_path: Path to the config file. Defaults to ~/mcp-researcher/config.yaml
            
        Returns:
            Path to the created config file
            
        Raises:
            FileExistsError: If the config file already exists
        """
        if config_path is None:
            config_path = DEFAULT_CONFIG_PATH
        
        # Check if file already exists
        if config_path.exists():
            raise FileExistsError(f"Configuration file already exists at: {config_path}")
        
        # Create parent directory if it doesn't exist
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write YAML with comments
        with open(config_path, "w") as f:
            f.write(CONFIG_FILE_HEADER)
            yaml.dump({"deep_research": DEFAULT_DEEP_RESEARCH_CONFIG}, f, default_flow_style=False)
        
        return config_path
    
    @classmethod
    def reset_config_file(cls, config_path: Optional[Path] = None) -> Path:
        """Reset the configuration file to default values.
        
        This will delete the existing config file and create a new one with defaults.
        
        Args:
            config_path: Path to the config file. Defaults to ~/mcp-researcher/config.yaml
            
        Returns:
            Path to the reset config file
            
        Raises:
            FileNotFoundError: If the config file doesn't exist
        """
        if config_path is None:
            config_path = DEFAULT_CONFIG_PATH
        
        # Check if file exists
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found at: {config_path}")
        
        # Delete the existing file
        config_path.unlink()
        
        # Create a new default config file
        return cls.init_config_file(config_path)


# Load settings with YAML support
settings = Settings.load_from_yaml()