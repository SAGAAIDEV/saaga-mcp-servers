from loguru import logger
from mcp_gsuite.config.logging import setup_logging

# Initialize logging
setup_logging()

from mcp_gsuite.tools.gmail.query_emails import query_gmail_emails
from mcp_gsuite.tools.gmail.create_reply import create_reply
from mcp_gsuite.tools.gmail.get_email_by_id import (
    get_email_by_id,
)
from mcp_gsuite.tools.gmail.create_draft import create_draft
from mcp_gsuite.tools.gmail.get_attachment import get_attachment
from mcp_gsuite.tools.gmail.send_draft import send_draft
from mcp_gsuite.tools.gmail.create_label import create_label
from mcp_gsuite.tools.gmail.set_email_labels import set_email_labels
from mcp_gsuite.tools.gmail.update_draft import update_draft
from mcp_gsuite.tools.gmail.get_gmail_logs import get_gmail_logs

from mcp_gsuite.tools.calendar.list_calendars import list_calendars
from mcp_gsuite.tools.calendar.get_events import get_events
from mcp_gsuite.tools.calendar.create_event import create_event
from mcp_gsuite.tools.calendar.delete_event import delete_event
from mcp_gsuite.tools.calendar.update_event import update_event
from mcp_gsuite.tools.calendar.get_colors import get_calendar_colors

from mcp_gsuite.tools.admin.get_user_activity_report import get_user_activity_report
from mcp_gsuite.tools.auth import auth


# from saaga_mcp_base.base.base_mcp import create_mcp
from mcp.server.fastmcp import FastMCP


def main():
    logger.info("Starting MCP GSuite server...")
    logger.debug(f"Available tools count: {len(locals().get('all_tools', []))}")
    
    all_tools = [
        query_gmail_emails,
        create_reply,
        get_email_by_id,
        create_draft,
        get_attachment,
        send_draft,
        create_label,
        set_email_labels,
        update_draft,
        get_gmail_logs,
        list_calendars,
        get_events,
        create_event,
        delete_event,
        update_event,
        get_calendar_colors,
        get_user_activity_report,
        auth,
    ]

    logger.info(f"Registering {len(all_tools)} tools with MCP server")
    
    mcp = FastMCP("mcp_gsuite")
    for tool in all_tools:
        logger.debug(f"Adding tool: {tool.__name__}")
        mcp.add_tool(tool)

    # mcp = create_mcp("mcp_gsuite", tools=all_tools)
    logger.info("Starting MCP server on stdio transport")
    mcp.run(transport="stdio")


# Optionally expose other important items at package level
__all__ = ["main"]
