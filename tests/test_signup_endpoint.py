"""Tests for POST /activities/{activity_name}/signup endpoint."""

import pytest
from urllib.parse import quote


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


def test_signup_email_validation_invalid_formats(client, invalid_email):
    """Test signup with various invalid email formats (current behavior accepts them)."""
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": invalid_email})

    # Assert - Current behavior accepts invalid emails
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_signup_email_validation_whitespace(client):
    """Test signup with email containing whitespace."""
    # Arrange
    activity_name = "Chess Club"
    email = " student@example.com "  # Leading/trailing spaces

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert - Current behavior accepts whitespace in emails
    assert response.status_code == 200


def test_signup_activity_name_with_special_characters(client, activity_name_with_special_chars):
    """Test signup with activity names containing special characters."""
    # Arrange
    email = "student@example.com"

    # Act
    response = client.post(f"/activities/{activity_name_with_special_chars}/signup", params={"email": email})

    # Assert - Should return 404 for non-existent activity
    assert response.status_code == 404


def test_signup_activity_name_empty(client, empty_activity_name):
    """Test signup with empty or whitespace-only activity names."""
    # Arrange
    email = "student@example.com"

    # Act - URL encode the activity name to handle special characters
    encoded_activity = quote(empty_activity_name, safe='')
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": email})

    # Assert - Should return 404 for invalid activity name
    assert response.status_code == 404


def test_signup_activity_name_case_sensitivity(client):
    """Test that signup is case-sensitive for activity names."""
    # Arrange
    email = "student@example.com"

    # Act - Try with different case
    response = client.post(f"/activities/chess club/signup", params={"email": email})  # lowercase

    # Assert - Should return 404 because "Chess Club" != "chess club"
    assert response.status_code == 404

    # Verify correct case works
    response_correct = client.post(f"/activities/Chess Club/signup", params={"email": email})
    assert response_correct.status_code == 200


def test_signup_http_method_validation_get(client):
    """Test that GET on signup endpoint returns 405 Method Not Allowed."""
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.get(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 405


def test_signup_http_method_validation_put(client):
    """Test that PUT on signup endpoint returns 405 Method Not Allowed."""
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.put(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 405


def test_signup_http_method_validation_delete(client):
    """Test that DELETE on signup endpoint returns 405 Method Not Allowed."""
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 405


def test_signup_response_validation_success(client, valid_email):
    """Test signup response format for successful signups."""
    # Arrange
    activity_name = "Programming Class"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": valid_email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert activity_name in data["message"]
    assert valid_email in data["message"]


def test_signup_response_validation_invalid_activity(client):
    """Test signup response format for invalid activity names."""
    # Arrange
    invalid_activity = "Invalid Activity"
    email = "student@example.com"

    # Act
    response = client.post(f"/activities/{invalid_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    # For 404, response might be JSON or plain text depending on FastAPI config
    # Just check it's not 200


def test_signup_attempt_exceed_capacity_current_behavior(client):
    """Test current behavior when attempting to exceed capacity (documents known bug)."""
    # Arrange
    activity_name = "Gym Class"
    email_base = "capacity_test"

    # Get max_participants
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    max_participants = activities_data[activity_name]["max_participants"]

    # Act - Try to sign up one more than max
    for i in range(max_participants + 1):
        email = f"{email_base}{i}@example.com"
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
        assert response.status_code == 200  # Current behavior allows exceeding

    # Assert - Verify we exceeded
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert len(activities_data[activity_name]["participants"]) > max_participants


def test_signup_prevent_duplicates_current_behavior(client):
    """Test current behavior allowing duplicate signups (documents known bug)."""
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate_test@example.com"

    # Act - Sign up multiple times
    for _ in range(3):
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
        assert response.status_code == 200  # Current behavior allows

    # Assert - Verify duplicates exist
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    participants = activities_data[activity_name]["participants"]
    assert participants.count(email) == 3