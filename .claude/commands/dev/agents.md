
This is the claude directory
/Users/andrew/saga/saaga-mcp-servers/.claude

Commands contain claude code commands, prompts, the sub folders are the agent.
agents.sh contain the claude configuration 
mcp_configs contain json configuration of the different agents defined in agents.sh
AN agent consists of 
    A system prompt that drives the style of the agent.
    Commands in commands/<agent_name>/ these are prompts and workflows of how to use the tools.
    mcp_configs The agents utility belt.


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


