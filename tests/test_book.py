import pytest
import datetime

from .client import client
import server

book_base_link = '/book'


class TestPurchasePlaces:
    def test_book_success(self, client, mocker):
        mocker.patch.object(
            server,
            'competitions',
            [
                {
                    "name": "TestCompetition",
                    "date": f"{datetime.date.today().year + 1}-10-22 13:30:00",
                    "numberOfPlaces": "15"
                }
            ]
        )
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
        response = client.get(f'{book_base_link}/TestCompetition/Test name')
        assert response.status_code == 200

    def test_book_unexist_competition_error(self, client, mocker):
        # try to load book view on unexist competition should return 403
        mocker.patch.object(
            server,
            'competitions',
            [
                {
                    "name": "TestCompetition",
                    "date": f"{datetime.date.today().year + 1}-10-22 13:30:00",
                    "numberOfPlaces": "15"
                }
            ]
        )
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
        response = client.get(f'{book_base_link}/unexistCompetition/Test name')
        assert response.status_code == 302

    def test_book_unexist_club_error(self, client, mocker):
        # try to load book view on unexist club should return 403
        mocker.patch.object(
            server,
            'competitions',
            [
                {
                    "name": "TestCompetition",
                    "date": f"{datetime.date.today().year + 1}-10-22 13:30:00",
                    "numberOfPlaces": "15"
                }
            ]
        )
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
        response = client.get(f'{book_base_link}/TestCompetition/unexistClub')
        assert response.status_code == 302
