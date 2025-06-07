from gpt_researcher import GPTResearcher
import os

from mcp_researcher.core.config import settings
from mcp_researcher.core.logging import logger

# Enable hybrid research: web search + MCP
os.environ["RETRIEVER"] = "tavily,mcp"
os.environ["TAVILY_API_KEY"] = settings.tavily_api_key
os.environ["OPENAI_API_KEY"] = settings.openai_api_key

# Set research configuration
os.environ["DEEP_RESEARCH_BREADTH"] = str(settings.deep_research.breadth)
os.environ["DEEP_RESEARCH_DEPTH"] = str(settings.deep_research.depth)
os.environ["DEEP_RESEARCH_CONCURRENCY"] = str(settings.deep_research.concurrency)
os.environ["TOTAL_WORDS"] = str(settings.deep_research.total_words)


async def research(
    query: str,
    report_type: str = "deep",
    tone: str = "objective",
    role: str = "senior software architect",
) -> str:
    """
    Perform comprehensive research on a topic using GPT Researcher with MCP integration.

    This function leverages GPT Researcher to conduct web searches via Tavily API and
    compile comprehensive research reports using AI analysis. It supports hybrid research
    combining web search results with MCP data sources.

    Args:
        query: The research question or topic to investigate. Should be a clear,
               specific question or topic for best results.
        report_type: Type of report to generate. Valid options:
                     - "research_report": Standard research report format
                     - "resource_report": Focus on resources and references
                     - "outline_report": Structured outline format
                     - "custom_report": Custom format based on query
                     - "detailed_report": Comprehensive detailed analysis
                     - "subtopic_report": Report focused on subtopics
                     - "deep": Deep research with comprehensive analysis (default)
        sources: Optional list of specific source URLs to include in the research.
                 If provided, these will be prioritized in the analysis.
        tone: Writing tone for the report. Valid options:
              - "objective": Impartial and unbiased presentation (default)
              - "formal": Academic standards with sophisticated language
              - "analytical": Critical evaluation and detailed examination
              - "persuasive": Convincing the audience of a viewpoint
              - "informative": Clear and comprehensive information
              - "explanatory": Clarifying complex concepts
              - "descriptive": Detailed depiction of phenomena
              - "critical": Judging validity and relevance
              - "comparative": Highlighting differences and similarities
              - "speculative": Exploring hypotheses and implications
              - "reflective": Personal insights and experiences
              - "narrative": Story-telling approach
              - "humorous": Light-hearted and engaging
              - "optimistic": Highlighting positive findings
              - "pessimistic": Focusing on limitations and challenges
              - "simple": Basic vocabulary for young readers
              - "casual": Conversational and relaxed style
        role: The role/perspective to adopt when conducting research.
              Default is "senior software architect". This influences the focus,
              technical depth, and practical considerations in the report.
              Examples: "data scientist", "product manager", "security analyst",
              "DevOps engineer", "junior developer", "CTO", "researcher"

    Returns:
        A formatted research report as a string containing:
        - Executive summary of findings
        - Detailed analysis with citations
        - Key insights and conclusions
        - References to sources used

    Raises:
        Exception: If API keys are missing or if the research process fails.

    Example:
        report = await research(
            "What are the latest developments in quantum computing?",
            report_type="deep",
            tone="analytical",
            role="senior software architect"
        )
    """
    logger.info(f"Starting research for query: {query}")
    logger.info(f"Report type: {report_type}, Tone: {tone}, Role: {role}")

    researcher = GPTResearcher(
        query=query,
        report_type=report_type,
        tone=tone,
        role=role,
        mcp_configs=[
            {
                "name": "tavily",
                "command": "npx",
                "args": ["-y", "tavily-mcp@0.1.2"],
                "env": {"TAVILY_API_KEY": settings.tavily_api_key},
            }
        ],
    )

    logger.debug("Conducting research...")
    context = await researcher.conduct_research()

    logger.debug("Writing report...")
    report = await researcher.write_report()

    logger.info("Research completed successfully")
    return report
