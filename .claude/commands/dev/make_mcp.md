.claude
├── agents.sh
├── commands
│   ├── coms.md
│   ├── delegate.md
│   ├── dev
│   │   └── agents.md
│   ├── do.md
│   ├── document.md
│   └── ea
│       ├── email.md
│       └── meeting.md
├── mcp_configs
│   ├── .mcp.conduit.json
│   ├── .mcp.dev.json
│   ├── .mcp.ea.example.json
│   ├── .mcp.ea.json
│   └── .mcp.procure.json
├── settings.json
├── settings.local.json
└── system_prompts
    ├── dev.md
    └── ea.md
├── src # contains the mcp servers by category.

MCP server Creation
create in category 
cookiecutter gh:codingthefuturewithai/mcp-cookie-cutter

- `project_name`: Human-readable name (e.g., "My MCP Server")
- `project_slug`: Python package name (e.g., "my_mcp_server")
- `description`: Short description of your project
- `author_name`: Your name
- `author_email`: Your email
- `server_port`: Port for SSE server (default: 3001)


In the folder created, read the CLAUDE.md file for install and configuration instructions.



