from typing import Optional

from ollama import ChatResponse, chat


async def transform_content(
    content: str,
    output_format: str,
    prompt: Optional[str] = None,
    custom_fields: Optional[list[dict[str, str]]] = None,
) -> str:
    """
    Transforms web content using Ollama based on specified format and instructions.

    Args:
        content: The extracted web content to transform
        output_format: Desired output format (summary/json/bullet_points/markdown)
        prompt: Optional custom instructions for the transformation
        custom_fields: Optional list of field definitions for JSON output

    Returns:
        Transformed content as string
    """
    # Base system prompts for each format
    format_prompts = {
        "summary": "Create a concise summary of the following text. Do not include unnecessary instructions or details.",
        "json": "Convert the following text into a JSON structure. RETURN JSON, NOTHING ELSE!",
        "bullet_points": "Convert the following text into key bullet points. Do not include unnecessary instructions or details.",
        "markdown": "Convert the following text into well-structured markdown. Do not include unnecessary instructions or details.",
    }

    # Construct the system message
    system_msg = format_prompts.get(
        output_format,
        "Transform the following text.",
    )

    if output_format == "json" and custom_fields:
        # Add field specifications for JSON output
        field_specs = "\nUse the following fields:\n" + "\n".join(
            [f"- {field['key']}: {field['description']}" for field in custom_fields]
        )
        system_msg += field_specs

    # Add custom prompt if provided
    if prompt:
        system_msg += f"\n\nSpecific instructions:\n{prompt}"

    # Construct the messages list
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": content},
    ]

    try:
        # Call Ollama
        response: ChatResponse = chat(
            model="llama3:latest",  # Assuming llama2 is installed
            messages=messages,
        )

        return response["message"]["content"]

    except Exception as e:
        raise Exception(f"Error calling Ollama API: {e!s}") from e


def format_json_response(text: str) -> str:
    """
    Ensures the response is properly formatted when JSON is requested.

    Args:
        text: The response text from Ollama

    Returns:
        Properly formatted JSON string
    """
    # If the response already looks like JSON, return it
    if text.strip().startswith("{") and text.strip().endswith("}"):
        return text

    # Otherwise, try to extract JSON from markdown code blocks
    if "```json" in text:
        start = text.find("```json") + 7
        end = text.find("```", start)
        if end != -1:
            return text[start:end].strip()

    return text
