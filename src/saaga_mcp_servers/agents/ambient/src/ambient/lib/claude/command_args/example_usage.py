"""
Example usage of the Claude command generation system.

This module demonstrates how to analyze issues and generate appropriate Claude commands
with the right tools and MCP server configurations.
"""

from .graph import generate_claude_config, generate_claude_command


def example_github_issue_analysis():
    """Example: Analyzing a GitHub-related development issue."""

    issue_description = """
    I need to create a new feature branch for implementing user authentication,
    update the main authentication module, create tests, and then open a pull request
    for review. The implementation needs to be tested locally before pushing.
    """

    # Analyze the issue and get tool configuration
    config = generate_claude_config(issue_description)

    print("=== GitHub Development Issue Analysis ===")
    print(f"Issue: {issue_description[:100]}...")
    print(f"\nAllowed Tools: {config.allowed_tools}")
    print(f"Disallowed Tools: {config.disallowed_tools}")
    print(f"Required MCP Servers: {config.required_mcp_servers}")
    print(f"Reasoning: {config.reasoning}")

    # Generate Claude command
    prompt = "Help me implement user authentication feature as described in the issue"
    command = generate_claude_command(config, prompt)
    print(f"\nGenerated Claude Command:")
    print(" ".join(command))

    return config


def example_database_issue_analysis():
    """Example: Analyzing a database-related issue."""

    issue_description = """
    I need to analyze customer purchase data from our SQLite database,
    create summary reports, and generate business insights. The analysis
    should identify top customers, popular products, and seasonal trends.
    No data should be modified, only read and analyzed.
    """

    config = generate_claude_config(issue_description)

    print("\n=== Database Analysis Issue ===")
    print(f"Issue: {issue_description[:100]}...")
    print(f"\nAllowed Tools: {config.allowed_tools}")
    print(f"Disallowed Tools: {config.disallowed_tools}")
    print(f"Required MCP Servers: {config.required_mcp_servers}")
    print(f"Reasoning: {config.reasoning}")

    prompt = "Analyze the customer database and generate business insights"
    command = generate_claude_command(config, prompt)
    print(f"\nGenerated Claude Command:")
    print(" ".join(command))

    return config


def example_communication_issue_analysis():
    """Example: Analyzing a communication/notification issue."""

    issue_description = """
    I need to send project updates to the team via Slack, schedule a meeting
    for next week in Google Calendar, and send follow-up emails to stakeholders
    about the project status. This is routine communication for project management.
    """

    config = generate_claude_config(issue_description)

    print("\n=== Communication Issue ===")
    print(f"Issue: {issue_description[:100]}...")
    print(f"\nAllowed Tools: {config.allowed_tools}")
    print(f"Disallowed Tools: {config.disallowed_tools}")
    print(f"Required MCP Servers: {config.required_mcp_servers}")
    print(f"Reasoning: {config.reasoning}")

    prompt = "Help me coordinate team communication and schedule meetings"
    command = generate_claude_command(config, prompt)
    print(f"\nGenerated Claude Command:")
    print(" ".join(command))

    return config


if __name__ == "__main__":
    """Run example analyses when script is executed directly."""

    print("Claude Command Generation Examples")
    print("=" * 50)

    try:
        # Run examples
        example_github_issue_analysis()
        example_database_issue_analysis()
        example_communication_issue_analysis()

    except Exception as e:
        print(f"Error running examples: {e}")
        print(
            "Make sure the MCP documentation file exists and the environment is properly configured."
        )
