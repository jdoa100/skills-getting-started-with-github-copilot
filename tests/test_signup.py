"""Tests for the /activities/{activity_name}/signup POST endpoint."""


def test_signup_successful(client):
    """Test successful signup for an activity."""
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", json={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": "Signed up successfully"}

    # Verify the email was added to participants
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_nonexistent_activity(client):
    """Test signup for a nonexistent activity returns 404."""
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", json={"email": email})

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data == {"detail": "Activity not found"}


def test_signup_duplicate_email(client):
    """Test signup with an email already signed up returns 400."""
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate@example.com"

    # First signup
    client.post(f"/activities/{activity_name}/signup", json={"email": email})

    # Act - Second signup with same email
    response = client.post(f"/activities/{activity_name}/signup", json={"email": email})

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert data == {"detail": "Already signed up"}


def test_signup_empty_email(client):
    """Test signup with empty email string."""
    # Arrange
    activity_name = "Programming Class"
    email = ""

    # Act
    response = client.post(f"/activities/{activity_name}/signup", json={"email": email})

    # Assert
    assert response.status_code == 200  # App currently accepts empty email
    data = response.json()
    assert data == {"message": "Signed up successfully"}

    # Verify empty email was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_invalid_email_format(client):
    """Test signup with invalid email format (app currently accepts any string)."""
    # Arrange
    activity_name = "Art Club"
    email = "invalid-email-format"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", json={"email": email})

    # Assert
    assert response.status_code == 200  # App doesn't validate email format
    data = response.json()
    assert data == {"message": "Signed up successfully"}