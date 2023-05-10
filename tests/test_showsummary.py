import pytest

from .client import client
import server


class TestShowSummary:
    def test_showSummary_error(self, client, mocker):
        mocker.patch.object(
            server,
            'clubs',
            [
                {
                    "name": "Test name",
                    "email": "test@mail.com",
                    "points": "15"
                },
            ]
        )
        response = client.post(
            '/showSummary',
            data={
                'email': 'wrongMail@adress.com'
            }
        )
        assert response.status_code == 302

    def test_showSummary_success(self, client, mocker):
        mocker.patch.object(
            server,
            'clubs',
            [
                {
                    "name": "Test name",
                    "email": "test@mail.com",
                    "points": "15"
                },
            ]
        )
        response = client.post(
            '/showSummary',
            data={
                'email': 'test@mail.com'
            }
        )
        assert response.status_code == 200
