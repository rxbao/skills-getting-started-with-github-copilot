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