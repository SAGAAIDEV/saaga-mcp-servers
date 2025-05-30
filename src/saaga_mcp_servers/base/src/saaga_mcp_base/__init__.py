from .lib.datetime.tools.datetime import get_date, get_time
from .lib.datetime.tools.wiat import wait
from .base.base_mcp import create_mcp


from .base.base_mcp import create_mcp
from .lib.logging import read_logs, logger
from .lib.scheduler.tools.celery import (
    start_scheduler_services,
    stop_scheduler_services,
)


__all__ = ["create_mcp", "logger"]


def hello() -> str:
    return "Hello from saaga-mcp-base!"


def run_server():
    logger.info("Base server is running.")
    print("Base Server is running")
    mcp = create_mcp(
        "base",
        tools=[
            read_logs,
            start_scheduler_services,
            stop_scheduler_services,
            get_time,
            wait,
        ],
        parallel_tools=[get_date],
    )
    mcp.run(transport="stdio")


def main():
    print("Main")
