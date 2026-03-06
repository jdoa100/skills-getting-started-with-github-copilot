"""Tests for the /activities GET endpoint."""


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all available activities with correct structure."""
    # Arrange - TestClient fixture provides the client, activities are predefined in app

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # Based on the predefined activities in the app

    # Check that a known activity has the expected structure
    chess_club = data.get("Chess Club")
    assert chess_club is not None
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_get_activities_includes_expected_activities(client):
    """Test that GET /activities includes all expected activity names."""
    # Arrange - TestClient fixture provides the client

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Art Club",
        "Music Club",
        "Debate Club",
        "Science Club",
        "Drama Club",
        "Photography Club"
    ]
    assert set(data.keys()) == set(expected_activities)