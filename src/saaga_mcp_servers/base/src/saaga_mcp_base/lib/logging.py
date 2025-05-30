"""
Logger configuration for the QA package.

This module provides a simplified logger using PrettyJSONSink to write human-readable
JSON logs to qa.log.
"""

import sqlite3
import sys
import threading
from typing import List, Dict, Any, Callable, TypeVar, cast
import functools
from pathlib import Path

from loguru import logger

from ..config.env import settings

# Configure and remove default logger
logger.remove()

# Create thread-local storage for database connections
local = threading.local()

# Flag to track if stdout logging is enabled
stdout_enabled = False


def enable_stdout_logging(level="INFO"):
    """
    Enable logging to stdout for easier debugging.

    Args:
        level: Minimum log level to output (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    global stdout_enabled
    if not stdout_enabled:
        logger.add(sys.stdout, level=level)
        stdout_enabled = True
        logger.info(f"Stdout logging enabled at {level} level")


def get_connection(db_path: str = None):
    """Get or create a thread-local SQLite connection."""
    if db_path is None:
        db_path = settings.sqldb_path

    # Ensure the directory for the database exists using pathlib
    db_path_obj = Path(db_path)
    db_dir = db_path_obj.parent
    if db_dir:
        db_dir.mkdir(parents=True, exist_ok=True)

    if not hasattr(local, "conn") or local.conn is None:
        local.conn = sqlite3.connect(db_path)
        cursor = local.conn.cursor()
        # Create logs table if it doesn't exist
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool TEXT,
            prev_tool TEXT,
            is_continuous BOOLEAN,
            timestamp TEXT,
            level TEXT,
            message TEXT,
            function TEXT,
            file TEXT,
            line INTEGER
        )
        """
        )
        local.conn.commit()
    return local.conn


def setup_db_logging(
    db_path: str = None, enable_stdout: bool = False, stdout_level: str = "INFO"
):
    """Set up database logging with thread-safe connections."""
    if db_path is None:
        db_path = settings.sqldb_path
    # Initialize the main connection to create the table
    conn = get_connection(db_path)

    # Define a function that will process each log and insert it into the database
    def db_sink(message):
        # Get thread-local connection
        thread_conn = get_connection(db_path)
        cursor = thread_conn.cursor()

        record = message.record
        current_tool = record["extra"].get("tool", None)

        try:
            # Get the previous tool entry
            cursor.execute("SELECT tool FROM logs ORDER BY id DESC LIMIT 1")
            prev_row = cursor.fetchone()
            prev_tool = prev_row[0] if prev_row else None
            is_continuous = current_tool == prev_tool and current_tool is not None

            cursor.execute(
                "INSERT INTO logs (tool, prev_tool, is_continuous, timestamp, level, message, function, file, line) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    current_tool,
                    prev_tool,
                    is_continuous,
                    record["time"].isoformat(),
                    record["level"].name,
                    record["message"],
                    record["function"],
                    record["file"].path,
                    record["line"],
                ),
            )
            thread_conn.commit()
        except Exception as e:
            # Log to stderr if database logging fails
            import sys

            print(f"Error writing to log database: {str(e)}", file=sys.stderr)

    # Add the sink to logger
    logger.add(db_sink, level="INFO")

    # Optionally enable stdout logging
    if enable_stdout:
        enable_stdout_logging(stdout_level)

    return conn


async def read_logs(
    n: int = 15, db_path: str = None, level: str = "INFO", tool: str = None
) -> List[Dict]:
    """
    Read the last n log entries from the log database, grouped by contiguous tool blocks.

    Args:
        n: Number of log entries to read
        db_path: Path to the log database. Defaults to path from settings.
        level: Filter logs by level (INFO, WARNING, ERROR, etc.)
        tool: Filter logs by tool name

    Returns:
        List of log entries as dictionaries, grouped by contiguous tool blocks
    """
    if db_path is None:
        db_path = settings.sqldb_path
    try:
        # Create a new connection for this specific read operation
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Query for contiguous blocks of the same tool
        query = """
        WITH tool_blocks AS (
            SELECT *, 
                   row_number() OVER (ORDER BY id) - 
                   row_number() OVER (PARTITION BY tool ORDER BY id) AS block_id
            FROM logs
            WHERE tool IS NOT NULL
        )
        SELECT * FROM tool_blocks
        """
        params = []
        where_clauses = []

        if level:
            where_clauses.append("level = ?")
            params.append(level)

        if tool:
            where_clauses.append("tool = ?")
            params.append(tool)

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        query += " ORDER BY id DESC LIMIT ?"
        params.append(n)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        # Convert rows to dictionaries
        logs = [dict(row) for row in rows]

        conn.close()
        return logs
    except Exception as e:
        logger.error(f"Error reading logs: {str(e)}")
        return []


async def get_contiguous_tool_blocks(
    db_path: str = None, limit: int = 100
) -> List[Dict]:
    """
    Get blocks of contiguous logs from the same tool.

    Args:
        db_path: Path to the log database. Defaults to path from settings.
        limit: Maximum number of log entries to retrieve

    Returns:
        List of log blocks, where each block contains logs from the same tool
    """
    if db_path is None:
        db_path = settings.sqldb_path
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Query to identify and group contiguous tool blocks
        query = """
        WITH tool_segments AS (
            SELECT *,
                   tool != IFNULL(LAG(tool) OVER (ORDER BY id), '') AS new_segment
            FROM logs
            WHERE tool IS NOT NULL
            ORDER BY id DESC
            LIMIT ?
        ),
        segments AS (
            SELECT *,
                   SUM(new_segment) OVER (ORDER BY id) AS segment_id
            FROM tool_segments
        )
        SELECT segment_id, tool, COUNT(*) AS count, 
               MIN(id) AS start_id, MAX(id) AS end_id,
               MIN(timestamp) AS start_time, MAX(timestamp) AS end_time
        FROM segments
        GROUP BY segment_id, tool
        ORDER BY segment_id DESC
        """

        cursor.execute(query, (limit,))
        rows = cursor.fetchall()

        # Convert rows to dictionaries
        blocks = [dict(row) for row in rows]

        # For each block, get the actual log entries
        for block in blocks:
            query = """
            SELECT * FROM logs 
            WHERE id BETWEEN ? AND ?
            ORDER BY id
            """
            cursor.execute(query, (block["start_id"], block["end_id"]))
            block_logs = [dict(row) for row in cursor.fetchall()]
            block["logs"] = block_logs

        conn.close()
        return blocks
    except Exception as e:
        logger.error(f"Error getting contiguous tool blocks: {str(e)}")
        return []


setup_db_logging(settings.sqldb_path)
# Log startup message
logger.info("Logger initialized with Sqlite3 (thread-safe)")

T = TypeVar("T", bound=Callable[..., Any])


def tool_logger(func: T) -> T:
    """Decorator that binds the function name as a tool to the loguru logger.

    Args:
        func: The function to decorate

    Returns:
        Decorated function with logger binding
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Simply use the contextualize method for the duration of the function call
        with logger.contextualize(tool=func.__name__):
            return await func(*args, **kwargs)

    return cast(T, wrapper)
