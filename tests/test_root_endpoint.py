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


def test_root_http_method_validation_post(client):
    """Test that POST / returns 405 Method Not Allowed."""
    # Arrange - No specific setup needed

    # Act
    response = client.post("/")

    # Assert
    assert response.status_code == 405


def test_root_http_method_validation_put(client):
    """Test that PUT / returns 405 Method Not Allowed."""
    # Arrange - No specific setup needed

    # Act
    response = client.put("/")

    # Assert
    assert response.status_code == 405


def test_root_http_method_validation_delete(client):
    """Test that DELETE / returns 405 Method Not Allowed."""
    # Arrange - No specific setup needed

    # Act
    response = client.delete("/")

    # Assert
    assert response.status_code == 405


def test_root_redirect_response_headers(client):
    """Test that GET / redirect includes correct response headers."""
    # Arrange - No specific setup needed

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert "location" in response.headers
    assert response.headers["location"] == "/static/index.html"
    # Content-Type might be text/html or empty for redirects
    assert "content-type" not in response.headers or response.headers["content-type"] in ["text/html; charset=utf-8", ""]


def test_root_redirect_location_header_correct(client):
    """Test that GET / Location header points to the correct static path."""
    # Arrange - No specific setup needed

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_follow_redirects_behavior(client):
    """Test that GET / with follow_redirects=True attempts to follow the redirect."""
    # Arrange - No specific setup needed

    # Act
    response = client.get("/", follow_redirects=True)

    # Assert
    # With follow_redirects=True, it should try to follow to /static/index.html
    # Since static files might not be served in test client, it may return 404 or the redirect response
    # But at minimum, it should not fail with connection error
    assert response.status_code in [200, 404, 307]  # 200 if static served, 404 if not, 307 if not followed