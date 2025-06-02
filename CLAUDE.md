# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

SAAGA MCP Servers is a monorepo containing multiple Model Context Protocol (MCP) servers that transform fragmented business communication and workflow automation into seamless, AI-driven productivity platforms. Target markets include social media managers, e-commerce operators, and sales professionals.

## Architecture

The codebase is organized as a monorepo with servers categorized by function:
- `src/saaga_mcp_servers/base/` - Core infrastructure (Celery, Redis, logging, scheduling)
- `src/saaga_mcp_servers/db/` - Database servers (SQLite, Neo4j)
- `src/saaga_mcp_servers/development/` - Dev tools (Conduit, Git, GitHub, templates)
- `src/saaga_mcp_servers/operations/` - Business operations (GSuite, Slack, Browserbase, Zoom)
- `src/saaga_mcp_servers/social/` - Social media integrations (Bluesky)
- `src/saaga_mcp_servers/agents/` - AI agent configurations

Each server follows a consistent structure:
- Python: `pyproject.toml`, `src/package_name/`, `__main__.py`, `config/`, `lib/`, `tools/`
- TypeScript: `package.json`, `index.ts`, `src/`, `tsconfig.json`

## Common Commands

### Python Servers (using UV)
```bash
# Install dependencies
uv sync

# Run a server
uv --directory=/path/to/server run server-name

# Run tests
uv --directory=/path/to/server run pytest

# Run linting (if configured)
uv --directory=/path/to/server run ruff check
uv --directory=/path/to/server run black .
```

### TypeScript Servers
```bash
# Neo4j server (uses Bun)
cd src/saaga_mcp_servers/db/neo4j-mcp
bun install
bun run start

# Slack server (uses npm)
cd src/saaga_mcp_servers/operations/mcp-slack
npm install
npm run build
```

### Go Servers (GitHub)
```bash
cd src/saaga_mcp_servers/development/mcp-github
go build ./cmd/github-mcp-server
go test ./...
```

### Creating New Servers
Use the cookie-cutter template:
```bash
cd src/saaga_mcp_servers/development/mcp-cookie-cutter
# Follow the template to create new server structure
```

## MCP Server Configuration

Servers are configured in `.mcp.json`. Each entry specifies:
- `command`: The executable to run (uv, npx, shell script)
- `args`: Arguments to pass
- `env`: Environment variables

Example:
```json
{
  "saaga-mcp-gsuite": {
    "command": "uv",
    "args": ["--directory", "/path/to/mcp-gsuite", "run", "saaga-mcp-gsuite"],
    "env": {
      "GSUITE_SERVICE_ACCOUNT_JSON": "path/to/credentials.json"
    }
  }
}
```

## Testing Patterns

- Python: Use pytest, tests go in `tests/` directory
- Go: Standard Go testing with `*_test.go` files
- Look for project-specific pytest configuration in `pyproject.toml`

## Key Infrastructure Components

### Base Server (`saaga-mcp-base`)
Provides core utilities:
- Task scheduling with Celery/Redis
- Parallel tool execution
- Activity logging (SQLite)
- Exception handling
- Approval management

### Conduit (Atlassian Integration)
Complex production server example with:
- Multi-site configuration
- YAML-based settings
- Both CLI and MCP interfaces
- Comprehensive test coverage

## Important Patterns

1. **Authentication**: Each server manages its own credentials
2. **Multi-site Support**: Servers can connect to multiple service instances
3. **Logging**: Integration with base logging infrastructure
4. **Tool Organization**: Tools are modular and placed in `tools/` directories
5. **Configuration**: Use pydantic-settings for environment management

## Development Tips

- Always check the server's README.md for specific setup instructions
- Environment variables are typically required for authentication
- Python projects use UV for fast dependency management
- TypeScript projects may use either Bun or npm
- Test files follow `test_*.py` or `*_test.go` naming patterns