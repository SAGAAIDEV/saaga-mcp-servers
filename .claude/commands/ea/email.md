# Claude Code Email Inbox Cleanup Guide

This guide provides commands and workflows for using Claude Code to efficiently clean up your email inbox using both browser automation and Gmail API tools.

## Prerequisites

### Required MCP Servers
- **GSuite MCP**: For direct Gmail API operations

### Setup
```json
// .claude_desktop_config.json
{
  "mcpServers": {
    "browsermcp": {
      "command": "npx",
      "args": ["@browsermcp/mcp@latest"]
    },
    "gsuite": {
      "command": "python",
      "args": ["-m", "mcp_gsuite"]
    }
  }
}
```

## Common Email Cleanup Commands

### 1. Navigate to Gmail
```
Navigate to Gmail inbox
```
or
```
Go to mail.google.com
```

### 2. Unsubscribe from Marketing Emails

#### Using Browser Automation
```
Hover over the [sender] email and click the unsubscribe button
```
Example:
```
Hover over the Upwork email to reveal the unsubscribe button, then click it
```

#### Using Gmail API
```
Find all emails from [sender] and unsubscribe
```

### 3. Mass Delete Emails

#### Delete by Sender
```
Delete all emails from [sender]
```

#### Delete Old Emails
```
Delete all emails older than [X] days/months/years
```

#### Delete by Category
```
Delete all promotional emails
Delete all social media notifications
Delete all emails in the Updates category
```

### 4. Archive Emails

#### Archive Specific Emails
```
Archive the email from [sender] about [subject]
```

#### Bulk Archive
```
Archive all read emails older than 30 days
Archive all emails from [sender] but keep unread ones
```

### 5. Organize with Labels

#### Create Labels
```
Create a label called [label name]
```

#### Apply Labels
```
Label all emails from [sender] as [label name]
Move all emails about [topic] to [label name]
```

### 6. Search and Filter

#### Find Specific Emails
```
Find all emails with attachments larger than 10MB
Search for emails from [sender] in the last week
Show me all unread emails from [date range]
```

#### Complex Searches
```
Find all emails from [sender1] OR [sender2] with attachments
Search for emails with subject containing [keyword] but NOT from [sender]
```

## Workflow Examples

### Complete Inbox Cleanup Workflow
```
1. Show me all promotional emails from the last month
2. Unsubscribe from any senders I haven't opened emails from
3. Delete all remaining promotional emails older than 7 days
4. Archive all read emails older than 30 days
5. Create labels for important projects
6. Move project-related emails to their respective labels
```

### Newsletter Management
```
1. Find all newsletter subscriptions
2. Show me which ones I haven't read in the last month
3. Unsubscribe from inactive newsletters
4. Create a "Newsletters" label
5. Move all remaining newsletters to this label
```

### Attachment Cleanup
```
1. Find all emails with large attachments (>5MB)
2. Download important attachments to local storage
3. Delete emails with attachments older than 6 months
```

## Advanced Commands

### Using Gmail Search Operators
```
Search for: from:amazon.com has:attachment larger:5M
Search for: is:unread category:social older_than:1m
Search for: subject:"invoice" OR subject:"receipt" newer_than:1y
```

### Batch Operations
```
Select all emails matching [criteria] and [action]
Mark all emails from [sender] as read
Star all emails with subject containing [keyword]
```

### Smart Filtering
```
Create a filter to automatically archive emails from [sender]
Set up a filter to label emails with [keyword] as [label]
Create a filter to delete emails matching [pattern]
```

## Tips for Efficient Cleanup

1. **Start with Unsubscribing**: Prevent future clutter by unsubscribing from unwanted lists first
2. **Use Bulk Actions**: Process similar emails together rather than one by one
3. **Create a Label System**: Organize remaining emails into logical categories
4. **Set Up Filters**: Automate future organization with Gmail filters
5. **Regular Maintenance**: Schedule periodic cleanups to prevent inbox overflow

## Troubleshooting

### Browser Automation Issues
- If hover actions don't reveal buttons, try clicking on the email first
- Use keyboard shortcuts when available (e.g., `j` and `k` to navigate)
- Refresh the page if elements become unresponsive

### API Limitations
- Gmail API has rate limits; space out bulk operations
- Some actions require specific permissions
- Use "me" or your full email address as user_id

### Common Errors
- "Stale aria-ref": Refresh the page or get a new snapshot
- "No OAuth credentials": Ensure GSuite MCP is properly authenticated
- "Element not found": Try alternative descriptions or wait for page load

## Safety Considerations

1. **Always Preview Before Bulk Delete**: Review what will be deleted
2. **Use Archive Instead of Delete**: For emails you might need later
3. **Test Filters**: Run searches before applying bulk actions
4. **Backup Important Emails**: Download or forward critical communications
5. **Check Trash**: Gmail keeps deleted items for 30 days

## Example Session

```
User: Help me clean up my Gmail inbox

Claude: I'll help you clean up your Gmail inbox. Let me start by navigating to Gmail.

[Navigates to Gmail]

Claude: I can see you have 10 unread emails. Let me analyze your inbox:
- 3 promotional emails
- 2 social media notifications  
- 5 work-related emails

What would you like to focus on first?

User: Let's get rid of the promotional emails

Claude: I'll help you with the promotional emails. First, let me hover over them to check for unsubscribe options...

[Continues with cleanup process]
```

## Useful Gmail Keyboard Shortcuts

When using browser automation, these shortcuts can speed up the process:
- `c` - Compose new email
- `j` - Move to next email
- `k` - Move to previous email
- `x` - Select conversation
- `e` - Archive
- `#` - Delete
- `l` - Label
- `shift + i` - Mark as read
- `shift + u` - Mark as unread

Remember to be in the main Gmail view (not inside an email) for these shortcuts to work.