# saaga-mcp-base

A utility wrapper designed to extend the functionality of Model Context Protocol (MCP) servers with scheduling, parallelization, logging, and enhanced capabilities.

## Documentation

📖 **Complete project documentation is available on Confluence:**  
[saaga-mcp-base Documentation](https://saaga-team.atlassian.net/wiki/spaces/SD/pages/27361284)

The Confluence page includes detailed information about:
- Project vision and overview
- Key features and capabilities
- Base tools and functionality
- Deployment and integration examples
- Target audience and use cases

📋 **Development and Future Work:**  
[Future Work: Scheduler System Enhancement](https://saaga-team.atlassian.net/wiki/spaces/SD/pages/27328560)

This document outlines the roadmap for enhancing the scheduler system from prototype to production-ready:
- Current state assessment and gaps
- Priority-based implementation roadmap
- Crontab support and recurring task scheduling
- Schedule management MCP tools
- Advanced features and enterprise capabilities

## Quick Overview

`saaga-mcp-base` provides MCP tools with:

- **Scheduling Capabilities:** Coordinate and time tool execution with datetime and crontab support
- **Parallelization:** Run multiple tools or instances concurrently
- **Logging:** Comprehensive activity monitoring to SQLite
- **Exception Handling:** Robust error management and reporting
- **Approval Database:** System for managing tool operation approvals

## Getting Started

For detailed setup instructions, deployment options, and usage examples, please refer to the [Confluence documentation](https://saaga-team.atlassian.net/wiki/spaces/SD/pages/27361284).

## Target Audience

Developers and administrators working with MCP servers who require enhanced control, observability, and resilience for their MCP tool integrations.
