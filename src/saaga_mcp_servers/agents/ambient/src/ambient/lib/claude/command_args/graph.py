from langchain_anthropic import ChatAnthropic

from pathlib import Path

from .prompt import get_claude_command_generator_prompt_template
from ambient.config.settings import config
from .structured_output import ClaudeCommandConfig, IssueAnalysisInput


def get_claude_command_generator_chain():
    """
    Initialize and return the Claude command configuration generation chain.

    This chain takes an issue description and MCP documentation, then generates
    a structured configuration specifying which tools should be allowed/disallowed
    and which MCP servers are required.

    Returns:
        The Claude command configuration chain that can process issue descriptions.
    """
    prompt = get_claude_command_generator_prompt_template()
    model = ChatAnthropic(
        model="claude-sonnet-4-20250514", api_key=config.ANTHROPIC_API_KEY
    )
    chain = prompt | model.with_structured_output(ClaudeCommandConfig)

    return chain


def generate_claude_config(
    issue_description: str,
) -> ClaudeCommandConfig:
    """
    Analyze an issue description and generate Claude command configuration.

    Args:
        issue_description: Description of the issue or task to be solved

    Returns:
        ClaudeCommandConfig: Configuration with allowed/disallowed tools and required servers
    """
    # Read the MCP documentation
    docs_path = (
        Path(__file__).parent.parent.parent.parent
        / "config"
        / "MCP_Servers_and_Tools.md"
    )

    try:
        with open(docs_path, "r", encoding="utf-8") as f:
            mcp_documentation = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"MCP documentation not found at {docs_path}")

    # Create the input
    analysis_input = IssueAnalysisInput(
        issue_description=issue_description, mcp_documentation=mcp_documentation
    )

    # Get the chain and invoke it
    chain = get_claude_command_generator_chain()
    result = chain.invoke(
        {
            "issue_description": analysis_input.issue_description,
            "mcp_documentation": analysis_input.mcp_documentation,
        }
    )

    return result


def generate_claude_command(
    config: ClaudeCommandConfig, prompt_text: str, mcp_config_path: str = None
) -> list[str]:
    """
    Generate the actual Claude command list based on the configuration.

    Args:
        config: ClaudeCommandConfig with tool and server specifications
        prompt_text: The prompt text to pass to Claude
        mcp_config_path: Path to MCP configuration file (defaults to settings.mcp_json)

    Returns:
        List of command arguments for Claude
    """
    if mcp_config_path is None:
        mcp_config_path = settings.mcp_json

    cmd = ["claude", f"'{prompt_text}'"]

    # Add disallowed tools
    if config.disallowed_tools:
        cmd.extend(["--disallowedTools", ",".join(config.disallowed_tools)])

    # Add allowed tools if needed (Claude allows all by default)
    # This would require Claude to support --allowedTools flag
    # if config.allowed_tools:
    #     cmd.extend(["--allowedTools", ",".join(config.allowed_tools)])

    # Add MCP configuration
    cmd.extend(["--mcp-config", mcp_config_path, "--dangerously-skip-permissions"])

    return cmd
