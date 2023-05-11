import pytest

from .client import client
import server


class TestLogout:
    def test_logout_success(self, client):
        response = client.get('/logout')
        assert response.status_code == 302
