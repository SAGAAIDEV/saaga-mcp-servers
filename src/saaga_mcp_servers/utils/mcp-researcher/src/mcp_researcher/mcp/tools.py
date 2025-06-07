"""MCP tools for the researcher service."""

import asyncio
from typing import Dict, Any

from mcp.server.fastmcp import FastMCP
from ..core.services import research
from ..core.logging import logger


def register_tools(mcp: FastMCP) -> None:
    """Register all tools with the MCP server."""

    @mcp.tool()
    async def research_topic(
        query: str,
        report_type: str = "deep",
        tone: str = "objective",
        role: str = "senior software architect"
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

        Returns:
            A dictionary containing:
            - success (bool): Whether the research completed successfully
            - query (str): The original research query
            - report_type (str): The type of report generated
            - tone (str): The tone used in the report
            - role (str): The role/perspective used
            - report (str): The comprehensive research report (if successful)
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

            # Run the async research function
            report = await research(query, report_type=report_type, tone=tone, role=role)

            return {
                "success": True, 
                "query": query, 
                "report_type": report_type,
                "tone": tone,
                "role": role,
                "report": report
            }
        except Exception as e:
            logger.error(f"MCP: Research failed: {e}")
            return {"success": False, "query": query, "error": str(e)}

    @mcp.tool()
    def research_sync(
        query: str,
        report_type: str = "deep",
        tone: str = "objective",
        role: str = "senior software architect"
    ) -> Dict[str, Any]:
        """
        Synchronous version of research_topic for compatibility with sync environments.
        
        This is a synchronous wrapper around the async research_topic function,
        providing the same comprehensive research capabilities for use in
        environments that don't support async/await.

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

        Returns:
            A dictionary containing:
            - success (bool): Whether the research completed successfully
            - query (str): The original research query
            - report_type (str): The type of report generated
            - tone (str): The tone used in the report
            - role (str): The role/perspective used
            - report (str): The comprehensive research report (if successful)
            - error (str): Error message (if unsuccessful)
            
        Note:
            This function internally uses asyncio.run() to execute the async
            research function. For better performance in async environments,
            use research_topic() instead.
        """
        try:
            logger.info(f"MCP: Starting sync research for query: {query}")
            logger.info(f"MCP: Report type: {report_type}, Tone: {tone}, Role: {role}")

            # Run the async research function synchronously
            report = asyncio.run(research(query, report_type=report_type, tone=tone, role=role))

            return {
                "success": True, 
                "query": query, 
                "report_type": report_type,
                "tone": tone,
                "role": role,
                "report": report
            }
        except Exception as e:
            logger.error(f"MCP: Sync research failed: {e}")
            return {"success": False, "query": query, "error": str(e)}
