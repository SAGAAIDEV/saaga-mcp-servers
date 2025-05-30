from datetime import datetime, timedelta
from saaga_mcp_base.lib.logging import logger


async def get_date(days_offset: int = 0) -> str:
    """
    Returns a date string in YYYY-MM-DD format. days_offset 0 fives today.

    Args:
        days_offset: Number of days to offset from current date (default: 0)

    Returns:
        String representation of date in YYYY-MM-DD format
    """

    logger.info(f"get_date called with days_offset: {days_offset}")
    date_to_return = (datetime.now() + timedelta(days=days_offset)).strftime("%Y-%m-%d")
    logger.info(f"get_date returning: {date_to_return}")
    return date_to_return


async def get_time() -> str:
    """
    Returns the current time of day as a string.

    Args:
        format_24h: If True, returns time in 24-hour format (HH:MM:SS).
                   If False, returns time in 12-hour format with AM/PM (HH:MM:SS AM/PM)

    Returns:
        String representation of current time
    """

    logger.info(f"get_time called with format_24h")

    time_to_return = datetime.now().strftime("%H:%M:%S")

    logger.info(f"get_time returning: {time_to_return}")
    return time_to_return
