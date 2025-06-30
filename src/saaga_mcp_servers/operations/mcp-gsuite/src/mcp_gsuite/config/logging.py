"""Logging configuration for MCP GSuite"""
import os
from pathlib import Path
from loguru import logger
import sys

def setup_logging(log_to_file: bool = True):
    """Configure logging for the MCP server"""
    # Remove default handler
    logger.remove()
    
    # Always log to stdout with a simpler format for MCP compatibility
    logger.add(
        sys.stdout,
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    )
    
    # Log to file
    if log_to_file:
        # Get the project root directory (mcp-gsuite)
        # __file__ is in src/mcp_gsuite/config/logging.py
        # We need to go up 4 levels: config -> mcp_gsuite -> src -> mcp-gsuite
        project_root = Path(__file__).parent.parent.parent.parent
        log_dir = project_root / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / "mcp-gsuite.log"
        
        logger.add(
            log_file,
            rotation="10 MB",  # Rotate when file reaches 10MB
            retention="7 days",  # Keep logs for 7 days
            level="DEBUG",  # More verbose logging to file
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
            enqueue=True,  # Thread-safe logging
            backtrace=True,  # Include backtrace on errors
            diagnose=True   # Include variable values in traceback
        )
        
        # Also create a separate error log
        error_log_file = log_dir / "mcp-gsuite-errors.log"
        logger.add(
            error_log_file,
            rotation="10 MB",
            retention="30 days",  # Keep error logs longer
            level="ERROR",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
            enqueue=True,
            backtrace=True,
            diagnose=True
        )
        
        logger.info(f"Logging initialized - Main log: {log_file}, Error log: {error_log_file}")
    
    return logger