# Email Unsubscribe Instructions

This document provides step-by-step instructions for unsubscribing from vendor emails using the browser MCP server.

## Prerequisites
- Gmail API authenticated (use mcp__gsuite__auth if needed)
- Browser MCP server must be running
- Gmail credentials configured

## Steps to Unsubscribe

### 1. Get Inbox Emails and Identify Vendors
- Query Gmail to get all inbox emails
```
Use: mcp__gsuite__query_gmail_emails
Parameters:
- user_id: "saaga@saaga.dev"
- query: "in:inbox"
- max_results: 50
```
- Review the results to identify vendor/marketing emails
- Common vendor indicators:
  - Category labels: CATEGORY_PROMOTIONS, CATEGORY_UPDATES
  - From addresses ending in: noreply@, notifications@, marketing@
  - Subjects with: "Your subscription", "Welcome to", "New from", etc.

### 2. Navigate to Gmail
```
Use: mcp__browsermcp__browser_navigate
URL: https://mail.google.com
```

### 3. Find the Vendor Email
- Take a snapshot to see available emails in inbox
```
Use: mcp__browsermcp__browser_snapshot
```

### 4. Hover Over the Email
- Hover over the email row in the inbox to reveal the unsubscribe button
```
Use: mcp__browsermcp__browser_hover
Element: "[Vendor email subject line]"
Ref: [Reference from snapshot]
```

### 5. Take Snapshot to See Revealed Button
- After hovering, take a snapshot to see the unsubscribe button
```
Use: mcp__browsermcp__browser_snapshot
```

### 6. Click Unsubscribe
- Click on the revealed unsubscribe button
```
Use: mcp__browsermcp__browser_click
Element: "Unsubscribe button"
Ref: [Reference from snapshot]
```

### 7. Complete Unsubscribe Process
- If redirected to an unsubscribe page:
  - Take a snapshot to see options
  - Click confirm/submit button if required
```
Use: mcp__browsermcp__browser_click
Element: "Confirm unsubscribe"
Ref: [Reference from snapshot]
```

### 8. Return to Gmail and Delete Email
- Navigate back to Gmail if needed
```
Use: mcp__browsermcp__browser_go_back
```
- Or navigate directly
```
Use: mcp__browsermcp__browser_navigate
URL: https://mail.google.com
```

### 9. Delete the Email
- Use Gmail API to remove the email
```
Use: mcp__gsuite__set_email_labels
Parameters:
- user_id: "saaga@saaga.dev"
- message_id: [Email ID from original query]
- label_names_to_remove: ["INBOX"]
- label_names_to_add: ["TRASH"]
```

## Example Workflow

```bash
# 1. Get inbox emails and identify vendors
mcp__gsuite__query_gmail_emails \
  --user_id "saaga@saaga.dev" \
  --query "in:inbox" \
  --max_results 50

# Review output for vendor emails (e.g., Bitwarden with ID "19773bad7cdc55ac")

# 2. Navigate to Gmail
mcp__browsermcp__browser_navigate --url "https://mail.google.com"

# 3. Take snapshot to see emails in inbox
mcp__browsermcp__browser_snapshot

# 4. Hover over vendor email (e.g., Bitwarden) to reveal unsubscribe button
mcp__browsermcp__browser_hover --element "Your Bitwarden onboarding checklist" --ref "[ref_from_snapshot]"

# 5. Take snapshot to see the revealed unsubscribe button
mcp__browsermcp__browser_snapshot

# 6. Click the unsubscribe button
mcp__browsermcp__browser_click --element "Unsubscribe" --ref "[ref_from_snapshot]"

# 7. Complete unsubscribe process on vendor site if needed
# (Take snapshots and click confirm buttons as required)

# 8. Delete email from inbox using Gmail API
mcp__gsuite__set_email_labels \
  --user_id "saaga@saaga.dev" \
  --message_id "19773bad7cdc55ac" \
  --label_names_to_remove '["INBOX"]' \
  --label_names_to_add '["TRASH"]'
```

## Tips
- Some emails hide the unsubscribe link until you hover
- Check both top and bottom of emails for unsubscribe options
- Some vendors require confirmation on their website
- Use screenshot tool to capture the process if needed
- Consider creating a filter to auto-delete future emails from the vendor

## Common Unsubscribe Locations
1. Footer of email (most common)
2. Small text near sender info at top
3. Gmail's native unsubscribe button (appears for some senders)
4. Hidden in "View this email in browser" links