# tests/conftest.py
import sys
from pathlib import Path

import pytest


# Add the project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from src.app import app as flask_app


@pytest.fixture
def app():
    """Create application for the tests."""
    app = flask_app
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()
