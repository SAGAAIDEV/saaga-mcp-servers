# Sprint Plan: Ambient Agent MVP

## Sprint Overview
**Sprint Goal**: Deliver a functional Ambient Agent that monitors Jira for new tasks and triggers Claude code execution
**Duration**: 2 weeks (10 working days)
**Team Size**: 1 developer
**Start Date**: 2025-01-06
**End Date**: 2025-01-17

## Sprint Objectives
1. Initialize UV library structure in the agents/ambient folder
2. Integrate Conduit library for Jira API access
3. Implement continuous polling loop with graceful shutdown
4. Create Claude code subprocess execution module
5. Implement logging and error handling
6. Deliver working MVP with hard-coded project configuration

## User Stories & Tasks

### Day 1-2: Project Setup and Structure
**Story**: As a developer, I need a properly structured UV library for the Ambient Agent

**Tasks**:
- [ ] Initialize UV project in `/src/saaga_mcp_servers/agents/ambient/`
- [ ] Create `pyproject.toml` with Python 3.12 and dependencies
- [ ] Set up project structure with proper Python packaging
- [ ] Configure Conduit as a dependency
- [ ] Create basic README with setup instructions
- [ ] Set up development environment and virtual environment

**Acceptance Criteria**:
- UV project initialized and installable
- All dependencies properly declared
- Basic project structure follows Python best practices

### Day 3-4: Core Loop Implementation
**Story**: As a user, I need the agent to run continuously and handle termination gracefully

**Tasks**:
- [ ] Create `main.py` module with async event loop
- [ ] Implement signal handlers for Control-C (SIGINT)
- [ ] Create configurable polling interval (default 60 seconds)
- [ ] Implement graceful shutdown mechanism
- [ ] Add basic health check logging
- [ ] Create CLI entry point for the agent

**Acceptance Criteria**:
- Agent runs continuously until terminated
- Clean shutdown on Control-C
- Proper async/await implementation
- No zombie processes or resource leaks

### Day 5-6: Jira Integration via Conduit
**Story**: As a user, I need the agent to retrieve Jira issues from a specific project

**Tasks**:
- [ ] Configure Conduit client with hard-coded project key
- [ ] Implement JQL query for "To Do" status issues
- [ ] Create issue fetching method with error handling
- [ ] Implement issue deduplication logic
- [ ] Add issue metadata extraction (key, summary, description)
- [ ] Create issue state tracking to prevent reprocessing

**Acceptance Criteria**:
- Successfully connects to Jira via Conduit
- Retrieves all "To Do" issues from hard-coded project
- Tracks processed issues to avoid duplicates
- Handles API errors gracefully

### Day 7-8: Claude Code Integration
**Story**: As a user, I need Claude code to be executed for each new Jira issue

**Tasks**:
- [ ] Implement subprocess spawning for Claude code
- [ ] Configure Claude with `--no-confirm` flag for non-interactive mode
- [ ] Pass Jira issue data to `do.md` command
- [ ] Capture stdout and stderr streams
- [ ] Implement execution timeout handling
- [ ] Add process cleanup on termination

**Acceptance Criteria**:
- Claude code executes without user interaction
- All output is captured and logged
- No permission prompts from Claude
- Processes are cleaned up properly

### Day 9: Logging and Monitoring
**Story**: As an operator, I need comprehensive logging for debugging and monitoring

**Tasks**:
- [ ] Set up structured JSON logging
- [ ] Log all Jira API interactions
- [ ] Log Claude code execution details
- [ ] Add execution timing metrics
- [ ] Implement log rotation configuration
- [ ] Create debug mode with verbose output

**Acceptance Criteria**:
- All significant events are logged
- Logs include timestamps and context
- Error stack traces are captured
- Log levels are configurable

### Day 10: Testing and Documentation
**Story**: As a maintainer, I need the code to be tested and documented

**Tasks**:
- [ ] Write unit tests for core modules
- [ ] Create integration tests with mock APIs
- [ ] Document configuration options
- [ ] Create operational runbook
- [ ] Write troubleshooting guide
- [ ] Perform end-to-end testing

**Acceptance Criteria**:
- 70%+ test coverage achieved
- All public APIs documented
- README includes usage examples
- Known issues documented

## Technical Implementation Details

### Hard-coded Configuration (Sprint 1)
```python
# Initial hard-coded configuration
JIRA_PROJECT = "AGENT"  # Hard-coded project key
POLL_INTERVAL = 60  # seconds
JQL_QUERY = f"project = {JIRA_PROJECT} AND status = 'To Do'"
CLAUDE_COMMAND = ["claude", "code", "--no-confirm", "do.md"]
```

### Main Loop Pseudocode
```python
async def main():
    # Initialize Conduit client
    jira_client = JiraClient()
    processed_issues = set()
    
    try:
        while True:
            # Fetch issues from Jira
            issues = await fetch_jira_issues(jira_client, JQL_QUERY)
            
            # Process new issues
            for issue in issues:
                if issue.key not in processed_issues:
                    await process_issue(issue)
                    processed_issues.add(issue.key)
            
            # Wait for next poll
            await asyncio.sleep(POLL_INTERVAL)
            
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
        await cleanup()
```

## Definition of Done
- [ ] Code is written and peer-reviewed
- [ ] Unit tests pass with 70%+ coverage
- [ ] Integration tests pass
- [ ] Documentation is complete
- [ ] Code follows Python style guidelines
- [ ] No critical bugs or security issues
- [ ] Successfully processes test Jira issues
- [ ] Logs are comprehensive and useful

## Risks and Mitigation
1. **Risk**: Conduit API changes or limitations
   - **Mitigation**: Pin Conduit version, have fallback to direct Jira API

2. **Risk**: Claude code execution failures
   - **Mitigation**: Implement retry logic and timeout handling

3. **Risk**: Memory leaks from long-running process
   - **Mitigation**: Monitor memory usage, implement periodic cleanup

4. **Risk**: Jira API rate limiting
   - **Mitigation**: Implement exponential backoff, respect rate limits

## Sprint Retrospective Topics
- Effectiveness of hard-coded configuration approach
- Conduit library integration experience
- Claude code subprocess management challenges
- Logging verbosity and usefulness
- Performance under continuous operation

## Next Sprint Preview
- Configuration file support (YAML)
- Multiple project monitoring
- Enhanced error recovery
- Metrics and monitoring endpoints
- Docker containerization
- Advanced Claude command templates