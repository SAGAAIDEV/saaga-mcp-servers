# Operations MCP Servers

This directory contains MCP servers designed for managing internal communications and operational services for teams and processes. These servers provide seamless integration with popular business tools and platforms.

## Overview

The operations servers enable AI assistants to interact with essential business communication and productivity tools, facilitating automated workflows, information retrieval, and team coordination.

## Available Servers

### 1. **mcp-gdrive** - Google Drive Integration
**Purpose**: File management and document access across Google Drive

**Key Capabilities**:
- **Search**: Find files across Google Drive using flexible search queries
- **File Access**: Read files with automatic format conversion:
  - Google Docs → Markdown
  - Google Sheets → CSV  
  - Google Presentations → Plain text
  - Google Drawings → PNG
  - Native files in their original format
- **Resource Management**: List and paginate through drive files
- **Authentication**: OAuth2 flow with credential persistence

**Use Cases**:
- Document retrieval for AI analysis
- Automated content processing
- File discovery and organization
- Cross-platform document access

---

### 2. **mcp-gsuite** - Gmail & Calendar Integration
**Purpose**: Comprehensive Google Workspace communication and scheduling management

**Gmail Features**:
- **Email Management**: Query, read, and organize emails with advanced search
- **Draft Operations**: Create, update, delete, and send email drafts
- **Reply System**: Automated reply generation with thread support
- **Attachment Handling**: Download and process email attachments
- **Label Management**: Create and apply labels for email organization
- **Multi-Account Support**: Manage multiple Google accounts simultaneously

**Calendar Features**:
- **Event Management**: Create, update, and delete calendar events
- **Multi-Calendar Support**: Work across personal, team, and project calendars
- **Scheduling**: Time-aware event creation with timezone support
- **Attendee Management**: Handle meeting invitations and notifications

**Use Cases**:
- Automated email responses and management
- Meeting scheduling and coordination
- Information extraction from emails
- Calendar-based workflow automation
- Cross-account communication management

---

### 3. **mcp-server-browserbase** - Web Automation
**Purpose**: Browser-based automation and web interaction capabilities

**Components**:
- **Browserbase Integration**: Cloud browser automation platform
- **Stagehand Framework**: Advanced web interaction and automation
- **Session Management**: Persistent browser sessions for complex workflows

**Capabilities**:
- Web scraping and data extraction
- Automated form filling and submissions
- Dynamic web page interaction
- Screenshot and visual verification
- Multi-step web workflows

**Use Cases**:
- Automated data collection from web sources
- Process automation for web-based tools
- Quality assurance and testing workflows
- Information gathering from dynamic websites

---

### 4. **mcp-slack** - Team Communication
**Purpose**: Slack workspace integration for team communication and coordination

**Core Features**:
- **Channel Management**: List and access public channels
- **Message Operations**: Post messages and replies to conversations
- **Thread Management**: Participate in threaded discussions
- **Reaction System**: Add emoji reactions to messages
- **History Access**: Retrieve channel history and conversation context
- **User Management**: Access user profiles and workspace information

**Communication Capabilities**:
- Automated message posting and responses
- Real-time team notifications
- Conversation monitoring and analysis
- Cross-channel information sharing

**Use Cases**:
- Automated status updates and notifications
- Team coordination and communication
- Information broadcast across channels
- Integration with other operational workflows

## Integration Benefits

These operational MCP servers work together to create a comprehensive business automation ecosystem:

1. **Unified Communication**: Email, chat, and document sharing in one interface
2. **Process Automation**: Reduce manual tasks across multiple platforms
3. **Information Flow**: Seamless data movement between systems
4. **Team Coordination**: Enhanced collaboration through automated workflows
5. **Multi-Platform Access**: Single interface for multiple business tools

## Authentication & Security

All servers implement secure authentication patterns:
- **OAuth2 flows** for Google services
- **Token-based authentication** for Slack
- **Credential persistence** with secure storage
- **Multi-account support** where applicable

## Getting Started

Each server includes comprehensive setup documentation:
- Authentication configuration guides
- Docker deployment options
- Usage examples and best practices
- Integration patterns for common workflows

This suite of operational MCP servers transforms how AI assistants interact with business tools, enabling sophisticated automation and seamless workflow integration across essential communication and productivity platforms.
