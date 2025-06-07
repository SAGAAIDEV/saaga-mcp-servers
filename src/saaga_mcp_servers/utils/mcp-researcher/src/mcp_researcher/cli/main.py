import asyncio
import fire

from mcp_researcher.core.config import settings
from mcp_researcher.core.logging import logger
from mcp_researcher.core.services import research
from .config import ConfigCLI


class MCPResearcherCLI:
    """MCP Researcher Command Line Interface."""
    
    def __init__(self):
        """Initialize the CLI with sub-commands."""
        self.config = ConfigCLI()

    def hello(self, name: str = "World") -> None:
        """
        Print a hello message.
        
        Args:
            name: Name to greet (default: World)
        """
        logger.info(f"Hello, {name}!")
        
        # Safely print API keys (showing only first 4 chars)
        try:
            tavily_key = settings.tavily_api_key[:4] + "..." if settings.tavily_api_key else "NOT SET"
            anthropic_key = settings.anthropic_api_key[:4] + "..." if settings.anthropic_api_key else "NOT SET"
            openai_key = settings.openai_api_key[:4] + "..." if hasattr(settings, 'openai_api_key') and settings.openai_api_key else "NOT SET"
            
            logger.info("API Keys Status:")
            logger.info(f"  Tavily API Key: {tavily_key}")
            logger.info(f"  Anthropic API Key: {anthropic_key}")
            logger.info(f"  OpenAI API Key: {openai_key}")
            logger.debug("API keys loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load API keys: {e}")

    def version(self) -> None:
        """Print the version information."""
        logger.info("MCP Researcher v0.1.0")

    def status(self) -> None:
        """Check the status of the MCP Researcher."""
        from ..core.constants import DEFAULT_CONFIG_PATH
        
        logger.info("MCP Researcher is ready!")
        logger.debug("Debug logging is enabled")
        
        # Show config file location
        logger.info(f"Config file: {DEFAULT_CONFIG_PATH}")
        logger.info(f"Config exists: {DEFAULT_CONFIG_PATH.exists()}")
        
        # Show research configuration
        logger.info("Research Configuration:")
        logger.info(f"  Deep Research Breadth: {settings.deep_research.breadth}")
        logger.info(f"  Deep Research Depth: {settings.deep_research.depth}")
        logger.info(f"  Deep Research Concurrency: {settings.deep_research.concurrency}")
        logger.info(f"  Total Words: {settings.deep_research.total_words}")
    
    def research(
        self, 
        query: str, 
        report_type: str = "deep", 
        sources: list[str] = None,
        tone: str = "objective",
        role: str = "senior software architect"
    ) -> None:
        """
        Perform comprehensive research on a topic using GPT Researcher.
        
        This command leverages GPT Researcher to conduct web searches via Tavily API and
        compile comprehensive research reports using AI analysis.
        
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
                     Example: --sources "https://example.com" "https://another.com"
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
        
        Examples:
            mcp-researcher research "What is quantum computing?"
            mcp-researcher research "Latest AI developments" --report_type outline_report
            mcp-researcher research "Python best practices" --tone analytical
            mcp-researcher research "Climate change" --tone simple --report_type detailed_report
            mcp-researcher research "Microservices patterns" --role "DevOps engineer"
            mcp-researcher research "AI ethics" --role "product manager" --tone informative
        """
        if sources is None:
            sources = []
            
        logger.info(f"Research query: {query}")
        logger.info(f"Report type: {report_type}")
        logger.info(f"Tone: {tone}")
        logger.info(f"Role: {role}")
        if sources:
            logger.info(f"Sources: {sources}")
        
        # Run the async research function
        try:
            report = asyncio.run(research(
                query, 
                report_type=report_type, 
                sources=sources,
                tone=tone,
                role=role
            ))
            logger.info("Research Report:")
            logger.info("-" * 80)
            logger.info(report)
            logger.info("-" * 80)
        except Exception as e:
            logger.error(f"Research failed: {e}")


def main():
    """Entry point for the CLI."""
    fire.Fire(MCPResearcherCLI())


if __name__ == "__main__":
    main()