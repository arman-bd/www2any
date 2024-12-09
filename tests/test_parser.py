import os
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from parser import extract_main_content


def test_extract_main_content_with_article():
    """Test content extraction when article tag is present."""
    html = """
    <html>
        <head><title>Test</title></head>
        <body>
            <header>Header content</header>
            <nav>Navigation</nav>
            <article>
                <h1>Main Article</h1>
                <p>This is the main content.</p>
            </article>
            <footer>Footer content</footer>
        </body>
    </html>
    """
    content = extract_main_content(html)

    assert "Main Article" in content
    assert "This is the main content" in content
    assert "Header content" not in content
    assert "Footer content" not in content


def test_extract_main_content_without_article():
    """Test content extraction when no article tag is present."""
    html = """
    <html>
        <body>
            <div class="content">
                <h1>Main Content</h1>
                <p>This is the main content.</p>
            </div>
            <div class="sidebar">Sidebar content</div>
        </body>
    </html>
    """
    content = extract_main_content(html)

    assert "Main Content" in content
    assert "This is the main content" in content


def test_extract_main_content_removes_scripts():
    """Test that JavaScript is removed from content."""
    html = """
    <html>
        <body>
            <article>
                <h1>Title</h1>
                <script>alert('test');</script>
                <p>Content</p>
            </article>
        </body>
    </html>
    """
    content = extract_main_content(html)

    assert "alert" not in content
    assert "Title" in content
    assert "Content" in content
