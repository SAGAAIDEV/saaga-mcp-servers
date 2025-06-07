import subprocess
import asyncio
from datetime import datetime
from ambient.config import settings
from pydantic import BaseModel, ConfigDict
from typing import TextIO, Optional, Union
from pathlib import Path
import io
from loguru import logger


class ClaudeProcess(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    issue_key: str
    process: Optional[subprocess.Popen] = None
    stdout_fd: Union[TextIO, io.TextIOWrapper]
    stderr_fd: Union[TextIO, io.TextIOWrapper]

    @classmethod
    def create(cls, issue_key: str):
        # Create log files for this issue
        log_dir: Path = Path("logs")
        log_dir.mkdir(exist_ok=True)  # Ensure log directory exists
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stdout_file = log_dir / f"{issue_key}_{timestamp}_stdout.log"
        stderr_file = log_dir / f"{issue_key}_{timestamp}_stderr.log"
        return cls(
            issue_key=issue_key,
            stdout_fd=open(stdout_file, "w"),
            stderr_fd=open(stderr_file, "w"),
        )

    def run(self, cmd):
        logger.info(
            f"Running command for issue {self.issue_key}\n\n: {' '.join(cmd)}\n\n"
        )
        self.process = subprocess.Popen(
            cmd,
            stdout=self.stdout_fd,
            stderr=self.stderr_fd,
            text=True,
        )

    def close_files(self):
        """Close file descriptors to free resources"""
        if hasattr(self.stdout_fd, "close"):
            self.stdout_fd.close()
        if hasattr(self.stderr_fd, "close"):
            self.stderr_fd.close()
