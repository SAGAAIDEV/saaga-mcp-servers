"""Configuration file loader for Ambient Agent"""

import json
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple

from loguru import logger

from .config.settings import settings


class ConfigLoader:
    """Loads command configuration files from the config directory"""

    def __init__(self):
        """
        Initialize the config loader using settings configuration
        """
        self.config_dir = settings.config_dir
        # self.command_md_file = self.config_dir / "command.md"
        # self.mcp_command_json_file = self.config_dir / ".mcp.command.json"

    def load_command_config(self, command: str) -> Tuple[Optional[str], Optional[Dict]]:
        """
        Load command.md and .mcp.command.json files for a specific command

        Args:
            command: The command name to load configuration for

        Returns:
            Tuple of (command_md_content, mcp_command_json_content)

        Raises:
            SystemExit: If required files don't exist
        """
        command_md_file = self.config_dir / f"{command}.md"
        mcp_command_json_file = self.config_dir / f".mcp.{command}.json"

        command_md_content = self._load_command_md(command_md_file)
        mcp_command_json_content = self._load_mcp_command_json(mcp_command_json_file)

        return command_md_content, mcp_command_json_content

    def _load_command_md(self, command_md_file: Path) -> Optional[str]:
        """
        Load the command.md file

        Args:
            command_md_file: Path to the command markdown file

        Returns:
            Content of command.md file or None if not found

        Raises:
            SystemExit: If file doesn't exist
        """
        if not command_md_file.exists():
            logger.error(f"Required file '{command_md_file}' not found")
            sys.exit(1)

        try:
            with open(command_md_file, "r", encoding="utf-8") as f:
                content = f.read()
                logger.info(f"Successfully loaded command.md from {command_md_file}")
                return content
        except Exception as e:
            logger.error(f"Failed to read command.md: {e}")
            sys.exit(1)

    def _load_mcp_command_json(self, mcp_command_json_file: Path) -> Optional[Dict]:
        """
        Load the .mcp.command.json file

        Args:
            mcp_command_json_file: Path to the MCP command JSON file

        Returns:
            Parsed JSON content or None if not found

        Raises:
            SystemExit: If file doesn't exist
        """
        if not mcp_command_json_file.exists():
            logger.error(f"Required file '{mcp_command_json_file}' not found")
            sys.exit(1)
        return mcp_command_json_file

        try:
            with open(mcp_command_json_file, "r", encoding="utf-8") as f:
                content = json.load(f)
                logger.info(
                    f"Successfully loaded .mcp.command.json from {mcp_command_json_file}"
                )
                return content
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in .mcp.command.json: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Failed to read .mcp.command.json: {e}")
            sys.exit(1)

    def validate_config(self) -> bool:
        """
        Validate that all required configuration files exist

        Returns:
            True if all files exist, False otherwise
        """
        missing_files = []

        if not self.command_md_file.exists():
            missing_files.append(str(self.command_md_file))

        if not self.mcp_command_json_file.exists():
            missing_files.append(str(self.mcp_command_json_file))

        if missing_files:
            logger.error(
                f"Missing required configuration files: {', '.join(missing_files)}"
            )
            return False

        logger.info("All required configuration files found")
        return True
