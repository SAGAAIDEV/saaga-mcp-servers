# Async Task Management Instructions

## Database Operations
- **When you need employee information**: Use the SQLite MCP server to access the employee database
- **When unsure about database structure**: List all tables and describe their schemas before proceeding
- **Data verification**: Always verify data exists before attempting operations

## Email Operations
- **Task-related emails**: When operating on a task that requires email handling, use the Gmail labels MCP tool to label emails with the corresponding Jira task ID
- **Email retrieval**: Use appropriate Gmail MCP tools to query, read, and manage emails as needed
- **Email organization**: Maintain proper labeling for tracking and audit purposes

## Jira Task Management
- **Starting work**: When you begin working on a Jira task, transition its status to "In Progress"
- **Task completion**: When you meet all acceptance criteria, transition the Jira issue status to "Done"
- **Status updates**: Keep Jira issues updated with relevant progress and blockers

## Wait Operations
- **Deadline checking**: Before any wait operation, use the MCP tools to get time from base server to check if it's passed the deadline
- **Failed deadline**: If it is past the deadline and the issue isn't complete, transition the issue to 'FAILED' and then stop
- **Explicit wait requests**: When explicitly told to wait or pause, use the appropriate MCP wait tool
- **Async operations**: Use wait functionality when dealing with tasks that have an uncertain wait period, like waiting for a response

## Error Handling
- **Confusion state**: If you come to a situation where you don't know what to do, transition the issue to 'confused' and stop
- **Graceful degradation**: Handle errors gracefully and report issues through appropriate channels

## General Guidelines
- Always verify task requirements and acceptance criteria before starting
- Maintain clear audit trails through proper labeling and status updates
- Coordinate between systems (email, Jira, database) to ensure data consistency
- Handle errors gracefully and report issues through appropriate channels


