# Vision Document: saaga-mcp-base

## Overview

`saaga-mcp-base` is a utility wrapper designed to extend the functionality of Model Context Protocol (MCP) servers.

## Key Features

The primary goals of `saaga-mcp-base` are to provide MCP tools with:

*   **Scheduling Capabilities:** Enabling the coordination and timing of tool execution.
    These scheduling capabilities are implemented as decorators that are applied to the Python functions *before* they are converted into MCP tools. This pre-decoration approach allows for modification of the function's signature and its docstring, which in turn influences how the MCP server perceives and presents the tool.
    Specifically, these decorators can extend the function or MCP tool arguments to accept a `datetime` for a specific execution time, or a `crontab` string to enable recurrent scheduling via Celery and the `celery-redbeat` extension. This allows tools to be effectively scheduled for one-time or periodic execution.
*   **Parallelization Capabilities:** Allowing multiple tools or instances of tools to run concurrently for improved efficiency.
*   **Logging Functionality:** Comprehensive logging for monitoring tool activity, performance, and errors to sqlite.
*   **Exception Handling:** Robust mechanisms to catch, manage, and report exceptions occurring within MCP tools to support development.
*   **Approval Database:** A system for managing and storing approvals related to tool operations or data access.


## Base Tools

To support the core functionalities and provide administrative capabilities, `saaga-mcp-base` will include the following base tools:

### 1. Service Management Tools
   - **Start Redis:** Initiates the Redis service, essential for Celery's message brokering and `celery-redbeat`'s schedule storage.
   - **Start Flower:** Launches the Flower monitoring tool for Celery, providing a web-based interface to observe tasks and workers.
   - **Start Celery Worker:** Starts a Celery worker process to execute scheduled and parallel tasks.

### 2. Celery Query Tools
   - **List Scheduled Tasks:** Provides a consolidated view of:
     - One-off tasks scheduled for a specific future execution time via MCP.
     - Periodic (recurring) tasks managed by Celery Redbeat, detailing their `crontab` schedules and next run times.
   - **Update Scheduled Task:** Allows modification of existing scheduled tasks. This could include changing the execution time for one-off tasks or adjusting the `crontab` schedule for periodic tasks.
   - **Delete Scheduled Task:** Enables the removal of a specific one-off or periodic task from the schedule.

### 3. Database Service Management Tools
   (Assuming a general database is used for the Approval Database or other persistent storage, distinct from Redis)
   /Users/andrew/saga/saaga-mcp-base/src/saaga_mcp_base/lib/scheduler/core/processes.py
   /Users/andrew/saga/saaga-mcp-base/src/saaga_mcp_base/lib/scheduler/tools/celery.py
   - **Start Database Service:** Initiates the primary database service.
   - **Stop Database Service:** Halts the primary database service.
   - **Ping Database Service:** Checks the connectivity and responsiveness of the primary database service.

## Deployment and Integration

`saaga-mcp-base` is designed to be compatible with standard MCP server deployment methods, including installation via Docker or `uvx` as part of an `mcp.json` configuration. This allows for flexible integration into existing MCP ecosystems.

Below are examples of how other MCP servers are configured using `uvx` and `docker` in an `mcp.json` file, illustrating similar deployment patterns that can be adopted for `saaga-mcp-base`:

Servers have their own config files that are determined by their client interfaces making credential management easier. See conduit for how it achieves this.

```json
{
    "mcp-servers" : {
        "conduit": {
            "command": "/Users/andrew/saga/mcp-servers/dev/conduit/.venv/bin/mcp-server-conduit"
        },
    }
}
```

## Target Audience

This utility is aimed at developers and administrators working with MCP servers who require enhanced control, observability, and resilience for their MCP tool integrations.
