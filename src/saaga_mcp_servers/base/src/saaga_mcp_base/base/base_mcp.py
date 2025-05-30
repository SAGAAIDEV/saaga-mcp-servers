from mcp.server.fastmcp import FastMCP
from typing import Callable, List

from ..lib.exceptions import exception_handler
from ..lib.logging import logger, tool_logger
from ..lib.parallelize import parallelize


def create_mcp(
    name: str, tools: List[Callable], parallel_tools: List[Callable] = None
) -> FastMCP:
    """Creates and configures a FastMCP instance with specified tools and extended functionality.

    This function serves as a central extension point for all MCP functionality. It applies
    global decorators (like logging) to all tool functions before registering them with the
    MCP server. This pattern allows for consistent application of cross-cutting concerns
    across all MCP tools.

    Applications of this extension pattern include:
        - Logging tool execution to SQL databases (currently implemented)
        - Adding exception handling and error reporting
        - Implementing scheduling or rate limiting
        - Adding authentication or authorization checks
        - Performance monitoring and metrics collection

    To add additional global functionality, create a new decorator and apply it in this function.

    Args:
        name: The name for the FastMCP instance.
        fns: A list of functions to be registered as tools with the MCP instance.
        parallel_fns: A list of functions to be registered as parallelized tools.

    Returns:
        A configured FastMCP instance with extended functionality.
    """
    mcp = FastMCP(name)

    # Register regular tools
    for fn in tools:
        decorated_fn = exception_handler(fn)
        decorated_fn = tool_logger(decorated_fn)
        # TODO: Extend scheudler and parallizer decorators, these should be passed in
        # in different lists, like schedulable, and parallelizable

        mcp.tool()(decorated_fn)

    if parallel_tools:
        for fn in parallel_tools:
            decorated_fn = exception_handler(fn)
            decorated_fn = tool_logger(decorated_fn)
            parallelized_fn = parallelize(decorated_fn)
            mcp.tool()(parallelized_fn)

    return mcp
