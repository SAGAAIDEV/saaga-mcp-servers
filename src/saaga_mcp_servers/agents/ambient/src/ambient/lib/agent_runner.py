"""
Agent Runner Module

Handles the processing of individual Jira issues through the Claude pipeline.
"""

import asyncio
from loguru import logger

from .claude.claude_process import ClaudeProcess
from .claude.prompt.procurement import get_procurement_prompt
from .claude.command_args.graph import generate_claude_config
from .claude.command_args.command_builder import create_command_args


async def run_agent_for_issue(issue):
    """
    Process a single Jira issue through the Claude pipeline.

    Args:
        jira_client: The Jira client instance
        issue: The Jira issue dictionary
    """
    try:
        issue_key = issue.get("key")
        logger.info(f"Processing issue: {issue_key}")

        # Transition issue to in progress

        # Get issue description
        description = issue.get("fields", {}).get("description", "No description")
        logger.debug(f"Issue description: {description[:100]}...")

        # Generate claude prompt
        prompt = get_procurement_prompt(issue_key)
        logger.debug(f"Generated prompt for {issue_key}")

        # Configure claude agent
        claude_command_config = generate_claude_config(description)
        logger.debug(f"Generated Claude config for {issue_key}")

        # Create command arguments
        cmd_args = create_command_args(
            claude_command_config,
            prompt=prompt,
        )
        logger.debug(f"Created command args for {issue_key}")

        # Run agent
        claude = ClaudeProcess.create(issue_key)
        logger.info(f"Starting Claude process for {issue_key}")

        # Kick off the Claude process without waiting for it to complete
        asyncio.get_event_loop().run_in_executor(None, claude.run, cmd_args)

        logger.info(f"Claude process launched for issue: {issue_key}")

    except Exception as e:
        logger.error(f"Error processing issue {issue_key}: {e}")
        raise


async def process_issues_async(issues):
    """
    Process multiple issues concurrently by kicking off Claude processes.

    Args:
        jira_client: The Jira client instance
        issues: List of Jira issues to process
    """
    if not issues:
        logger.info("No issues to process")
        return

    logger.info(f"Launching Claude processes for {len(issues)} issues")

    # Kick off all Claude processes without waiting
    for issue in issues:
        await run_agent_for_issue(issue)

    logger.info(f"All {len(issues)} Claude processes have been launched")
