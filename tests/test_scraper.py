import os
import sys

import pytest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from scraper import scrape_url


@pytest.mark.asyncio
async def test_scrape_valid_url():
    """Test scraping a valid URL."""
    url = "https://example.com"
    html_content = await scrape_url(url)

    assert html_content is not None
    assert len(html_content) > 0
    assert "<html" in html_content.lower()
    assert "</html>" in html_content.lower()


@pytest.mark.asyncio
async def test_scrape_invalid_url():
    """Test scraping an invalid URL."""
    url = "https://this-is-an-invalid-url-that-does-not-exist.com"

    with pytest.raises(Exception):  # noqa: B017
        await scrape_url(url)


@pytest.mark.asyncio
async def test_scrape_url_content():
    """Test if the scraper captures the main content."""
    url = "https://example.com"
    html_content = await scrape_url(url)

    # Check for common elements that should be present
    assert "<head" in html_content.lower()
    assert "<body" in html_content.lower()
    assert "<title" in html_content.lower()
