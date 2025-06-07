"""MCP tools for the researcher service."""

import asyncio
from pathlib import Path
from typing import Dict, Any, Optional

from mcp.server.fastmcp import FastMCP
from ..core.services import research as research_service
from ..core.logging import logger


def register_tools(mcp: FastMCP) -> None:
    """Register all tools with the MCP server."""

    @mcp.tool()
    async def research(
        query: str,
        report_type: str = "deep",
        tone: str = "objective",
        role: str = "senior software architect",
        output_file: Optional[str] = None,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """
        Perform comprehensive research on a topic using GPT Researcher with web search.

        This tool leverages GPT Researcher to conduct thorough research by:
        1. Searching the web using Tavily API for relevant sources
        2. Analyzing and synthesizing information from multiple sources
        3. Generating a comprehensive, well-structured research report

        The research process includes fact-checking, source validation, and
        AI-powered analysis to ensure high-quality, accurate results.

        Args:
            query: The research question or topic to investigate. Should be a clear,
                   specific question or topic. Examples:
                   - "What are the latest breakthroughs in renewable energy?"
                   - "How does blockchain technology work?"
                   - "What is the current state of AI in healthcare?"
            report_type: Type of report to generate (default: "deep"). Options:
                         research_report, resource_report, outline_report, custom_report,
                         detailed_report, subtopic_report, deep
            tone: Writing tone for the report (default: "objective"). Options:
                  objective, formal, analytical, persuasive, informative, explanatory,
                  descriptive, critical, comparative, speculative, reflective, narrative,
                  humorous, optimistic, pessimistic, simple, casual
            role: The role/perspective to adopt (default: "senior software architect").
                  Examples: data scientist, product manager, security analyst,
                  DevOps engineer, junior developer, CTO, researcher
            output_file: Optional file path to save the report. If provided, the report
                        will be written to this file in addition to being returned.

        Returns:
            A dictionary containing:
            - success (bool): Whether the research completed successfully
            - query (str): The original research query
            - report_type (str): The type of report generated
            - tone (str): The tone used in the report
            - role (str): The role/perspective used
            - report (str): The comprehensive research report (if successful)
            - output_file (str): Path where report was saved (if output_file was provided)
            - error (str): Error message (if unsuccessful)

        Example Response:
            {
                "success": true,
                "query": "What is quantum computing?",
                "report_type": "deep",
                "tone": "analytical",
                "role": "senior software architect",
                "report": "# Quantum Computing: A Comprehensive Overview\\n\\n..."
            }
        """
        try:
            logger.info(f"MCP: Starting research for query: {query}")
            logger.info(f"MCP: Report type: {report_type}, Tone: {tone}, Role: {role}")
            if output_file:
                logger.info(f"MCP: Output file: {output_file}")

            # Run the async research function
            if not dry_run:
                report = await research_service(
                    query, report_type=report_type, tone=tone, role=role
                )
            else:
                report = "This is a dry run"

            result = {
                "success": True,
                "query": query,
                "report_type": report_type,
                "tone": tone,
                "role": role,
            }

            # Save to file if requested
            if output_file:
                try:
                    output_path = Path(output_file)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    output_path.write_text(report, encoding="utf-8")
                    result["output_file"] = str(output_path.absolute())
                    logger.info(f"MCP: Report saved to {output_path.absolute()}")
                    return result
                except Exception as e:
                    logger.error(f"MCP: Failed to save report to file: {e}")
                    result["file_error"] = str(e)
                    return result

            result["report"] = report
            return result
        except Exception as e:
            logger.error(f"MCP: Research failed: {e}")
            return {"success": False, "query": query, "error": str(e)}
