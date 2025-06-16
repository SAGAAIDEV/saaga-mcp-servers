ea() {
    claude --mcp-config /Users/andrew/saga/saaga-mcp-servers/.claude/mcp_configs/.mcp.ea.json --system-prompt "$(cat /Users/andrew/saga/saaga-mcp-servers/.claude/system_prompts/ea.md)" --disallowedTools "mcp__slack__slack_list_channels" "$@"
}

dev() {
    claude --mcp-config /Users/andrew/saga/saaga-mcp-servers/.claude/mcp_configs/.mcp.dev.json --system-prompt "$(cat /Users/andrew/saga/saaga-mcp-servers/.claude/system_prompts/dev.md)" --dangerously-skip-permissions "$@"
}

spirit() {
    claude --mcp-config /Users/andrew/saga/saaga-mcp-servers/.claude/mcp_configs/.mcp.spirit.json --system-prompt "$(cat /Users/andrew/saga/saaga-mcp-servers/.claude/system_prompts/spirit.md)" --disallowedTools "Write(*.py)" --dangerously-skip-permissions "$@"
}