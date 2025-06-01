import time


async def wait(minutes: float) -> str:
    """
    Wait for the specified number of minutes.
    This is for having an agent wait to check some information.

    Args:
        minutes: Number of minutes to wait (can be a decimal for partial minutes)

    Returns:
        A message indicating how long the function waited
    """
    if minutes <= 0:
        return "No waiting needed - minutes must be positive"

    seconds = minutes * 60
    time.sleep(seconds)

    return f"Waited for {minutes} minutes ({seconds} seconds)"
