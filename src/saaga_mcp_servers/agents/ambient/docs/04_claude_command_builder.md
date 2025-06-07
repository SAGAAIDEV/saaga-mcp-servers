# Claude Command Builder Feature - Functional Refactor

## Overview

The Claude Command Builder is a functional system that enhances the ambient agent's ability to execute Claude with optimal, task-specific MCP server configurations. This system follows a clear functional pipeline: Get Jiras → Read Jira → Ask for Clarity → Build Command → Run Subprocess.

## Problem Statement

Currently, the ambient agent uses a static MCP configuration (`MCP_JSON`) for all Claude executions, which:

- Loads unnecessary MCP servers that may not be relevant to the task
- Exposes all available tools, creating potential security and complexity issues
- Provides suboptimal performance due to loading unused resources
- Lacks flexibility for different types of tasks that may require different tool sets

## Solution: Functional Pipeline

The Claude Command Builder will be a series of focused functions that form a clear pipeline:

```
get_jiras() → read_jira() → ask_for_clarity() → build_claude_command() → run_subprocess_claude_command()
```

Each function has a single responsibility and can be tested, maintained, and extended independently.

## Architecture

### Core Data Types

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path
from enum import Enum

@dataclass
class JiraIssue:
    """Immutable representation of a Jira issue"""
    key: str
    issue_type: str
    summary: str
    description: str
    status: str
    assignee: str
    labels: List[str]
    custom_fields: Dict[str, Any]
    priority: str
    project_key: str

@dataclass
class TaskRequirements:
    """Requirements determined from task analysis"""
    required_mcp_servers: List[str]
    required_tools: List[str]
    disallowed_tools: List[str]
    additional_args: List[str]
    security_level: str

@dataclass
class ClaudeCommand:
    """Complete Claude command configuration"""
    cmd_args: List[str]
    mcp_config_path: Path
    working_directory: Path
    environment_vars: Dict[str, str]
    timeout: Optional[int]

@dataclass
class ExecutionResult:
    """Result of Claude command execution"""
    success: bool
    return_code: int
    stdout: str
    stderr: str
    execution_time: float
```

### Function Pipeline

#### 1. Get Jiras

```python
def get_jiras(jql_query: str, max_results: int = 50) -> List[str]:
    """
    Retrieve Jira issue keys based on a JQL query.
    
    Args:
        jql_query: JQL query to filter issues
        max_results: Maximum number of issues to return
        
    Returns:
        List of Jira issue keys
        
    Example:
        >>> get_jiras("assignee = currentUser() AND status = 'To Do'")
        ['PROJ-123', 'PROJ-124', 'PROJ-125']
    """
    pass

def get_unassigned_jiras(project_key: str) -> List[str]:
    """Get unassigned issues for a specific project"""
    return get_jiras(f"project = {project_key} AND assignee is EMPTY")

def get_my_active_jiras() -> List[str]:
    """Get issues assigned to current user that are in progress"""
    return get_jiras("assignee = agent@saaga.dev AND status IN ('In Progress', 'To Do')")
```

#### 2. Read Jira

```python
def read_jira(issue_key: str) -> JiraIssue:
    """
    Fetch complete Jira issue details.
    
    Args:
        issue_key: Jira issue key (e.g., 'PROJ-123')
        
    Returns:
        Complete JiraIssue object
        
    Raises:
        JiraNotFoundError: If issue doesn't exist
        JiraPermissionError: If user lacks access
    """
    pass

def read_multiple_jiras(issue_keys: List[str]) -> List[JiraIssue]:
    """Read multiple Jira issues efficiently"""
    return [read_jira(key) for key in issue_keys]
```

#### 3. Ask for Clarity

```python
def ask_for_clarity(issue: JiraIssue) -> JiraIssue:
    """
    Analyze issue and ask for clarification if needed.
    
    This function determines if the issue has sufficient information
    for Claude to work on it effectively. If not, it will:
    - Post comments asking for clarification
    - Update issue status if needed
    - Return updated issue
    
    Args:
        issue: The Jira issue to analyze
        
    Returns:
        Updated JiraIssue (may be same if no clarification needed)
    """
    pass

def needs_clarification(issue: JiraIssue) -> bool:
    """Check if an issue needs clarification"""
    # Check for missing description, vague requirements, etc.
    if not issue.description or len(issue.description.strip()) < 50:
        return True
    
    # Check for ambiguous language
    ambiguous_words = ['maybe', 'probably', 'might', 'could be']
    if any(word in issue.description.lower() for word in ambiguous_words):
        return True
        
    return False

def generate_clarification_questions(issue: JiraIssue) -> List[str]:
    """Generate specific questions to ask for clarification"""
    questions = []
    
    if not issue.description:
        questions.append("Could you provide more details about what needs to be done?")
    
    if issue.issue_type == "Bug" and "error" not in issue.description.lower():
        questions.append("What specific error or unexpected behavior are you experiencing?")
    
    return questions
```

#### 4. Build Claude Command

```python
def build_claude_command(issue: JiraIssue, base_config_path: Path) -> ClaudeCommand:
    """
    Build optimized Claude command for the given issue.
    
    Args:
        issue: Jira issue to work on
        base_config_path: Path to full MCP configuration
        
    Returns:
        Complete ClaudeCommand ready for execution
    """
    requirements = analyze_task_requirements(issue)
    config_path = create_minimal_mcp_config(requirements, base_config_path)
    cmd_args = construct_command_args(issue, config_path, requirements)
    
    return ClaudeCommand(
        cmd_args=cmd_args,
        mcp_config_path=config_path,
        working_directory=Path.cwd(),
        environment_vars=get_environment_vars(requirements),
        timeout=determine_timeout(issue)
    )

def analyze_task_requirements(issue: JiraIssue) -> TaskRequirements:
    """Analyze what MCP servers and tools are needed"""
    required_servers = determine_required_servers(issue)
    required_tools = determine_required_tools(issue)
    disallowed_tools = determine_disallowed_tools(issue)
    
    return TaskRequirements(
        required_mcp_servers=required_servers,
        required_tools=required_tools,
        disallowed_tools=disallowed_tools,
        additional_args=[],
        security_level=determine_security_level(issue)
    )

def determine_required_servers(issue: JiraIssue) -> List[str]:
    """Determine which MCP servers are needed based on issue content"""
    servers = set()
    content = f"{issue.summary} {issue.description}".lower()
    
    # Server mapping based on keywords
    server_keywords = {
        'mcp-git': ['git', 'repository', 'commit', 'branch', 'merge', 'code'],
        'mcp-github': ['github', 'pull request', 'pr', 'review'],
        'confluence-mcp': ['documentation', 'wiki', 'confluence', 'docs'],
        'sqlite-mcp': ['database', 'sql', 'query', 'data'],
        'gsuite-mcp': ['email', 'calendar', 'google', 'gmail'],
        'slack-mcp': ['slack', 'notification', 'message'],
        'browserbase-mcp': ['browser', 'ui', 'test', 'automation']
    }
    
    for server, keywords in server_keywords.items():
        if any(keyword in content for keyword in keywords):
            servers.add(server)
    
    # Issue type based requirements
    if issue.issue_type.lower() == 'bug':
        servers.update(['mcp-git', 'sqlite-mcp'])
    elif issue.issue_type.lower() in ['story', 'task']:
        servers.add('mcp-git')
    
    return list(servers)

def create_minimal_mcp_config(requirements: TaskRequirements, base_config_path: Path) -> Path:
    """Create minimal MCP config with only required servers"""
    # Load base config
    # Filter to only required servers
    # Write to temporary file
    # Return path to minimal config
    pass

def construct_command_args(issue: JiraIssue, config_path: Path, requirements: TaskRequirements) -> List[str]:
    """Construct the full Claude command arguments"""
    args = [
        'claude',
        '--mcp-config', str(config_path),
        '--task', f"Work on Jira issue {issue.key}: {issue.summary}"
    ]
    
    if requirements.disallowed_tools:
        args.extend(['--disallowedTools', ','.join(requirements.disallowed_tools)])
    
    args.extend(requirements.additional_args)
    return args
```

#### 5. Run Subprocess Claude Command

```python
import subprocess
from typing import Optional

def run_subprocess_claude_command(command: ClaudeCommand) -> ExecutionResult:
    """
    Execute Claude command as subprocess.
    
    Args:
        command: Complete Claude command configuration
        
    Returns:
        ExecutionResult with stdout, stderr, and metadata
    """
    import time
    start_time = time.time()
    
    try:
        result = subprocess.run(
            command.cmd_args,
            cwd=command.working_directory,
            env=command.environment_vars,
            timeout=command.timeout,
            capture_output=True,
            text=True
        )
        
        execution_time = time.time() - start_time
        
        return ExecutionResult(
            success=result.returncode == 0,
            return_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            execution_time=execution_time
        )
    
    except subprocess.TimeoutExpired:
        return ExecutionResult(
            success=False,
            return_code=-1,
            stdout="",
            stderr="Command timed out",
            execution_time=command.timeout or 0
        )
    except Exception as e:
        return ExecutionResult(
            success=False,
            return_code=-1,
            stdout="",
            stderr=str(e),
            execution_time=time.time() - start_time
        )

def run_claude_with_retry(command: ClaudeCommand, max_retries: int = 3) -> ExecutionResult:
    """Run Claude command with retry logic"""
    for attempt in range(max_retries):
        result = run_subprocess_claude_command(command)
        if result.success:
            return result
        
        # Add exponential backoff
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)
    
    return result
```

### Orchestration Functions

```python
def process_single_jira(issue_key: str, base_config_path: Path) -> ExecutionResult:
    """Process a single Jira issue through the complete pipeline"""
    # Read Jira
    issue = read_jira(issue_key)
    
    # Ask for clarity if needed
    issue = ask_for_clarity(issue)
    
    # Build command
    command = build_claude_command(issue, base_config_path)
    
    # Execute
    return run_subprocess_claude_command(command)

def process_multiple_jiras(issue_keys: List[str], base_config_path: Path) -> List[ExecutionResult]:
    """Process multiple Jira issues"""
    return [process_single_jira(key, base_config_path) for key in issue_keys]

def process_my_active_work(base_config_path: Path) -> List[ExecutionResult]:
    """Process all active issues assigned to current user"""
    issue_keys = get_my_active_jiras()
    return process_multiple_jiras(issue_keys, base_config_path)
```

## Usage Examples

### Basic Usage

```python
from pathlib import Path

# Process a single issue
result = process_single_jira("PROJ-123", Path("config/mcp.json"))
print(f"Success: {result.success}")
print(f"Output: {result.stdout}")

# Process all my active issues
results = process_my_active_work(Path("config/mcp.json"))
for i, result in enumerate(results):
    print(f"Issue {i+1}: {'✓' if result.success else '✗'}")
```

### Step-by-step Usage

```python
# Get issues
issue_keys = get_jiras("project = MYPROJ AND status = 'To Do'")

# Read specific issue
issue = read_jira("PROJ-123")

# Check if clarification is needed
if needs_clarification(issue):
    questions = generate_clarification_questions(issue)
    print("Need clarification:", questions)
    issue = ask_for_clarity(issue)

# Build and run command
command = build_claude_command(issue, Path("config/mcp.json"))
result = run_subprocess_claude_command(command)
```

### Batch Processing

```python
# Get all unassigned issues for a project
unassigned = get_unassigned_jiras("MYPROJ")

# Process each one
for issue_key in unassigned:
    print(f"Processing {issue_key}...")
    result = process_single_jira(issue_key, Path("config/mcp.json"))
    if result.success:
        print(f"✓ Completed {issue_key}")
    else:
        print(f"✗ Failed {issue_key}: {result.stderr}")
```

## Benefits of Functional Approach

### Single Responsibility
- Each function does exactly one thing
- Easy to understand, test, and maintain
- Clear input/output contracts

### Composability
- Functions can be combined in different ways
- Easy to create new workflows
- Reusable components

### Testability
- Each function can be unit tested independently
- Pure functions (where possible) are easier to test
- Clear mocking boundaries

### Debugging
- Easy to trace through the pipeline
- Can inspect data at each step
- Clear error boundaries

### Extensibility
- Easy to add new functions to the pipeline
- Can swap out implementations
- Plugin-style architecture possible

## Configuration

### Environment Variables
- `JIRA_BASE_URL`: Jira instance URL
- `JIRA_USERNAME`: Jira username
- `JIRA_API_TOKEN`: Jira API token
- `CLAUDE_TIMEOUT_SECONDS`: Default timeout for Claude commands
- `MCP_TEMP_DIR`: Directory for temporary MCP configs

### Config Files
- `task_mappings.yaml`: Task type to MCP server mappings
- `security_rules.yaml`: Tool security classifications
- `keyword_patterns.yaml`: Content analysis patterns

## Testing Strategy

```python
# Unit tests for each function
def test_determine_required_servers():
    issue = JiraIssue(
        key="TEST-1",
        summary="Fix git authentication bug",
        description="Users can't authenticate with git repository",
        # ... other fields
    )
    servers = determine_required_servers(issue)
    assert 'mcp-git' in servers

def test_needs_clarification():
    vague_issue = JiraIssue(summary="Fix the thing", description="")
    assert needs_clarification(vague_issue) == True

# Integration tests for pipeline
def test_complete_pipeline():
    result = process_single_jira("TEST-123", Path("test_config.json"))
    assert result.success == True
```

## Future Enhancements

1. **Parallel Processing**: Process multiple issues concurrently
2. **Caching**: Cache MCP configs and issue data
3. **Metrics**: Add timing and success rate tracking
4. **Webhooks**: React to Jira events automatically
5. **AI Analysis**: Use LLM to better analyze task requirements

## Conclusion

This functional refactor provides a clean, maintainable, and extensible system for processing Jira issues with Claude. Each function has a clear responsibility, making the system easier to understand, test, and modify. The pipeline approach makes it easy to add new steps or modify existing ones without affecting the entire system. 