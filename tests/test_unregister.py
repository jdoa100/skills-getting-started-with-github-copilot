"""Tests for the /activities/{activity_name}/signup DELETE endpoint."""


def test_unregister_successful(client):
    """Test successful unregistration from an activity."""
    # Arrange
    activity_name = "Music Club"
    email = "student@example.com"

    # First sign up
    client.post(f"/activities/{activity_name}/signup", json={"email": email})

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", json={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": "Unregistered successfully"}

    # Verify the email was removed from participants
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_nonexistent_activity(client):
    """Test unregister from a nonexistent activity returns 404."""
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@example.com"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", json={"email": email})

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data == {"detail": "Activity not found"}


def test_unregister_not_signed_up(client):
    """Test unregister with an email not signed up returns 400."""
    # Arrange
    activity_name = "Debate Club"
    email = "notsignedup@example.com"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", json={"email": email})

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert data == {"detail": "Not signed up"}


def test_unregister_empty_email(client):
    """Test unregister with empty email string."""
    # Arrange
    activity_name = "Science Club"
    email = ""

    # First sign up with empty email
    client.post(f"/activities/{activity_name}/signup", json={"email": email})

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", json={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": "Unregistered successfully"}