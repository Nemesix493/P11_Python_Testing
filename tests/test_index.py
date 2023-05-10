import pytest

from .client import client
import server


class TestIndex:
    def test_index_success(self, client):
        response = client.get('/')
        assert response.status_code == 200