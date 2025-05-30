# Technology Stack: saaga-mcp-base

**Version:** 0.0.1
**Date:** 2025-05-09
**Status:** Draft
**Architect/Lead:** Andrew

## 1. Overview
    *   `saaga-mcp-base` is a foundational Python library for building Model Context Protocol (MCP) servers.

## 2. Core Technology
    *   **Language/Runtime:** Python
    *   **Exact Version:** 3.12
    *   **Rationale:** Python 3.12 is a stable, well-supported version compatible with key dependencies (e.g., Celery, MCP), suitable for a foundational library. It offers good scalability, security, maintainability, and performance for typical MCP server workloads.

## 3. Runtime Dependencies
Managed via `pyproject.toml`, built on Python 3.12, and uses SQLite for local data storage. Key dependencies include:
*   **celery:** Distributed task queuing.
*   **celery-redbeat:** Database-backed periodic task scheduler for Celery.
*   **fire:** Python library for automatically generating command line interfaces (CLIs).
*   **flower:** Web-based monitoring for Celery.
*   **loguru:** Logging.
*   **mcp:** Core MCP library.
*   **pydantic-settings:** Application settings management.
*   **redis:** In-memory data store (Celery broker/backend).
*   **requests:** HTTP requests.
*   **uv:** Fast Python package installer and resolver.
Dependencies in `pyproject.toml` must be kept current.

## 4. Dependency Management File(s)
    *   **File(s):** Lock file (e.g., `requirements.lock` preferred)
    *   **Location:** Repository root (e.g., `/`)
    *   **Generation Command (Example):** `pip-compile requirements.in > requirements.lock`
    *   **Note:** Lock files list all exact runtime dependency versions.

## 5. Verification Summaries
    *   **Dependency Conflict Check:** [Tool, Date, Status, e.g., "No conflicts via `pipdeptree` on YYYY-MM-DD"]
    *   **License Compliance Check:** [Tool, Status, e.g., "All licenses comply per tool X review"]
    *   **Security Vulnerability Scan:** [Tool, Date, Findings, e.g., "`pip-audit` on YYYY-MM-DD: 0 critical"]

## 6. Versioning and Update Policy
    *   **Policy:** All runtime dependencies MUST be locked to exact versions in lock files. Version ranges are prohibited in source files.
    *   **Rationale:** Ensures reproducible builds, predictable behavior, and security.
    *   **Update Process:** [e.g., "Quarterly reviews or critical security advisories, requiring full checks (Sec 5) and PR approval."]

## 7. Excluded Dependencies (Optional)
    *   Development/testing dependencies (e.g., `pytest`, `black`) are not part of the runtime stack but should be version-locked separately. 