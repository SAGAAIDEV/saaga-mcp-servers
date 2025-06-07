# Ambient Agent Configuration

The Ambient Agent uses Pydantic BaseSettings for configuration management. This allows configuration through environment variables, .env files, or direct instantiation.

## Configuration Options

### Polling Configuration
- `AMBIENT_POLL_INTERVAL_SECONDS` (int, default: 300): How often to check for new issues (seconds)
- `AMBIENT_MAX_ISSUES_PER_POLL` (int, default: 10): Maximum issues to process per poll (1-100)
- `AMBIENT_DRY_RUN` (bool, default: false): If true, don't actually process issues

### MCP Configuration
- `AMBIENT_BASE_MCP_CONFIG_PATH` (str, default: "config/mcp.json"): Path to MCP configuration file

### Operation Configuration
- `AMBIENT_MAX_RETRIES` (int, default: 3): Maximum retries for failed operations
- `AMBIENT_TIMEOUT_SECONDS` (int, optional): Timeout for individual operations (None for no timeout)
- `AMBIENT_JIRA_QUERY_TIMEOUT` (int, default: 30): Timeout for Jira API queries (seconds)

### Logging Configuration
- `AMBIENT_LOG_LEVEL` (str, default: "INFO"): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

## Configuration Methods

### 1. Environment Variables
Set environment variables with the `AMBIENT_` prefix:
```bash
export AMBIENT_POLL_INTERVAL_SECONDS=300
export AMBIENT_DRY_RUN=true
export AMBIENT_LOG_LEVEL=DEBUG
```

### 2. .env File
Create a `.env` file in the ambient directory:
```
AMBIENT_POLL_INTERVAL_SECONDS=300
AMBIENT_MAX_ISSUES_PER_POLL=10
AMBIENT_DRY_RUN=false
AMBIENT_LOG_LEVEL=INFO
```

### 3. Command Line Arguments
Override settings via command line arguments:
```bash
python -m ambient poll --poll-interval 60 --dry-run true --log-level DEBUG
```

### 4. Programmatic Configuration
```python
from ambient.config.settings import PollConfig

# Use defaults
config = PollConfig()

# Override specific values
config = PollConfig(
    poll_interval_seconds=60,
    dry_run=True,
    log_level="DEBUG"
)
```

## Configuration Validation

The Pydantic settings include automatic validation:
- `poll_interval_seconds` must be >= 1
- `max_issues_per_poll` must be between 1 and 100
- `log_level` must be a valid logging level
- `base_mcp_config_path` cannot be empty
- `timeout_seconds` and `jira_query_timeout` must be > 0 if specified

## Development vs Production

### Development Configuration
```
AMBIENT_POLL_INTERVAL_SECONDS=30
AMBIENT_MAX_ISSUES_PER_POLL=5
AMBIENT_DRY_RUN=true
AMBIENT_LOG_LEVEL=DEBUG
```

### Production Configuration
```
AMBIENT_POLL_INTERVAL_SECONDS=600
AMBIENT_MAX_ISSUES_PER_POLL=20
AMBIENT_DRY_RUN=false
AMBIENT_LOG_LEVEL=INFO
AMBIENT_TIMEOUT_SECONDS=1200
```

## Advanced Features

### Configuration Properties
- `mcp_config_path`: Returns Path object for MCP config
- `get_effective_timeout()`: Returns timeout value for operations
- `is_development_mode()`: Returns true if dry_run and debug logging are enabled

### Environment Variable Prefix
All environment variables use the `AMBIENT_` prefix to avoid conflicts with other applications.

### Configuration Priority
1. Command line arguments (highest priority)
2. Environment variables
3. .env file
4. Default values (lowest priority) 