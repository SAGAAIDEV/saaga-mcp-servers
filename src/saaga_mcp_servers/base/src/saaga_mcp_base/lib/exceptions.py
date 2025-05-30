"""
Exception handling for MCP tools.

This module provides exception handling decorators for MCP tools used by the SaagaLint server.
These decorators capture traceback information from exceptions and format it for chat history,
ensuring that errors are properly logged and presented to users.
"""

import functools

import traceback
from typing import Any, Callable, Dict, TypeVar, cast

from .logging import logger


T = TypeVar("T", bound=Callable[..., Any])


def exception_handler(func: T) -> T:
    """Decorator that catches and formats exceptions from MCP tool calls.

    This decorator wraps MCP tool functions to catch any exceptions they raise,
    logs them with full traceback information, and returns a standardized error
    dictionary that can be displayed in the chat history. It prevents exceptions
    from propagating up the call stack, ensuring the server remains stable.

    Args:
        func: The MCP tool function to decorate.

    Returns:
        The decorated function that handles exceptions.

    Example:
        ```python
        @exception_handler
        async def my_mcp_tool(arg1, arg2):
            # Tool implementation
            return result
        ```
    """

    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Wraps the decorated function with exception handling.

        Args:
            *args: Positional arguments to pass to the decorated function.
            **kwargs: Keyword arguments to pass to the decorated function.

        Returns:
            Either the original function result or an error dictionary containing
            exception details if an exception occurred.
        """
        try:
            logger.debug(
                f"Calling async function {func.__name__} with "
                f"args={args}, kwargs={kwargs}"
            )
            return await func(*args, **kwargs)
        except Exception as e:
            tb_str = traceback.format_exc()
            logger.exception(tb_str)
            # Include exception details in the return dictionary
            error_return = {
                "Status": "Exception",
                "Message": str(e),
                "ExceptionType": type(e).__name__,
                "Traceback": tb_str,
            }
            return error_return

    # The decorator now directly returns the wrapper
    return cast(T, wrapper)
