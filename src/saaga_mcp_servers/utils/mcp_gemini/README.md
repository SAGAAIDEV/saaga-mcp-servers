# MCP Gemini

An MCP server that integrates Google's Gemini AI models, providing AI-powered text generation capabilities to MCP-compatible tools and assistants.

## Overview

MCP Gemini bridges Google's powerful Gemini AI models with the Model Context Protocol (MCP), allowing AI assistants and tools to leverage Gemini's advanced language understanding and generation capabilities. The server provides a simple interface for text generation with support for the latest Gemini models, including gemini-2.5-pro-preview-06-05.

## Features

- **Gemini AI Integration**: Direct access to Google's latest Gemini models for text generation
- **Streaming Support**: Real-time streaming of generated responses
- **Flexible Configuration**: Customizable model selection, temperature, and output token limits
- **Multiple Transport Modes**: Supports both stdio and SSE (Server-Sent Events) transports
- **Echo Tool**: Built-in echo tool for testing and development
- **Comprehensive Logging**: OS-specific log management with rotation support

## Installation

### From PyPI (if published)

There are two main ways to use the server if it's published on PyPI:

**Option 1: Install and then Run (Recommended for regular use)**

First, install the package into your Python environment using UV:
```bash
# Install using UV
uv pip install mcp_gemini

# If you don't have UV, you can use pip:
# pip install mcp_gemini
```

Once installed, you can run the server from your terminal:
```bash
mcp_gemini-server
```

**Option 2: Run Directly with `uvx` (For quick use without permanent installation)**

If you want to run the server without installing it into your current environment (or to run a specific version easily), you can use `uvx`. This is handy for one-off tasks or testing.

```bash
# Run the latest version of the server directly from PyPI
uvx mcp_gemini mcp_gemini-server

# You can also specify a version:
# uvx mcp_gemini==1.2.3 mcp_gemini-server
```
This command tells `uvx` to fetch the `mcp_gemini` package and execute its `mcp_gemini-server` command.

### From Source

```bash
# Clone the repository
git clone <your-repository-url>
cd mcp_gemini

# Create and activate a virtual environment using UV
uv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode using UV
uv pip install -e .
```

## Available Tools

### gemini_generate

Generate text using Google's Gemini AI models with streaming support.

**Parameters:**
- `prompt` (string, required): The input text prompt for generation
- `model` (string, optional): The Gemini model to use (defaults to `gemini-2.5-pro-preview-06-05`)
- `response_mime_type` (string, optional): MIME type for response (defaults to `text/plain`)
- `temperature` (float, optional): Sampling temperature from 0.0 to 2.0
- `max_output_tokens` (integer, optional): Maximum number of tokens to generate

**Returns:**
- TextContent with the generated text

**Example usage:**
```bash
# Basic generation
python mcp_gemini/client/gemini_test.py "Write a haiku about coding"

# With custom parameters
python mcp_gemini/client/gemini_test.py "Explain quantum computing" --temperature 0.7 --max-tokens 500

# Using specific model
python mcp_gemini/client/gemini_test.py "Tell me a joke" --model gemini-2.5-pro-preview-06-05
```

### echo

Echo back the input text with optional case transformation.

**Parameters:**
- `text` (string, required): The text to echo back
- `transform` (string, optional): Case transformation - either "upper" or "lower"

**Returns:**
- TextContent with the (optionally transformed) text

**Example usage:**
```bash
# Basic echo
mcp_gemini-client "Hello, World"

# With transformation
mcp_gemini-client "Hello, World" --transform upper
```

## Usage

This MCP server provides two entry points:

1. `mcp_gemini-server`: The MCP server that handles tool requests
   ```bash
   # Run with stdio transport (default)
   mcp_gemini-server

   # Run with SSE transport
   mcp_gemini-server --transport sse
   ```

## Logging

The server logs all activity to both stderr and a rotating log file. Log files are stored in OS-specific locations:

- **macOS**: `~/Library/Logs/mcp-servers/mcp_gemini.log`
- **Linux**: 
  - Root user: `/var/log/mcp-servers/mcp_gemini.log`
  - Non-root: `~/.local/state/mcp-servers/logs/mcp_gemini.log`
- **Windows**: `%USERPROFILE%\AppData\Local\mcp-servers\logs\mcp_gemini.log`

Log files are automatically rotated when they reach 10MB, with up to 5 backup files kept.

You can configure the log level using the `LOG_LEVEL` environment variable:
```bash
# Set log level to DEBUG for more detailed logging
LOG_LEVEL=DEBUG mcp_gemini-server
```

Valid log levels are: DEBUG, INFO (default), WARNING, ERROR, CRITICAL

2. `mcp_gemini-client`: A convenience client for testing
   ```bash
   mcp_gemini-client "your command here"
   ```

**[➡️ REPLACE: Add any additional usage examples, common patterns, or best practices specific to your tools]**

## Requirements

- Python 3.11 or later (< 3.13)
- Operating Systems: Linux, macOS, Windows

**[➡️ REPLACE: Add any additional requirements specific to your MCP server:]
- Special system dependencies
- External services or APIs needed
- Network access requirements
- Hardware requirements (if any)**

## Configuration

### Environment Variables

- **GEMINI_API_KEY** (required): Your Google Gemini API key. Get one from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **LOG_LEVEL** (optional): Logging level - DEBUG, INFO, WARNING, ERROR, or CRITICAL (default: INFO)
- **MCP_SERVER_NAME** (optional): Custom name for the MCP server (default: "MCP Gemini")

### Setting up the API Key

```bash
# Set the API key in your environment
export GEMINI_API_KEY="your-api-key-here"

# Or set it when running the server
GEMINI_API_KEY="your-api-key-here" mcp_gemini-server
```

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed development instructions.

**[➡️ REPLACE: Add any project-specific development notes, guidelines, or requirements]**

## Troubleshooting

Common issues and their solutions:

**[➡️ REPLACE: Add troubleshooting guidance specific to your MCP server. Remove this section if not needed.]**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

**[➡️ REPLACE: Add your name and contact information]**

---

[Replace this example Echo server README with documentation specific to your MCP server. Use this structure as a template, but customize all sections to describe your server's actual functionality, tools, and configuration options.]
