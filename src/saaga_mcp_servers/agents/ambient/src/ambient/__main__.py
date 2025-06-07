#!/usr/bin/env python3
"""
Ambient Agent v2 - Jira Polling Main

A functional polling system that continuously checks for Jira issues
assigned to agent@saaga.dev and processes them through the Claude
command builder pipeline.
"""

import asyncio
import fire
from loguru import logger

from ambient.config import settings
from .lib.jira.client import JiraClient
from .lib.agent_runner import process_issues_async


class AmbientAgent:
    """Main Ambient Agent class with CLI commands"""

    def __init__(self):
        self._jira = JiraClient()
        # Configure loguru for console output
        logger.remove()  # Remove default handler
        logger.add(
            sink=lambda msg: print(msg, end=""),
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="INFO",
        )

    def poll(self):
        """Start polling for Jira issues assigned to agent@saaga.dev"""
        logger.info("Starting Ambient Agent polling...")
        asyncio.run(self._poll_loop())

    async def _poll_loop(self):
        """Main polling loop that checks for issues every minute"""
        logger.info("Poll loop started - checking for issues every 60 seconds")

        while True:
            try:
                logger.debug("Checking for new Jira issues...")
                await self._check_and_process_issues()

                logger.debug("Waiting 60 seconds before next check...")
                await asyncio.sleep(60)  # Wait 1 minute

            except KeyboardInterrupt:
                logger.info("Received interrupt signal, stopping polling...")
                break
            except Exception as e:
                logger.error(f"Error during polling: {e}")
                logger.info("Continuing polling after error...")
                await asyncio.sleep(60)  # Wait before retrying

    async def _check_and_process_issues(self):
        """Check for issues and process them asynchronously"""
        try:
            issues = self._jira.get_agent_assigned_issues()

            if not issues:
                logger.debug("No issues found assigned to agent@saaga.dev")
                return

            logger.info(f"Found {len(issues)} issues to process")

            for issue in issues:
                self._jira.transition_to_in_progress(issue.get("key"))

            # Process all issues concurrently
            await process_issues_async(issues)

        except Exception as e:
            logger.error(f"Error checking/processing issues: {e}")
            raise

    def check_once(self):
        """Check for issues once without polling"""
        logger.info("Running single check for issues...")
        asyncio.run(self._check_and_process_issues())
        logger.info("Single check completed")

    def status(self):
        """Check current status and configuration"""
        logger.info("=== Ambient Agent Status ===")
        logger.info(f"Jira client configured: {self._jira is not None}")

        try:
            issues = self._jira.get_agent_assigned_issues()
            logger.info(f"Current issues assigned to agent: {len(issues)}")

            if issues:
                for issue in issues:
                    issue_key = issue.get("key")
                    summary = issue.get("fields", {}).get("summary", "No summary")
                    logger.info(f"  - {issue_key}: {summary}")

        except Exception as e:
            logger.error(f"Error checking status: {e}")


def main():
    """Main entry point using Google Fire"""
    fire.Fire(AmbientAgent)


if __name__ == "__main__":
    main()
