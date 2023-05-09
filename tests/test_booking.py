import pytest

from .client import client
import server

purchase_link = '/purchasePlaces'

class TestPurchasePlaces:
    def test_purchase_places_success(self, client, mocker):
        mocker.patch.object(
            server,
            'competitions', 
            [
                {
                    "name": "TestCompetition",
                    "date": "2023-10-22 13:30:00",
                    "numberOfPlaces": "15"
                }
            ]
        )
        mocker.patch.object(
            server,
            'clubs', 
            [
                {
                    "name":"Test name",
                    "email":"test@mail.com",
                    "points":"15"
                },
            ]
        )
        response = client.post(
            purchase_link,
            data={
                'club': "Test name",
                'competition': "TestCompetition",
                'places': 6
            }
        )
        assert response.status_code == 200
    
    def test_purchase_places_over_12_error(self, client, mocker):
        # try to purchase more than 12 places must return 403 
        mocker.patch.object(
            server,
            'competitions', 
            [
                {
                    "name": "TestCompetition",
                    "date": "2023-10-22 13:30:00",
                    "numberOfPlaces": "15"
                }
            ]
        )
        mocker.patch.object(
            server,
            'clubs', 
            [
                {
                    "name":"Test name",
                    "email":"test@mail.com",
                    "points":"15"
                },
            ]
        )
        response = client.post(
            purchase_link,
            data={
                'club': "Test name",
                'competition': "TestCompetition",
                'places': 13
            }
        )
        assert response.status_code == 403

    def test_purchase_places_over_club_allowed_error(self, client, mocker):
        # try to purchase more than the club allowed point must return 403 
        mocker.patch.object(
            server,
            'competitions', 
            [
                {
                    "name": "TestCompetition",
                    "date": "2023-10-22 13:30:00",
                    "numberOfPlaces": "15"
                }
            ]
        )
        mocker.patch.object(
            server,
            'clubs', 
            [
                {
                    "name":"Test name",
                    "email":"test@mail.com",
                    "points":"6"
                },
            ]
        )
        response = client.post(
            purchase_link,
            data={
                'club': "Test name",
                'competition': "TestCompetition",
                'places': 7
            }
        )
        assert response.status_code == 403

    def test_purchase_places_over_competition_allowed_error(self, client, mocker):
        # try to purchase more than the competition places must return 403 
        mocker.patch.object(
            server,
            'competitions', 
            [
                {
                    "name": "TestCompetition",
                    "date": "2023-10-22 13:30:00",
                    "numberOfPlaces": "6"
                }
            ]
        )
        mocker.patch.object(
            server,
            'clubs', 
            [
                {
                    "name":"Test name",
                    "email":"test@mail.com",
                    "points":"15"
                },
            ]
        )
        response = client.post(
            purchase_link,
            data={
                'club': "Test name",
                'competition': "TestCompetition",
                'places': 7
            }
        )
        assert response.status_code == 403
    
    def test_purchase_places_past_competition_error(self, client, mocker):
        # try to purchase places on a competition passed must return 403 
        mocker.patch.object(
            server,
            'competitions', 
            [
                {
                    "name": "TestCompetition",
                    "date": "2022-10-22 13:30:00",
                    "numberOfPlaces": "15"
                }
            ]
        )
        mocker.patch.object(
            server,
            'clubs', 
            [
                {
                    "name":"Test name",
                    "email":"test@mail.com",
                    "points":"15"
                },
            ]
        )
        response = client.post(
            purchase_link,
            data={
                'club': "Test name",
                'competition': "TestCompetition",
                'places': 6
            }
        )
        assert response.status_code == 403
