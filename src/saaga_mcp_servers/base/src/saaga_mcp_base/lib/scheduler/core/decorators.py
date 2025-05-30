"""
Decorator system for scheduling MCP tools.

This module provides decorators for scheduling MCP tool functions to run at a specified time.
It includes the `scheduled_tool` decorator which adds an optional 'datetime' parameter to
any MCP tool function, allowing it to be scheduled for future execution using Celery.

The module also contains helper functions for updating function signatures and docstrings
to maintain proper documentation and type hints when adding parameters.
"""

import functools
import inspect
import sys
import os
import importlib
from datetime import datetime
from typing import Callable, Optional, Any, Union, Dict, get_type_hints
import asyncio
from .celery_app import app


def _update_docstring(func: Callable, param_name: str, param_doc: str) -> None:
    """
    Update a function's docstring to include documentation for a new parameter.

    Args:
        func: The function whose docstring should be updated
        param_name: The name of the parameter to document
        param_doc: The documentation string for the parameter
    """
    if func.__doc__:
        # If the function already has a docstring, append to it
        original_doc = func.__doc__.rstrip()
        param_full_doc = f"""

    Args:
        ...
        {param_name}: {param_doc}
        """

        # Check if the docstring already has an Args section
        if "Args:" in original_doc:
            # If it does, we need to be more careful about how we append
            lines = original_doc.split("\n")
            args_index = -1

            for i, line in enumerate(lines):
                if "Args:" in line:
                    args_index = i
                    break

            if args_index >= 0:
                # Insert our parameter in the Args section
                param_arg = f"""
        {param_name}: {param_doc}"""

                # Find where to insert (after the last arg)
                insert_index = args_index + 1
                while insert_index < len(lines) and (
                    lines[insert_index].strip() == ""
                    or lines[insert_index].startswith(" ")
                ):
                    insert_index += 1

                lines.insert(insert_index, param_arg)
                func.__doc__ = "\n".join(lines)
        else:
            # Just append our param doc
            func.__doc__ = original_doc + param_full_doc
    else:
        # If the function doesn't have a docstring, create one
        func.__doc__ = f"""
    Args:
        {param_name}: {param_doc}
    """


def _update_signature(
    func: Callable, param_name: str, param_annotation: type, default=None
) -> inspect.Signature:
    """
    Update a function's signature to include a new parameter.

    Args:
        func: The function whose signature should be updated
        param_name: The name of the parameter to add
        param_annotation: The type annotation for the parameter
        default: The default value for the parameter

    Returns:
        The updated signature
    """
    # Get the original signature
    sig = inspect.signature(func)

    # Only add if it doesn't already exist
    if param_name not in sig.parameters:
        # Get the original parameters
        params = list(sig.parameters.values())

        # Create a new parameter with default=None
        new_param = inspect.Parameter(
            name=param_name,
            kind=inspect.Parameter.KEYWORD_ONLY,
            default=default,
            annotation=param_annotation,
        )

        # Add the parameter
        params.append(new_param)

        # Create a new signature with the added parameter
        new_sig = sig.replace(parameters=params)
    else:
        # Use the original signature if parameter already exists
        new_sig = sig

    # Update the original function's signature
    func.__signature__ = new_sig

    # Update the original function's annotations
    if hasattr(func, "__annotations__"):
        func.__annotations__[param_name] = param_annotation

    return new_sig


def scheduled_tool(func: Callable) -> Callable:
    """
    Decorator that wraps an MCP tool function and adds scheduling capability.

    This decorator adds an optional 'datetime' parameter to the wrapped function.
    When this parameter is provided, the function execution is scheduled for that time
    using Celery's delay method. The datetime parameter should be a string in ISO format.

    Schedule Time Format:
    - Use ISO 8601 format: 'YYYY-MM-DDTHH:MM:SS'
      Example: '2023-12-31T23:59:59' for December 31, 2023 at 11:59:59 PM

    Args:
        func: The MCP tool function to wrap

    Returns:
        Callable: The wrapped function with scheduling capability and an added datetime parameter
    """
    # Get the current module path
    curr_module = sys.modules[__name__]
    module_path = curr_module.__name__

    # Create a task name for better clarity
    task_name = f"{module_path}.{func.__name__}"

    # Update the docstring with datetime parameter documentation
    datetime_doc = "Optional[str] - When provided, schedules the function to run\n                 at the specified time. Format: 'YYYY-MM-DDTHH:MM:SS'\n                 Example: '2023-12-31T23:59:59' for December 31, 2023 at 11:59:59 PM"
    _update_docstring(func, "datetime", datetime_doc)
    # Update the signature with the datetime parameter
    new_sig = _update_signature(func, "datetime", Optional[str], None)

    # Create a Celery task for the function
    @app.task(name=task_name)
    def celery_task(*args, **kwargs):
        """Celery task that executes the wrapped function."""
        print(f"Executing scheduled task: {task_name}")
        if inspect.iscoroutinefunction(func):
            # For coroutine functions, we need to run them in an event loop

            loop = asyncio.get_event_loop()
            return loop.run_until_complete(func(*args, **kwargs))
        else:
            return func(*args, **kwargs)

    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        """
        Wrapper function that adds scheduling capability to the original function.
        """
        # Extract datetime parameter if present
        schedule_time = kwargs.pop("datetime", None)

        if schedule_time:
            # Convert string to datetime
            try:
                schedule_time = datetime.fromisoformat(schedule_time)
            except ValueError:
                raise ValueError(
                    "datetime string must be in ISO format (YYYY-MM-DDTHH:MM:SS)"
                )

            # Calculate delay in seconds from now
            now = datetime.now()
            delay_seconds = max(0, (schedule_time - now).total_seconds())

            # Schedule the task with Celery
            result = celery_task.apply_async(
                args=args, kwargs=kwargs, countdown=delay_seconds
            )

            return {
                "status": "scheduled",
                "task_id": result.id,
                "scheduled_time": schedule_time.isoformat(),
            }
        else:
            # Execute the function immediately
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

    # Copy the updated signature to the wrapper as well
    wrapper.__signature__ = new_sig

    # Store the task reference on the wrapped function
    wrapper.celery_task = celery_task

    return wrapper
