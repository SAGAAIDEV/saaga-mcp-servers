"""
Jira Client for Ambient Agent

A client for interacting with Jira issues through the conduit MCP server.
"""

from loguru import logger
from typing import List, Dict, Any, Optional
from conduit.platforms.jira import JiraClient as ConduitJiraClient


class JiraClient:
    """
    A client for interacting with Jira issues.

    This client uses the conduit MCP server to communicate with Jira.
    """

    def __init__(self, site_alias: Optional[str] = None):
        """
        Initialize the Jira client.

        Args:
            site_alias: Optional site alias for Atlassian instance
        """
        self.jira_client = ConduitJiraClient(site_alias="default")
        self.jira_client.connect()
        logger.info(f"Initialized Jira client with site_alias: {site_alias}")

    def get_agent_assigned_issues(self, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Get issues assigned to agent@saaga.dev that are active.

        Args:
            max_results: Maximum number of issues to return

        Returns:
            List of issue dictionaries
        """
        jql = "assignee = 'agent@saaga.dev' AND status IN ('To Do', 'Open')"
        issues = self.jira_client.search(jql)
        return issues

    def transition_to_in_progress(self, issue_key: str) -> bool:
        """
        Transition a Jira issue to "In Progress" status.

        Args:
            issue_key: The Jira issue key (e.g., "PROJ-123")

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Transitioning issue {issue_key} to In Progress")

            # Use the conduit MCP function to update the issue status
            # This function will be available via the MCP protocol when the agent runs

            result = self.jira_client.transition_status(issue_key, status="In Progress")

            logger.info(f"Successfully transitioned issue {issue_key} to In Progress")
            return True

        except Exception as e:
            logger.error(
                f"Failed to transition issue {issue_key} to In Progress: {str(e)}"
            )
            return False
