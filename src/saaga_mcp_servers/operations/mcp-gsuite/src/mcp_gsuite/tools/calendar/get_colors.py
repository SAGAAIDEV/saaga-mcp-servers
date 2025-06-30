import json
import asyncio
from mcp_gsuite.lib.accounts import format_docstring_with_user_id_arg
from ...lib import calendar
from loguru import logger


@format_docstring_with_user_id_arg
async def get_calendar_colors(
    user_id: str,
) -> str:
    """
    Get the color definitions available in Google Calendar.
    
    This returns the color palette used by Google Calendar for both calendars and events.
    Each color has an ID, background color, and foreground color in hex format.

    Args:
        user_id: {user_id_arg}

    Returns:
        str: JSON string containing calendar and event color definitions.
    """
    logger.info(f"Getting calendar colors for user_id: {user_id}")
    try:
        calendar_service = calendar.CalendarService(user_id=user_id)
        logger.debug(
            f"CalendarService initialized for user_id: {user_id} for get_calendar_colors"
        )

        colors = await asyncio.to_thread(calendar_service.get_colors)

        logger.info(
            f"Successfully retrieved calendar colors for user_id: {user_id}"
        )
        return json.dumps(colors, indent=2)

    except Exception as e:
        logger.error(
            f"Error in get_calendar_colors for user_id: {user_id}. Error: {str(e)}",
            exc_info=True,
        )
        error_response = {
            "error": f"Failed to get calendar colors for {user_id}: {str(e)}",
            "user_id": user_id,
        }
        raise Exception(json.dumps(error_response, indent=2))