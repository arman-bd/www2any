import os
import sys

import pytest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from llm import transform_content


@pytest.mark.asyncio
async def test_transform_content_summary():
    """Test content transformation with summary format."""
    content = "This is a test article. It contains important information about testing."
    result = await transform_content(content=content, output_format="summary")

    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_transform_content_json():
    """Test content transformation with JSON format and custom fields."""
    content = """
    Product: Test Product
    Price: $99.99
    Features: Feature 1, Feature 2
    """

    custom_fields = [
        {"key": "name", "description": "Product name"},
        {"key": "price", "description": "Product price"},
        {"key": "features", "description": "List of features"},
    ]

    result = await transform_content(
        content=content, output_format="json", custom_fields=custom_fields
    )

    assert result is not None
    assert '"name"' in result.lower()
    assert '"price"' in result.lower()
    assert '"features"' in result.lower()


@pytest.mark.asyncio
async def test_transform_content_with_custom_prompt():
    """Test content transformation with custom prompt."""
    content = "This is a test article about product testing."
    custom_prompt = "Extract key testing steps and results"

    result = await transform_content(
        content=content, output_format="bullet_points", prompt=custom_prompt
    )

    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0
