#!/usr/bin/env python3
"""
Ambient Agent - Main Module
Continuously monitors Jira for new tasks and triggers Claude code execution
"""

import asyncio
import os
import signal
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Set, Optional, Dict

from loguru import logger

try:
    from conduit.platforms.jira import JiraClient
except ImportError:
    logger.error(
        "conduit-connect is not installed. Please run: pip install conduit-connect"
    )
    sys.exit(1)

# Configure loguru
logger.remove()  # Remove default handler
# Console logging with colors
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
)
# File logging with rotation
logger.add(
    "logs/ambient_{time:YYYY-MM-DD}.log",
    rotation="00:00",  # New file every day at midnight
    retention="7 days",  # Keep logs for 7 days
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
)

# Hard-coded configuration for MVP
JIRA_PROJECT = "AGENT"
POLL_INTERVAL = 10  # seconds
JQL_QUERY = f'project = {JIRA_PROJECT} AND status = "To Do"'
MCP_JSON = "/Users/andrew/saga/saaga-mcp-servers/src/saaga_mcp_servers/agents/ambient/.ambient_agent.mcp.json"


class AmbientAgent:
    """Main agent class that handles Jira monitoring and Claude execution"""

    def __init__(self):
        self.jira_client: Optional[JiraClient] = None
        self.processed_issues: Set[str] = set()
        self.running_processes: Dict[str, subprocess.Popen] = {}
        self.running = True
        self.log_dir = Path("logs")
        self._setup_log_directory()

    def _setup_log_directory(self):
        """Create log directory if it doesn't exist"""
        self.log_dir.mkdir(exist_ok=True)
        logger.info(f"Log directory: {self.log_dir.absolute()}")

    async def initialize(self):
        """Initialize the Jira client connection"""
        try:
            logger.info("Initializing Jira client via Conduit...")
            self.jira_client = JiraClient()
            self.jira_client.connect()
            logger.info("Successfully connected to Jira")
        except Exception as e:
            logger.error(f"Failed to initialize Jira client: {e}")
            raise

    async def fetch_jira_issues(self):
        """Fetch issues from Jira using JQL query"""
        try:
            logger.debug(f"Executing JQL query: {JQL_QUERY}")
            issues = self.jira_client.search(JQL_QUERY)
            logger.info(f"Found {len(issues)} issues in Jira")
            return issues
        except Exception as e:
            logger.error(f"Error fetching Jira issues: {e}")
            return []

    async def process_issue(self, issue):
        """Process a single Jira issue by triggering Claude code (non-blocking)"""
        issue_key = issue.get("key")
        # Get initial summary for logging, but we'll use the full issue details later
        initial_summary = issue.get("fields", {}).get("summary", "No summary")

        logger.info(f"Processing issue {issue_key}: {initial_summary}")

        # Create log files for this issue
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stdout_file = self.log_dir / f"{issue_key}_{timestamp}_stdout.log"
        stderr_file = self.log_dir / f"{issue_key}_{timestamp}_stderr.log"

        # Read the do.md file to get task instructions
        do_md_path = Path("/Users/andrew/saga/saaga-mcp-servers/.claude/commands/do.md")
        if not do_md_path.exists():
            logger.error(f"do.md file not found at {do_md_path}")
            return

        try:
            with open(do_md_path, "r") as f:
                do_instructions = f.read()
        except Exception as e:
            logger.error(f"Failed to read do.md: {e}")
            return

        # Get full Jira ticket content
        try:
            # Fetch the full issue details
            full_issue = self.jira_client.get(issue_key)

            # Extract all relevant fields from the full issue
            issue_summary = full_issue.get("fields", {}).get("summary", "No summary")
            description = full_issue.get("fields", {}).get(
                "description", "No description"
            )
            status = (
                full_issue.get("fields", {}).get("status", {}).get("name", "Unknown")
            )
            assignee = full_issue.get("fields", {}).get("assignee", {})
            assignee_name = (
                assignee.get("displayName", "Unassigned") if assignee else "Unassigned"
            )
            created = full_issue.get("fields", {}).get("created", "Unknown")

            # Format the Jira ticket content with both summary and description
            jira_content = f"""Jira Ticket: {issue_key}
Summary: {issue_summary}
Status: {status}
Assignee: {assignee_name}
Created: {created}

Description:
{description}"""

        except Exception as e:
            logger.error(f"Failed to fetch full issue details for {issue_key}: {e}")
            # Fallback to basic info from search results
            fallback_summary = issue.get("fields", {}).get("summary", "No summary")
            fallback_description = issue.get("fields", {}).get(
                "description", "No description"
            )
            jira_content = f"""Jira Ticket: {issue_key}
Summary: {fallback_summary}

Description:
{fallback_description}"""
            # Update variables for environment
            issue_summary = fallback_summary

        # Construct the command prompt that includes do.md content, task directive, and Jira content
        prompt = f"{do_instructions}\n\n## Execute Task: {issue_key}\n\n{jira_content}"

        # Build the Claude command with -p flag
        cmd = [
            "claude",
            f"'{prompt}'",
            "--disallowedTools",
            "Write",
            "--mcp-config",
            MCP_JSON,
            "--dangerously-skip-permissions",
        ]
        logger.info(f"Claude command: {' '.join(cmd)}")

        try:
            # Open log files
            stdout_fd = open(stdout_file, "w")
            stderr_fd = open(stderr_file, "w")

            # Run Claude code as non-blocking subprocess
            logger.info(f"Executing Claude command (non-blocking): {' '.join(cmd)}")
            logger.info(f"Stdout log: {stdout_file}")
            logger.info(f"Stderr log: {stderr_file}")

            process = subprocess.Popen(
                cmd,
                stdout=stdout_fd,
                stderr=stderr_fd,
                text=True,
            )

            # Store the process reference
            self.running_processes[issue_key] = process

            # Start monitoring task
            asyncio.create_task(
                self._monitor_process(issue_key, process, stdout_fd, stderr_fd)
            )

            logger.info(f"Started Claude process for {issue_key} (PID: {process.pid})")

        except Exception as e:
            logger.error(f"Error starting Claude for issue {issue_key}: {e}")
            if "stdout_fd" in locals():
                stdout_fd.close()
            if "stderr_fd" in locals():
                stderr_fd.close()

    async def _monitor_process(
        self, issue_key: str, process: subprocess.Popen, stdout_fd, stderr_fd
    ):
        """Monitor a running subprocess and clean up when done"""
        try:
            # Wait for process to complete
            return_code = await asyncio.get_event_loop().run_in_executor(
                None, process.wait
            )

            # Close file descriptors
            stdout_fd.close()
            stderr_fd.close()

            # Remove from running processes
            if issue_key in self.running_processes:
                del self.running_processes[issue_key]

            if return_code == 0:
                logger.success(
                    f"Claude process for {issue_key} completed successfully (PID: {process.pid})"
                )
            else:
                logger.error(
                    f"Claude process for {issue_key} failed with exit code {return_code} (PID: {process.pid})"
                )

        except Exception as e:
            logger.error(f"Error monitoring process for {issue_key}: {e}")
            stdout_fd.close()
            stderr_fd.close()

    async def check_running_tasks(self):
        """Check status of running tasks and terminate completed/failed/confused ones"""
        if not self.running_processes:
            return

        # Create a copy of keys to avoid modifying dict during iteration
        issue_keys = list(self.running_processes.keys())

        for issue_key in issue_keys:
            try:
                # Fetch current status from Jira
                issue = self.jira_client.get(issue_key)
                status = (
                    issue.get("fields", {}).get("status", {}).get("name", "").lower()
                )

                # Check if task is in a terminal state
                if status.lower() in ["done", "failed", "confused"]:
                    logger.info(f"Task {issue_key} is now in '{status}' status")

                    # Try to get the process
                    process = self.running_processes.get(issue_key)

                    if process is None:
                        # Process not found, just remove from dict
                        logger.warning(
                            f"Process for {issue_key} not found in tracking dict"
                        )
                        if issue_key in self.running_processes:
                            del self.running_processes[issue_key]
                    else:
                        # Process found, terminate it
                        try:
                            # Check if process is still running
                            if process.poll() is None:
                                logger.info(
                                    f"Terminating process for completed task {issue_key} (PID: {process.pid})"
                                )
                                process.terminate()

                                # Give it a chance to terminate gracefully
                                try:
                                    process.wait(timeout=5)
                                    logger.info(
                                        f"Process for {issue_key} terminated successfully"
                                    )
                                except subprocess.TimeoutExpired:
                                    logger.warning(
                                        f"Force killing process for {issue_key}"
                                    )
                                    process.kill()
                                    process.wait()  # Wait for it to actually die
                            else:
                                logger.debug(
                                    f"Process for {issue_key} already terminated with code {process.returncode}"
                                )

                            # Remove from tracking dict
                            del self.running_processes[issue_key]

                        except Exception as e:
                            logger.error(
                                f"Error terminating process for {issue_key}: {e}"
                            )
                            # Still try to remove from dict
                            if issue_key in self.running_processes:
                                del self.running_processes[issue_key]

            except Exception as e:
                logger.error(f"Error checking status for {issue_key}: {e}")

    @logger.catch
    async def run(self):
        """Main execution loop"""
        await self.initialize()

        logger.info(f"Starting Ambient Agent monitoring project '{JIRA_PROJECT}'")
        logger.info(f"Polling interval: {POLL_INTERVAL} seconds")
        logger.info("Press Ctrl+C to stop")

        while self.running:
            try:
                # Fetch current issues
                issues = await self.fetch_jira_issues()

                # Process new issues
                new_issues_count = 0
                for issue in issues:
                    issue_key = issue.get("key")
                    if issue_key and issue_key not in self.processed_issues:
                        await self.process_issue(issue)
                        self.processed_issues.add(issue_key)
                        new_issues_count += 1

                if new_issues_count > 0:
                    logger.info(f"Processed {new_issues_count} new issues")
                else:
                    logger.debug("No new issues found")

                # Check status of running processes and their Jira tasks
                await self.check_running_tasks()

                # Report on running processes
                if self.running_processes:
                    logger.info(
                        f"Currently running Claude processes: {len(self.running_processes)}"
                    )
                    for issue_key, process in self.running_processes.items():
                        logger.debug(f"  - {issue_key} (PID: {process.pid})")

                # Wait for next poll
                logger.debug(f"Sleeping for {POLL_INTERVAL} seconds...")
                await asyncio.sleep(POLL_INTERVAL)

            except asyncio.CancelledError:
                logger.info("Received cancellation signal")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                await asyncio.sleep(POLL_INTERVAL)

    def shutdown(self):
        """Graceful shutdown"""
        logger.info("Shutting down Ambient Agent...")
        self.running = False

        # Terminate all running processes
        if self.running_processes:
            logger.info(
                f"Terminating {len(self.running_processes)} running Claude processes..."
            )
            for issue_key, process in self.running_processes.items():
                try:
                    logger.info(
                        f"Terminating process for {issue_key} (PID: {process.pid})"
                    )
                    process.terminate()
                    # Give it a chance to terminate gracefully
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        logger.warning(f"Force killing process for {issue_key}")
                        process.kill()
                except Exception as e:
                    logger.error(f"Error terminating process for {issue_key}: {e}")


def handle_shutdown(signame):
    """Handle shutdown signals"""
    logger.info(f"Received {signame}")

    # Cancel all running tasks
    try:
        # Python 3.9+
        for task in asyncio.all_tasks():
            task.cancel()
    except AttributeError:
        # Python 3.7-3.8
        for task in asyncio.Task.all_tasks():
            task.cancel()


@logger.catch
def main():
    """Main entry point"""
    logger.info("Starting Ambient Agent...")
    agent = AmbientAgent()

    # Set up signal handlers
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda _s, _f: handle_shutdown(sig.name))

    # Run the agent
    try:
        asyncio.run(agent.run())
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except asyncio.CancelledError:
        pass
    finally:
        agent.shutdown()
        logger.info("Ambient Agent stopped")


if __name__ == "__main__":
    main()
