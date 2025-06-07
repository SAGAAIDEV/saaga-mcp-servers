#!/usr/bin/env python3
"""
Ambient Agent CLI using Google Fire
"""

import asyncio
import fire
import signal
import sys

from loguru import logger

from ambient_old.config.settings import settings
from ambient_old.config_loader import ConfigLoader
from ambient_old.main import AmbientAgent
from ambient_old.utils.transcriber import (
    run_realtime_transcription,
)


class AmbientCLI:
    """Command line interface for Ambient Agent"""

    def __init__(self):
        """Initialize the CLI"""
        logger.info("Initializing Ambient CLI")

        # Initialize configuration loader
        self.config_loader = ConfigLoader()

        # Configure loguru for CLI
        logger.remove()  # Remove default handler
        # Console logging with colors
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="INFO",
        )
        # File logging with rotation
        logger.add(
            f"{settings.log_dir}/ambient_{{time:YYYY-MM-DD}}.log",
            rotation=settings.log_rotation_time,
            retention=f"{settings.log_retention_days} days",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="DEBUG",
        )

    def run(self, command: str) -> None:
        """
        Execute a command

        Args:
            command: The command string to execute
        """
        print(f"Executing command: {command}")
        logger.info(f"Executing command: {command}")
        # Load the configuration for the specific command
        #get jiras
        #transition jira to in progress
        #build claude command

        command_md, mcp_command_json = self.config_loader.load_command_config(command)

        logger.info(f"Command MD loaded: {bool(command_md)}")
        logger.info(f"MCP Command JSON loaded: {bool(mcp_command_json)}")
        # TODO: Implement actual command execution logic using loaded configs
        transcribed_text = run_realtime_transcription()
        logger.info(f"Transcribed text: {transcribed_text}")

        cmd = [
            "claude",
            "-p",
            f"'{transcribed_text}'",
            "--disallowedTools",
            "Write",
            "--mcp-config",
            str(mcp_command_json),
            "--dangerously-skip-permissions",
        ]
        logger.info(f"Claude command: {' '.join(cmd)}")

    def run_2(self):
        #get jira
        #build claude command
            #build prompt
            #select tools
            #build mcp config
            #select disallowed tools
        #return result
        pass

    def watch(self) -> None:
        """
        Start watching Jira for new tasks and automatically execute them with Claude
        """
        print("Starting Ambient Agent in watch mode...")
        logger.info("Starting Ambient Agent in watch mode...")

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

    def status(self) -> None:
        """
        Show current agent status
        """
        print("Ambient Agent Status:")
        print(f"  Jira Project: {settings.jira_project}")
        print(f"  Poll Interval: {settings.poll_interval} seconds")
        print(f"  Log Directory: {settings.log_dir}")
        # TODO: Add more status information

    def config(self) -> None:
        """
        Show current configuration
        """
        print("Ambient Agent Configuration:")
        print(f"  JIRA_PROJECT: {settings.jira_project}")
        print(f"  POLL_INTERVAL: {settings.poll_interval}")
        print(f"  JQL_QUERY: {settings.jql_query}")
        print(f"  MCP_JSON: {settings.mcp_json}")
        print(f"  LOG_DIR: {settings.log_dir}")
        print(f"  LOG_RETENTION_DAYS: {settings.log_retention_days}")
        print(f"  CONFIG_DIR: {settings.config_dir}")


def main():
    """Main entry point for the CLI"""
    fire.Fire(AmbientCLI)


if __name__ == "__main__":
    main()
