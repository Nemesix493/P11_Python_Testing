import multiprocessing
import datetime

import server

clubs = [
    {
        "name": "TestClub",
        "email": "testclub@test.com",
        "points": "13"
    }
]

competitions = [
    {
        "name": "TestCompetition",
        "date": f"{datetime.date.today().year + 1}-10-22 13:30:00",
        "numberOfPlaces": "15"
    }
]


def run_flask_server():
    server.is_test_server = True
    server.clubs = clubs
    server.competitions = competitions
    server.app.run()


def start_server():
    global flask_process
    flask_process = multiprocessing.Process(target=run_flask_server)
    flask_process.start()


def stop_server():
    flask_process.terminate()
    flask_process.join()
