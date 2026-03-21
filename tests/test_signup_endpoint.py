"""Tests for POST /activities/{activity_name}/signup endpoint."""

import pytest


def test_signup_successful_adds_participant(client):
    """Test that successful signup adds email to participants list."""
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]

    # Verify email was added to participants
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data[activity_name]["participants"]


def test_signup_invalid_activity_returns_404(client):
    """Test that signup with invalid activity name returns 404."""
    # Arrange
    invalid_activity = "NonExistent Activity"
    email = "student@example.com"

    # Act
    response = client.post(f"/activities/{invalid_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404


def test_signup_allows_duplicates(client):
    """Test that current implementation allows duplicate signups (known bug)."""
    # Arrange
    activity_name = "Programming Class"
    email = "duplicate@example.com"

    # Act - Sign up twice
    client.post(f"/activities/{activity_name}/signup", params={"email": email})
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert - Current behavior allows duplicates
    assert response.status_code == 200

    # Verify email appears twice in participants
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    participants = activities_data[activity_name]["participants"]
    assert participants.count(email) == 2


def test_signup_allows_exceeding_capacity(client):
    """Test that current implementation allows exceeding max_participants (known bug)."""
    # Arrange
    activity_name = "Gym Class"
    email_base = "student"

    # Get current max_participants
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    max_participants = activities_data[activity_name]["max_participants"]

    # Act - Sign up more than max_participants
    for i in range(max_participants + 2):  # Exceed limit by 2
        email = f"{email_base}{i}@example.com"
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
        assert response.status_code == 200  # Current behavior allows it

    # Assert - Verify we exceeded the limit
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    participants_count = len(activities_data[activity_name]["participants"])
    assert participants_count > max_participants


def test_signup_with_empty_email(client):
    """Test signup with empty email string."""
    # Arrange
    activity_name = "Chess Club"
    email = ""

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert - Current behavior accepts empty email
    assert response.status_code == 200


def test_signup_response_format(client):
    """Test that signup response has expected message format."""
    # Arrange
    activity_name = "Programming Class"
    email = "test@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)