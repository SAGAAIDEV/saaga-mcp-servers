from typing import List
import json
from pathlib import Path
import logging

from ambient.config.settings import config as settings
from .structured_output import ClaudeCommandConfig


def create_command_args(config: ClaudeCommandConfig, prompt: str) -> List[str]:
    """
    Create command arguments for the Claude CLI based on the configuration.
    Reads the MCP config file and filters it based on required_mcp_servers.

    Args:
        config: ClaudeCommandConfig instance containing the configuration
        prompt: The prompt to send to Claude

    Returns:
        List of command arguments as strings
    """
    cmd = ["claude", "-p", f"'{prompt}'"]

    # Add disallowed tools if any
    if config.disallowed_tools:
        cmd.extend(["--disallowedTools"] + config.disallowed_tools)

    # Add allowed tools if any (assuming there's an --allowedTools argument)
    if config.allowed_tools:
        cmd.extend(["--allowedTools"] + config.allowed_tools)

    # Read and filter MCP config
    mcp_config_path = "/Users/andrew/saga/saaga-mcp-servers/.mcp.json"
    with open(mcp_config_path, "r") as f:
        full_config = json.load(f)

    # Filter the config to only include required MCP servers
    filtered_config = {"mcpServers": {}}
    for server_name in config.required_mcp_servers:
        if server_name in full_config.get("mcpServers", {}):
            filtered_config["mcpServers"][server_name] = full_config["mcpServers"][
                server_name
            ]

    # Create config directory if it doesn't exist
    config_dir = settings.mcp_json_dir
    config_dir.mkdir(parents=True, exist_ok=True)

    # Save filtered config to JSON file
    config_file_path = config_dir / "filtered_mcp_config.json"
    with open(config_file_path, "w") as f:
        json.dump(filtered_config, f, indent=2)

    # Log the filtered config
    full_path = config_file_path.resolve()
    logging.info(f"Saved MCP config to {full_path}")
    logging.info(f"Filtered MCP config: {json.dumps(filtered_config, indent=2)}")

    # Add MCP config file path
    cmd.extend(["--mcp-config", str(full_path)])

    # Add dangerous skip permissions flag
    cmd.append("--dangerously-skip-permissions")

    return cmd
