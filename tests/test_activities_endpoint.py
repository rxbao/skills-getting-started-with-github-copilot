"""Tests for GET /activities endpoint."""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities with correct structure."""
    # Arrange - No specific setup needed as activities are hardcoded

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 3  # Should have 3 activities

    # Check that all expected activities are present
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
    assert set(data.keys()) == set(expected_activities)

    # Check structure of each activity
    for activity_name, activity_data in data.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_get_activities_includes_participants(client):
    """Test that GET /activities includes participants lists."""
    # Arrange - No specific setup needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()

    # Verify participants are lists (may be empty)
    for activity_data in data.values():
        assert isinstance(activity_data["participants"], list)


def test_get_activities_data_types(client):
    """Test that GET /activities returns correct data types."""
    # Arrange - No specific setup needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()

    for activity_data in data.values():
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_get_activities_http_method_validation_post(client):
    """Test that POST /activities returns 405 Method Not Allowed."""
    # Arrange - No specific setup needed

    # Act
    response = client.post("/activities")

    # Assert
    assert response.status_code == 405


def test_get_activities_http_method_validation_put(client):
    """Test that PUT /activities returns 405 Method Not Allowed."""
    # Arrange - No specific setup needed

    # Act
    response = client.put("/activities")

    # Assert
    assert response.status_code == 405


def test_get_activities_http_method_validation_delete(client):
    """Test that DELETE /activities returns 405 Method Not Allowed."""
    # Arrange - No specific setup needed

    # Act
    response = client.delete("/activities")

    # Assert
    assert response.status_code == 405


def test_get_activities_response_headers(client):
    """Test that GET /activities returns correct response headers."""
    # Arrange - No specific setup needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"


def test_get_activities_response_consistency(client):
    """Test that GET /activities returns consistent data across multiple requests."""
    # Arrange - No specific setup needed

    # Act
    response1 = client.get("/activities")
    response2 = client.get("/activities")

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json() == response2.json()


def test_get_activities_activity_names_with_spaces(client):
    """Test that GET /activities handles activity names with spaces correctly."""
    # Arrange - No specific setup needed (Chess Club has spaces)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data  # Verify space-containing name is present
    assert isinstance(data["Chess Club"], dict)


def test_get_activities_activity_names_case_sensitivity(client):
    """Test that GET /activities preserves case sensitivity in activity names."""
    # Arrange - No specific setup needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    # Check that case is preserved (assuming hardcoded names)
    assert "Chess Club" in data
    assert "chess club" not in data  # Should not match lowercase
    assert "Programming Class" in data
    assert "programming class" not in data
