from playwright.async_api import async_playwright


async def scrape_url(url: str) -> str:
    """
    Scrapes a webpage using Playwright and returns the HTML content.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page()

            # Load the URL
            await page.goto(url, wait_until="networkidle", timeout=60000)

            # Wait for content to load
            await page.wait_for_load_state("domcontentloaded", timeout=60000)

            # Get the full HTML content
            content = await page.content()

            return content
        finally:
            await browser.close()
