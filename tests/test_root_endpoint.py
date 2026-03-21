"""Tests for GET / root endpoint redirect."""

import pytest


def test_root_redirects_to_static_index(client):
    """Test that GET / redirects to /static/index.html."""
    # Arrange - No specific setup needed

    # Act
    response = client.get("/", follow_redirects=False)  # Don't follow redirects

    # Assert
    assert response.status_code in [301, 302, 307, 308]  # Redirect status codes
    assert response.headers.get("location") == "/static/index.html"


def test_root_redirect_is_permanent(client):
    """Test that GET / uses temporary redirect (307)."""
    # Arrange - No specific setup needed

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307  # Temporary redirect (FastAPI default)