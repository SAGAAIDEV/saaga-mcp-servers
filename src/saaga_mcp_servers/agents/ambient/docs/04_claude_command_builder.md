# Claude Command Builder Feature

## Overview

The Claude Command Builder is a new feature that enhances the ambient agent's ability to execute Claude with optimal, task-specific MCP server configurations. Instead of using a static MCP configuration for all tasks, this feature dynamically creates minimal, focused configurations that include only the necessary MCP servers and tools required for each specific task.

## Problem Statement

Currently, the ambient agent uses a static MCP configuration (`MCP_JSON`) for all Claude executions, which:

- Loads unnecessary MCP servers that may not be relevant to the task
- Exposes all available tools, creating potential security and complexity issues
- Provides suboptimal performance due to loading unused resources
- Lacks flexibility for different types of tasks that may require different tool sets

## Solution: Dynamic Command Builder

The Claude Command Builder will be an intelligent object that:

1. **Analyzes Task Requirements**: Examines the Jira ticket content, type, and context to determine what MCP servers and tools are needed
2. **Creates Minimal MCP Config**: Generates a paired-down `mcp.json` containing only required servers
3. **Sets Targeted Tool Restrictions**: Configures `--disallowedTools` to enable only necessary tools
4. **Builds Optimized Commands**: Constructs Claude commands with optimal configurations

## Architecture

### Core Components

#### 1. `ClaudeCommandBuilder` Class

```python
class ClaudeCommandBuilder:
    """Builds optimized Claude commands with minimal MCP configurations"""
    
    def __init__(self, base_mcp_config_path: Path, temp_config_dir: Path):
        """
        Args:
            base_mcp_config_path: Path to the full MCP configuration file
            temp_config_dir: Directory for storing temporary minimal configs
        """
    
    def build_command(self, task_context: TaskContext) -> ClaudeCommand:
        """Build a Claude command optimized for the given task"""
    
    def analyze_task_requirements(self, task_context: TaskContext) -> TaskRequirements:
        """Analyze what MCP servers and tools are needed for the task"""
    
    def create_minimal_config(self, requirements: TaskRequirements) -> Path:
        """Create a minimal mcp.json with only required servers"""
    
    def determine_disallowed_tools(self, requirements: TaskRequirements) -> List[str]:
        """Determine which tools should be disabled for security/focus"""
```

#### 2. `TaskContext` Class

```python
@dataclass
class TaskContext:
    """Context information about the task to be executed"""
    
    issue_key: str
    issue_type: str
    summary: str
    description: str
    status: str
    assignee: str
    labels: List[str]
    custom_fields: Dict[str, Any]
    priority: str
    project_key: str
```

#### 3. `TaskRequirements` Class

```python
@dataclass
class TaskRequirements:
    """Requirements determined from task analysis"""
    
    required_mcp_servers: List[str]
    required_tools: List[str]
    disallowed_tools: List[str]
    additional_args: List[str]
    security_level: SecurityLevel
```

#### 4. `ClaudeCommand` Class

```python
@dataclass
class ClaudeCommand:
    """Represents a complete Claude command ready for execution"""
    
    cmd_args: List[str]
    mcp_config_path: Path
    working_directory: Path
    environment_vars: Dict[str, str]
    timeout: Optional[int]
```

### Task Analysis Engine

The builder will include an intelligent analysis engine that maps task characteristics to MCP server requirements:

#### Task Type Mapping

| Task Type | Required MCP Servers | Key Tools |
|-----------|---------------------|-----------|
| Code Review | `mcp-git`, `mcp-github` | `git_diff`, `file_read`, `github_create_pr_review` |
| Bug Investigation | `mcp-git`, `mcp-transcriber` | `git_log`, `file_search`, `transcribe_logs` |
| Documentation | `confluence-mcp` | `create_page`, `update_page`, `search_pages` |
| Data Analysis | `sqlite-mcp`, `gsuite-mcp` | `sql_query`, `read_sheets`, `create_charts` |
| Testing | `mcp-git`, `browserbase-mcp` | `git_status`, `run_tests`, `browser_navigate` |

#### Content Keywords Analysis

The system will analyze ticket content for keywords that indicate required tools:

- **Git/Version Control**: "commit", "branch", "merge", "repository" → `mcp-git`
- **Database**: "query", "SQL", "database", "table" → `sqlite-mcp`
- **Documentation**: "document", "wiki", "confluence", "README" → `confluence-mcp`
- **Communication**: "email", "slack", "notification" → `gsuite-mcp`, `slack-mcp`
- **Testing**: "test", "automation", "browser", "UI" → `browserbase-mcp`

### Security and Tool Filtering

#### Security Levels

```python
class SecurityLevel(Enum):
    MINIMAL = "minimal"      # Only read operations
    STANDARD = "standard"    # Read + safe write operations
    ELEVATED = "elevated"    # Full access (requires approval)
```

#### Default Tool Restrictions

- **Always Disallowed**: Tools that could cause system-wide changes
- **Conditionally Allowed**: Tools enabled only when specifically needed
- **Always Allowed**: Safe read-only tools

### Configuration Generation

#### Minimal MCP Config Structure

```json
{
  "mcpServers": {
    "required-server-1": {
      "command": "path/to/server",
      "args": ["--config", "path"],
      "env": {
        "VAR": "value"
      }
    }
  }
}
```

## Implementation Plan

### Phase 1: Core Infrastructure
1. Create base classes (`ClaudeCommandBuilder`, `TaskContext`, etc.)
2. Implement basic task analysis for common patterns
3. Create minimal config generation functionality
4. Add basic security filtering

### Phase 2: Advanced Analysis
1. Implement machine learning-based task classification
2. Add support for custom task type definitions
3. Create feedback loop for improving recommendations
4. Add performance optimization features

### Phase 3: Integration
1. Integrate with existing `ProcessManager`
2. Add configuration management UI
3. Implement monitoring and analytics
4. Create comprehensive testing suite

## Usage Example

```python
# Initialize the command builder
builder = ClaudeCommandBuilder(
    base_mcp_config_path=Path("config/full_mcp.json"),
    temp_config_dir=Path("temp/mcp_configs")
)

# Create task context from Jira issue
context = TaskContext(
    issue_key="PROJ-123",
    issue_type="Bug",
    summary="Fix authentication error in user login",
    description="Users unable to log in due to OAuth token validation failure...",
    labels=["backend", "authentication", "urgent"],
    project_key="PROJ"
)

# Build optimized command
command = builder.build_command(context)

# Execute with subprocess
process = subprocess.Popen(
    command.cmd_args,
    cwd=command.working_directory,
    env=command.environment_vars,
    # ... other subprocess args
)
```

## Benefits

### Performance
- **Faster Startup**: Loading only required MCP servers reduces initialization time
- **Lower Memory Usage**: Minimal configuration uses less system resources
- **Reduced Network Overhead**: Fewer active connections to external services

### Security
- **Principle of Least Privilege**: Only necessary tools are available
- **Reduced Attack Surface**: Fewer exposed interfaces and capabilities
- **Granular Control**: Fine-tuned permissions per task type

### Maintainability
- **Modular Design**: Easy to add new task types and MCP servers
- **Clear Separation**: Task analysis logic separated from execution
- **Testable Components**: Each component can be unit tested independently

### Flexibility
- **Task-Specific Optimization**: Each execution optimized for its specific needs
- **Easy Extension**: New MCP servers and tools can be easily integrated
- **Configuration Management**: Centralized control over tool availability

## Configuration

### Environment Variables
- `CLAUDE_COMMAND_BUILDER_TEMP_DIR`: Directory for temporary MCP configs
- `CLAUDE_COMMAND_BUILDER_CACHE_SIZE`: Number of configs to cache
- `CLAUDE_COMMAND_BUILDER_SECURITY_LEVEL`: Default security level

### Config Files
- `task_mappings.yaml`: Task type to MCP server mappings
- `security_rules.yaml`: Tool security classifications
- `keyword_patterns.yaml`: Content analysis patterns

## Monitoring and Analytics

The command builder will provide metrics on:
- **Server Usage**: Which MCP servers are most commonly required
- **Tool Utilization**: Tool usage patterns across different task types
- **Performance Impact**: Execution time improvements with minimal configs
- **Security Events**: Blocked tool access attempts

## Future Enhancements

1. **AI-Powered Analysis**: Use LLM to analyze task requirements more intelligently
2. **Learning System**: Improve recommendations based on execution outcomes
3. **Multi-Agent Support**: Coordinate tool allocation across multiple agents
4. **Dynamic Scaling**: Automatically scale MCP server resources based on demand
5. **Integration APIs**: Provide APIs for external systems to influence tool selection

## Testing Strategy

- **Unit Tests**: Test each component in isolation
- **Integration Tests**: Test end-to-end command building and execution
- **Performance Tests**: Measure startup time and resource usage improvements
- **Security Tests**: Verify tool restrictions are properly enforced
- **Regression Tests**: Ensure new features don't break existing functionality

## Conclusion

The Claude Command Builder represents a significant enhancement to the ambient agent's capabilities, providing intelligent, secure, and performant Claude execution with minimal overhead. By dynamically configuring MCP servers and tools based on task requirements, this feature will improve both the efficiency and security of the agent's operations while maintaining flexibility for diverse use cases. 