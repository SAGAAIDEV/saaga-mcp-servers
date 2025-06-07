# MCP Servers and Tools Directory

This document provides a comprehensive list of all MCP servers available in the saaga-mcp-servers repository and their associated tools.

## Base Infrastructure

### saaga-mcp-base
Core infrastructure and utilities for other MCP servers.

**Tools:**
- `mcp__base__read_logs` - Read log entries from the log database
- `mcp__base__start_scheduler_services` - Start Redis, Celery worker, Celery beat, and Flower
- `mcp__base__stop_scheduler_services` - Stop all managed services
- `mcp__base__get_time` - Get current time
- `mcp__base__wait` - Wait for specified number of minutes
- `mcp__base__get_date` - Get date with optional offset

## Database Servers

### mcp-sqlite
SQLite database operations server.

**Tools:**
- `mcp__sqlite__read_query` - Execute SELECT queries
- `mcp__sqlite__write_query` - Execute INSERT, UPDATE, or DELETE queries
- `mcp__sqlite__create_table` - Create new tables
- `mcp__sqlite__list_tables` - List all tables in database
- `mcp__sqlite__describe_table` - Get schema information for a table
- `mcp__sqlite__append_insight` - Add business insights to memo

### mcp-neo4j
Neo4j graph database server.

**Tools:**
- `mcp__neo4j__Connect` - Connect to Neo4j with explicit credentials
- `mcp__neo4j__ConnectWithEnv` - Connect using environment variables
- `mcp__neo4j__Query` - Execute Cypher queries
- `mcp__neo4j__GetDatabaseInfo` - Get database information
- `mcp__neo4j__GetConnectionStatus` - Check connection status
- `mcp__neo4j__Disconnect` - Disconnect from database

## Development Tools

### mcp-git
Git version control operations.

**Tools:**
- `mcp__git__git_status` - Show working tree status
- `mcp__git__git_diff_unstaged` - Show unstaged changes
- `mcp__git__git_diff_staged` - Show staged changes
- `mcp__git__git_diff` - Show differences between branches/commits
- `mcp__git__git_commit` - Record changes to repository
- `mcp__git__git_add` - Add files to staging area
- `mcp__git__git_reset` - Unstage all changes
- `mcp__git__git_log` - Show commit logs
- `mcp__git__git_create_branch` - Create new branch
- `mcp__git__git_checkout` - Switch branches
- `mcp__git__git_show` - Show commit contents
- `mcp__git__git_init` - Initialize new repository
- `mcp__git__git_merge` - Merge branches
- `mcp__git__git_push` - Push changes to remote

### mcp-github
GitHub API integration for repository management.

**Tools:**
- `mcp__github__add_issue_comment` - Add comment to issue
- `mcp__github__add_pull_request_review_comment_to_pending_review` - Add comment to pending PR review
- `mcp__github__assign_copilot_to_issue` - Assign Copilot to work on issue
- `mcp__github__create_and_submit_pull_request_review` - Create and submit PR review
- `mcp__github__create_branch` - Create new branch
- `mcp__github__create_issue` - Create new issue
- `mcp__github__create_or_update_file` - Create or update file
- `mcp__github__create_pending_pull_request_review` - Create pending PR review
- `mcp__github__create_pull_request` - Create new pull request
- `mcp__github__create_repository` - Create new repository
- `mcp__github__delete_file` - Delete file from repository
- `mcp__github__delete_pending_pull_request_review` - Delete pending PR review
- `mcp__github__dismiss_notification` - Mark notification as read/done
- `mcp__github__fork_repository` - Fork repository
- `mcp__github__get_code_scanning_alert` - Get code scanning alert details
- `mcp__github__get_commit` - Get commit details
- `mcp__github__get_file_contents` - Get file/directory contents
- `mcp__github__get_issue` - Get issue details
- `mcp__github__get_issue_comments` - Get issue comments
- `mcp__github__get_me` - Get authenticated user details
- `mcp__github__get_notification_details` - Get notification details
- `mcp__github__get_pull_request` - Get PR details
- `mcp__github__get_pull_request_comments` - Get PR comments
- `mcp__github__get_pull_request_diff` - Get PR diff
- `mcp__github__get_pull_request_files` - Get PR files
- `mcp__github__get_pull_request_reviews` - Get PR reviews
- `mcp__github__get_pull_request_status` - Get PR status
- `mcp__github__get_secret_scanning_alert` - Get secret scanning alert
- `mcp__github__get_tag` - Get tag details
- `mcp__github__list_branches` - List repository branches
- `mcp__github__list_code_scanning_alerts` - List code scanning alerts
- `mcp__github__list_commits` - List commits
- `mcp__github__list_issues` - List repository issues
- `mcp__github__list_notifications` - List GitHub notifications
- `mcp__github__list_pull_requests` - List pull requests
- `mcp__github__list_secret_scanning_alerts` - List secret scanning alerts
- `mcp__github__list_tags` - List repository tags
- `mcp__github__manage_notification_subscription` - Manage notification subscriptions
- `mcp__github__manage_repository_notification_subscription` - Manage repo notifications
- `mcp__github__mark_all_notifications_read` - Mark all notifications as read
- `mcp__github__merge_pull_request` - Merge pull request
- `mcp__github__push_files` - Push multiple files in single commit
- `mcp__github__request_copilot_review` - Request Copilot code review
- `mcp__github__search_code` - Search for code
- `mcp__github__search_issues` - Search for issues
- `mcp__github__search_repositories` - Search for repositories
- `mcp__github__search_users` - Search for users
- `mcp__github__submit_pending_pull_request_review` - Submit pending PR review
- `mcp__github__update_issue` - Update existing issue
- `mcp__github__update_pull_request` - Update existing PR
- `mcp__github__update_pull_request_branch` - Update PR branch

### mcp-conduit
Atlassian integration (Jira and Confluence).

**Tools:**
- `mcp__conduit__list_atlassian_sites` - List configured Jira/Confluence sites
- `mcp__conduit__get_confluence_page` - Get Confluence page content in markdown
- `mcp__conduit__search_jira_issues` - Search Jira issues using JQL
- `mcp__conduit__create_jira_issue` - Create new Jira issue
- `mcp__conduit__update_jira_issue` - Update Jira issue
- `mcp__conduit__update_jira_status` - Update Jira issue status
- `mcp__conduit__get_jira_boards` - Get Jira boards
- `mcp__conduit__get_jira_sprints` - Get sprints from board
- `mcp__conduit__add_issues_to_jira_sprint` - Add issues to sprint
- `mcp__conduit__create_jira_sprint` - Create new sprint
- `mcp__conduit__get_jira_remote_links` - Get issue remote links
- `mcp__conduit__list_all_confluence_pages` - List all pages in space
- `mcp__conduit__create_confluence_page_from_markdown` - Create Confluence page from markdown
- `mcp__conduit__get_project_overview` - Get unified project overview
- `mcp__conduit__update_confluence_page` - Update existing Confluence page

## Operations Tools

### mcp-gsuite
Google Workspace integration (Gmail and Calendar).

**Tools:**
- `mcp__gsuite__auth` - Authenticate with Google
- `mcp__gsuite__query_gmail_emails` - Search Gmail emails
- `mcp__gsuite__create_reply` - Create email reply
- `mcp__gsuite__get_email_by_id` - Get complete email by ID
- `mcp__gsuite__create_draft` - Create draft email
- `mcp__gsuite__get_attachment` - Retrieve email attachment
- `mcp__gsuite__send_draft` - Send draft email
- `mcp__gsuite__create_label` - Create Gmail label
- `mcp__gsuite__set_email_labels` - Add/remove email labels
- `mcp__gsuite__update_draft` - Update draft email
- `mcp__gsuite__list_calendars` - List all calendars
- `mcp__gsuite__get_events` - Get calendar events
- `mcp__gsuite__create_event` - Create calendar event
- `mcp__gsuite__delete_event` - Delete calendar event
- `mcp__gsuite__update_event` - Update calendar event

### mcp-slack
Slack workspace integration.

**Tools:**
- `mcp__slack__slack_list_channels` - List public channels
- `mcp__slack__slack_post_message` - Post message to channel
- `mcp__slack__slack_reply_to_thread` - Reply to message thread
- `mcp__slack__slack_add_reaction` - Add emoji reaction
- `mcp__slack__slack_get_channel_history` - Get channel messages
- `mcp__slack__slack_get_thread_replies` - Get thread replies
- `mcp__slack__slack_get_users` - List workspace users
- `mcp__slack__slack_get_user_profile` - Get user profile details

### mcp-browsermcp
Browser automation and web interaction.

**Tools:**
- `mcp__browsermcp__browser_navigate` - Navigate to URL
- `mcp__browsermcp__browser_go_back` - Go to previous page
- `mcp__browsermcp__browser_go_forward` - Go to next page
- `mcp__browsermcp__browser_snapshot` - Capture page accessibility snapshot
- `mcp__browsermcp__browser_click` - Click on element
- `mcp__browsermcp__browser_hover` - Hover over element
- `mcp__browsermcp__browser_type` - Type text into element
- `mcp__browsermcp__browser_select_option` - Select dropdown option
- `mcp__browsermcp__browser_press_key` - Press keyboard key
- `mcp__browsermcp__browser_wait` - Wait for specified time
- `mcp__browsermcp__browser_get_console_logs` - Get browser console logs
- `mcp__browsermcp__browser_screenshot` - Take page screenshot

## Utility Servers

### mcp-transcriber
Audio and video transcription service.

**Tools:**
- `mcp__transcriber__transcribe_file` - Transcribe audio/video file
- `mcp__transcriber__read_transcript` - Read saved transcription

## Claude Code Built-in Tools

### Core Tools
- `Task` - Launch agent for complex searches
- `Bash` - Execute bash commands
- `Read` - Read file contents
- `Write` - Write file contents
- `Edit` - Edit file with string replacement
- `MultiEdit` - Multiple edits to single file
- `Glob` - Find files by pattern
- `Grep` - Search file contents
- `LS` - List directory contents
- `NotebookRead` - Read Jupyter notebook
- `NotebookEdit` - Edit Jupyter notebook
- `WebFetch` - Fetch and analyze web content
- `WebSearch` - Search the web
- `TodoRead` - Read todo list
- `TodoWrite` - Manage todo list