import pytest

from .client import client
import server


class TestClubsPoints:
    def test_clubs_points_success(self, client):
        response = client.get('/clubs-points')
        assert response.status_code == 200