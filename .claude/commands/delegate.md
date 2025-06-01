# Task Delegation Instructions

## Overview
When delegating tasks, create a comprehensive Jira issue in the **AGENT** project only. Do not create issues in any other project.

## Required MCP Tools
- **Jira Creation**: Use `mcp_conduit_create_jira_issue` with project set to "AGENT"
- **Project Verification**: Use `mcp_conduit_search_jira_issues` to verify the AGENT project exists if needed
- **Date/Time Reference**: Use `mcp_base_get_date` to get current date for deadline calculation
- **Current Time**: Use `mcp_base_get_time` to get current time for deadline setting



### Realistic Deadline Calculation
- **Simple tasks (1-2 hours)**: Same day or next day
- **Medium tasks (4-8 hours)**: 1-3 days
- **Complex tasks (1-2 days)**: 3-7 days  
- **Large tasks (3+ days)**: 1-2 weeks

Always add buffer time for realistic expectations.

## Mandatory Jira Issue Components

### 1. Summary
- Create a clear, concise title that describes the task objective
- Format: "[TASK TYPE] - Brief Description"
- Examples: "[TASK] - Implement user authentication", "[BUG] - Fix email notification system"

### 2. Description Structure
The description MUST include all of the following sections:

#### **Objective**
- Clear statement of what needs to be accomplished
- Business context and importance

#### **Acceptance Criteria**
- Specific, measurable criteria that define task completion
- Use numbered list format:
  1. Criterion 1 - specific and testable
  2. Criterion 2 - specific and testable
  3. Criterion 3 - specific and testable
- Each criterion must be verifiable and unambiguous

#### **Deadline**
- Use MCP base tools to get current date/time for reference
- Calculate realistic deadline based on task complexity
- Format: "Due: YYYY-MM-DD by HH:MM [timezone]" 
- **Example process**:
  1. Call `mcp_base_get_date` with `[{"days_offset": 0}]` to get today's date
  2. Call `mcp_base_get_time` to get current time
  3. Add appropriate buffer (e.g., 3 days for medium task)
  4. Set deadline: "Due: 2024-01-18 by 17:00 EST"

#### **Technical Guidance**
- List specific MCP tools that should be used
- Provide step-by-step technical approach when applicable
- Include any relevant API endpoints, databases, or external systems
- Specify integration requirements or dependencies

#### **Resources & References**
- Link to relevant documentation
- Include any existing Jira tickets or Confluence pages
- Provide access credentials or system information if needed

### 3. Issue Type
- Set appropriate issue type: "Task", "Story", "Bug", "Epic"
- Default to "Task" unless specifically requested otherwise

## Validation Checklist
Before creating the Jira issue, verify:
- [ ] Used `mcp_base_get_date` to determine current date for deadline calculation
- [ ] Used `mcp_base_get_time` to get current time reference
- [ ] Project is set to "AGENT"
- [ ] Summary is clear and descriptive
- [ ] All five description sections are complete
- [ ] Acceptance criteria are specific and measurable
- [ ] Deadline is realistic and clearly stated with proper date/time format
- [ ] Technical guidance includes specific MCP tools
- [ ] Issue type is appropriate

## Example Usage with Date/Time Tools

```
# First, get current date and time for reference
Call mcp_base_get_date with kwargs_list: [{"days_offset": 0}]
Call mcp_base_get_time

# For a medium complexity task, add 3 days
Call mcp_base_get_date with kwargs_list: [{"days_offset": 3}]

# Then create the Jira issue
Project: AGENT
Summary: [TASK] - Implement automated email response system
Description:
**Objective**
Create an automated email response system that processes customer inquiries and provides initial responses using AI.

**Acceptance Criteria**
1. System can read incoming emails from support@company.com
2. AI processes email content and generates appropriate responses
3. System automatically sends responses within 5 minutes of receipt
4. All interactions are logged in the database with timestamps

**Deadline**
Due: 2024-01-18 by 17:00 EST
(Calculated using current date 2024-01-15 + 3 days buffer for medium complexity task)

**Technical Guidance**
- Use `mcp_gsuite_query_gmail_emails` to monitor incoming emails
- Use `mcp_gsuite_create_reply` to send automated responses
- Use `mcp_sqlite_write_query` to log interactions
- Use AI processing for content analysis and response generation

**Resources & References**
- Gmail API documentation: [link]
- Related ticket: AGENT-123
```

## Error Prevention
- **NEVER** create Jira issues in projects other than "AGENT"
- **ALWAYS** include all mandatory sections in the description
- **VERIFY** deadline feasibility before setting
- **CONFIRM** technical guidance is specific and actionable 