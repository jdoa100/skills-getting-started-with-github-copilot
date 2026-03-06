import pytest
from fastapi.testclient import TestClient

from src.app import app


@pytest.fixture
def client():
    """Fixture providing a FastAPI TestClient for testing endpoints."""
    return TestClient(app)