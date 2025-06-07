"""
Prompt instructions for LLMs to analyze issues and determine required MCP tools and servers.
This module provides prompt templates for analyzing task descriptions and mapping them to available tools.
"""

from langchain.prompts import PromptTemplate


def get_claude_command_generator_prompt_template():
    """
    Create a LangChain PromptTemplate for analyzing issues and generating Claude command configurations.

    This template guides the analysis of issue descriptions to determine:
    - Which tools should be allowed
    - Which tools should be disallowed
    - Which MCP servers are required
    - Reasoning for the decisions

    Returns:
        PromptTemplate: A LangChain prompt template for Claude command configuration.
    """

    template = """
CLAUDE COMMAND CONFIGURATION TASK

INSTRUCTIONS

You are an expert system analyst. Your task is to analyze a given issue description and determine the optimal set of tools and MCP servers required to solve it effectively and safely.

<issue_description>
{issue_description}
</issue_description>

<mcp_documentation>
{mcp_documentation}
</mcp_documentation>

ANALYSIS REQUIREMENTS

Based on the issue description and the available MCP servers and tools documentation, you need to determine:

1. **ALLOWED TOOLS**: Which specific tools should be available to solve this issue
   - Include both MCP server tools (format: mcp__server__tool_name) and Claude built-in tools
   - Be specific - include only tools that are directly relevant to the task
   - Consider the full workflow needed to complete the task
   - Examples: ["mcp__git__git_status", "mcp__github__create_issue", "Read", "Write", "Bash"]

2. **DISALLOWED TOOLS**: Which tools should be explicitly blocked
   - Include tools that could be dangerous or counterproductive for this specific task
   - Consider tools that might cause unintended side effects
   - Include tools that are completely irrelevant to prevent misuse
   - Examples: ["mcp__slack__slack_post_message", "mcp__gsuite__send_draft", "Write"] (if inappropriate)

3. **REQUIRED MCP SERVERS**: Which MCP servers need to be active
   - List the server names (without mcp__ prefix) that provide the needed tools
   - Only include servers whose tools are actually needed
   - Examples: ["git", "github", "sqlite"] (not "mcp-git", just "git")

4. **REASONING**: Provide a clear explanation of your decisions
   - Explain why specific tools are needed
   - Justify why certain tools are disallowed
   - Describe the expected workflow

ANALYSIS GUIDELINES:

- **Safety First**: Always err on the side of caution. If a tool could cause damage, disallow it unless absolutely necessary
- **Principle of Least Privilege**: Only allow tools that are directly needed for the task
- **Workflow Thinking**: Consider the complete end-to-end process needed to solve the issue
- **Tool Categories**:
  - Development: git, github, file operations (Read, Write, Edit)
  - Database: sqlite, neo4j operations
  - Communication: slack, gsuite (email/calendar)
  - Operations: browser automation, transcription
  - System: bash commands, file system operations

SPECIFIC CONSIDERATIONS:

- For coding tasks: Usually need Read, Write, Edit, Bash, and potentially git/github tools
- For database tasks: Need appropriate database server tools (sqlite, neo4j)
- For communication tasks: Need slack or gsuite tools
- For research tasks: May need WebSearch, WebFetch, browser tools
- For documentation: Need Read, Write, and potentially confluence tools

DANGEROUS TOOLS TO CONSIDER RESTRICTING:
- Write operations in production environments
- Mass communication tools (bulk emails, broad slack messages)
- Destructive database operations
- System-level bash commands that could affect infrastructure

RESOURCES
Claude cmd help
<claude help terminal output>
cld -h
Usage: claude [options] [command] [prompt]

Claude Code - starts an interactive session by default, use -p/--print for non-interactive output

Arguments:
  prompt                          Your prompt

Options:
  -d, --debug                     Enable debug mode
  --verbose                       Override verbose mode setting from config
  -p, --print                     Print response and exit (useful for pipes)
  --output-format <format>        Output format (only works with --print): "text" (default), "json" (single result), or "stream-json" (realtime streaming) (choices:
                                  "text", "json", "stream-json")
  --mcp-debug                     [DEPRECATED. Use --debug instead] Enable MCP debug mode (shows MCP server errors)
  --dangerously-skip-permissions  Bypass all permission checks. Only works in Docker containers with no internet access.
  --allowedTools <tools...>       Comma or space-separated list of tool names to allow (e.g. "Bash(git:*) Edit")
  --disallowedTools <tools...>    Comma or space-separated list of tool names to deny (e.g. "Bash(git:*) Edit")
  --mcp-config <file or string>   Load MCP servers from a JSON file or string
  -c, --continue                  Continue the most recent conversation
  -r, --resume [sessionId]        Resume a conversation - provide a session ID or interactively select a conversation to resume
  --model <model>                 Model for the current session. Provide an alias for the latest model (e.g. 'sonnet' or 'opus') or a model's full name (e.g.
                                  'claude-sonnet-4-20250514').
  -v, --version                   Output the version number
  -h, --help  
</claude help terminal output>

OUTPUT FORMAT:
Follow the structured output schema exactly. Provide comprehensive lists and clear reasoning.
"""

    prompt = PromptTemplate(
        input_variables=["issue_description", "mcp_documentation"],
        template=template,
    )

    return prompt
