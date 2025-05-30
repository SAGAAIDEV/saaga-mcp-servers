# Technical Requirements Document: saaga-mcp-base

**Version:** 1.0
**Date:** 2024-07-30
**Status:** Draft

## 1. Introduction
   1.1. Purpose
       *   This document defines the technical requirements for the `saaga-mcp-base` system.
   1.2. Scope
       *   Defines the technical specifications for the core `saaga-mcp-base` components, including technology stack considerations, operating system compatibility, configuration, data storage, security, and performance.
   1.3. Definitions, Acronyms, and Abbreviations
       *   **MCP:** Model Context Protocol
   1.5. Overview
       *   `saaga-mcp-base` is a foundational library that other developers can import when building their own MCP (Model Context Protocol) servers. It provides core functionalities and tools to extend the capabilities of MCP, enabling a standardized way to create and manage custom tools and integrations.

## 2. Functional Requirements
   *   **TR-FR-SCHED-001: Start All Services**
       *   Description: The scheduler should be able to start all dependent services.
       *   Source: User Request
       *   Inputs: Command to start services.
       *   Processing Logic: Initiates Redis, Celery worker, Celery Beat, and Flower services.
       *   Outputs: Confirmation of service startup or error messages.
       *   Error Handling: Log errors if a service fails to start.
       *   Dependencies: Redis, Celery, Celery Beat, Flower installations.
       *   Priority: High
   *   **TR-FR-SCHED-002: Ping Services**
       *   Description: The scheduler should be able to ping services to verify they are running.
       *   Source: User Request
       *   Inputs: Command to ping services.
       *   Processing Logic: Sends a ping request to Redis, Celery worker, Celery Beat, and Flower services.
       *   Outputs: Status of each service (running/not running).
       *   Error Handling: Log errors if a service does not respond to ping.
       *   Dependencies: Running services.
       *   Priority: High
   *   **TR-FR-SCHED-003: Stop All Services**
       *   Description: The scheduler should be able to stop all dependent services.
       *   Source: User Request
       *   Inputs: Command to stop services.
       *   Processing Logic: Terminates Redis, Celery worker, Celery Beat, and Flower services.
       *   Outputs: Confirmation of service shutdown or error messages.
       *   Error Handling: Log errors if a service fails to stop.
       *   Dependencies: Running services.
       *   Priority: High
   *   **TR-FR-SCHED-004: Schedule MCP Tool Execution**
       *   Description: Any MCP tool wrapped with the scheduler from the base MCP should support one-time and periodic scheduling, and parallel execution. (celery-redbeat looks like a good option)
       *   Source: User Request
       *   Inputs:
           *   Original MCP tool arguments.
           *   Specific date and time for one-time execution.
           *   Crontab arguments for periodic scheduling (via Celery Beat).
       *   Processing Logic:
           *   For one-time execution: Adds a task to Celery to run at the specified date/time.
           *   For periodic execution: Configures Celery Beat with the crontab schedule.
           *   Ensures that multiple tasks and schedules can run concurrently.
       *   Outputs: Confirmation of task scheduling; task execution results.
       *   Error Handling: Log errors related to scheduling (e.g., invalid crontab, past date for one-time). Log task execution errors.
       *   Dependencies: Celery, Celery Beat.
       *   Priority: High
   *   **TR-FR-SCHED-005: Restart All Services**
       *   Description: The scheduler should be able to restart all dependent services.
       *   Source: User Request
       *   Inputs: Command to restart services.
       *   Processing Logic: Effectively stops and then starts all dependent services (Redis, Celery worker, Celery Beat, and Flower).
       *   Outputs: Confirmation of service restart or error messages for each stage (stop/start).
       *   Error Handling: Log errors if a service fails to stop or fails to start during the restart sequence.
       *   Dependencies: Redis, Celery, Celery Beat, Flower installations.
       *   Priority: High
   *   **TR-FR-SCHED-006: Get Once-Scheduled Celery Tasks**
       *   Description: The system should provide a way to list all Celery tasks that are scheduled for a one-time execution.
       *   Source: User Request
       *   Inputs: Command to retrieve once-scheduled tasks.
       *   Processing Logic: Query Celery to identify and retrieve details of tasks scheduled with a specific execution time (not periodic).
       *   Outputs: A list of once-scheduled tasks, including their IDs, scheduled time, and task name/arguments.
       *   Error Handling: Log errors if the task list cannot be retrieved.
       *   Dependencies: Celery.
       *   Priority: Medium
   *   **TR-FR-SCHED-007: Get Periodic Celery Beat Tasks**
       *   Description: The system should provide a way to list all tasks that are scheduled for periodic execution via Celery Beat.
       *   Source: User Request
       *   Inputs: Command to retrieve periodic tasks.
       *   Processing Logic: Query Celery Beat (e.g., via `celery-redbeat` if used, or standard Celery Beat mechanisms) to retrieve the list of all configured periodic tasks and their schedules.
       *   Outputs: A list of periodic tasks, including their names, schedules (e.g., crontab expression), and task arguments.
       *   Error Handling: Log errors if the periodic task list cannot be retrieved.
       *   Dependencies: Celery, Celery Beat.
       *   Priority: Medium
   *   **TR-FR-SCHED-008: Update Scheduled Tasks**
       *   Description: The system should allow updating existing scheduled tasks, including their execution time (for one-time tasks) or schedule (for periodic tasks), and their arguments.
       *   Source: User Request
       *   Inputs: Task identifier (ID for one-time, name for periodic), new schedule/time, new arguments.
       *   Processing Logic:
           *   For one-time tasks: Modify the existing Celery task's scheduled time or parameters.
           *   For periodic tasks: Update the Celery Beat schedule entry (e.g., in `celery-redbeat`).
       *   Outputs: Confirmation of the update or error message.
       *   Error Handling: Log errors if the task cannot be found or if the update fails (e.g., invalid new schedule).
       *   Dependencies: Celery, Celery Beat.
       *   Priority: Medium
   *   **TR-FR-SCHED-009: Delete Scheduled Tasks**
       *   Description: The system should allow deleting scheduled tasks, both one-time and periodic.
       *   Source: User Request
       *   Inputs: Task identifier (ID for one-time, name for periodic).
       *   Processing Logic:
           *   For one-time tasks: Remove the task from Celery's schedule.
           *   For periodic tasks: Remove the task from Celery Beat's configuration (e.g., in `celery-redbeat`).
       *   Outputs: Confirmation of deletion or error message.
       *   Error Handling: Log errors if the task cannot be found or if deletion fails.
       *   Dependencies: Celery, Celery Beat.
       *   Priority: Medium
   *   **TR-FR-LOG-001: Logger Export and Usability**
       *   Description: The logging module (`src/saaga_mcp_base/lib/logging.py`) must be designed and packaged to be easily importable and usable by external Python packages (e.g., `mcp-gsuite`) that depend on `saaga-mcp-base`. It should provide a clear and stable API for external consumers to ensure logs are correctly routed. There is a problem with the logger not writing to the db when imported into
       other packages.
       *   Source: User Request (Logger import issue)
       *   Inputs: N/A (Design requirement for the library module).
       *   Processing Logic: External packages should be able to import the `logger` object and `tool_logger` decorator from `saaga_mcp_base.lib.logging`. The `setup_db_logging` function should ensure that if called multiple times (e.g., by base and then by an importing package), it doesn't cause errors and correctly configures the shared logging instance.
       *   Outputs: Successful logging to the configured SQLite database (specified by `settings.sqldb_path`) from both `saaga-mcp-base` internal components and external packages.
       *   Error Handling: Clear documentation and error handling for scenarios where the logger might be misconfigured by an external consumer.
       *   Dependencies: Python packaging, `saaga_mcp_base` library structure, `loguru` configuration.
       *   Priority: High
   *   **TR-FR-LOG-002: Read Tool Logs**
       *   Description: The system should provide an MCP tool that can read and retrieve logs from the SQLite database, with the ability to filter logs by specific tool names. This enables users to query logs for any tool that has been logged using the `tool_logger` decorator or direct logger usage.
       *   Source: User Request
       *   Inputs: 
           *   Tool name (optional) to filter logs for a specific tool.
           *   Date range (optional) to filter logs by time period.
           *   Log level (optional) to filter by severity (DEBUG, INFO, WARNING, ERROR, CRITICAL).
           *   Limit (optional) to restrict the number of returned log entries.
       *   Processing Logic: Query the SQLite database (specified by `settings.sqldb_path`) to retrieve log entries. Apply filters based on provided inputs: tool name matching, date range filtering, log level filtering. Return results in chronological order (most recent first by default).
       *   Outputs: A list of log entries matching the specified criteria, including timestamp, log level, tool name, message, and any additional context/metadata.
       *   Error Handling: Log errors if the database cannot be accessed, if invalid filter parameters are provided, or if the query fails. Return appropriate error messages to the user.
       *   Dependencies: SQLite database with logs table, `saaga_mcp_base.lib.logging` module, database access permissions.
       *   Priority: High
   *   **TR-FR-UTIL-001: Get Current Date and Time**
       *   Description: The system should provide an MCP tool that can retrieve the current date and/or time of day in various formats. This utility tool helps users get timestamp information for scheduling, logging, or general reference purposes.
       *   Source: User Request
       *   Inputs:
           *   Format type (optional): Specify output format such as 'date', 'time', 'datetime', 'iso', 'timestamp', or 'custom'.
           *   Timezone (optional): Specify timezone for the output (defaults to system local timezone).
           *   Custom format (optional): Custom datetime format string when format type is 'custom'.
       *   Processing Logic: 
           *   Retrieve current system date/time.
           *   Apply timezone conversion if specified.
           *   Format the output according to the requested format type:
               *   'date': YYYY-MM-DD
               *   'time': HH:MM:SS
               *   'datetime': YYYY-MM-DD HH:MM:SS
               *   'iso': ISO 8601 format (YYYY-MM-DDTHH:MM:SS±HHMM)
               *   'timestamp': Unix timestamp
               *   'custom': User-specified format string
       *   Outputs: Formatted date/time string according to the specified format and timezone.
       *   Error Handling: Log errors for invalid timezone specifications or custom format strings. Return appropriate error messages for malformed requests.
       *   Dependencies: Python `datetime` module, timezone handling libraries (e.g., `pytz` or `zoneinfo`).
       *   Priority: Medium
   *   **TR-FR-EXC-001: Exception Handling Decorator**
       *   Description: The system should provide a decorator that can be applied to MCP tools to handle exceptions and return detailed traceback information to the LLM context window. This decorator is particularly useful during development phases to help debug issues by providing comprehensive error information to the LLM for analysis and troubleshooting assistance. 
       *   This is complete and working. But should have a look over by a professional.
       *   Source: User Request
       *   Inputs:
           *   Decorated function: Any MCP tool function that may raise exceptions.
           *   Exception context: Runtime errors, validation failures, or unexpected conditions during tool execution.
       *   Processing Logic:
           *   Wrap the target function execution in a try-catch block.
           *   On exception occurrence:
               *   Capture the full traceback with stack trace information.
               *   Format the traceback in a readable manner for LLM consumption.
               *   Include exception type, error message, and relevant context.
               *   Return the formatted exception information as part of the tool's response.
           *   On successful execution: Pass through the normal function result without modification.
           *   Provide configuration options to enable/disable detailed traceback output (useful for development vs. production modes).
       *   Outputs: 
           *   On success: Original function return value.
           *   On exception: Structured error response containing exception type, message, and formatted traceback for LLM debugging assistance.
       *   Error Handling: The decorator itself should be robust and not raise additional exceptions. If the decorator encounters internal errors, it should fall back to basic error reporting.
       *   Dependencies: Python `traceback` module, exception handling utilities, configuration management for debug mode settings.
       *   Priority: Medium
   *   **TR-FR-CLI-001: Command Line Installation and Configuration**
       *   Description: The system should provide a comprehensive command-line interface for installation, configuration, and management of `saaga-mcp-base`. This should enable users to easily set up, configure, and manage the system without manual file editing.
       *   Source: User Request
       *   Inputs:
           *   Installation command: Initialize the system configuration and required directories.
           *   Configuration commands: List, add, update, or remove configuration settings.
           *   Service management commands: Start, stop, restart, and check status of services.
           *   Database management commands: Initialize databases, check connections, and manage database paths.
       *   Processing Logic:
           *   **Installation (`saaga-mcp-base --init`)**:
               *   Create necessary directories (e.g., `config/`, `db/`, logs).
               *   Generate default YAML configuration files (`config/database.yaml`, etc.).
               *   Set up initial database schemas.
               *   Provide guided setup for essential configuration (Redis connection, database paths).
           *   **Configuration Management**:
               *   `saaga-mcp-base config list`: Display current configuration settings from YAML files.
               *   `saaga-mcp-base config set <key> <value>`: Update configuration values.
               *   `saaga-mcp-base config get <key>`: Retrieve specific configuration values.
               *   `saaga-mcp-base config clean`: Reset configuration to defaults or remove all settings.
           *   **Service Management**:
               *   `saaga-mcp-base services start`: Start all required services (Redis, Celery, Flower).
               *   `saaga-mcp-base services stop`: Stop all services gracefully.
               *   `saaga-mcp-base services restart`: Restart all services.
               *   `saaga-mcp-base services status`: Check and display status of all services.
           *   **Database Management**:
               *   `saaga-mcp-base db init`: Initialize all configured databases with required schemas.
               *   `saaga-mcp-base db test`: Test database connections and report status.
       *   Outputs: 
           *   Success/failure messages for each operation.
           *   Formatted configuration listings.
           *   Service status reports.
           *   Database connection test results.
       *   Error Handling: 
           *   Clear error messages for invalid commands or parameters.
           *   Validation of configuration values before applying changes.
           *   Rollback mechanisms for failed configuration updates.
           *   Graceful handling of missing dependencies or services.
       *   Dependencies: 
           *   Command-line argument parsing (Google Fire library preferred).
           *   YAML configuration file management.
           *   Service management utilities.
           *   Database connection libraries.
       *   Priority: High

## 3. Non-Functional Requirements
   *   3.1. Performance
       *   **TR-NFR-PERF-001: General Responsiveness**
           *   Description: The system should be reasonably responsive for typical administrative and tool execution workloads.
           *   Metric: Not explicitly defined at this stage.
           *   Target Value: Reasonably responsive (Subjective, monitoring needed).
           *   Rationale: Based on initial project phase, focus on functionality over strict performance benchmarks. Performance will be monitored, and optimizations will be considered if bottlenecks are identified.
           *   Priority: Medium
       *   **(Add other performance requirements, metrics, and targets as they are defined.)**
   *   3.2. Scalability
       *   **(Define scalability requirements, e.g., handling increased load, number of concurrent tasks.)**
   *   3.3. Reliability
       *   **(Define reliability requirements, e.g., uptime, error tolerance, recovery from failures.)**
   *   3.4. Usability (Technical aspects, e.g., API consistency)
       *   **(Define technical usability aspects, e.g., consistency and ease of use of APIs for integrating new tools.)**
   *   3.5. Security
       *   **TR-NFR-SEC-001: Secret Management**
           *   Description: API keys, passwords, and other sensitive secrets must not be directly exposed to or passed through any Large Language Model (LLM) integrated with or using the Model Context Protocol tools. Secure methods (e.g., environment variables, dedicated secrets management systems accessed by the tools directly) must be employed.
           *   Metric: Absence of secrets in LLM inputs/outputs.
           *   Target Value: 100% compliance.
           *   Rationale: Prevent compromise of sensitive credentials.
           *   Priority: High
   *   **TR-NFR-MAINT-002: Logger Module Clarity for External Integration**
       *   Description: The logging module (`src/saaga_mcp_base/lib/logging.py`) must be clearly documented, detailing how external packages can import and utilize its functionalities (e.g., the `logger` instance, `tool_logger` decorator, and the initialization process). The design should minimize the need for complex setup by external consumers.
       *   Metric: Ease of integration documented by example or clear API guidelines.
       *   Target Value: A developer can integrate and use the logger in an external package by importing necessary components and relying on the `saaga-mcp-base`'s primary initialization of `setup_db_logging`.
       *   Rationale: Promotes reusability, consistency in logging across the ecosystem, and reduces integration challenges for developers building on `saaga-mcp-base`.
       *   Priority: High
   *   3.7. Compatibility
       *   **TR-NFR-COMP-001: Operating System Compatibility**
           *   Description: The application is expected to be universally compatible across operating systems that support Python 3.12 and the specified libraries. Standard Python virtual environments should ensure consistent behavior.
           *   Metric: Successful installation and execution on supported OS.
           *   Target Value: 100% compatibility with major operating systems supporting Python 3.12.
           *   Rationale: Ensure broad usability for developers and users.
           *   Priority: High
   *   **TR-DA-LOG-001: Consistent SQLite Logging from External Packages**
       *   Description: When the logger from `saaga_mcp_base.lib.logging` is utilized by external packages, all log entries (including those from these external packages) must be reliably written to the central SQLite database instance defined by `settings.sqldb_path`.
       *   Data Model/Schema: The existing `logs` table schema as defined in `src/saaga_mcp_base/lib/logging.py`.
       *   Persistence: File-based, managed by the `logging` module and SQLite.
       *   Rationale: Ensures a unified and centralized logging store for all operations within the ecosystem relying on `saaga-mcp-base`, facilitating comprehensive monitoring and debugging.
       *   Dependencies: Correct initialization and configuration of the `loguru` logger and its SQLite sink, consistent resolution of `settings.sqldb_path`.
       *   Priority: High

## 4. Interface Requirements
   *   4.1. User Interfaces (If applicable, technical aspects)
       *   **(Define technical aspects of user interfaces if any, e.g., requirements for APIs serving a frontend.)**
   *   4.2. System Interfaces (APIs, protocols)
       *   **TR-IF-MCP-001: Model Context Protocol (MCP) Interface**
           *   Description: The primary interface for interacting with the `saaga-mcp-base` system is the standard Model Context Protocol (MCP) interface defined within `__main__.py`. It supports two operational modes: direct command-line execution and a Server-Sent Events (SSE) server.
           *   Data Format: Standard Python dictionaries / JSON for requests and responses.
           *   Protocol:
               *   Command Line: Standard command-line arguments and I/O.
               *   SSE Server: HTTP with Server-Sent Events for streaming responses.
           *   Authentication: (Specify authentication methods for accessing the MCP server/tools - **Needs detail**)
           *   Error Handling: Errors are handled by the `exception.py` module, returning a JSON error response that includes the traceback.



## 5. Data Requirements
   *   **TR-DA-STOR-001: Database Storage Location**
       *   Description: Database paths for `saaga-mcp-base` (e.g., for the approval system, `celery-redbeat` if not using Redis exclusively) should be configured via a YAML configuration file located at `config/database.yaml`. This file should define paths for all database instances used by the system.
       *   Data Model/Schema: YAML configuration with database path mappings.
       *   Persistence: File-based configuration with database paths defined in YAML. Redis persistence should be configured separately.
       *   Rationale: Provides centralized, version-controlled configuration of database locations while maintaining flexibility for different deployment environments.
       *   Priority: High
   *   **TR-DA-CONFIG-001: Configuration Storage**
       *   Description: Database configuration, including paths and connection parameters, should be defined in a YAML configuration file. Environment variables may still be used for sensitive information like passwords, but database paths and other non-sensitive configuration should be managed through the YAML config.
       *   Data Model/Schema: YAML configuration structure.
       *   Persistence: Version-controlled YAML configuration file with environment-specific overrides.
       *   Rationale: Provides clear, maintainable configuration management while maintaining security for sensitive data.
       *   Priority: High

## 6. Security Requirements
   *   **TR-SEC-REDIS-001: Redis Database Authentication**
       *   Description: The Redis database instance used by `saaga-mcp-base` (including for Celery and `celery-redbeat`) must be secured with a strong password.
       *   Threat/Vulnerability Addressed: Unauthorized access to task queue, scheduler data, and other potentially sensitive information stored in Redis.
       *   Control/Mitigation: Configure the Redis server to require password authentication through environment variables and ensure the `saaga-mcp-base` application is configured with the correct password.
       *   Verification Method: Attempt to connect to the Redis instance without a password; the connection should be rejected.


## 7. Assumptions and Constraints
   *   7.1. Assumptions
       *   **ASSUMPTION-TECH-001: Python Environment**
           *   Description: It is assumed that a compatible Python 3.11 environment with necessary libraries can be set up on the target operating systems using standard tools like `venv` or `conda`.
       *   **ASSUMPTION-TECH-002: Technology Stack Availability**
           *   Description: It is assumed that the specified core technologies (Celery, Redis, Flower, celery-redbeat, Loguru) are available and can be integrated. (Refer to docs/saaga-mcp-base/03_technology_stack.md for details).
       *   **(Add other assumptions, e.g., regarding external services, network access.)**
   *   7.2. Technical Constraints
       *   **CONSTRAINT-DEPLOY-001: Deployment Options**
           *   Description: The system must support deployment via `uvx` and Docker containers.
           *   Rationale: Provide flexible and standardized deployment methods for users.
           *   Priority: High
       *   **CONSTRAINT-CONFIG-001: Environment Variable Configuration**
           *   Description: Critical configuration parameters must be configurable via environment variables when running the server, supporting both `uvx` and Docker deployment methods.
           *   Priority: High


