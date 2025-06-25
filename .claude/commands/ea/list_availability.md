TASK: Extract "Available" calendar events, post to Slack

1. mcp_gsuite_auth(random_string="auth")
2. Get current week dates, use mcp_gsuite_get_events(user_id=authenticated_email, time_min=week_start, time_max=week_end, include_color_rgb=true)
3. Filter events: summary="Available"
4. Format: "Available Time Slots This Week:\n\n**[Day], [Month] [Date], [Year]**\n- Time: [Start] - [End] ([Timezone])"
5. mcp_slack_slack_post_message(channel_id=provided_channel, text=formatted_message) 