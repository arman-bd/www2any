import re

from bs4 import BeautifulSoup, Comment


CONTENT_LENGTH_THRESHOLD = 100


def extract_main_content(html: str) -> str:
    """
    Extracts the main content from HTML using heuristics and BeautifulSoup.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove unwanted elements
    for element in soup.find_all(["script", "style", "nav", "footer", "header"]):
        element.decompose()

    # Remove comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Try to find main content container
    main_content = None
    possible_containers = [
        soup.find("main"),
        soup.find("article"),
        soup.find(id=re.compile(r"content|main|article", re.I)),
        soup.find(class_=re.compile(r"content|main|article", re.I)),
    ]

    for container in possible_containers:
        if container and len(container.get_text(strip=True)) > CONTENT_LENGTH_THRESHOLD:
            main_content = container
            break

    # If no main content container found, use body
    if not main_content:
        main_content = soup.find("body")

    # Clean the text
    if main_content:
        # Remove extra whitespace
        text = " ".join(main_content.get_text(separator=" ").split())
        return text

    return ""
