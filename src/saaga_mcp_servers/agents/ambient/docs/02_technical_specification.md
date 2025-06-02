# Technical Requirements Document: Ambient Agent

## 1. Introduction

### 1.1 Document Purpose
This Technical Requirements Document (TRD) defines the comprehensive technical specifications for the Ambient Agent, a Python-based monitoring service that integrates Jira task management with automated Claude code execution.

### 1.2 Project Overview
The Ambient Agent is a lightweight UV library that continuously monitors Jira for new project tasks and automatically triggers Claude code execution with corresponding project commands, enabling autonomous task-to-action workflow automation.

### 1.3 Document Scope
This document covers:
- System architecture and design patterns
- Technical requirements and constraints
- Integration specifications with Jira and Claude code
- Development and deployment requirements
- Testing and quality assurance standards

## 2. System Architecture

### 2.1 High-Level Architecture
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Jira Cloud    │────▶│  Ambient Agent  │────▶│  Claude Code    │
│      API        │     │   (UV Library)   │     │   Subprocess    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         ▲                        │                        │
         │                        ▼                        ▼
         │              ┌─────────────────┐     ┌─────────────────┐
         └──────────────│  Conduit MCP    │     │   Task Output   │
                        │    Library       │     │      Logs       │
                        └─────────────────┘     └─────────────────┘
```

### 2.2 Component Design
- **Main Service Loop**: Asynchronous polling mechanism with configurable intervals
- **Jira Integration Module**: REST API client using Conduit library
- **Task Detection Engine**: Stateful task tracking with deduplication
- **Process Manager**: Subprocess lifecycle management with timeout handling
- **Configuration Manager**: YAML-based configuration with environment variable support

### 2.3 Data Flow
1. Agent polls Jira API via Conduit library
2. New tasks are detected and validated
3. Claude code subprocess is spawned with task context
4. Process output is captured and logged
5. Task status is updated and tracked

## 3. Functional Requirements

### 3.1 Jira Integration
- **FR-001**: Connect to Jira using configured API tokens via Conduit library
- **FR-002**: Poll Jira API at configurable intervals (default: 60 seconds)
- **FR-003**: Query tasks using JQL with project-specific filters
- **FR-004**: Detect new tasks based on creation timestamp and status
- **FR-005**: Support multiple Jira sites through Conduit's multi-site configuration

### 3.2 Task Processing
- **FR-006**: Extract task metadata (key, summary, description, assignee)
- **FR-007**: Map task types to Claude code commands
- **FR-008**: Pass task context as command arguments
- **FR-009**: Track processed tasks to prevent duplicates
- **FR-010**: Handle task filtering based on configurable criteria

### 3.3 Claude Code Execution
- **FR-011**: Spawn Claude code as subprocess with proper environment
- **FR-012**: Pass task-specific commands and arguments
- **FR-013**: Capture stdout/stderr output streams
- **FR-014**: Implement configurable execution timeouts
- **FR-015**: Handle process termination and cleanup

### 3.4 Configuration Management
- **FR-016**: Load configuration from YAML files
- **FR-017**: Support environment variable overrides
- **FR-018**: Validate configuration on startup
- **FR-019**: Support hot-reloading of configuration
- **FR-020**: Secure storage of API tokens

## 4. Non-Functional Requirements

### 4.1 Performance Requirements
- **NFR-001**: Process new task detection within 2 seconds of API response
- **NFR-002**: Support monitoring up to 100 projects simultaneously
- **NFR-003**: Handle API rate limits gracefully with exponential backoff
- **NFR-004**: Memory footprint under 100MB during normal operation
- **NFR-005**: CPU usage under 5% during idle polling

### 4.2 Reliability Requirements
- **NFR-006**: 99.9% uptime for monitoring service
- **NFR-007**: Automatic recovery from transient failures
- **NFR-008**: Graceful degradation when Jira API is unavailable
- **NFR-009**: No data loss for detected tasks
- **NFR-010**: Subprocess crash isolation

### 4.3 Security Requirements
- **NFR-011**: Secure storage of Jira API tokens
- **NFR-012**: No logging of sensitive task data
- **NFR-013**: Subprocess execution in sandboxed environment
- **NFR-014**: Input validation for all external data
- **NFR-015**: Secure inter-process communication

### 4.4 Maintainability Requirements
- **NFR-016**: Comprehensive logging with configurable levels
- **NFR-017**: Metrics collection for monitoring
- **NFR-018**: Clear error messages and stack traces
- **NFR-019**: Modular architecture for easy extension
- **NFR-020**: Documentation for all public APIs

## 5. Technical Constraints

### 5.1 Technology Stack
- **Language**: Python 3.12
- **Package Manager**: UV (latest version)
- **Async Framework**: asyncio for concurrent operations
- **HTTP Client**: aiohttp or httpx for async requests
- **Configuration**: PyYAML for configuration parsing
- **Logging**: Python standard logging with JSON formatter

### 5.2 Dependencies
- **Conduit Library**: For Jira API integration (from saaga-mcp-servers/development/conduit)
- **Claude Code**: External executable accessible via subprocess
- **Python Standard Library**: subprocess, asyncio, logging, json, datetime

### 5.3 Development Constraints
- Must be packaged as a UV library
- Must support installation via pip/pipx
- Must follow Python PEP standards
- Must include type hints for all public APIs
- Must maintain 80%+ test coverage

## 6. Integration Requirements

### 6.1 Jira Integration via Conduit
- **IR-001**: Use Conduit's JiraClient for all Jira operations
- **IR-002**: Support Conduit's multi-site configuration
- **IR-003**: Handle Conduit's error responses gracefully
- **IR-004**: Respect Conduit's rate limiting mechanisms
- **IR-005**: Use Conduit's authentication methods

### 6.2 Claude Code Integration
- **IR-006**: Spawn Claude code using subprocess.Popen
- **IR-007**: Pass environment variables for context
- **IR-008**: Stream output in real-time
- **IR-009**: Handle process signals properly
- **IR-010**: Clean up zombie processes

### 6.3 External Interfaces
- **IR-011**: REST API endpoint for health checks
- **IR-012**: Metrics endpoint for monitoring
- **IR-013**: Configuration reload endpoint
- **IR-014**: Task status query endpoint
- **IR-015**: Subprocess management endpoints

## 7. Data Requirements

### 7.1 Task State Management
- **DR-001**: Store processed task IDs in memory-efficient structure
- **DR-002**: Persist task state across restarts
- **DR-003**: Implement task state TTL for cleanup
- **DR-004**: Support state export/import
- **DR-005**: Handle state corruption gracefully

### 7.2 Configuration Schema
```yaml
ambient_agent:
  polling_interval: 60  # seconds
  execution_timeout: 300  # seconds
  
  jira:
    site_alias: "default"  # Conduit site configuration
    projects:
      - key: "PROJ1"
        jql_filter: "status = 'To Do'"
        command_template: "process-task {key} {summary}"
      - key: "PROJ2"
        jql_filter: "status = 'Ready' AND labels = 'auto-process'"
        command_template: "handle-request {key}"
  
  claude_code:
    executable_path: "/usr/local/bin/claude-code"
    environment:
      CLAUDE_API_KEY: "${CLAUDE_API_KEY}"
    working_directory: "/tmp/claude-tasks"
  
  logging:
    level: "INFO"
    format: "json"
    output: "stdout"
```

### 7.3 Output Requirements
- **DR-006**: Log all task detections with metadata
- **DR-007**: Record subprocess execution results
- **DR-008**: Generate execution reports
- **DR-009**: Export metrics in Prometheus format
- **DR-010**: Support log rotation and archival

## 8. Testing Requirements

### 8.1 Unit Testing
- **TR-001**: 80% code coverage minimum
- **TR-002**: Mock all external dependencies
- **TR-003**: Test all error paths
- **TR-004**: Validate all configuration scenarios
- **TR-005**: Test async operations thoroughly

### 8.2 Integration Testing
- **TR-006**: Test Jira API integration with mock server
- **TR-007**: Test subprocess execution with mock commands
- **TR-008**: Test configuration loading and validation
- **TR-009**: Test error recovery mechanisms
- **TR-010**: Test performance under load

### 8.3 System Testing
- **TR-011**: End-to-end workflow testing
- **TR-012**: Stress testing with high task volumes
- **TR-013**: Reliability testing with failure injection
- **TR-014**: Security testing for input validation
- **TR-015**: Performance benchmarking

## 9. Deployment Requirements

### 9.1 Packaging
- **DP-001**: Distribute as UV package on PyPI
- **DP-002**: Include all dependencies in pyproject.toml
- **DP-003**: Support pip, pipx, and uv installation
- **DP-004**: Include CLI entry points
- **DP-005**: Bundle configuration templates

### 9.2 Runtime Environment
- **DP-006**: Support Linux, macOS, and Windows
- **DP-007**: Run as system service or container
- **DP-008**: Support Docker deployment
- **DP-009**: Include systemd service files
- **DP-010**: Support Kubernetes deployment

### 9.3 Monitoring & Operations
- **DP-011**: Health check endpoints
- **DP-012**: Prometheus metrics export
- **DP-013**: Structured logging for analysis
- **DP-014**: Graceful shutdown handling
- **DP-015**: Configuration validation on startup

## 10. Success Criteria

### 10.1 Acceptance Criteria
- Successfully polls Jira and detects new tasks
- Executes Claude code with correct parameters
- Handles errors gracefully without crashing
- Maintains configured polling schedule
- Provides comprehensive operational visibility

### 10.2 Performance Benchmarks
- Task detection latency < 2 seconds
- Memory usage < 100MB
- CPU usage < 5% idle
- Support for 100+ concurrent projects
- 99.9% service availability

### 10.3 Quality Metrics
- Zero critical bugs in production
- 80%+ automated test coverage
- All APIs documented
- Configuration examples provided
- Deployment guides completed

## 11. Appendices

### 11.1 Glossary
- **UV**: Modern Python package installer and resolver
- **Conduit**: Enterprise knowledge integration service for Jira/Confluence
- **JQL**: Jira Query Language for advanced search
- **Claude Code**: AI-powered code generation and execution tool
- **MCP**: Model Context Protocol for AI tool integration

### 11.2 References
- Conduit Documentation: `/saaga-mcp-servers/development/conduit/README.md`
- UV Documentation: https://github.com/astral-sh/uv
- Jira REST API: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- Python asyncio: https://docs.python.org/3/library/asyncio.html

### 11.3 Revision History
- v1.0.0 - Initial technical specification (2025-01-06)