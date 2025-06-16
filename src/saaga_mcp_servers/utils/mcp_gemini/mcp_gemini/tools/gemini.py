"""Gemini AI tool implementation for MCP server"""

import os
from typing import Optional, Dict, Any
from mcp import types
from google import genai
from google.genai import types as genai_types
from mcp_gemini.logging_config import logger


def gemini_generate(
    prompt: str,
    model: Optional[str] = None,
    response_mime_type: Optional[str] = None,
    temperature: Optional[float] = None,
    max_output_tokens: Optional[int] = None,
) -> types.TextContent:
    """
    Generate text using Google's Gemini AI model.

    Args:
        prompt: The input text prompt for generation
        model: The Gemini model to use (defaults to gemini-2.5-pro-preview-06-05)
        response_mime_type: MIME type for response (defaults to text/plain)
        temperature: Sampling temperature (0.0 to 2.0)
        max_output_tokens: Maximum number of tokens to generate

    Returns:
        TextContent: The generated text response
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY environment variable not set")
        return types.TextContent(
            type="text",
            text="Error: GEMINI_API_KEY environment variable not set. Please set it before using the Gemini tool.",
            format="text/plain",
        )

    try:
        client = genai.Client(api_key=api_key)

        # Use provided model or default
        model_name = model or "gemini-2.5-pro-preview-06-05"

        # Create content
        contents = [
            genai_types.Content(
                role="user",
                parts=[
                    genai_types.Part.from_text(text=prompt),
                ],
            ),
        ]

        # Configure generation
        config_params: Dict[str, Any] = {
            "response_mime_type": response_mime_type or "text/plain",
        }

        if temperature is not None:
            config_params["temperature"] = temperature

        if max_output_tokens is not None:
            config_params["max_output_tokens"] = max_output_tokens

        generate_content_config = genai_types.GenerateContentConfig(**config_params)

        # Generate response
        response_text = ""
        for chunk in client.models.generate_content_stream(
            model=model_name,
            contents=contents,
            config=generate_content_config,
        ):
            if chunk.text:
                response_text += chunk.text

        logger.info(f"Generated response using model {model_name}")

        return response_text

    except Exception as e:
        logger.error(f"Error generating with Gemini: {e}", exc_info=True)
        return types.TextContent(
            type="text",
            text=f"Error generating response: {str(e)}",
            format="text/plain",
        )
