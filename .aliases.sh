ea() {
    claude --mcp-config ./.mcp.ea.json --system-prompt "$(cat .claude/system_prompts/ea.md)" --disallowedTools "mcp__slack__slack_list_channels" "$@"
}