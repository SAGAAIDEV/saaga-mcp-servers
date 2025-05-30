# Scheduler Service

A task scheduling service using Celery, Redis, and Flower for distributed task processing.

## Directory Structure

```
scheduler/
├── __init__.py            # Package initialization
├── cli.py                 # Command-line entry point 
├── core/                  # Core components
│   ├── __init__.py
│   ├── celery_app.py      # Celery application configuration
│   └── redis_client.py    # Redis client for direct operations
├── tasks/                 # Task definitions
│   ├── __init__.py
│   └── base_tasks.py      # Core tasks
├── config/                # Configuration
│   ├── __init__.py
│   └── flower_config.py   # Flower monitoring configuration
├── utils/                 # Utility scripts
│   ├── __init__.py
│   ├── start.py           # Script to start components
│   └── send_hello_task.py # Example task sender
└── tests/                 # Tests
    └── __init__.py
```

## Getting Started

### Prerequisites

- Python 3.8+
- Redis server

### Installation

Install dependencies:

```bash
uv add celery redis flower
```

### Running the Services

Use the start script to run all components:

```bash
# Start all components (Redis, Celery worker, beat, and Flower)
python -m src.services.mcp.scheduler.start --all

# Or start specific components
python -m src.services.mcp.scheduler.start --redis --worker --beat --flower

# You can also specify ports
python -m src.services.mcp.scheduler.start --all --redis-port 6379 --flower-port 5555
```

This will start:
- Redis server (for message broker)
- Celery worker (for task execution)
- Celery beat (for periodic tasks)
- Flower (for monitoring)

### Running Tasks

Send a hello world task:

```bash
python -m src.services.mcp.scheduler.utils.send_hello_task --name "Your Name"
```

## Monitoring

Access the Flower monitoring UI at: http://localhost:5555

## Using Scheduled Tools with MCP

The scheduler provides a `scheduled_tool` decorator that can be used with MCP tools to make them schedulable.

### Decorating MCP Tools for Scheduling

The key is to apply the decorators in the correct order:

1. Apply the `@mcp.tool()` decorator first (closest to the function)
2. Apply the `@scheduled_tool` decorator second (above the MCP decorator)

### Example: Decorating an MCP Tool

Here's an example from `server.py` showing how to decorate an MCP tool:

```python
from mcp.server.fastmcp import FastMCP
from src.services.mcp.scheduler.core.decorators import scheduled_tool

# Initialize the FastMCP server
mcp = FastMCP("hello")

# For execution order: scheduled_tool runs first, then mcp.tool
# In Python, decorators are executed from bottom to top
@mcp.tool()
@scheduled_tool
async def greet(name: str) -> str:
    """Generate a greeting message for the given name.

    Args:
        name: The name to include in the greeting

    Returns:
        A greeting message with the provided name
    """
    return f"hello {name}"
```

Important notes:
- The `@scheduled_tool` decorator must be placed ABOVE the `@mcp.tool()` decorator
- Do not provide a description in the `@mcp.tool()` decorator to ensure the function's docstring is used
- The docstring should follow the standard format with Args and Returns sections

### Using Scheduled Tools with LLMs

When an LLM calls a tool decorated with `@scheduled_tool`, it can either:

1. Execute the tool immediately (default behavior)
2. Schedule the tool for future execution by providing a datetime parameter

#### Immediate Execution

```
Call the greet tool with name="World"
```

#### Scheduled Execution

```
Call the greet tool with name="World" and schedule it for tomorrow at 9 AM
```

The LLM will automatically add a `datetime` parameter to the tool call, which can be:
- An ISO 8601 formatted string (e.g., "2023-12-31T09:00:00")
- A natural language datetime that will be converted to ISO format

### Advanced Usage

#### Custom Task Names

By default, tasks are named based on their function name. You can customize this:

```python
@mcp.tool()
@scheduled_tool(task_name="custom_greeting_task")
async def greet(name: str) -> str:
    """Generate a greeting message."""
    return f"hello {name}"
```

#### Error Handling

Tasks that fail will be logged in Flower. You can implement custom error handling:

```python
@mcp.tool()
@scheduled_tool(max_retries=3, retry_backoff=True)
async def greet(name: str) -> str:
    """Generate a greeting message."""
    try:
        return f"hello {name}"
    except Exception as e:
        # Log error
        raise
```

## Development

### Adding New Tasks

1. Create a new task file in the `tasks/` directory
2. Import the Celery app: `from src.services.mcp.scheduler.core.celery_app import app`
3. Define your tasks using the `@app.task` decorator
4. Import your tasks in `tasks/__init__.py`

### Running Tests

```bash
pytest src/services/mcp/scheduler/tests/
```

## Troubleshooting

### Common Issues

1. **Tasks not executing**: Ensure Redis and Celery worker are running
2. **Scheduling errors**: Verify datetime format is correct (ISO 8601)
3. **Monitoring not available**: Check if Flower is running on the correct port

### Checking Service Status

```bash
# Check if Redis is running
redis-cli ping

# Check Celery worker status
celery -A src.services.mcp.scheduler.core.celery_app status

# Check if Flower is accessible
curl http://localhost:5555
```

## Configuration

Configuration is loaded from environment variables and `.env` files through the `src.config.env` module. 