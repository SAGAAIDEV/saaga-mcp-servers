"""Process management for Claude execution"""

import asyncio
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from loguru import logger

from .config import DO_MD_PATH, MCP_JSON


class ProcessManager:
    """Manages Claude subprocess execution and lifecycle"""
    
    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.running_processes: Dict[str, subprocess.Popen] = {}
    
    async def execute_claude(self, issue_key: str, issue_data: dict) -> Optional[subprocess.Popen]:
        """Execute Claude code for a specific issue"""
        # Get issue details
        issue_summary = issue_data.get("summary", "No summary")
        description = issue_data.get("description", "No description")
        status = issue_data.get("status", "Unknown")
        assignee_name = issue_data.get("assignee", "Unassigned")
        created = issue_data.get("created", "Unknown")
        
        # Create log files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stdout_file = self.log_dir / f"{issue_key}_{timestamp}_stdout.log"
        stderr_file = self.log_dir / f"{issue_key}_{timestamp}_stderr.log"
        
        # Read do.md instructions
        if not DO_MD_PATH.exists():
            logger.error(f"do.md file not found at {DO_MD_PATH}")
            return None
        
        try:
            with open(DO_MD_PATH, "r") as f:
                do_instructions = f.read()
        except Exception as e:
            logger.error(f"Failed to read do.md: {e}")
            return None
        
        # Format Jira content
        jira_content = f"""Jira Ticket: {issue_key}
Summary: {issue_summary}
Status: {status}
Assignee: {assignee_name}
Created: {created}

Description:
{description}"""
        
        # Construct Claude prompt
        prompt = f"{do_instructions}\n\n## Execute Task: {issue_key}\n\n{jira_content}"
        
        # Build Claude command
        cmd = [
            "claude",
            f"'{prompt}'",
            "--disallowedTools",
            "Write",
            "--mcp-config",
            MCP_JSON,
            "--dangerously-skip-permissions",
        ]
        
        logger.info(f"Executing Claude command for {issue_key}")
        
        try:
            # Open log files
            stdout_fd = open(stdout_file, "w")
            stderr_fd = open(stderr_file, "w")
            
            # Start subprocess
            process = subprocess.Popen(
                cmd,
                stdout=stdout_fd,
                stderr=stderr_fd,
                text=True,
            )
            
            # Store process reference
            self.running_processes[issue_key] = process
            
            # Start monitoring task
            asyncio.create_task(
                self._monitor_process(issue_key, process, stdout_fd, stderr_fd)
            )
            
            logger.info(f"Started Claude process for {issue_key} (PID: {process.pid})")
            logger.info(f"Stdout log: {stdout_file}")
            logger.info(f"Stderr log: {stderr_file}")
            
            return process
            
        except Exception as e:
            logger.error(f"Error starting Claude for issue {issue_key}: {e}")
            if 'stdout_fd' in locals():
                stdout_fd.close()
            if 'stderr_fd' in locals():
                stderr_fd.close()
            return None
    
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
    
    def terminate_process(self, issue_key: str, force: bool = False) -> bool:
        """Terminate a running process for the given issue key"""
        process = self.running_processes.get(issue_key)
        
        if process is None:
            logger.warning(f"Process for {issue_key} not found in tracking dict")
            if issue_key in self.running_processes:
                del self.running_processes[issue_key]
            return False
        
        try:
            # Check if process is still running
            if process.poll() is None:
                logger.info(f"Terminating process for {issue_key} (PID: {process.pid})")
                
                if force:
                    process.kill()
                else:
                    process.terminate()
                    # Give it a chance to terminate gracefully
                    try:
                        process.wait(timeout=5)
                        logger.info(f"Process for {issue_key} terminated successfully")
                    except subprocess.TimeoutExpired:
                        logger.warning(f"Force killing process for {issue_key}")
                        process.kill()
                        process.wait()
            else:
                logger.debug(f"Process for {issue_key} already terminated with code {process.returncode}")
            
            # Remove from tracking dict
            if issue_key in self.running_processes:
                del self.running_processes[issue_key]
            
            return True
            
        except Exception as e:
            logger.error(f"Error terminating process for {issue_key}: {e}")
            # Still try to remove from dict
            if issue_key in self.running_processes:
                del self.running_processes[issue_key]
            return False
    
    def terminate_all_processes(self):
        """Terminate all running processes"""
        if not self.running_processes:
            return
        
        logger.info(f"Terminating {len(self.running_processes)} running Claude processes...")
        
        for issue_key in list(self.running_processes.keys()):
            self.terminate_process(issue_key)
    
    def get_running_processes(self) -> Dict[str, subprocess.Popen]:
        """Get dictionary of currently running processes"""
        return self.running_processes