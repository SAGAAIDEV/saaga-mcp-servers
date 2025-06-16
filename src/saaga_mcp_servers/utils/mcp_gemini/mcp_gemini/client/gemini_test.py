"""Test client for Gemini MCP tool"""

import asyncio
import click
from typing import Optional
from mcp import ClientSession, StdioServerParameters
from mcp.types import TextContent
from mcp.client.stdio import stdio_client


async def call_gemini(
    prompt: str, 
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None
) -> str:
    """
    Call the Gemini tool via MCP server.
    
    Args:
        prompt: The text prompt to send to Gemini
        model: Optional model name to use
        temperature: Optional temperature for sampling
        max_tokens: Optional max output tokens
        
    Returns:
        The generated text from Gemini
    """
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="mcp_gemini-server",
        args=[],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # Build arguments
            arguments = {"prompt": prompt}
            if model:
                arguments["model"] = model
            if temperature is not None:
                arguments["temperature"] = temperature
            if max_tokens is not None:
                arguments["max_output_tokens"] = max_tokens
                
            # Call the gemini_generate tool
            result = await session.call_tool("gemini_generate", arguments=arguments)
            if isinstance(result, TextContent):
                return result.text
            else:
                return str(result)


@click.command()
@click.argument("prompt", type=str)
@click.option("--model", type=str, help="Gemini model to use")
@click.option("--temperature", type=float, help="Sampling temperature (0.0-2.0)")
@click.option("--max-tokens", type=int, help="Maximum output tokens")
def main(prompt: str, model: Optional[str], temperature: Optional[float], max_tokens: Optional[int]):
    """Send a prompt to Gemini AI via MCP server."""
    try:
        response = asyncio.run(call_gemini(prompt, model, temperature, max_tokens))
        print(response)
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()